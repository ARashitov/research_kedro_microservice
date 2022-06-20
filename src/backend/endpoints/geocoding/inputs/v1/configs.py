"""
    About: Module with endpoints configuration to separate logic from definition
"""
from fastapi import File, Header, status

from src.backend.starter import get_endpoint_route
from src.backend.starter import get_endpoint_tag
from src.backend.starter import read_raw_catalog_content


NAME_INPUT_REGISTY = "02_intermediate__geocoding__input"
PATH_INPUT_REGISTRY = read_raw_catalog_content()[NAME_INPUT_REGISTY]["path"]


ENDPOINT = {
    "path": get_endpoint_route(__file__),
    "description": ("Endpoint uploading inputs for geocoding pipeline"),
    "status_code": status.HTTP_202_ACCEPTED,
    "tags": [get_endpoint_tag(__file__)],
    "deprecated": False,
}


HEADERS = {
    "task_id": Header(
        default=None,
        description="[OPTIONAL] Task id to save uploaded task under",
        convert_underscores=False,
    ),
    "file": File(...),
}
