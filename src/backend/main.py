"""
    Main file starting web application
    Author: Adil Rashitov <adil@wastelabs.co>
"""
from fastapi import FastAPI

from . import middleware
from .endpoints import template
from .starter import metadata


app = FastAPI(
    title=metadata.title,
    description=metadata.description,
    version=metadata.version,
    contact={
        "name": "Adil Rashitov",
        "email": "adil@wastelabs.co",
    },
)

middleware.log_endpoint_calls(app)

template.get_endpoint.v1.register_endpoint(app)
template.run_pipeline.v1.register_endpoint(app)
template.run_broken_pipeline.v1.register_endpoint(app)
