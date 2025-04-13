from typing import Dict

from technical_blog_smolagents.tools.blog_tools import (
    create_roadmap_file,
    research_topic,
)

from smolagents import (
    CodeAgent,
    DuckDuckGoSearchTool,
    HfApiModel,
    VisitWebpageTool,
)


class BlogPlanningAgent:
    """Agent responsible for planning the blog posts."""

    def __init__(self, model=None):
        """Initialize the blog planning agent.

        Args:
            model: The model to use for the agent (default: HfApiModel)
        """
        # Use provided model or default to HfApiModel
        self.model = model or HfApiModel()

        # Create search and research tools for the agent
        self.tools = [
            DuckDuckGoSearchTool(),
            VisitWebpageTool(),
            research_topic,
            create_roadmap_file,
        ]

        # Create the agent with tools
        self.agent = CodeAgent(
            tools=self.tools,
            model=self.model,
            name="blog_planning_agent",
            description="This agent plans blog posts by researching topics and creating outlines.",
        )

    def create_blog_roadmap(self, topic: str, goal: str) -> Dict:
        """Create a roadmap for the blog series.

        Args:
            topic: The main topic of the blog series
            goal: The goal/purpose of the blog series

        Returns:
            Dictionary containing the roadmap information
        """
        task = f"""
        You are a blog planning agent. Your task is to create a comprehensive roadmap for a blog series on the topic:
        "{topic}"

        Goal of the blog series:
        "{goal}"

        Follow these steps:
        1. Research the topic using the research_topic tool to gather relevant information
        2. Plan a series of 5-7 blog posts that would comprehensively cover the topic
        3. For each blog post, create a title and detailed description (at least 3-4 sentences) of what it will cover
        4. Use create_roadmap_file to save your roadmap
        5. Return a JSON with the following format:
           {{
               "topic": "The topic",
               "goal": "The goal",
               "posts": [
                   {{"title": "Post 1 Title", "description": "Post 1 description"}},
                   {{"title": "Post 2 Title", "description": "Post 2 description"}},
                   ...
               ]
           }}

        Make sure your blog posts follow a logical progression, with each building on previous posts.
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
