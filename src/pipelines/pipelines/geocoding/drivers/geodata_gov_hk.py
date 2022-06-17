from copy import deepcopy
from typing import Any, Dict, List, Tuple

import pandas as pd
import requests

from .abstract import GenericFormattingDriver, GenericGeocodingDriver
from ..nodes import HK_GRID_CRDS, WSG_84_CRS
from ..nodes import project_coordinates


_DEFAULT_API_NAME = "Geodata HK Gov"
_DEFAULT_VALUE_FOR_EMPTY_RESPONSE = {
    "addressZH": "",
    "nameZH": "",
    "x": 841372,
    "y": 821141,
    "nameEN": "",
    "addressEN": "",
}


class GeodataGovHK(GenericGeocodingDriver):
    """
    Government geospatail data
    """

    @staticmethod
    def format_raw_response(
        query: str,
        responses: List[Dict[str, Any]],
        params: Dict[str, Any],
        *args,
        **kwargs,
    ) -> pd.DataFrame:
        """
        Function performs formatting data to make ready it be offloaded to L2 cache

        Args:
        query (str): query executed against api
        response (List[Dict[str, Any]]): raw response content
        params (Dict[str, Any]): kedro google map geocoding formatting parameters

        Returns:
        pd.DataFrame: Formatted response
        """
        # 1. Selection best coordinates
        # NOTE: we assume that first response is the most accurate
        response = GovHKFormatter.get_first_record(query, responses)
        geocode = pd.DataFrame(response)

        # 2. Extend with features
        geocode["api"] = _DEFAULT_API_NAME
        geocode = project_coordinates(
            geocode,
            in_lon_lat=("x", "y"),
            out_lon_lat=("lng", "lat"),
            src_trgt_crs=(HK_GRID_CRDS, WSG_84_CRS),
        )
        geocode = geocode.rename(columns=params["rename_columns"])

        # 3. Formatting columns
        geocode = geocode.loc[:, params["output_columns"]]
        return geocode

    @staticmethod
    def query(query: str, address: str, *args, **kwargs) -> Tuple[str, Any]:
        """Function runs query of single address

        Args:
        query (str): full query url
        address (str): address to look for

        Returns:
        Tuple[str, Any]: query response partitioned over query
        """
        try:
            with requests.Session() as api_session:
                GenericGeocodingDriver.log_query(
                    query,
                    address,
                    _DEFAULT_API_NAME,
                    processing_status="start",
                )
                response = api_session.get(
                    query,
                    headers={"Connection": "close"},
                    timeout=3,
                )
                response.raise_for_status()
                GenericGeocodingDriver.log_query(
                    query,
                    address,
                    _DEFAULT_API_NAME,
                    processing_status="finish",
                )
                return (address, response.json())
        except Exception as query_error:
            GenericGeocodingDriver.log_query_failure(
                driver=_DEFAULT_API_NAME,
                query=query,
                address=address,
                exception_message=str(query_error),
            )


class GovHKFormatter(GenericFormattingDriver):
    """
    GeodataGovHK raw response formatting utilities
    """

    @staticmethod
    def _extend_response(
        response: Dict[str, str],
        query: str,
        match_found: bool,
    ) -> Dict[str, str]:
        response["search_address"] = query
        response["match_found"] = match_found
        return response

    @staticmethod
    def get_first_record(query: str, responses: List[Dict[str, str]]):
        try:
            response = deepcopy(responses[0])
            response = GovHKFormatter._extend_response(response, query, True)
        except Exception as exc:
            response = deepcopy(_DEFAULT_VALUE_FOR_EMPTY_RESPONSE)
            response = GovHKFormatter._extend_response(response, query, False)
            GenericFormattingDriver.log_formatting_failure(
                driver=_DEFAULT_API_NAME,
                query=query,
                response=response,
                exception_message=str(exc),
            )
        return [response]
