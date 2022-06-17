import io
import os
from typing import Any, Callable, Dict, Union

import pandas as pd
import pandera.io
import requests


def get_environment_variables():
    return os.environ


def format_output_dataframe(
    df: pd.DataFrame,
    rename_params: Union[Dict[str, str], None] = None,
    add_features_params: Union[Dict[str, str], None] = None,
    dtypes_params: Union[Dict[str, str], None] = None,
    duplicate_columns: Union[Dict[str, str], None] = None,
) -> pd.DataFrame:
    """
    Module performing data formatting

    Args:
    df: Source dataframe to format
    rename_params: Column rename dictionary of mapping
    dtypes_params: Column types dictionary of mapping

    Returns:
        pd.DataFrame: _description_
    """

    if add_features_params is not None:
        n_records = df.shape[0]
        _df = pd.DataFrame(
            {col: [default] * n_records for col, default in add_features_params.items()},
        )
        df = pd.concat([df, _df], axis=1)

    if duplicate_columns is not None:
        _df = pd.DataFrame(
            {trgt_col: df[src_col].copy() for trgt_col, src_col in duplicate_columns.items()},
        )
        df = pd.concat([df, _df], axis=1)

    if rename_params is not None:
        df = df.rename(columns=rename_params)

    if dtypes_params is not None:
        for col, _dtype in dtypes_params.items():
            df[col] = df[col].astype(_dtype)

    return df


def make_partition(data: Any, partition_key: str) -> Dict[str, pd.DataFrame]:
    """
    Function framing task into dictionary
    partition further exported as partitioned dataset

    Args:
        task: Dataframe to wrap as partition
        task_id: key over which dataframe will be listed in dict

    Returns:
        Dict[str, pd.DataFrame]: Data partition
    """
    return {partition_key: data}


def read_partition(catalog: Dict[str, Callable], partition_key: str) -> Any:
    """
    Reads partition from kedro paritioned dataset registry

    Args:
        catalog: Catalog data registry
        partition_key: partition key

    Returns:
        Any: Data stored under specified partition key in registry
    """
    return catalog[partition_key]()


def validate_data_schema(
    df: pd.DataFrame,
    schema: requests.models.Response,
) -> pd.DataFrame:
    """
    Node performing data validation according to pandera schema

    Args:
        df: source pandas dataframe
        schema: url get response content

    Returns:
        pd.DataFrame: Validated dataframe
    """
    schema = pandera.io.from_yaml(io.StringIO(schema.text))
    df = schema.validate(df)
    return df
