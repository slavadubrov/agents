# Agents Planner

The Agents Planner is a multi-agent system designed to help users plan and design AI agent workflows. It uses a sequential agent architecture to analyze tasks, design agents, create workflows, and generate comprehensive descriptions of the planned agent system.

## Overview

The Agents Planner helps users break down complex tasks into manageable components and design appropriate AI agents to handle each part of the workflow. It provides a structured approach to planning multi-agent systems by analyzing requirements, suggesting agent designs, and creating detailed workflow descriptions.

This agent demonstrates a multi-stage planning workflow that takes user requirements and transforms them into a complete agent system design. The process is largely automated, requiring minimal human interaction while providing comprehensive output.

## Agent Details

### Agent Architecture

The Agents Planner consists of several specialized sub-agents that work together in a sequential manner:

1. **Task Analyzer Agent**: Analyzes the user's requirements and breaks them down into specific tasks
2. **Agent Designer Agent**: Designs appropriate agents for each identified task
3. **Workflow Designer Agent**: Creates a workflow that coordinates the designed agents
4. **Final Description Agent**: Generates a comprehensive description of the entire system

### Key Features

#### Agents

- **root_agent**: The main entry point that orchestrates the entire planning process
- **planning_agents**: A sequential agent that coordinates the task analysis, agent design, and workflow design phases
- **task_analyzer_agent**: Analyzes and breaks down complex tasks
- **agent_designer_agent**: Designs appropriate agents for specific tasks
- **workflow_designer_agent**: Creates coordination workflows
- **final_description_agent**: Generates comprehensive system descriptions

#### Components

- **Sequential Agent Architecture**: Ensures ordered execution of planning steps
- **Task Analysis**: Breaks down complex requirements into manageable components
- **Agent Design**: Creates specialized agents for specific tasks
- **Workflow Design**: Develops coordination patterns between agents
- **System Description**: Generates detailed documentation of the planned system

## Setup and Installation

1. **Prerequisites:**

   **Python Environment:**

   Ensure you have Python 3.8+ installed on your system. It's recommended to use a virtual environment:

   ```bash
   python -m venv .venv
   source venv/bin/activate
   ```

2. **Installation:**

   Clone this repository and change to the repo directory:

   ```bash
   git clone <repository-url>
   cd agents-planner
   ```

   Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration:**

   Copy the example environment file and update it with your settings:

   ```bash
   cp .env.example .env
   ```

   Edit the `.env` file and fill in the required variables.

## Running the Agent

Make sure you are have configured the gcp project before run and do:

```bash
gcloud auth login
```

To run the Agents Planner:

```bash
adk run agents_planner
```

or

```bash
adk web
```

The agent will prompt you for your requirements and then guide you through the planning process, generating a comprehensive agent system design.

## Development

### Project Structure

```
agents_planner/
├── agents_planner/
│   ├── modules/
│   │   ├── constants.py
│   │   └── __init__.py
│   ├── sub_agents/
│   │   ├── agent_designer/
│   │   ├── final_description/
│   │   ├── task_analyzer/
│   │   └── workflow_designer/
│   ├── agent.py
│   └── __init__.py
└── README.md
```

### Common Issues

If you encounter any issues:

1. Ensure all dependencies are installed correctly
2. Check your `.env` file configuration
3. Verify Python version compatibility
4. Check the logs for detailed error messages

For additional help, please open an issue in the repository.
