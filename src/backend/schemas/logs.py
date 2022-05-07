from typing import Any, Union
from pydantic import BaseModel


class EndpointLogRecord(BaseModel):
    """Schema used to capture endpoint call details"""

    app_environment: str
    app_version: str

    request_uri: str
    request_method: str
    request_path: str
    request_size: int
    request_datetime: str
    request_headers: Any

    response_status_code: int
    response_size: int
    response_datetime: str
    response_duration: Union[float, str]
    response_headers: Any

    exception_details: Any
