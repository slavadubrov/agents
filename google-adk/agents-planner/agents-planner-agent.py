"""
This is the main agent that orchestrates the planning process.
"""

from pathlib import Path

import typer
from constants import (
    STATE_AGENT_DESCRIPTIONS,
    STATE_FINAL_DESCRIPTION,
    STATE_SUBTASKS,
    STATE_TASK,
    STATE_WORKFLOW_PATTERN,
)
from dotenv import load_dotenv
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from sub_agents.agent_designer.agent import agent_designer_agent
from sub_agents.final_description.agent import final_description_agent
from sub_agents.task_analyzer.agent import task_analyzer_agent
from sub_agents.workflow_designer.agent import workflow_designer_agent
from utils import save_to_file

load_dotenv()

APP_NAME = "agents_planner_app"
USER_ID = "planner_user_01"
SESSION_ID = "planner_session_01"
OUTPUT_DIR = "data"

app = typer.Typer()
planning_agents = SequentialAgent(
    name="PlanningAgents",
    sub_agents=[task_analyzer_agent, agent_designer_agent, workflow_designer_agent],
)

agents_planner_agent = SequentialAgent(
    name="AgentsPlannerAgent", sub_agents=[planning_agents, final_description_agent]
)

session_service = InMemorySessionService()
session = session_service.create_session(
    app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
)
runner = Runner(
    agent=agents_planner_agent, app_name=APP_NAME, session_service=session_service
)


def plan_agent_system(task_description, verbose=False):
    """
    Helper function to plan an agent system based on a task description.

    Args:
        task_description (str): A description of the task to be accomplished.
        verbose (bool): If True, print additional debug information including session state.

    Returns:
        str: The final markdown description of the agent system.
    """
    print(f"Planning agent system for task: {task_description}")

    session = session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    session.state[STATE_TASK] = task_description
    print(f"Set task in session state: {task_description[:50]}...")

    content = types.Content(
        role="user",
        parts=[
            types.Part(text=f"Plan an agent system for this task: {task_description}")
        ],
    )

    print("Running the agent system...")
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    print("\n--- Agent Execution Events ---")
    for event in events:
        if event.is_final_response():
            source = event.source if hasattr(event, "source") else "Unknown"
            print(f"Agent Response Source: {source}")
            response_text = event.content.parts[0].text
            print(f"Agent Response Text: {response_text[:100]}...")
        elif event.actions and event.actions.state_delta:
            print(f"State Delta Event: {event.actions.state_delta}")
    print("--- End Agent Execution Events ---\n")

    session = session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    if verbose:
        _print_session_state(session)

    return session.state.get(STATE_FINAL_DESCRIPTION, "Not set")


def _print_session_state(session):
    """Helper function to print the current state of the session."""
    print("\nChecking session state:")
    task_state = session.state.get(STATE_TASK, "Not set")
    subtasks_state = session.state.get(STATE_SUBTASKS, "Not set")
    agent_descriptions_state = session.state.get(STATE_AGENT_DESCRIPTIONS, "Not set")
    workflow_pattern_state = session.state.get(STATE_WORKFLOW_PATTERN, "Not set")
    final_description_state = session.state.get(STATE_FINAL_DESCRIPTION, "Not set")

    print(f"Task: {'Set' if task_state != 'Not set' else 'Not set'}")
    print(f"Subtasks: {'Set' if subtasks_state != 'Not set' else 'Not set'}")
    print(
        f"Agent Descriptions: {'Set' if agent_descriptions_state != 'Not set' else 'Not set'}"
    )
    print(
        f"Workflow Pattern: {'Set' if workflow_pattern_state != 'Not set' else 'Not set'}"
    )
    print(
        f"Final Description: {'Set' if final_description_state != 'Not set' else 'Not set'}"
    )


@app.command()
def main(
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
):
    """Plans an agent system based on a predefined task description."""
    task = """
    Create a system that helps users plan and book travel itineraries.
    The system should be able to suggest destinations based on user preferences,
    find flights and accommodations, create daily itineraries, and provide
    real-time updates during the trip.
    """

    final_description = plan_agent_system(task, verbose=verbose)
    print("\n--- Final Agent System Description ---")
    print(final_description)
    print("--- End Final Agent System Description ---")

    # Save the final description to a markdown file using the utility function
    output_filename = "agent_system_plan.md"
    output_path = Path(OUTPUT_DIR)

    # Ensure the directory exists
    output_path.mkdir(parents=True, exist_ok=True)

    output_file = output_path / output_filename
    save_to_file(final_description, str(output_file))


if __name__ == "__main__":
    app()
