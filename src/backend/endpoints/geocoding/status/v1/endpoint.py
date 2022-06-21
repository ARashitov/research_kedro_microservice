from fastapi import FastAPI
from pydantic import parse_obj_as
from src.backend import shared

from . import configs
from . import schemas


def register_endpoint(app: FastAPI) -> None:
    @app.post(**configs.ENDPOINT)
    async def trigger_pipeline(
        jobs_ids_list: schemas.StatusRequest,
    ):
        jobs_status = shared.AWS_BATCH_CLIENT.describe_jobs(**jobs_ids_list.dict())
        return parse_obj_as(schemas.JobStatusResponse, jobs_status)
