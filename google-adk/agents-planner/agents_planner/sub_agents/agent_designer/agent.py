"""
This agent is responsible for designing appropriate agents for each subtask.
"""

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import google_search

from ... import MODEL
from ...modules.constants import STATE_AGENT_DESCRIPTIONS
from .prompt import (
    INSTRUCTION,
)

agent_designer_agent = LlmAgent(
    name="AgentDesignerAgent",
    model=MODEL,
    instruction=INSTRUCTION,
    description="Designs appropriate agents for each subtask.",
    tools=[google_search],
    output_key=STATE_AGENT_DESCRIPTIONS,
)
