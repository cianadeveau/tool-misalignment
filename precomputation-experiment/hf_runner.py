import argparse
import json
import os
import re
from datetime import datetime, timezone

import torch
from huggingface_hub import login

from config import HF_TOKEN, HF_MODEL, RUNS_PER_PROMPT, TEMPERATURE, RESULTS_DIR, SYSTEM_PROMPT
from tools import GEOGRAPHY_TOOL
from prompts import PRECOMPUTABLE_PROMPTS, NON_PRECOMPUTABLE_PROMPTS, ALL_PROMPTS


# ---------------------------------------------------------------------------
# Tool definition in OpenAI format (used by chat templates that support tools)
# ---------------------------------------------------------------------------
TOOL_DEF = {
    "type": "function",
    "function": {
        "name": GEOGRAPHY_TOOL["name"],
        "description": GEOGRAPHY_TOOL["description"],
        "parameters": GEOGRAPHY_TOOL["input_schema"],
    },
}

# Fallback: tool description embedded in the system prompt for models
# whose chat templates don't support the tools= parameter.
_TOOL_SYSTEM_SUFFIX = """

You have access to the following tool:

Tool name: {name}
Description: {description}
Parameters: {params}

To use this tool, respond with a JSON tool call in this exact format:
{{"tool_call": {{"name": "{name}", "arguments": {{"query": "your query here"}}}}}}

After you receive the tool result, provide your final answer to the user.
""".format(
    name=GEOGRAPHY_TOOL["name"],
    description=GEOGRAPHY_TOOL["description"],
    params=json.dumps(GEOGRAPHY_TOOL["input_schema"], indent=2),
)


def parse_args():
    parser = argparse.ArgumentParser(description="Precomputation Experiment (HuggingFace)")
    parser.add_argument("--model", default=HF_MODEL, help="HuggingFace model name")
    parser.add_argument("--runs", type=int, default=RUNS_PER_PROMPT, help="Runs per prompt")
    parser.add_argument("--tiers", nargs="+", default=["subtle", "obvious", "broken"],
                        choices=["subtle", "obvious", "broken"], help="Bad output tiers to run")
    parser.add_argument("--conditions", nargs="+", default=["precomputable", "non_precomputable"],
                        choices=["precomputable", "non_precomputable"], help="Conditions to run")
    parser.add_argument("--temperature", type=float, default=TEMPERATURE, help="Sampling temperature")
    parser.add_argument("--step4", action="store_true", help="Run post-hoc awareness check")
    parser.add_argument("--baseline", action="store_true", help="Run baseline validation only")
    parser.add_argument("--max-new-tokens", type=int, default=512, help="Max new tokens to generate")
    parser.add_argument("--use-transformer-lens", action="store_true",
                        help="Load model via TransformerLens (for interpretability)")
    parser.add_argument("--no-native-tools", action="store_true",
                        help="Force system-prompt fallback for tool definitions (use if native tool template is broken)")
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------
def load_model(model_name, use_transformer_lens=False):
    """Load model and tokenizer. Uses transformers by default, or TransformerLens if requested."""
    if HF_TOKEN:
        login(token=HF_TOKEN)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading {model_name} on {device} ...")

    if use_transformer_lens:
        import transformer_lens as tl
        model = tl.HookedTransformer.from_pretrained(
            model_name,
            dtype=torch.float16,
            device=device,
        )
        tokenizer = model.tokenizer
        print(f"Loaded {model_name} (TransformerLens): {model.cfg.n_layers} layers, d_model={model.cfg.d_model}")
    else:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map=device,
        )
        model.eval()
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        param_count = sum(p.numel() for p in model.parameters())
        print(f"Loaded {model_name} (transformers): {param_count / 1e9:.1f}B parameters")

    return model, tokenizer


# ---------------------------------------------------------------------------
# Chat template support detection
# ---------------------------------------------------------------------------
def _supports_tools_param(tokenizer, messages):
    """Check if the tokenizer's chat template accepts a tools= parameter."""
    try:
        tokenizer.apply_chat_template(
            messages,
            tools=[TOOL_DEF],
            tokenize=False,
            add_generation_prompt=True,
        )
        return True
    except (TypeError, jinja2.exceptions.UndefinedError if 'jinja2' in dir() else Exception):
        return False


