"""
This agent is responsible for creating a comprehensive markdown description of the agent system.
"""

from constants import GEMINI_MODEL, STATE_FINAL_DESCRIPTION
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import google_search

from .prompt import (
    INSTRUCTION,
)

final_description_agent = LlmAgent(
    name="FinalDescriptionAgent",
    model=GEMINI_MODEL,
    instruction=INSTRUCTION,
    description="Creates a comprehensive markdown description of the agent system.",
    tools=[google_search],
    output_key=STATE_FINAL_DESCRIPTION,
)
