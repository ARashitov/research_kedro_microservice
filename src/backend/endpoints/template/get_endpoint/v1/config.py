"""
    About: Module for local endpoint configurations
    Author: Adil Rashitov
"""
from fastapi import Header
from fastapi import status

from .....schemas.base import Status
from .....starter import get_endpoint_route
from .....starter import get_endpoint_tag


ENDPOINT_DETAILS = {
    "path": get_endpoint_route(__file__),
    "response_model": Status,
    "response_description": ("Okay template message"),
    "description": ("Template get endpoint"),
    "status_code": status.HTTP_200_OK,
    "tags": [get_endpoint_tag(__file__)],
}

HEADERS = {
    "your_message": Header(
        default=None,
        description="(Optional) message header",
        convert_underscores=False,
        example="Hello world!",
    ),
}
