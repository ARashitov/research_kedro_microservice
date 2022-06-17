import os
from copy import deepcopy
from typing import Any, Dict, List

import googlemaps
import numpy as np
import pandas as pd

from .abstract import GenericFormattingDriver
from .abstract import GenericGeocodingDriver


_GOOGLE_MAP_API_KEY = os.environ["google_maps_key"]
_DEFAULT_CATEGORY = "other"
_DEFAULT_API_NAME = "Google Maps"
_DEFAULT_VALUE_FOR_EMPTY_RESPONSE = {
    "address_components": [],
    "formatted_address": "",
    "partial_match": False,
    "place_id": "",
    "plus_code": {},
    "types": "establishment",
    "search_address": "",
    "match_type": "",
    "location_type": "",
    "viewport": {},
    "lat": 22.343233,
    "lng": 114.136316,
    "administrative_area_level_1": np.NaN,
    "neighborhood": np.NaN,
    "premise": np.NaN,
    "route": np.NaN,
    "street_number": np.NaN,
    "subpremise": np.NaN,
    "establishment": np.NaN,
    "types_category": _DEFAULT_CATEGORY,
    "location_type_category": _DEFAULT_CATEGORY,
    "no_match_found": True,
    "match_found": False,
    "api": _DEFAULT_API_NAME,
}


class GoogleMap(GenericGeocodingDriver):
    """
    Google map query driver
    """

    @staticmethod
    def _init_google_map_client(
        driver_params: Dict[str, Any],
        key: str,
    ) -> googlemaps.Client:
        driver_init_params = driver_params["init"]
        driver_init_params["key"] = key
        gmaps = googlemaps.Client(**driver_init_params)
        return gmaps

    @staticmethod
    def _handle_empty_response(response: Any) -> List[Any]:
        # NOTE: below is one of the corner case we met during operations
        if response is None:
            response = []
        return response

    @staticmethod
    def query(
        query: str,
        address: str,
        driver_params: Dict[str, Any],
        *args,
        **kwargs,
    ) -> pd.DataFrame:
        """Function runs query of single address

        Args:
        query (str): query string
        driver_params (Dict[str, Any]): query string

        Returns:
        pd.DataFrame: query results.
        """

        try:
            GenericGeocodingDriver.log_query(
                query=query,
                address=address,
                driver=_DEFAULT_API_NAME,
                processing_status="start",
            )
            gmaps = GoogleMap._init_google_map_client(
                driver_params,
                _GOOGLE_MAP_API_KEY,
            )
            response = gmaps.geocode(query)
            response = GoogleMap._handle_empty_response(response)
            GenericGeocodingDriver.log_query(
                query=query,
                address=address,
                driver=_DEFAULT_API_NAME,
                processing_status="finish",
            )
            return (address, response)
        except Exception as query_error:
            GenericGeocodingDriver.log_query_failure(
                driver=_DEFAULT_API_NAME,
                query=query,
                address=address,
                exception_message=str(query_error),
            )

    @staticmethod
    def format_raw_response(
        query: str,
        response: Dict[str, Any],
        params: Dict[str, Any],
        *args,
        **kwargs,
    ) -> pd.DataFrame:
        """
        Function performs formatting data to make ready it be offloaded to L2 cache

        Args:
        query (str): query executed against api
        response (Dict[str, Any]): raw response content
        params (Dict[str, Any]): kedro google map geocoding formatting parameters

        Returns:
        pd.DataFrame: Formatted response
        """
        if len(response) != 0:
            geocode = pd.DataFrame(response)
            geocode["search_address"] = query
            geocode = GmapFormatter.unpack_geocoding_response(geocode)
            geocode = GmapFormatter.unpack_address_components(
                geocode,
                params["components_of_interest"],
            )
            geocode = GmapFormatter.add_location_categoires(
                geocode,
                params["main_types"],
                params["main_location_types"],
            )
            geocode = GmapFormatter.flag_match_found(
                geocode,
                params["order_sequence"],
            )
        else:
            GenericFormattingDriver.log_formatting_failure(
                driver=_DEFAULT_API_NAME,
                query=query,
                response=response,
                exception_message="Empty api response",
            )
            geocode = pd.DataFrame([deepcopy(_DEFAULT_VALUE_FOR_EMPTY_RESPONSE)])
            geocode["search_address"] = query

        geocode["api"] = _DEFAULT_API_NAME

        geocode = geocode.loc[:, params["l2_cache_columns"]]
        return geocode


