import io
from typing import Tuple

import boto3
from fastapi import FastAPI
import pandas as pd
from src.backend.settings import AWS_CREDENTIALS

from . import configs


def _get_bucket_and_fpath(s3_bucket_path: str, task_id: str) -> Tuple[str]:
    _split = s3_bucket_path.split("//")[1].split("/", 1)
    s3_bucket, s3_fpath = _split[0], _split[1] + task_id
    return s3_bucket, s3_fpath


def read_csv_from_s3(
    task_id: str,
):
    """Uploads byte arrayt to S3 bucket

    Args:
        file (bytearray): file-like bytes array
        aws_access_key_id (str): aws credentials
        aws_secret_access_key (str): aws credentials
        s3_kedro_path (str): catalog registry `path` keyword
        fname (str): source filename
    """
    s3_bucket, s3_fpath = _get_bucket_and_fpath(configs.PATH_OUTPUT_REGISTRY, task_id)
    s3 = boto3.client("s3", **AWS_CREDENTIALS)
    print(s3_fpath)
    obj = s3.get_object(Bucket=s3_bucket, Key=s3_fpath)
    return pd.read_csv(obj["Body"])


def enforce_csv_extension_to(task_id: str) -> str:
    return task_id.split(".")[0] + ".csv"


def register_endpoint(app: FastAPI) -> None:
    @app.get(**configs.ENDPOINT)
    async def get_task(
        task_id: str = configs.HEADERS["task_id"],
    ):

        task_id = enforce_csv_extension_to(task_id)
        df = read_csv_from_s3(task_id=task_id)

        buffer = io.StringIO()
        df.to_csv(buffer, index=False)
        return {
            "csv_content": buffer.getvalue(),
            "fname": task_id,
        }
