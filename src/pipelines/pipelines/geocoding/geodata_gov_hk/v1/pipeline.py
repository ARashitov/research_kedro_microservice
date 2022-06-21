"""
This is a boilerplate pipeline 'example'
generated using Kedro 0.18.0
"""

from kedro.pipeline import Pipeline, node

from src.pipelines.pipelines import config_pipeline
from src.pipelines.pipelines.nodes import read_partition
from src.pipelines.pipelines.nodes import make_partition

from . import nodes
from ...nodes import generate_queries


def create_pipeline(**kwargs) -> Pipeline:
    return config_pipeline.create_pipeline() + Pipeline(
        [
            node(
                func=read_partition,
                inputs=[
                    "02_intermediate__geocoding__input",
                    "params:common.task_id",
                ],
                outputs="02_intermediate__geocoding__v1__original_data",
                name="geocoding__geodata_gov_hk__v1__read_source_data",
            ),
            node(
                func=generate_queries,
                inputs=[
                    "02_intermediate__geocoding__v1__original_data",
                    "params:geocoding.v1.input_addres_column",
                    "params:geocoding.v1.api.geodata_gov_hk.url_template",
                    "params:geocoding.v1.replace_keyword",
                    "params:geocoding.v1.query_colname",
                ],
                outputs="02_intermediate__geocoding__v1__queries",
                name="geocoding__geodata_gov_hk__v1__queries_generation",
            ),
            node(
                func=nodes.run_api_queries,
                inputs=[
                    "02_intermediate__geocoding__v1__queries",
                    "params:geocoding.v1.input_addres_column",
                    "params:geocoding.v1.query_colname",
                    "params:geocoding.v1.api.geodata_gov_hk.n_process",
                ],
                outputs="02_intermediate__geocoding__v1__query_responses",
                name="geocoding__geodata_gov_hk__v1__extraction_of_geocodes",
            ),
            node(
                func=nodes.flatten_api_response,
                inputs=[
                    "02_intermediate__geocoding__v1__query_responses",
                    "params:geocoding.v1.api.geodata_gov_hk",
                ],
                outputs="02_intermediate__geocoding__v1__reformatted",
                name="geocoding__geodata_gov_hk__v1__reformate",
            ),
            node(
                func=nodes.join_geocodes_back,
                inputs=[
                    "02_intermediate__geocoding__v1__original_data",
                    "02_intermediate__geocoding__v1__reformatted",
                    "params:geocoding.v1.input_addres_column",
                ],
                outputs="02_intermediate__geocoding__v1__finished",
                name="geocoding__geodata_gov_hk__v1__geocodes_expansion",
            ),
            node(
                func=make_partition,
                inputs=[
                    "02_intermediate__geocoding__v1__finished",
                    "params:common.task_id",
                ],
                outputs="02_intermediate__geocoding__output",
                name="geocoding__geodata_gov_hk__v1__export_result",
            ),
        ],
    )
