from typing import Dict, Tuple, Union
from fastapi import FastAPI

from src.backend import shared
from . import configs


def factory_job_instance(shared_job_def_config: Dict[str, Union[str, int, float]], task_id: str) -> Tuple[str]:
    shared_job_def_config["jobName"] = task_id
    shared_job_def_config["containerOverrides"] = {
        "command": ["kedro", "run", "--pipeline=geocoding.geodata_gov_hk.v1", "--env=test"],
        "environment": [
            {
                "name": "task_id",
                "value": task_id,
            },
        ],
    }
    return shared_job_def_config


def register_endpoint(app: FastAPI) -> None:
    @app.post(**configs.ENDPOINT)
    async def trigger_pipeline(
        task_id: str = configs.HEADERS["task_id"],
    ):

        job_def_instance = factory_job_instance(shared.AWS_BATCH_SUBMIT_JOB_CONFIGS, task_id)
        return shared.AWS_BATCH_CLIENT.submit_job(**job_def_instance)
