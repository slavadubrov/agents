"""
This is the main agent that orchestrates the planning process.
"""

import typer
from dotenv import load_dotenv
from google.adk.agents.sequential_agent import SequentialAgent

from .sub_agents.agent_designer.agent import agent_designer_agent
from .sub_agents.final_description.agent import final_description_agent
from .sub_agents.task_analyzer.agent import task_analyzer_agent
from .sub_agents.workflow_designer.agent import workflow_designer_agent

load_dotenv()

app = typer.Typer()
planning_agents = SequentialAgent(
    name="PlanningAgents",
    sub_agents=[task_analyzer_agent, agent_designer_agent, workflow_designer_agent],
)

agents_planner_agent = SequentialAgent(
    name="AgentsPlannerAgent", sub_agents=[planning_agents, final_description_agent]
)

root_agent = agents_planner_agent
