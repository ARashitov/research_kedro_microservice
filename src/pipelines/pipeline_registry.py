"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

from .pipelines import example


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    return {
        "__default__": example.create_pipeline(),
        "example": example.create_pipeline(),
    }
