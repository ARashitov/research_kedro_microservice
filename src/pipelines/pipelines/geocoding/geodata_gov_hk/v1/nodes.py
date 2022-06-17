"""
This is a boilerplate pipeline 'example'
generated using Kedro 0.18.0
"""
import platform

if platform.system() == "Darwin":
    from multiprocess import Pool
else:
    from multiprocessing import Pool
from typing import Any, Dict, List
import pandas as pd

from src.pipelines.pipelines.geocoding.drivers import registry

from ..config import DRIVER_NAME


def _query_sequential(driver, queries, addresses):
    return dict(
        map(
            driver.query,
            queries,
            addresses,
        ),
    )


def _query_parallel(driver, queries, addresses, n_parallel):
    with Pool(n_parallel) as pool:
        geocodes = pool.starmap(
            driver.query,
            zip(
                queries,
                addresses,
            ),
        )
        geocodes = dict(geocodes)
    del pool
    return geocodes


def run_api_queries(df: pd.DataFrame, address_col: str, query_col: str, n_parallel: int) -> pd.DataFrame:
    driver = registry[DRIVER_NAME]

    if n_parallel == 1:
        geocodes = _query_sequential(driver, df[query_col], df[address_col])
    elif n_parallel > 1:
        geocodes = _query_parallel(driver, df[query_col], df[address_col], n_parallel)
    else:
        raise KeyError("n_parallel can't be less than 1")

    return geocodes


def _flatten_sequential(driver, queries, responses, driver_params) -> List[Dict[str, Any]]:
    geocodes = list(
        map(
            driver.format_raw_response,
            queries,
            responses,
            [driver_params] * len(responses),
        ),
    )
    return geocodes


def _flatten_parallel(driver, queries, responses, driver_params, n_parallel) -> List[Dict[str, Any]]:
    with Pool(n_parallel) as pool:
        geocodes = pool.starmap(
            driver.format_raw_response,
            zip(
                queries,
                responses,
                [driver_params] * len(responses),
            ),
        )
    del pool
    return geocodes


def flatten_api_response(
    api_response: Dict[str, List[Any]],
    driver_params: Dict[str, Any],
) -> pd.DataFrame:
    driver = registry[DRIVER_NAME]

    queries = list(api_response.keys())
    responses = list(api_response.keys())
    n_parallel = driver_params["n_process"]

    if n_parallel == 1:
        geocodes = _flatten_sequential(
            driver,
            queries,
            responses,
            driver_params,
        )
    elif n_parallel > 1:
        geocodes = _flatten_parallel(driver, queries, responses, driver_params, n_parallel)
    else:
        raise KeyError("n_parallel can't be less than 1")

    geocodes = pd.concat(geocodes).reset_index(drop=True)
    return geocodes


def join_geocodes_back(
    original_df: pd.DataFrame,
    geocodes: pd.DataFrame,
    input_address_col: str,
) -> pd.DataFrame:
    geocodes = geocodes.rename(columns={"search_address": input_address_col})
    original_df = original_df.merge(geocodes, how="left")
    return original_df