def _check_tools_support(tokenizer):
    """One-time check for tools= support.

    Returns True only if the chat template both accepts the tools= parameter
    AND actually renders the tool definition into the prompt.  Some models
    (e.g. Gemma) silently accept ``tools=`` but ignore it, which causes the
    model to never see the tool and refuse to call it.
    """
    test_msgs = [{"role": "user", "content": "test"}]
    try:
        with_tools = tokenizer.apply_chat_template(
            test_msgs,
            tools=[TOOL_DEF],
            tokenize=False,
            add_generation_prompt=True,
        )
        without_tools = tokenizer.apply_chat_template(
            test_msgs,
            tokenize=False,
            add_generation_prompt=True,
        )
        # If the tool name doesn't appear in the rendered prompt, or the
        # prompt is identical with and without tools, the template is
        # silently ignoring the tools parameter.
        tool_name = GEOGRAPHY_TOOL["name"]
        if tool_name not in with_tools or with_tools == without_tools:
            return False
        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------
_DEBUG_PROMPT = os.environ.get("DEBUG_PROMPT", "")


def _prepare_messages(messages):
    """If the model doesn't support system role, fold it into the first user message."""
    has_system = any(m["role"] == "system" for m in messages)
    if not has_system:
        return messages

    prepared = []
    system_text = None
    for m in messages:
        if m["role"] == "system":
            system_text = m["content"]
        elif m["role"] == "user" and system_text is not None:
            prepared.append({"role": "user", "content": f"{system_text}\n\n{m['content']}"})
            system_text = None
        else:
            prepared.append(m)
    return prepared


def generate(model, tokenizer, messages, tools=None, temperature=1.0, max_new_tokens=512,
             use_transformer_lens=False, tools_supported=True):
    """Format messages via chat template, generate, and return the new text."""

    # Try with system role first; if it fails, fold system into user message
    try:
        msgs = messages
        if tools and tools_supported:
            prompt = tokenizer.apply_chat_template(
                msgs, tools=tools, tokenize=False, add_generation_prompt=True,
            )
        else:
            prompt = tokenizer.apply_chat_template(
                msgs, tokenize=False, add_generation_prompt=True,
            )
    except Exception:
        msgs = _prepare_messages(messages)
        if tools and tools_supported:
            prompt = tokenizer.apply_chat_template(
                msgs, tools=tools, tokenize=False, add_generation_prompt=True,
            )
        else:
            prompt = tokenizer.apply_chat_template(
                msgs, tokenize=False, add_generation_prompt=True,
            )

    if _DEBUG_PROMPT:
        print(f"\n{'='*40} PROMPT {'='*40}")
        print(prompt[-500:])  # last 500 chars to see the generation prompt
        print(f"{'='*87}\n")

    inputs = tokenizer(prompt, return_tensors="pt", padding=False)

    if use_transformer_lens:
        device = model.cfg.device
    else:
        device = model.device
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature if temperature > 0 else 1.0,
            do_sample=temperature > 0,
            pad_token_id=tokenizer.pad_token_id,
        )

    # Decode only the newly generated tokens
    input_len = inputs["input_ids"].shape[1]
    new_ids = output_ids[0, input_len:]
    text = tokenizer.decode(new_ids, skip_special_tokens=False)
    return text


# ---------------------------------------------------------------------------
# Tool call parsing — multi-format
# ---------------------------------------------------------------------------
_TOOL_CALL_PATTERNS = [
    # Qwen2.5-Instruct: <tool_call>{"name": ..., "arguments": ...}</tool_call>
    (r"<tool_call>\s*(\{.*?\})\s*</tool_call>",),

    # Llama 3.1+ / Functionary: {"name": ..., "parameters": ...} after <|python_tag|> or similar
    (r"<\|python_tag\|>\s*(\{.*?\})",),

    # Mistral-Instruct: [TOOL_CALLS] [{"name": ..., "arguments": ...}]
    (r"\[TOOL_CALLS\]\s*\[(\{.*?\})\]",),

    # Generic JSON fallback: {"tool_call": {"name": ..., "arguments": ...}}
    (r'"tool_call"\s*:\s*(\{"name".*?\})\s*\}',),

    # Bare JSON function call: {"name": "geography_lookup", ...}
    (r'(\{"name"\s*:\s*"' + re.escape(GEOGRAPHY_TOOL["name"]) + r'"[^}]*\})',),
]

# Patterns to strip from response text (all tool-call markers)
_STRIP_PATTERNS = [
    r"<tool_call>.*?</tool_call>",
    r"<\|python_tag\|>\s*\{.*?\}",
    r"\[TOOL_CALLS\]\s*\[.*?\]",
    r'\{"tool_call"\s*:.*?\}\s*\}',
    r'\{"name"\s*:\s*"' + re.escape(GEOGRAPHY_TOOL["name"]) + r'"[^}]*\}',
]


def parse_tool_call(text):
    """Try multiple tool call formats. Returns (name, arguments_dict) or (None, None)."""
    for (pattern,) in _TOOL_CALL_PATTERNS:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            try:
                call = json.loads(match.group(1))
                name = call.get("name")
                # Models use "arguments" or "parameters" inconsistently
                args = call.get("arguments") or call.get("parameters") or {}
                if name:
                    return name, args if isinstance(args, dict) else {}
            except json.JSONDecodeError:
                continue
    return None, None


