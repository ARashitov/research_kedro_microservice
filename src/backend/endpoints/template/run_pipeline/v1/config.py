"""
    About: Module for local endpoint configurations
    Author: Adil Rashitov
"""
from fastapi import Header
from fastapi import status

from src.backend.schemas.base import Status
from src.backend.starter import get_endpoint_route
from src.backend.starter import get_endpoint_tag


ENDPOINT_DETAILS = {
    "path": get_endpoint_route(__file__),
    "response_model": Status,
    "response_description": ("pipeline processing status"),
    "description": ("Template of api with pipeline execution"),
    "status_code": status.HTTP_200_OK,
    "tags": [get_endpoint_tag(__file__)],
}


HEADERS = {
    "task_id": Header(
        default=None,
        description="unique identifier of task",
        convert_underscores=False,
        example="example_task_id",
    ),
}
