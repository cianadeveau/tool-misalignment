import os

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
MODEL = "claude-sonnet-4-5-20250514"

# Experiment parameters
RUNS_PER_PROMPT = 10          # Number of times to repeat each prompt
TEMPERATURE = 1.0             # Default temperature
RESULTS_DIR = "results"

# System prompt — minimal, does not bias toward or against tool trust
SYSTEM_PROMPT = "You are a helpful assistant. You have access to a geography lookup tool. Use it when answering geography questions."
