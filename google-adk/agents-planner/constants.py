import os

# --- Constants ---

GEMINI_MODEL = os.getenv("GOOGLE_GENAI_MODEL", "gemini-2.0-flash-exp")

# --- State Keys ---
STATE_TASK = "task"
STATE_SUBTASKS = "subtasks"
STATE_AGENT_DESCRIPTIONS = "agent_descriptions"
STATE_WORKFLOW_PATTERN = "workflow_pattern"
STATE_FINAL_DESCRIPTION = "final_description"
