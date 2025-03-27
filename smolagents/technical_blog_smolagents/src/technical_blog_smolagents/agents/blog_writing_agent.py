from typing import Dict, List

from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel, VisitWebpageTool
from smolagents.tools import PythonInterpreterTool

from technical_blog_smolagents.tools.blog_tools import (
    read_file,
    research_topic,
    save_to_file,
)


class BlogWritingAgent:
    """Agent responsible for writing blog posts."""

    def __init__(self, model=None):
        """Initialize the blog writing agent.

        Args:
            model: The model to use for the agent (default: HfApiModel)
        """
        # Use provided model or default to HfApiModel
        self.model = model or HfApiModel()

        # Create tools for the agent
        self.tools = [
            DuckDuckGoSearchTool(),
            VisitWebpageTool(),
            research_topic,
            save_to_file,
            read_file,
            PythonInterpreterTool(),
        ]

        # Create the agent with tools
        self.agent = CodeAgent(
            tools=self.tools,
            model=self.model,
            name="blog_writing_agent",
            description="This agent writes high-quality blog posts based on outlines.",
        )

    def write_blog_post(
        self,
        topic: str,
        goal: str,
        post_title: str,
        post_description: str,
        blog_roadmap: List[Dict],
        post_index: int,
        total_posts: int,
    ) -> Dict:
        """Write a blog post based on the provided outline.

        Args:
            topic: The main topic of the blog series
            goal: The goal/purpose of the blog series
            post_title: The title of the blog post to write
            post_description: The description/outline of the blog post
            blog_roadmap: List of all blog post outlines
            post_index: The index of the current post in the roadmap
            total_posts: The total number of posts in the roadmap

        Returns:
            Dictionary with title and content of the written blog post
        """
        post_index_plus_one = post_index + 1  # For human-readable numbering

        task = f"""
        You are a professional blog writer. Your task is to write a high-quality technical blog post with the following details:

        BLOG SERIES TOPIC: {topic}
        BLOG SERIES GOAL: {goal}

        POST TITLE: {post_title}
        POST DESCRIPTION: {post_description}
        POST NUMBER: {post_index_plus_one} of {total_posts}

        First, research the topic thoroughly using the research_topic tool to gather relevant information and facts.

        Then, write a comprehensive blog post that:
        1. Has an engaging introduction that hooks the reader
        2. Covers all aspects mentioned in the post description
        3. Includes code examples, diagrams, or other relevant technical content where appropriate
        4. Is well-structured with clear headings and subheadings
        5. Concludes with a summary and any relevant next steps or references
        6. Links to previous or upcoming posts in the series when relevant

        Make sure your content is:
        - Technically accurate and up-to-date
        - Written in a clear, engaging style
        - Properly formatted in Markdown
        - Contains appropriate headers, code blocks, and emphasis

        After writing the blog post, save it to a file using the save_to_file tool with the filename format:
        "Blog_Post_{post_index_plus_one}_{post_title.replace(" ", "_")}.md"

        Return the final blog post as a dictionary with the following format:
        {{
            "title": "The title of the blog post",
            "content": "The full content of the blog post in Markdown format"
        }}
        """

        # Run the agent with the task
        result = self.agent.run(task)

        # Convert the result to a dictionary if it's in string format
        if isinstance(result, str):
            # Try to extract JSON from the result
            import json
            import re

            json_pattern = r"\{[\s\S]*\}"
            match = re.search(json_pattern, result)

            if match:
                try:
                    return json.loads(match.group(0))
                except json.JSONDecodeError:
                    pass

        return result
