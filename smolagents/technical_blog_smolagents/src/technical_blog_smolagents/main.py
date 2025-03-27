#!/usr/bin/env python
import argparse
import asyncio
import logging
import os
from typing import Dict, List

from smolagents import CodeAgent, HfApiModel

from technical_blog_smolagents.agents.blog_planning_agent import BlogPlanningAgent
from technical_blog_smolagents.agents.blog_writing_agent import BlogWritingAgent
from technical_blog_smolagents.tools.blog_tools import parse_roadmap_file


# Configure logging
def setup_logging(log_file="output/blog_generation.log"):
    """Set up logging to file and console"""
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Create logger
    logger = logging.getLogger("blog_generator")
    logger.setLevel(logging.DEBUG)

    # File handler
    file_handler = logging.FileHandler(log_file)

    # Console handler
    console_handler = logging.StreamHandler()

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Initialize logger
logger = setup_logging()


class BlogManager:
    """Manager agent that coordinates the planning and writing agents."""

    def __init__(self, model=None):
        """Initialize the manager with specialized agents.

        Args:
            model: The LLM model to use (default: HfApiModel)
        """
        # Use provided model or default to HfApiModel
        self.model = model or HfApiModel()

        # Create specialized agents
        self.planning_agent = BlogPlanningAgent(model=self.model)
        self.writing_agent = BlogWritingAgent(model=self.model)

        # Create manager agent that can delegate to specialized agents
        self.manager_agent = CodeAgent(
            tools=[],
            model=self.model,
            managed_agents=[self.planning_agent.agent, self.writing_agent.agent],
            name="blog_manager",
            description="This agent manages the blog generation process by coordinating the planning and writing agents.",
        )

        # Initialize state storage
        self.blog_roadmap = []
        self.blog_posts = []
        self.topic = ""
        self.goal = ""

    def generate_blog_roadmap(
        self, topic: str, goal: str, roadmap_file: str = None
    ) -> List[Dict]:
        """Generate a roadmap for the blog series.

        Args:
            topic: The main topic for the blog series
            goal: The goal/purpose of the blog series
            roadmap_file: Optional path to an existing roadmap file

        Returns:
            List of blog post outlines
        """
        logger.info("Starting blog roadmap generation")

        self.topic = topic
        self.goal = goal

        # If a roadmap file is provided, parse it
        if roadmap_file:
            logger.info(f"Using existing roadmap file: {roadmap_file}")
            roadmap_data = parse_roadmap_file(roadmap_file)
            self.topic = roadmap_data["topic"] or self.topic
            self.goal = roadmap_data["goal"] or self.goal
            self.blog_roadmap = roadmap_data["post_outlines"]
            return self.blog_roadmap

        # Otherwise, use the planning agent to create a roadmap
        logger.info(f"Generating new roadmap for topic: {topic}")
        roadmap_data = self.planning_agent.create_blog_roadmap(topic, goal)

        if "posts" in roadmap_data:
            self.blog_roadmap = roadmap_data["posts"]
        else:
            logger.error("Planning agent did not return a valid roadmap")
            self.blog_roadmap = []

        return self.blog_roadmap

    async def write_blog_posts(self) -> List[Dict]:
        """Write all blog posts based on the roadmap.

        Returns:
            List of completed blog posts
        """
        logger.info("Starting blog posts writing")
        self.blog_posts = []

        if not self.blog_roadmap:
            logger.error("No blog roadmap available. Generate a roadmap first.")
            return []

        total_posts = len(self.blog_roadmap)

        # Process posts sequentially
        for i, post_outline in enumerate(self.blog_roadmap):
            logger.info(
                f"Writing blog post {i + 1}/{total_posts}: {post_outline['title']}"
            )

            post = await self._write_single_post(post_outline, i, total_posts)
            self.blog_posts.append(post)

        logger.info(f"Completed writing {len(self.blog_posts)} blog posts")
        return self.blog_posts

    async def _write_single_post(
        self, post_outline: Dict, index: int, total_posts: int
    ) -> Dict:
        """Write a single blog post.

        Args:
            post_outline: The outline for the blog post
            index: The index of the post in the roadmap
            total_posts: The total number of posts

        Returns:
            The completed blog post
        """
        post = self.writing_agent.write_blog_post(
            topic=self.topic,
            goal=self.goal,
            post_title=post_outline["title"],
            post_description=post_outline["description"],
            blog_roadmap=self.blog_roadmap,
            post_index=index,
            total_posts=total_posts,
        )

        return post

    def run(
        self,
        topic: str,
        goal: str,
        skip_planning: bool = False,
        roadmap_file: str = None,
    ) -> Dict:
        """Run the full blog generation process.

        Args:
            topic: The main topic for the blog series
            goal: The goal/purpose of the blog series
            skip_planning: Whether to skip the planning phase
            roadmap_file: Optional path to an existing roadmap file

        Returns:
            Dictionary with the generated content
        """
        logger.info("Starting Blog Generation Process")

        # Step 1: Generate blog roadmap
        if not skip_planning or roadmap_file:
            self.generate_blog_roadmap(topic, goal, roadmap_file)

        # Step 2: Write blog posts
        asyncio.run(self.write_blog_posts())

        logger.info("Blog Generation Process completed")

        return {
            "topic": self.topic,
            "goal": self.goal,
            "roadmap": self.blog_roadmap,
            "posts": self.blog_posts,
        }


def main():
    """Main entry point for the blog generation process."""
    parser = argparse.ArgumentParser(description="Generate technical blog posts")
    parser.add_argument("--topic", type=str, help="The main topic of the blog series")
    parser.add_argument("--goal", type=str, help="The goal/purpose of the blog series")
    parser.add_argument(
        "--skip-planning",
        action="store_true",
        help="Skip the planning phase and use an existing roadmap file",
    )
    parser.add_argument(
        "--roadmap-file",
        type=str,
        help="Path to the roadmap markdown file (required if --skip-planning is used)",
    )
    parser.add_argument(
        "--model-name",
        type=str,
        default=None,
        help="HuggingFace model name to use for the agents",
    )

    args = parser.parse_args()

    # Create a custom model if specified
    model = None
    if args.model_name:
        model = HfApiModel(model_id=args.model_name)

    # Create the blog manager
    manager = BlogManager(model=model)

    # Set default topic and goal if not provided
    topic = args.topic or "Python Design Patterns for Machine Learning"
    goal = (
        args.goal
        or """
        Create a comprehensive series of technical blog posts about comprehensive
        overview with examples of the most common design patterns used in machine
        learning. Each post should explain a specific pattern with real-world
        examples, code snippets, and diagrams. The content should be suitable for
        intermediate Python ML Engineers looking to improve their skills.
    """
    )

    # Run the manager
    manager.run(
        topic=topic,
        goal=goal,
        skip_planning=args.skip_planning,
        roadmap_file=args.roadmap_file,
    )


if __name__ == "__main__":
    main()
