# settings.py
import os

# --- Live, Mutable Settings ---
NUM_RESPONSES = 2
DEEPCONF_ENABLED = False # Disabled until streeaming redone for ollama
CONFIDENCE_THRESHOLD = 0.21 # Start with a reasonable default
RELIABILITY_THRESHOLD = 0.25 # The minimum group_low_conf for a response to be accepted without remediation
# --- Model Configuration ---
# Define your models here as they appear in `ollama list`
VERIFIER_MODEL = "qwen2:4b"
DRAFT_MODEL = "tinyllama:1b"

# Active Model for the entire application
ACTIVE_MODEL_NAME = VERIFIER_MODEL