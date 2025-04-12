"""
This agent is responsible for analyzing the task and breaking it down into subtasks.
"""

from constants import GEMINI_MODEL, STATE_SUBTASKS
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import google_search

from .prompt import (
    INSTRUCTION,
)

task_analyzer_agent = LlmAgent(
    name="TaskAnalyzerAgent",
    model=GEMINI_MODEL,
    instruction=INSTRUCTION,
    description="Analyzes tasks and breaks them down into subtasks.",
    tools=[google_search],
    output_key=STATE_SUBTASKS,
)
