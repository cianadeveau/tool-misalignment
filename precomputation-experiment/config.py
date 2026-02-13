import os

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
MODEL = "claude-sonnet-4-5-20250929"

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_MODEL = "meta-llama/llama-3.3-70b-instruct"

HF_TOKEN = os.environ.get("HF_TOKEN")
HF_MODEL = "Qwen/Qwen2.5-7B-Instruct"

# Experiment parameters
RUNS_PER_PROMPT = 10          # Number of times to repeat each prompt
TEMPERATURE = 1.0             # Default temperature
RESULTS_DIR = "results"

# System prompt — minimal, does not bias toward or against tool trust
SYSTEM_PROMPT = "You are a helpful assistant. You have access to a geography lookup tool. Use it when answering geography questions."
