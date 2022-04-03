"""
    About: Module for testing endpoint
    Author: Adil Rashitov
"""
from typing import Callable
from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient


def test__template__get_endpoint__without_message(client: TestClient, get_route: Callable, headers: Dict[str, str]):

    with client.get(url=get_route(__file__), headers=headers) as r:
        assert r.status_code == status.HTTP_200_OK
