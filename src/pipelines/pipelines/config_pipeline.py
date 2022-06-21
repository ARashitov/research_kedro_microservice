"""
This is a boilerplate pipeline 'example'
generated using Kedro 0.18.0
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import get_environment_variables


def create_pipeline(**kwargs) -> Pipeline:
    # TODO: cover by test case
    return pipeline(
        [
            node(
                func=get_environment_variables,
                inputs=None,
                outputs="02_intermediate__env_variables",
                name="config__env_vars_extraction",
            ),
            node(
                func=lambda x: x["task_id"],
                inputs="02_intermediate__env_variables",
                outputs="params:common.task_id",
                name="geocoding__config__extraction__task_id",
            ),
        ],
    )
