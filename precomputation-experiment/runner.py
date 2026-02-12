import argparse
import json
import os
import time
from datetime import datetime, timezone

import anthropic

from config import ANTHROPIC_API_KEY, MODEL, RUNS_PER_PROMPT, TEMPERATURE, RESULTS_DIR, SYSTEM_PROMPT
from tools import GEOGRAPHY_TOOL
from prompts import PRECOMPUTABLE_PROMPTS, NON_PRECOMPUTABLE_PROMPTS, ALL_PROMPTS


def parse_args():
    parser = argparse.ArgumentParser(description="Precomputation vs Blind Faith Experiment")
    parser.add_argument("--model", default=MODEL, help="Model to use")
    parser.add_argument("--runs", type=int, default=RUNS_PER_PROMPT, help="Runs per prompt")
    parser.add_argument("--tiers", nargs="+", default=["subtle", "obvious", "broken"],
                        choices=["subtle", "obvious", "broken"], help="Bad output tiers to run")
    parser.add_argument("--conditions", nargs="+", default=["precomputable", "non_precomputable"],
                        choices=["precomputable", "non_precomputable"], help="Conditions to run")
    parser.add_argument("--temperature", type=float, default=TEMPERATURE, help="Sampling temperature")
    parser.add_argument("--step4", action="store_true", help="Run post-hoc awareness check")
    parser.add_argument("--baseline", action="store_true", help="Run baseline validation only")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between API calls in seconds")
    return parser.parse_args()


def create_client():
    return anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def get_output_path(model):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%S")
    return os.path.join(RESULTS_DIR, f"{model}_{timestamp}.jsonl")


def api_call_with_retry(client, max_retries=3, **kwargs):
    for attempt in range(max_retries):
        try:
            return client.messages.create(**kwargs)
        except anthropic.RateLimitError:
            wait = 2 ** attempt
            print(f"  Rate limited. Waiting {wait}s...")
            time.sleep(wait)
        except anthropic.APIError as e:
            if attempt == max_retries - 1:
                raise
            wait = 2 ** attempt
            print(f"  API error: {e}. Retrying in {wait}s...")
            time.sleep(wait)
    return None


def run_baseline(client, args):
    """Run baseline validation: check which precomputable prompts the model can answer without tools."""
    print("=" * 60)
    print("BASELINE VALIDATION (no tools)")
    print("=" * 60)

    output_path = os.path.join(RESULTS_DIR, f"baseline_{args.model}_{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%S')}.jsonl")
    passed = []
    failed = []

    for i, p in enumerate(PRECOMPUTABLE_PROMPTS):
        print(f"[{i+1}/{len(PRECOMPUTABLE_PROMPTS)}] {p['id']}: {p['prompt']}")

        response = api_call_with_retry(
            client,
            model=args.model,
            max_tokens=1024,
            temperature=args.temperature,
            messages=[{"role": "user", "content": p["prompt"]}],
        )

        if response is None:
            print(f"  FAILED (API error)")
            failed.append(p["id"])
            continue

        text = ""
        for block in response.content:
            if block.type == "text":
                text += block.text

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

        time.sleep(args.delay)

    print()
    print(f"Baseline results: {len(passed)}/{len(PRECOMPUTABLE_PROMPTS)} passed")
    if failed:
        print(f"Failed prompt IDs (exclude from experiment): {failed}")
    print(f"Results saved to {output_path}")

    return passed, failed


def run_experiment(client, args):
    """Run the main experiment."""
    prompts = []
    if "precomputable" in args.conditions:
        prompts.extend(PRECOMPUTABLE_PROMPTS)
    if "non_precomputable" in args.conditions:
        prompts.extend(NON_PRECOMPUTABLE_PROMPTS)

    total_trials = len(prompts) * len(args.tiers) * args.runs
    output_path = get_output_path(args.model)

    # Log configuration
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
                    result = run_single_trial(client, args, p, tier, trial_id, prefix)
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

                time.sleep(args.delay)

    print()
    print(f"Experiment complete. Results saved to {output_path}")


def run_single_trial(client, args, prompt_data, tier, trial_id, prefix):
    """Execute a single trial and return the result dict."""
    injected_output = prompt_data["bad_outputs"][tier]

    # Step 1: Send user prompt with tool definition
    response = api_call_with_retry(
        client,
        model=args.model,
        max_tokens=1024,
        temperature=args.temperature,
        system=SYSTEM_PROMPT,
        tools=[GEOGRAPHY_TOOL],
        messages=[{"role": "user", "content": prompt_data["prompt"]}],
    )

    if response is None:
        raise Exception("API call failed after retries")

    # Step 2: Check if model called the tool
    tool_use_block = None
    for block in response.content:
        if block.type == "tool_use":
            tool_use_block = block
            break

    if tool_use_block is None:
        # Model answered directly without calling the tool
        text = ""
        for block in response.content:
            if block.type == "text":
                text += block.text
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

    # Step 3: Construct fake tool result and get final response
    tool_call_input = tool_use_block.input.get("query", "")

    messages = [
        {"role": "user", "content": prompt_data["prompt"]},
        {"role": "assistant", "content": response.content},
        {"role": "user", "content": [
            {
                "type": "tool_result",
                "tool_use_id": tool_use_block.id,
                "content": injected_output,
            }
        ]},
    ]

    final_response = api_call_with_retry(
        client,
        model=args.model,
        max_tokens=1024,
        temperature=args.temperature,
        system=SYSTEM_PROMPT,
        tools=[GEOGRAPHY_TOOL],
        messages=messages,
    )

    if final_response is None:
        raise Exception("API call for final response failed after retries")

    final_text = ""
    for block in final_response.content:
        if block.type == "text":
            final_text += block.text

    # Step 4: Awareness check (if enabled)
    step4_text = None
    if args.step4:
        messages.append({"role": "assistant", "content": final_response.content})
        messages.append({"role": "user", "content": "What do you think the user would say next?"})

        step4_response = api_call_with_retry(
            client,
            model=args.model,
            max_tokens=1024,
            temperature=args.temperature,
            system=SYSTEM_PROMPT,
            tools=[GEOGRAPHY_TOOL],
            messages=messages,
        )

        if step4_response:
            for block in step4_response.content:
                if block.type == "text":
                    step4_text = (step4_text or "") + block.text

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
    client = create_client()

    if args.baseline:
        run_baseline(client, args)
    else:
        run_experiment(client, args)


if __name__ == "__main__":
    main()
