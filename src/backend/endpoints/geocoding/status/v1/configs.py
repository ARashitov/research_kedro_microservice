"""
    About: Module with endpoints configuration to separate logic from definition
"""
from fastapi import Header, status

from src.backend.starter import get_endpoint_route
from src.backend.starter import get_endpoint_tag
from .schemas import JobStatusResponse


ENDPOINT = {
    "path": get_endpoint_route(__file__),
    "description": ("Endpoint monitoring pipeline status"),
    "status_code": status.HTTP_200_OK,
    "tags": [get_endpoint_tag(__file__)],
    "deprecated": False,
    "response_model": JobStatusResponse,
}


HEADERS = {
    "jobs_ids_list": Header(
        default=None,
        description="List of JobIds returned",
        convert_underscores=False,
    ),
}
