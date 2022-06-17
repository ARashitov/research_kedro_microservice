"""
This is a boilerplate pipeline 'example'
generated using Kedro 0.18.0
"""
from kedro.framework.context.context import KedroContext
from kedro.runner import SequentialRunner

from src.pipelines.pipelines import config_pipeline


def test_config_pipeline(context: KedroContext):

    runner = SequentialRunner()
    result = runner.run(
        config_pipeline.create_pipeline(),
        catalog=context.catalog,
    )

    assert "params:common.task_id" in result.keys()
    assert "params:credentials.google_maps_key" in result.keys()