class GmapFormatter(GenericFormattingDriver):
    """
    Google map raw response formatting utilities
    """

    @staticmethod
    def _mark_match_type(geocodes: pd.DataFrame) -> pd.DataFrame:
        """
        Defines if point is uniquely returned under `match_type` flag

        Args:
        geocodes (pd.DataFrame): source geocoded dataframe

        Returns:
        pd.DataFrame: extended dataframe
        """
        geocodes["match_type"] = "single_match"
        is_duplicated = geocodes.duplicated(["search_address"], keep=False)
        geocodes.loc[is_duplicated, "match_type"] = "multiple_matches"
        return geocodes

    @staticmethod
    def _unpack_columns_content(
        content: pd.DataFrame,
        columns: List[str],
    ) -> pd.DataFrame:
        """
        Function performing unpacking columns containing dictionaries

        Args:
        geocodes (pd.DataFrame): source geocoded dataframe
        columns (List[str]): list of columns to unpack

        Returns:
        pd.DataFrame: extended dataframe
        """
        _content = content.copy()
        for column in columns:
            _content = pd.concat(
                [_content.drop([column], axis=1), _content[column].apply(pd.Series)],
                axis=1,
            )
        return _content

    @staticmethod
    def unpack_geocoding_response(geocodes: pd.DataFrame) -> pd.DataFrame:
        """
        Args:
        geocodes (pd.DataFrame): source geocoded dataframe

        Returns:
        pd.DataFrame: unpacked dataframe
        """
        geocodes = GmapFormatter._mark_match_type(geocodes)
        geocodes = GmapFormatter._unpack_columns_content(
            geocodes,
            ["geometry", "location"],
        )
        geocodes = geocodes.explode("types", ignore_index=True)
        geocodes = geocodes.reset_index(drop=True)

        return geocodes

    @staticmethod
    def _flatten_address_component(components: pd.DataFrame) -> pd.DataFrame:
        """Function flatenning content of address_component column

        Args:
        components (pd.DataFrame): components table

        Returns:
        pd.DataFrame: components table
        """
        components = components.explode("address_components")
        # NOTE: code below joins over columns unpacked address_components
        components = pd.concat(
            [
                components.drop(columns=["address_components"]),
                components["address_components"].apply(pd.Series),
            ],
            axis=1,
        )
        components = components.explode(["types"])
        return components

    @staticmethod
    def _select_components(
        components: pd.DataFrame,
        interests: List[str],
    ) -> pd.DataFrame:
        """
        Performs selection of components listed in parameters

        Args:
        components (pd.DataFrame): address components table
        interests (List[str]): columns of interests

        Returns:
        pd.DataFrame: address components table
        """
        table_of_interests = pd.DataFrame({"types": interests})
        return components.merge(table_of_interests)

    @staticmethod
    def _reformat_table(components: pd.DataFrame) -> pd.DataFrame:
        """
        Reformats component table from adjacency to matrix form

        Args:
        components (pd.DataFrame): address components table

        Returns:
        pd.DataFrame: address components matrix table
        """
        components = components.drop(columns=["short_name"], errors="ignore")
        components = (
            pd.pivot_table(
                components,
                columns="types",
                index="__temp_id",
                values="long_name",
                aggfunc="sum",
            )
            .reset_index()
            .reset_index(drop=True)
        )
        return components

    @staticmethod
    def _join_components_back(
        geocode: pd.DataFrame,
        components: pd.DataFrame,
        components_list: List[str],
    ) -> pd.DataFrame:
        """
        Joins components back to geocoded and extends
        components not listed in components list

        Args:
        geocode (pd.DataFrame): geocode response
        components (pd.DataFrame): address components table
        components_list (List[str]): list of components to use

        Returns:
        pd.DataFrame: joined components table
        """
        geocode = geocode.merge(components, how="left", on="__temp_id")
        for component in components_list:
            if component not in geocode.keys():
                geocode[component] = np.NAN
        geocode.drop(columns=["__temp_id"], inplace=True)
        return geocode

    @staticmethod
    def unpack_address_components(
        geocode: pd.DataFrame,
        components_of_interest: List[str],
    ) -> pd.DataFrame:
        """Function unpacks address of interests

        Args:
        geocode (pd.DataFrame): source geocoding response table
        components_of_interest (List[str]): kedro parameters

        Returns:
        pd.DataFrame: unpacked dataframe
        """
        # 1. Creation of component_table
        geocode["__temp_id"] = geocode.reset_index(drop=True).index
        components = geocode.loc[:, ["__temp_id", "address_components"]].copy()

        # 2. Unpacking adress of interests & join back
        components = GmapFormatter._flatten_address_component(components)
        components = GmapFormatter._select_components(
            components,
            components_of_interest,
        )
        components = GmapFormatter._reformat_table(components)
        geocode = GmapFormatter._join_components_back(
            geocode,
            components,
            components_of_interest,
        )
        return geocode

    @staticmethod
    def add_location_categoires(
        geocode: pd.DataFrame,
        main_types: List[str],
        main_location_types: List[str],
    ) -> pd.DataFrame:
        """
        Add ordered category values for types and location types.
        """

        def _extend_category(
            geocode: pd.DataFrame,
            src_col: str,
            trgt_col: str,
            desired_categories: List[str],
        ) -> pd.DataFrame:

            is_in_categories = geocode[src_col].isin(desired_categories)
            geocode[trgt_col] = geocode[src_col].where(
                is_in_categories,
                _DEFAULT_CATEGORY,
            )
            return geocode

        geocode = _extend_category(geocode, "types", "types_category", main_types)
        geocode = _extend_category(
            geocode,
            "location_type",
            "location_type_category",
            main_location_types,
        )

        return geocode

    @staticmethod
    def flag_match_found(geocode: pd.DataFrame, order_sequence: List[str]):
        """Drop duplicates based on column order sequence (keep first).

        Args:
            data: duplicates to be dropped
            order_sequence: columns to use to sort values.
        """
        geocode = geocode.sort_values(order_sequence)
        geocode = geocode.drop_duplicates(["search_address"], keep="first")

        geocode["no_match_found"] = (
            (geocode["types_category"] == "other")
            | (geocode["location_type_category"] == "other")
            | (geocode["location_type_category"].isna())
        )
        geocode["match_found"] = ~geocode["no_match_found"]
        geocode.loc[geocode["no_match_found"], "match_type"] = "no_match_found"
        return geocode
