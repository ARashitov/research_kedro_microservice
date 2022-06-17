"""
This is a boilerplate pipeline 'example'
generated using Kedro 0.18.0
"""
import os
from typing import Dict

from kedro.pipeline import Pipeline
from kedro.runner import SequentialRunner


class TestGeocodingPipelineV1:
    def __path_env_var(self, task_id: str):
        os.environ["task_id"] = task_id

    def __choose_pipeline(self, pipelines: Dict[str, Pipeline], pipeline_name: str) -> Pipeline:
        return pipelines[pipeline_name]

    def test_geocoding_pipeline(
        self,
        geocoding_v1_env_task_id,
        geocoding_v1_pipeline_name,
        pipelines,
        catalog,
    ) -> Pipeline:
        runner = SequentialRunner()
        pipeline = self.__choose_pipeline(pipelines, geocoding_v1_pipeline_name)
        self.__path_env_var(geocoding_v1_env_task_id)

        runner.run(pipeline, catalog=catalog)
