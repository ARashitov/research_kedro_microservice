"""
    About: Module for api endpoint definition
    Author: Adil Rashitov
"""
from typing import Optional

from fastapi import FastAPI

from . import config


def register_endpoint(app: FastAPI):
    """Function performs registration fo endpoint to FastAPI

    Args:
        app (FastAPI): application
    """

    @app.get(**config.ENDPOINT_DETAILS)
    async def endpoint(
        your_message: Optional[str] = config.HEADERS["your_message"],
    ) -> config.Status:

        if your_message is None:
            your_message = "Succesfull endpoint call"

        return config.Status(message=your_message)
