"""This module provides the functions to communicate with players."""


def request_input(prompt: str = "") -> str:
    """Requests a move from a user.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        str: The user's input.

    """

    return input(prompt).lower()
