"""
This agent is responsible for designing appropriate agents for each subtask.
"""

from constants import GEMINI_MODEL, STATE_AGENT_DESCRIPTIONS
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import google_search

from .prompt import (
    INSTRUCTION,
)

agent_designer_agent = LlmAgent(
    name="AgentDesignerAgent",
    model=GEMINI_MODEL,
    instruction=INSTRUCTION,
    description="Designs appropriate agents for each subtask.",
    tools=[google_search],
    output_key=STATE_AGENT_DESCRIPTIONS,
)
