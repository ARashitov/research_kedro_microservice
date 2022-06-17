"""
This is a boilerplate pipeline 'example'
generated using Kedro 0.18.0
"""
import os
from kedro.framework.context.context import KedroContext
from kedro.runner import SequentialRunner

from src.pipelines.pipelines import config_pipeline


class TestConfigPipeline:
    def __patch_task_id_env_var(self):
        # TODO: Mock this module in future
        os.environ["task_id"] = "TEST_TASK_ID"

    def test_config_pipeline(self, context: KedroContext):

        self.__patch_task_id_env_var()

        runner = SequentialRunner()
        result = runner.run(
            config_pipeline.create_pipeline(),
            catalog=context.catalog,
        )

        assert "params:common.task_id" in result.keys()
        assert "params:credentials.google_maps_key" in result.keys()
