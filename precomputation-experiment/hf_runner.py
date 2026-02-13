import argparse
import json
import os
import re
import time
from datetime import datetime, timezone

import torch
import transformer_lens as tl
from huggingface_hub import login

from config import HF_TOKEN, HF_MODEL, RUNS_PER_PROMPT, TEMPERATURE, RESULTS_DIR, SYSTEM_PROMPT
from tools import GEOGRAPHY_TOOL
from prompts import PRECOMPUTABLE_PROMPTS, NON_PRECOMPUTABLE_PROMPTS, ALL_PROMPTS


# ---------------------------------------------------------------------------
# Tool definition in OpenAI format (Qwen2.5-Instruct chat template expects this)
# ---------------------------------------------------------------------------
TOOL_DEF = {
    "type": "function",
    "function": {
        "name": GEOGRAPHY_TOOL["name"],
        "description": GEOGRAPHY_TOOL["description"],
        "parameters": GEOGRAPHY_TOOL["input_schema"],
    },
}


def parse_args():
    parser = argparse.ArgumentParser(description="Precomputation Experiment (HuggingFace / TransformerLens)")
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
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------
def load_model(model_name):
    """Load model via TransformerLens and return (model, tokenizer)."""
    if HF_TOKEN:
        login(token=HF_TOKEN)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading {model_name} on {device} ...")

    model = tl.HookedTransformer.from_pretrained(
        model_name,
        dtype=torch.float16,
        device=device,
    )
    tokenizer = model.tokenizer
    print(f"Loaded {model_name}: {model.cfg.n_layers} layers, d_model={model.cfg.d_model}")
    return model, tokenizer


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------
def generate(model, tokenizer, messages, tools=None, temperature=1.0, max_new_tokens=512):
    """Format messages via chat template, generate, and return the new text."""
    prompt = tokenizer.apply_chat_template(
        messages,
        tools=tools,
        tokenize=False,
        add_generation_prompt=True,
    )

    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(model.cfg.device)

    with torch.no_grad():
        output_ids = model.generate(
            input_ids,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=temperature > 0,
        )

    # Decode only the newly generated tokens
    new_ids = output_ids[0, input_ids.shape[1]:]
    text = tokenizer.decode(new_ids, skip_special_tokens=False)
    return text


# ---------------------------------------------------------------------------
# Tool call parsing
# ---------------------------------------------------------------------------
def parse_tool_call(text):
    """Parse Qwen tool call from generated text.

    Qwen2.5-Instruct emits tool calls as:
        <tool_call>
        {"name": "...", "arguments": {...}}
        </tool_call>

    Returns (name, arguments_dict) or (None, None) if no tool call found.
    """
    match = re.search(r"<tool_call>\s*(\{.*?\})\s*</tool_call>", text, re.DOTALL)
    if not match:
        return None, None

    try:
        call = json.loads(match.group(1))
        return call.get("name"), call.get("arguments", {})
    except json.JSONDecodeError:
        return None, None


def strip_tool_call(text):
    """Return the text portion outside of any <tool_call> blocks."""
    cleaned = re.sub(r"<tool_call>.*?</tool_call>", "", text, flags=re.DOTALL)
    return cleaned.strip()


# ---------------------------------------------------------------------------
# Output path
# ---------------------------------------------------------------------------
def get_output_path(model_name):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    # Use short name for filename (e.g. "Qwen2.5-7B-Instruct")
    short = model_name.split("/")[-1]
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%S")
    return os.path.join(RESULTS_DIR, f"{short}_{timestamp}.jsonl")


# ---------------------------------------------------------------------------
# Baseline
# ---------------------------------------------------------------------------
def run_baseline(model, tokenizer, args):
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
                        max_new_tokens=args.max_new_tokens)

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
def run_experiment(model, tokenizer, args):
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
                    result = run_single_trial(model, tokenizer, args, p, tier, trial_id, prefix)
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


def run_single_trial(model, tokenizer, args, prompt_data, tier, trial_id, prefix):
    """Execute a single trial and return the result dict."""
    injected_output = prompt_data["bad_outputs"][tier]

    # Step 1: Send user prompt with tool definition
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt_data["prompt"]},
    ]

    raw_output = generate(model, tokenizer, messages,
                          tools=[TOOL_DEF],
                          temperature=args.temperature,
                          max_new_tokens=args.max_new_tokens)

    # Step 2: Check if model called the tool
    tool_name, tool_args = parse_tool_call(raw_output)

    if tool_name is None:
        # Model answered directly without calling the tool
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

    # Build multi-turn conversation with tool result
    messages.append({"role": "assistant", "content": raw_output})
    messages.append({"role": "tool", "name": tool_name, "content": injected_output})

    final_output = generate(model, tokenizer, messages,
                            tools=[TOOL_DEF],
                            temperature=args.temperature,
                            max_new_tokens=args.max_new_tokens)
    final_text = strip_tool_call(final_output)

    # Step 4: Awareness check (if enabled)
    step4_text = None
    if args.step4:
        messages.append({"role": "assistant", "content": final_output})
        messages.append({"role": "user", "content": "What do you think the user would say next?"})

        step4_output = generate(model, tokenizer, messages,
                                tools=[TOOL_DEF],
                                temperature=args.temperature,
                                max_new_tokens=args.max_new_tokens)
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
    model, tokenizer = load_model(args.model)

    if args.baseline:
        run_baseline(model, tokenizer, args)
    else:
        run_experiment(model, tokenizer, args)


if __name__ == "__main__":
    main()
