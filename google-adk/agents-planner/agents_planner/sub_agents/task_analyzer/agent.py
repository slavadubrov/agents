"""
This agent is responsible for analyzing the task and breaking it down into subtasks.
"""

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import google_search

from ... import MODEL
from ...modules.constants import STATE_SUBTASKS
from .prompt import (
    INSTRUCTION,
)

task_analyzer_agent = LlmAgent(
    name="TaskAnalyzerAgent",
    model=MODEL,
    instruction=INSTRUCTION,
    description="Analyzes tasks and breaks them down into subtasks.",
    tools=[google_search],
    output_key=STATE_SUBTASKS,
)
