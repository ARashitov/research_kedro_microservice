"""
This is a boilerplate pipeline 'example'
generated using Kedro 0.18.0
"""
import logging


def print_something() -> str:
    """Pipeline logs info & returns message

    Returns:
        str: Some message
    """
    logging.info("print_something() is called")
    return "Some message"
