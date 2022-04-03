"""
    About: module with base schemas
    Author: Adil Rashitov
"""
from typing import Any

from pydantic import BaseModel


class Status(BaseModel):
    """
    Status of something
    """

    message: Any
