"""
This is a boilerplate pipeline 'example'
generated using Kedro 0.18.0
"""

from kedro.pipeline import Pipeline, node, pipeline

from . import nodes


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=nodes.print_something,
                inputs=None,
                outputs="02_intermediate__example__message",
                name="example__message_logging",
            ),
        ],
    )
