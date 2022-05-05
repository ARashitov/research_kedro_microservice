import json
import logging
from datetime import datetime
from typing import Any, Dict, List

from fastapi import FastAPI, Request

from .schemas import logs
from .settings import ENVIRONMENT
from .starter import metadata


_DEFAULT_CONTENT_LENGTH_HEADER = 0
_DEFAULT_HEADERS = [
    "host",
    "accept",
    "upgrade-insecure-requests",
    "cookie",
    "user-agent",
    "accept-language",
    "accept-encoding",
    "connection",
]
ENDPOINT_LOGGER = logging.getLogger("endpoint")


def _get_user_headers(headers: Dict[str, Any]) -> List[str]:
    user_headers = set(list(headers.keys())) - set(_DEFAULT_HEADERS)
    user_headers = list(user_headers)
    return user_headers


def _remove_default_headers(headers: Dict[str, Any]) -> Dict[str, Any]:
    user_headers = _get_user_headers(headers)
    headers_to_log = {}
    for user_header in user_headers:
        headers_to_log[user_header] = headers[user_header]
    return headers_to_log


def _factory_log(
    request: Request,
    response: Request,
    request_time: datetime,
    response_time: datetime,
) -> logs.EndpointLogRecord:
    """Generates endpoint call log

    Args:
        request (Request): fast api endpoint request
        response (Request): fast api endpoint response
        request_time (datetime): request datetime
        response_time (datetime): response datetime

    Returns:
        logs.EndpointLogRecord: Endpoint log records
    """
    request_headers = dict(request.headers.items())
    response_headers = dict(response.headers.items())
    log = logs.EndpointLogRecord(
        app_environment=ENVIRONMENT,
        app_version=metadata.version,
        request_uri=str(request.url),
        request_method=request.method,
        request_path=request.url.path,
        request_size=int(request_headers.get("content-length", _DEFAULT_CONTENT_LENGTH_HEADER)),
        request_datetime=str(request_time),
        request_headers=_remove_default_headers(request_headers),
        response_status_code=response.status_code,
        response_size=int(response_headers.get("content-length", _DEFAULT_CONTENT_LENGTH_HEADER)),
        response_headers=_remove_default_headers(response_headers),
        response_datetime=str(response_time),
        response_duration=(response_time - request_time).total_seconds(),
    )
    return log


def _mark_service_time_to_header(
    response: Request,
    service_start_time: datetime,
    service_end_time: datetime,
) -> Request:
    duration = (service_end_time - service_start_time).total_seconds()
    response.headers["X-Process-Time"] = str(duration)
    return response


def _log_endpoint_call(log: logs.EndpointLogRecord):
    ENDPOINT_LOGGER.info(json.dumps(log.dict()))


def log_endpoint_calls(app: FastAPI):
    """Registers each endpoint call to fast api

    Args:
    app (FastAPI): Fast api application
    """

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):

        request_time = datetime.now()
        response = await call_next(request)
        response_time = datetime.now()

        response = _mark_service_time_to_header(response, request_time, response_time)

        log = _factory_log(request, response, request_time, response_time)
        _log_endpoint_call(log)

        return response
