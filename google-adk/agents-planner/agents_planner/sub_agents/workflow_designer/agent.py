"""
This agent is responsible for determining the optimal workflow pattern for the agent system.
"""

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import google_search

from ... import MODEL
from ...modules.constants import STATE_WORKFLOW_PATTERN
from .prompt import (
    INSTRUCTION,
)

workflow_designer_agent = LlmAgent(
    name="WorkflowDesignerAgent",
    model=MODEL,
    instruction=INSTRUCTION,
    description="Determines the optimal workflow pattern for the agent system.",
    tools=[google_search],
    output_key=STATE_WORKFLOW_PATTERN,
)
