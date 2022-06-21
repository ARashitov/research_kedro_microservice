import io
from typing import Tuple

import boto3
from fastapi import FastAPI, UploadFile
from src.backend.settings import AWS_CREDENTIALS
from . import configs


def _get_bucket_and_fpath(s3_bucket_path: str, task_id: str) -> Tuple[str]:
    _split = s3_bucket_path.split("//")[1].split("/", 1)
    s3_bucket, s3_fpath = _split[0], _split[1] + task_id
    return s3_bucket, s3_fpath


async def save_raw_input_to_s3(
    user_file: UploadFile,
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

    s3_bucket, s3_fpath = _get_bucket_and_fpath(configs.PATH_INPUT_REGISTRY, task_id)

    s3 = boto3.resource("s3", **AWS_CREDENTIALS)
    bucket = s3.Bucket(s3_bucket)

    with io.BytesIO() as buffer:
        buffer.write(await user_file.read())
        buffer.seek(0)
        bucket.upload_fileobj(buffer, s3_fpath)


def enforce_csv_extension_to(task_id: str) -> str:
    return task_id.split(".")[0] + ".csv"


def register_endpoint(app: FastAPI) -> None:
    @app.post(**configs.ENDPOINT)
    async def upload_task(
        task_id: str = configs.HEADERS["task_id"],
        csv_file: UploadFile = configs.HEADERS["file"],
    ):

        task_id = enforce_csv_extension_to(task_id)
        await save_raw_input_to_s3(user_file=csv_file, task_id=task_id)

        return {
            "status": "OK",
            "fname": task_id,
        }
