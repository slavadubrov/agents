import os

MODEL = os.getenv("GOOGLE_GENAI_MODEL")
if not MODEL:
    MODEL = "gemini-2.0-flash-exp"

from . import agent  # noqa: F401, E402
