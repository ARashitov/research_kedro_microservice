from typing import Tuple

import geopandas as gpd
import pandas as pd


HK_GRID_CRDS = "EPSG:2326"
WSG_84_CRS = "EPSG:4326"


def generate_queries(
    df: pd.DataFrame,
    address_col: str,
    url_template: str,
    replace_keyword: str,
    query_col: str,
) -> pd.DataFrame:

    addresses = df[address_col].to_list()
    queries = list(
        map(
            lambda template, address: template.replace(replace_keyword, address),
            [url_template] * len(addresses),
            addresses,
        ),
    )
    df[query_col] = queries
    df = df[[address_col, query_col]]
    return df


def project_coordinates(
    df: pd.DataFrame,
    in_lon_lat: Tuple[str],
    out_lon_lat: Tuple[str],
    src_trgt_crs: Tuple[str],
) -> pd.DataFrame:
    """Projects api crs to wsg84

    Args:
    df (pd.DataFrame): source data
    lon_in (str): source longitude colname
    lat_in (str): source latitude colname
    lon_out (str): output longitude colname
    lat_out (str): output latitude colname

    Returns:
    pd.DataFrame: Updated dataframe
    """
    geometry = gpd.points_from_xy(df.loc[:, in_lon_lat[0]], df.loc[:, in_lon_lat[1]])
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs=src_trgt_crs[0])
    gdf = gdf.to_crs(src_trgt_crs[1])
    df.loc[:, out_lon_lat[0]] = gdf.geometry.x
    df.loc[:, out_lon_lat[1]] = gdf.geometry.y
    del df["geometry"]
    return pd.DataFrame(df)
