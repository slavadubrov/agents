"""Utility functions for the agents-planner-agent."""


def save_to_file(content: str, filename: str):
    """Saves the given text content to a file.

    Args:
        content (str): The text content to save.
        filename (str): The name of the file to save to.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"\nSuccessfully saved content to {filename}")
    except IOError as e:
        print(f"\nError saving content to {filename}: {e}")