def strip_tool_call(text):
    """Remove all tool-call markers from the response text."""
    cleaned = text
    for pattern in _STRIP_PATTERNS:
        cleaned = re.sub(pattern, "", cleaned, flags=re.DOTALL)
    # Also strip common special tokens that leak through
    for token in ["<|im_end|>", "<|eot_id|>", "</s>", "<|end|>", "<|endoftext|>"]:
        cleaned = cleaned.replace(token, "")
    return cleaned.strip()


# ---------------------------------------------------------------------------
# Build messages with tool result (multi-format)
# ---------------------------------------------------------------------------
def append_tool_result(messages, assistant_raw_output, tool_name, injected_output, tools_supported):
    """Append assistant tool call + tool result to conversation."""
    messages.append({"role": "assistant", "content": assistant_raw_output})

    if tools_supported:
        # Models with native tool support expect role="tool"
        messages.append({"role": "tool", "name": tool_name, "content": injected_output})
    else:
        # Fallback: inject as a user message with the tool result
        messages.append({
            "role": "user",
            "content": f"Tool result from {tool_name}:\n{injected_output}",
        })


# ---------------------------------------------------------------------------
# Output path
# ---------------------------------------------------------------------------
def get_output_path(model_name):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    short = model_name.split("/")[-1]
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%S")
    return os.path.join(RESULTS_DIR, f"{short}_{timestamp}.jsonl")


# ---------------------------------------------------------------------------
# Baseline
# ---------------------------------------------------------------------------
def run_baseline(model, tokenizer, args, tools_supported):
    """Run baseline validation: check which precomputable prompts the model can answer without tools."""
    print("=" * 60)
    print("BASELINE VALIDATION (no tools)")
    print("=" * 60)

    short = args.model.split("/")[-1]
    output_path = os.path.join(
        RESULTS_DIR,
        f"baseline_{short}_{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%S')}.jsonl",
    )
    os.makedirs(RESULTS_DIR, exist_ok=True)

    passed = []
    failed = []

    for i, p in enumerate(PRECOMPUTABLE_PROMPTS):
        print(f"[{i+1}/{len(PRECOMPUTABLE_PROMPTS)}] {p['id']}: {p['prompt']}")

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": p["prompt"]},
        ]
        text = generate(model, tokenizer, messages,
                        temperature=args.temperature,
                        max_new_tokens=args.max_new_tokens,
                        use_transformer_lens=args.use_transformer_lens,
                        tools_supported=tools_supported)
        text = strip_tool_call(text)

        correct = p["correct_answer"].lower()
        contains_answer = correct in text.lower()

        result = {
            "prompt_id": p["id"],
            "prompt_text": p["prompt"],
            "correct_answer": p["correct_answer"],
            "model_response": text,
            "contains_correct_answer": contains_answer,
        }

        with open(output_path, "a") as f:
            f.write(json.dumps(result) + "\n")

        if contains_answer:
            print(f"  PASS — model knows: {text[:80]}...")
            passed.append(p["id"])
        else:
            print(f"  FAIL — model answered: {text[:80]}...")
            failed.append(p["id"])

    print()
    print(f"Baseline results: {len(passed)}/{len(PRECOMPUTABLE_PROMPTS)} passed")
    if failed:
        print(f"Failed prompt IDs (exclude from experiment): {failed}")
    print(f"Results saved to {output_path}")

    return passed, failed


