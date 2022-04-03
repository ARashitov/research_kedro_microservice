"""
    About: Module for conftest related to backend of web application
    Author: Adil Rashitov
"""
import os
from pathlib import Path
from typing import Callable
from typing import Dict

from fastapi.testclient import TestClient
import pytest

from ...backend.main import app


@pytest.fixture
def client() -> TestClient:
    """Initializes FastAPI application test client

    Returns:
        TestClient: FastAPI application test client
    """
    return TestClient(app)


@pytest.fixture
def get_route() -> Callable:
    """Returns function extraction endpoint route based
        on test file location

    Returns:
        Callable: FastAPI application test client
    """

    _endpoint_loc = "/src/tests/backend/endpoints/"

    def get_endpoint_route(endpoint_path: str) -> str:
        """Function extracts path from test file directory location

        Args:
            endpoint_path (str): endpoint path

        Returns:
            str: route name
        """

        # 1. Resolve full filepath & endpoint path
        project_path = str(Path().resolve())
        endpoints_path = project_path + _endpoint_loc

        # 2. Route naming extraction
        route = str(Path(os.path.realpath(endpoint_path)))
        route = route.split(endpoints_path)[1]
        route = route.rsplit("/", 1)[0]
        return f"http://127.0.0.1:8000/{route}"

    return get_endpoint_route


@pytest.fixture
def headers() -> Dict[str, str]:
    """Returns function extraction endpoint route based
        on test file location

    Returns:
        Callable: FastAPI application test client
    """
    return {
        "Connection": "close",
    }
