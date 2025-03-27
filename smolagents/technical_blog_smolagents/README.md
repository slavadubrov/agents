# Technical Blog Generator with Smolagents

This project uses [Smolagents](https://github.com/huggingface/smolagents) to create a multi-agent system for generating high-quality technical blog posts. The system includes specialized agents for planning and writing blog content, as well as a manager agent that coordinates the whole process.

## 📋 Features

- **Multi-agent architecture**: Uses specialized agents for different tasks (planning and writing)
- **Comprehensive planning**: Creates detailed blog roadmaps with well-structured outlines
- **High-quality content**: Generates technically accurate blog posts with code examples
- **Web research**: Agents can search the web for the latest information on topics
- **Workflow support**: Can skip planning and use existing roadmaps if desired

## 🚀 Installation

```bash
# Clone the repository
cd smolagents/technical_blog_smolagents

# Install the package in development mode
pip install -e .
```

## 🔧 Requirements

- Python 3.8+
- smolagents
- pydantic

## 💻 Usage

### Command-line Interface

The package provides a command-line interface to generate blog posts:

```bash
# Generate a blog series with default settings
technical-blog

# Generate a blog series with custom topic and goal
technical-blog --topic "Machine Learning Explainability" --goal "Create a series of blog posts explaining ML explainability techniques for data scientists"

# Skip planning phase and use an existing roadmap
technical-blog --skip-planning --roadmap-file "path/to/roadmap.md"

# Use a specific HuggingFace model
technical-blog --model-name "meta-llama/Llama-3.2-70B-Instruct"
```

### Python API

You can also use the package programmatically:

```python
from technical_blog_smolagents import BlogManager
from smolagents import HfApiModel

# Initialize with a custom model
model = HfApiModel(model_id="meta-llama/Llama-3.2-70B-Instruct")
manager = BlogManager(model=model)

# Generate blog content
result = manager.run(
    topic="GraphQL vs REST APIs",
    goal="Compare GraphQL and REST with practical examples and use cases",
    skip_planning=False,
    roadmap_file=None
)

# Access the generated content
print(f"Generated {len(result['posts'])} blog posts")
for post in result['posts']:
    print(f"- {post['title']}")
```

## 🧩 System Architecture

The system consists of three main components:

1. **Blog Planning Agent**: Researches topics and creates detailed outlines for blog posts.
2. **Blog Writing Agent**: Writes high-quality blog content based on the provided outlines.
3. **Blog Manager**: Coordinates the planning and writing agents to generate complete blog series.

Each agent has access to specialized tools:

- Web search capabilities via DuckDuckGo
- File reading and writing tools
- Python interpreter for code generation and manipulation

## 📄 Output Format

The generated content is saved in the `output` directory:

- `Blog_Series_Roadmap.md`: Contains the overall plan for the blog series
- `Blog_Post_1_Title.md`, `Blog_Post_2_Title.md`, etc.: Individual blog posts in Markdown format

## 🛠️ Development

For development, install the optional development dependencies:

```bash
pip install -e ".[dev]"
```

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.