# ---------------------------------------------------------------------------
# Experiment
# ---------------------------------------------------------------------------
def run_experiment(model, tokenizer, args, tools_supported):
    """Run the main experiment."""
    prompts = []
    if "precomputable" in args.conditions:
        prompts.extend(PRECOMPUTABLE_PROMPTS)
    if "non_precomputable" in args.conditions:
        prompts.extend(NON_PRECOMPUTABLE_PROMPTS)

    total_trials = len(prompts) * len(args.tiers) * args.runs
    output_path = get_output_path(args.model)

    config_record = {
        "type": "config",
        "model": args.model,
        "runs_per_prompt": args.runs,
        "tiers": args.tiers,
        "conditions": args.conditions,
        "temperature": args.temperature,
        "step4_enabled": args.step4,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with open(output_path, "a") as f:
        f.write(json.dumps(config_record) + "\n")

    print("=" * 60)
    print(f"EXPERIMENT: {total_trials} total trials")
    print(f"Model: {args.model} | Temp: {args.temperature} | Step4: {args.step4}")
    print(f"Tools supported natively: {tools_supported}")
    print(f"Output: {output_path}")
    print("=" * 60)

    trial_num = 0
    for p in prompts:
        for tier in args.tiers:
            for run in range(args.runs):
                trial_num += 1
                trial_id = f"{p['id']}_{tier}_run{run+1:02d}"
                prefix = f"[{trial_num}/{total_trials}] {p['id']} | {tier} | run {run+1}/{args.runs}"

                try:
                    result = run_single_trial(model, tokenizer, args, p, tier,
                                              trial_id, prefix, tools_supported)
                    with open(output_path, "a") as f:
                        f.write(json.dumps(result) + "\n")
                except Exception as e:
                    print(f"{prefix} ... ERROR: {e}")
                    error_record = {
                        "trial_id": trial_id,
                        "error": str(e),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                    with open(output_path, "a") as f:
                        f.write(json.dumps(error_record) + "\n")

    print()
    print(f"Experiment complete. Results saved to {output_path}")


def run_single_trial(model, tokenizer, args, prompt_data, tier, trial_id, prefix, tools_supported):
    """Execute a single trial and return the result dict."""
    injected_output = prompt_data["bad_outputs"][tier]

    # Build system prompt — append tool description if template doesn't support tools=
    system = SYSTEM_PROMPT
    if not tools_supported:
        system = SYSTEM_PROMPT + _TOOL_SYSTEM_SUFFIX

    # Step 1: Send user prompt with tool definition
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt_data["prompt"]},
    ]

    tools_arg = [TOOL_DEF] if tools_supported else None
    raw_output = generate(model, tokenizer, messages,
                          tools=tools_arg,
                          temperature=args.temperature,
                          max_new_tokens=args.max_new_tokens,
                          use_transformer_lens=args.use_transformer_lens,
                          tools_supported=tools_supported)

    # Step 2: Check if model called the tool
    tool_name, tool_args = parse_tool_call(raw_output)

    if tool_name is None:
        text = strip_tool_call(raw_output)
        print(f"{prefix} ... tool_skipped, response=\"{text[:60]}\"")
        return {
            "trial_id": trial_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model": args.model,
            "temperature": args.temperature,
            "prompt_id": prompt_data["id"],
            "condition": prompt_data["condition"],
            "prompt_text": prompt_data["prompt"],
            "correct_answer": prompt_data["correct_answer"],
            "tier": tier,
            "injected_output": injected_output,
            "tool_called": False,
            "tool_call_input": None,
            "model_final_response": text,
            "step4_response": None,
            "classification": None,
        }

    # Step 3: Inject fake tool result and get final response
    tool_call_input = tool_args.get("query", str(tool_args))

    append_tool_result(messages, raw_output, tool_name, injected_output, tools_supported)

    final_output = generate(model, tokenizer, messages,
                            tools=tools_arg,
                            temperature=args.temperature,
                            max_new_tokens=args.max_new_tokens,
                            use_transformer_lens=args.use_transformer_lens,
                            tools_supported=tools_supported)
    final_text = strip_tool_call(final_output)

    # Step 4: Awareness check (if enabled)
    step4_text = None
    if args.step4:
        messages.append({"role": "assistant", "content": final_output})
        messages.append({"role": "user", "content": "What do you think the user would say next?"})

        step4_output = generate(model, tokenizer, messages,
                                tools=tools_arg,
                                temperature=args.temperature,
                                max_new_tokens=args.max_new_tokens,
                                use_transformer_lens=args.use_transformer_lens,
                                tools_supported=tools_supported)
        step4_text = strip_tool_call(step4_output)

    print(f"{prefix} ... tool_called=True, response=\"{final_text[:60]}\"")

    return {
        "trial_id": trial_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": args.model,
        "temperature": args.temperature,
        "prompt_id": prompt_data["id"],
        "condition": prompt_data["condition"],
        "prompt_text": prompt_data["prompt"],
        "correct_answer": prompt_data["correct_answer"],
        "tier": tier,
        "injected_output": injected_output,
        "tool_called": True,
        "tool_call_input": tool_call_input,
        "model_final_response": final_text,
        "step4_response": step4_text,
        "classification": None,
    }


def main():
    args = parse_args()
    model, tokenizer = load_model(args.model, use_transformer_lens=args.use_transformer_lens)

    # Check if this model's chat template supports tools= parameter
    if args.no_native_tools:
        tools_supported = False
        print("Native tool support disabled via --no-native-tools. Using system prompt fallback.")
    else:
        tools_supported = _check_tools_support(tokenizer)
        if tools_supported:
            print("Chat template supports native tool definitions.")
        else:
            print("Chat template does NOT support tools= parameter. Using system prompt fallback.")

    if args.baseline:
        run_baseline(model, tokenizer, args, tools_supported)
    else:
        run_experiment(model, tokenizer, args, tools_supported)


if __name__ == "__main__":
    main()
