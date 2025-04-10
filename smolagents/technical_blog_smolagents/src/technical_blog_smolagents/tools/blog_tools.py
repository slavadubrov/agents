import os
import re
from typing import Dict, List, Optional

from smolagents import DuckDuckGoSearchTool, tool


@tool
def save_to_file(filename: str, content: str) -> str:
    """Save content to a file in the output directory.

    Args:
        filename: The name of the file (including extension)
        content: The content to save to the file

    Returns:
        A message confirming the file was saved
    """
    os.makedirs("output", exist_ok=True)
    filepath = os.path.join("output", filename)

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)

    return f"Content saved to {filepath}"


@tool
def read_file(filepath: str) -> str:
    """Read content from a file.

    Args:
        filepath: The path to the file to read

    Returns:
        The content of the file
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return f"File not found: {filepath}"


@tool
def parse_roadmap_file(roadmap_file_path: str) -> Dict:
    """Parse a roadmap markdown file to extract topic, goal, and blog post outlines.

    Args:
        roadmap_file_path: Path to the roadmap markdown file

    Returns:
        Dictionary containing the topic, goal, and list of blog post outlines
    """
    with open(roadmap_file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Extract topic
    topic_match = re.search(r"## Topic: (.+?)(?:\n|$)", content)
    topic = topic_match.group(1).strip() if topic_match else ""

    # Extract goal
    goal_match = re.search(r"## Goal\n(.*?)\n\n## Planned Posts", content, re.DOTALL)
    goal = goal_match.group(1).strip() if goal_match else ""

    # Extract planned posts
    post_outlines = []
    post_sections = re.finditer(
        r"### \d+\. (.+?)\n\n(.*?)(?=\n\n### \d+\.|$)", content, re.DOTALL
    )

    for match in post_sections:
        title = match.group(1).strip()
        description = match.group(2).strip()
        post_outlines.append({"title": title, "description": description})

    return {"topic": topic, "goal": goal, "post_outlines": post_outlines}


@tool
def create_roadmap_file(topic: str, goal: str, posts: List[Dict]) -> str:
    """Create a roadmap file based on the provided topic, goal, and post outlines.

    Args:
        topic: The main topic of the blog series
        goal: The overall goal/purpose of the blog series
        posts: List of dictionaries containing blog post outlines with 'title' and 'description' keys

    Returns:
        Path to the saved roadmap file
    """
    # Create the roadmap content
    roadmap_content = "# Blog Series Roadmap\n\n"
    roadmap_content += f"## Topic: {topic}\n\n"
    roadmap_content += f"## Goal\n{goal}\n\n"
    roadmap_content += "## Planned Posts\n\n"

    for i, post in enumerate(posts, 1):
        roadmap_content += f"### {i}. {post['title']}\n\n"
        roadmap_content += f"{post['description']}\n\n"

    # Save the roadmap
    os.makedirs("output", exist_ok=True)
    roadmap_path = "output/Blog_Series_Roadmap.md"

    with open(roadmap_path, "w", encoding="utf-8") as file:
        file.write(roadmap_content)

    return roadmap_path


# Create a specialized search tool for researching blog topics
@tool
def research_topic(topic: str, num_results: Optional[int] = 5) -> str:
    """Research a topic using DuckDuckGo search.

    Args:
        topic: The topic to research
        num_results: Number of search results to return (default: 5)

    Returns:
        A string with search results about the topic
    """
    search_tool = DuckDuckGoSearchTool()
    results = search_tool(topic)

    # Process and limit results
    if num_results and isinstance(results, list) and len(results) > num_results:
        results = results[:num_results]

    if isinstance(results, list):
        return "\n\n".join(
            [
                f"Source: {r['link']}\nTitle: {r['title']}\nSnippet: {r['snippet']}"
                for r in results
            ]
        )
    return str(results)
