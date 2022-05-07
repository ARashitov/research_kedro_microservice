"""
    About: Module for api endpoint definition
    Author: Adil Rashitov
"""
from typing import Optional
from fastapi import FastAPI, status

from src.backend.handlers.exception import get_http_exception

from . import config


def register_endpoint(app: FastAPI):
    """Function performs registration fo endpoint to FastAPI

    Args:
        app (FastAPI): application
    """

    @app.get(**config.ENDPOINT_DETAILS)
    async def endpoint(
        your_message: Optional[str] = config.HEADERS["your_message"],
        to_raise_exception: bool = config.HEADERS["to_raise_exception"],
    ) -> config.Status:

        if your_message is None:
            your_message = "Succesfull endpoint call"

        if to_raise_exception:
            try:
                _ = 1 / 0
            except ZeroDivisionError as exc_zero_div:
                raise get_http_exception(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message=str(exc_zero_div),
                )

        return config.Status(message=your_message)
