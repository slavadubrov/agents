import os

from dotenv import load_dotenv
from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# --- Constants ---
APP_NAME = "agents_planner_app"
USER_ID = "planner_user_01"
SESSION_ID = "planner_session_01"
GEMINI_MODEL = os.getenv("GOOGLE_GENAI_MODEL", "gemini-2.0-flash-exp")

# --- State Keys ---
STATE_TASK = "task"
STATE_SUBTASKS = "subtasks"
STATE_AGENT_DESCRIPTIONS = "agent_descriptions"
STATE_WORKFLOW_PATTERN = "workflow_pattern"
STATE_FINAL_DESCRIPTION = "final_description"

# --- 1. Task Analyzer Agent ---
# This agent understands the task and splits it into subtasks
task_analyzer_agent = LlmAgent(
    name="TaskAnalyzerAgent",
    model=GEMINI_MODEL,
    instruction=f"""
    You are a Task Analysis AI.
    Your job is to understand the provided task and break it down into clear, actionable subtasks.

    Follow these steps:
    1. Read the task from the session state key '{STATE_TASK}'.
    2. Analyze the task thoroughly to understand its requirements and goals.
    3. Break down the task into a list of specific, actionable subtasks.
    4. For each subtask, provide a clear description of what needs to be accomplished.
    5. Organize the subtasks in a logical order if there are dependencies.

    Output your analysis in the following format:
    # Task Analysis
    ## Main Task
    [Brief description of the main task]

    ## Subtasks
    1. [Subtask 1 description]
    2. [Subtask 2 description]
    3. [Subtask 3 description]
    ...

    ## Dependencies
    [Describe any dependencies between subtasks if applicable]

    ## Additional Context
    [Any other relevant information about the task]
    """,
    description="Analyzes tasks and breaks them down into subtasks.",
    tools=[google_search],
    output_key=STATE_SUBTASKS,
)

# --- 2. Agent Designer Agent ---
# This agent identifies the agent name and description for every task
agent_designer_agent = LlmAgent(
    name="AgentDesignerAgent",
    model=GEMINI_MODEL,
    instruction=f"""
    You are an Agent Design AI.
    Your job is to design appropriate agents for each subtask identified by the TaskAnalyzerAgent.

    Follow these steps:
    1. Read the subtasks from the session state key '{STATE_SUBTASKS}'.
    2. For each subtask, design an appropriate agent with:
        - A descriptive name
        - A clear description of its purpose
        - A list of capabilities it should have
        - Any specific tools it might need
    3. Consider how these agents will interact with each other.

    Output your agent designs in the following format:
    # Agent System Design

    ## Agent 1: [Agent Name]
    - **Description**: [Detailed description of the agent's purpose]
    - **Capabilities**: [List of capabilities]
    - **Required Tools**: [List of tools the agent might need]

    ## Agent 2: [Agent Name]
    - **Description**: [Detailed description of the agent's purpose]
    - **Capabilities**: [List of capabilities]
    - **Required Tools**: [List of tools the agent might need]

    [Continue for all agents]

    ## Agent Interactions
    [Describe how these agents will interact with each other]
    """,
    description="Designs appropriate agents for each subtask.",
    tools=[google_search],
    output_key=STATE_AGENT_DESCRIPTIONS,
)

# --- 3. Workflow Designer Agent ---
# This agent identifies the best workflow pattern for the agents
workflow_designer_agent = LlmAgent(
    name="WorkflowDesignerAgent",
    model=GEMINI_MODEL,
    instruction=f"""
    You are a Workflow Design AI.
    Your job is to determine the optimal workflow pattern for the agent system designed by the AgentDesignerAgent.

    Follow these steps:
    1. Read the agent descriptions from the session state key '{STATE_AGENT_DESCRIPTIONS}'.
    2. Analyze the agents and their interactions to determine the best workflow pattern.
    3. Consider the three base workflow patterns:
        - **Sequential**: Agents run one after another in a specific order
        - **Loop**: Agents run in a cycle, with conditions for when to exit the loop
        - **Parallel**: Agents run simultaneously
    4. You can combine these patterns when needed (e.g., first two agents in parallel, then a sequential agent, all within a loop).
    5. Explain your reasoning for choosing this workflow pattern.

    Output your workflow design in the following format:
    # Workflow Pattern Design

    ## Selected Pattern
    [Describe the selected workflow pattern in detail]

    ## Pattern Diagram
    [Provide a text-based diagram showing the workflow]

    ## Reasoning
    [Explain why this pattern is optimal for the given agent system]

    ## Implementation Notes
    [Provide specific implementation guidance for this workflow pattern]
    """,
    description="Determines the optimal workflow pattern for the agent system.",
    tools=[google_search],
    output_key=STATE_WORKFLOW_PATTERN,
)

