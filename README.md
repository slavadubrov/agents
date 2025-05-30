# AI Agents Framework Experiments

This repository contains my personal experiments with various AI agent frameworks, including:

- [CrewAI](https://github.com/joaomdmoura/crewai) - Framework for orchestrating role-playing autonomous AI agents
- [SmolAgents](https://github.com/smol-ai/smol-agent) - Lightweight framework for building autonomous agents
- [LangGraph](https://github.com/langchain-ai/langgraph) - Framework for building stateful, multi-agent workflows

## Experiments

Various experiments in this repository demonstrate:

- Different agent role configurations and architectures
- Task delegation and coordination between agents
- Specialized tools and capabilities
- Performance evaluations across frameworks
- Framework-specific features and best practices

## Requirements

Experiments typically require:

- Python 3.12+
- Various agent frameworks (CrewAI, SmolAgents, LangGraph)
- LangChain
- Different LLM connections and integrations

## Development Setup

### Prerequisites

- Python 3.12 or higher
- Make (for using Makefile commands)
- Git

### Initial Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

2. Set up the development environment:

```bash
make setup-dev
```

This will:

- Create and activate a virtual environment
- Install all dependencies
- Install development dependencies
- Set up pre-commit hooks

### Alternative Setup with uv

If you prefer using `uv` (a fast Python package installer and resolver):

1. Install `uv` if you haven't already:

On macOS with Homebrew:

```bash
brew install uv
```

Or using the install script:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
```

3. Install dependencies:

```bash
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt
```
