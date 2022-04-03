"""
    Main file starting web application
    Author: Adil Rashitov <adil@wastelabs.co>
"""
from fastapi import FastAPI

from .endpoints import template
from .starter import metadata

# 1. Application init
app = FastAPI(
    title=metadata.title,
    description=metadata.description,
    version=metadata.version,
    contact={
        "name": "Adil Rashitov",
        "email": "adil@wastelabs.co",
    },
)

# 2. Endpoints registration
template.get_endpoint.v1.register_endpoint(app)
