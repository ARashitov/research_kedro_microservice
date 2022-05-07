"""
    About: Init module
    Author: Adil Rashitov
"""

from .main import app
from .starter import init_kedro_session


__all__ = [
    "app",
    "init_kedro_session",
]
