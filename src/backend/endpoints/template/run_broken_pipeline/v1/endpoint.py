"""
    About: Module for api endpoint definition
    Author: Adil Rashitov
"""
from typing import Union
from fastapi import FastAPI, status

from kedro.io import MemoryDataSet

from src.backend.handlers.exception import excecute_pipeline
from src.backend.handlers.exception import get_http_exception
from src.backend.settings import ENVIRONMENT
from src.backend.starter import init_kedro_session

from . import config


PIPELINE = "division_by_zero"
TASK_ID_REGISTRY = "task_id"


def _validate_task_id_specification(task_id: str):
    if task_id is None or task_id == "":
        raise get_http_exception(
            status.HTTP_400_BAD_REQUEST,
            message="task_id header cannot be empty",
        )


def _create_catalog_extensions(task_id: str):
    return {TASK_ID_REGISTRY: MemoryDataSet(task_id)}


def register_endpoint(app: FastAPI):
    """Function performs registration fo endpoint to FastAPI

    Args:
        app (FastAPI): application
    """

    @app.get(**config.ENDPOINT_DETAILS)
    async def endpoint(
        task_id: Union[str, None] = config.HEADERS["task_id"],
    ) -> config.Status:

        _validate_task_id_specification(task_id)

        kedro_session = init_kedro_session(
            env=ENVIRONMENT,
            trace_id=task_id,
        )
        catalog_extensions = _create_catalog_extensions(task_id)

        result = excecute_pipeline(session=kedro_session, pipeline_name=PIPELINE, catalog_extensions=catalog_extensions)
        del result

        return config.Status(message="Succesfull finish pipeline execution")