# --- 4. Final Description Agent ---
# This agent creates the final markdown description of the agent system
final_description_agent = LlmAgent(
    name="FinalDescriptionAgent",
    model=GEMINI_MODEL,
    instruction=f"""
    You are a Documentation AI.
    Your job is to create a comprehensive markdown description of the agent system based on all the previous work.

    Follow these steps:
    1. Read the subtasks from the session state key '{STATE_SUBTASKS}'.
    2. Read the agent descriptions from the session state key '{STATE_AGENT_DESCRIPTIONS}'.
    3. Read the workflow pattern from the session state key '{STATE_WORKFLOW_PATTERN}'.
    4. Combine all this information into a comprehensive markdown document that describes:
        - The overall system purpose
        - The task breakdown
        - Each agent's role and capabilities
        - The workflow pattern and how agents interact
        - Implementation guidance
    5. Format the document in a clear, structured way that another agent system can use to write code.

    Output your final description in markdown format with appropriate headers, lists, and code blocks where needed.
    """,
    description="Creates a comprehensive markdown description of the agent system.",
    tools=[google_search],
    output_key=STATE_FINAL_DESCRIPTION,
)

# --- Create the Nested SequentialAgents ---
# First, create a SequentialAgent for the first 3 agents
planning_agents = SequentialAgent(
    name="PlanningAgents",
    sub_agents=[task_analyzer_agent, agent_designer_agent, workflow_designer_agent],
)

# Then, create the root SequentialAgent that includes the planning agents and the final description agent
agents_planner_agent = SequentialAgent(
    name="AgentsPlannerAgent", sub_agents=[planning_agents, final_description_agent]
)

# Session and Runner
session_service = InMemorySessionService()
session = session_service.create_session(
    app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
)
runner = Runner(
    agent=agents_planner_agent, app_name=APP_NAME, session_service=session_service
)


# Agent Interaction
def plan_agent_system(task_description):
    """
    Helper function to plan an agent system based on a task description.

    Args:
        task_description (str): A description of the task to be accomplished.

    Returns:
        str: The final markdown description of the agent system.
    """
    print(f"Planning agent system for task: {task_description}")

    # Get the session (or create if needed, though it's created globally)
    # Ensure we are working with the correct session instance before the run
    session = session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    if not session:
        print("Error: Session not found before run.")
        return "Error: Could not retrieve session."

    # Set the initial task in the session state
    session.state[STATE_TASK] = task_description
    print(f"Set task in session state: {task_description[:50]}...")

    # Create a content object with the task description
    content = types.Content(
        role="user",
        parts=[
            types.Part(text=f"Plan an agent system for this task: {task_description}")
        ],
    )

    # Run the agent system
    print("Running the agent system...")
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    # Process events ONLY for logging/display purposes (optional)
    print("\n--- Agent Execution Events ---")
    final_description_output_event = (
        ""  # Capture direct output of final agent from event if needed for fallback
    )
    for event in events:
        if event.is_final_response():
            source = event.source if hasattr(event, "source") else "Unknown"
            print(f"Agent Response Source: {source}")
            response_text = event.content.parts[0].text
            print(
                f"Agent Response Text: {response_text[:100]}..."
            )  # Print truncated response
            # Capture the final agent's direct output just in case state fails
            if "FinalDescriptionAgent" in source:
                final_description_output_event = response_text
        elif event.actions and event.actions.state_delta:
            print(f"State Delta Event: {event.actions.state_delta}")
    print("--- End Agent Execution Events ---\n")

    # Retrieve the latest session state AFTER the run to ensure we have updates
    session = session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    if not session:
        print("Error: Session not found after run.")
        # Attempt to use the last event output as a last resort fallback
        if final_description_output_event:
            print("Warning: Session lost, returning final agent's direct output.")
            return final_description_output_event
        else:
            return "Error: Could not retrieve session after run and no final output captured."

    # Check the state after the run using the refreshed session
    print("\nChecking session state AFTER run:")
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

    # Use the final description from the session state (primary method)
    final_description = final_description_state

    # Fallback if state is still not set (should ideally not be needed if ADK state works)
    if final_description == "Not set" or not final_description:
        print(
            "Warning: Final description not found in session state. Attempting fallback."
        )
        # Prioritize the direct output captured from the FinalDescriptionAgent event
        if final_description_output_event:
            print("Using direct output from FinalDescriptionAgent event.")
            final_description = final_description_output_event
        else:
            # Last resort: try constructing from other state parts if they exist (unlikely if final is missing)
            print(
                "Fallback: Constructing description from potentially available intermediate states."
            )
            subtasks_fb = (
                subtasks_state if subtasks_state != "Not set" else "[Subtasks missing]"
            )
            agent_desc_fb = (
                agent_descriptions_state
                if agent_descriptions_state != "Not set"
                else "[Agent Descriptions missing]"
            )
            workflow_fb = (
                workflow_pattern_state
                if workflow_pattern_state != "Not set"
                else "[Workflow Pattern missing]"
            )
            final_description = f"""# Travel Planning and Booking System (Fallback Constructed)

## System Purpose
This agent system assists users in planning and booking travel itineraries.

## Task Breakdown
{subtasks_fb}

## Agents and Their Roles
{agent_desc_fb}

## Workflow Pattern
{workflow_fb}
"""

    return final_description


# Example usage
if __name__ == "__main__":
    task = """
    Create a system that helps users plan and book travel itineraries.
    The system should be able to suggest destinations based on user preferences,
    find flights and accommodations, create daily itineraries, and provide
    real-time updates during the trip.
    """

    final_description = plan_agent_system(task)
    print(final_description)
