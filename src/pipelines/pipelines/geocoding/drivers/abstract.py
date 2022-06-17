import abc
from typing import Any, Dict, Literal, Tuple

import pandas as pd

from src.pipelines.settings import get_logger


LOGGER = get_logger()


class GenericGeocodingDriver(abc.ABC):
    """
    Generic driver describing child geocoding functionality
    """

    @staticmethod
    def preprocess_query_inputs(
        addresses: pd.DataFrame,
        driver_params: Dict[str, Any],
        *args,
        **kwargs,
    ) -> pd.DataFrame:
        """Function preprocess inputs to query from api
            by replacement of keywords in template by the ones
            provided in function arguments.

        Args:
        addresses (pd.DataFrame): addresses to generate url query for
        driver_params (Dict[str, Any]): preprocessing driver parameters

        Returns:
        pd.DataFrame: urls with generated queries
        """
        queries = []
        for search_address in addresses[driver_params["input_addres_column"]]:
            query = driver_params["url_template"].replace(driver_params["replace_keyword"], search_address)
            queries.append(query)
        addresses[driver_params["query_colname"]] = list(queries)
        return addresses

    @staticmethod
    def log_query_failure(
        query: str,
        address: str,
        driver: str,
        exception_message: str,
    ):
        LOGGER.error(
            {
                "query": query,
                "address": address,
                "stage": "Geocoding API call",
                "driver": driver,
                "message": exception_message,
            },
        )

    @staticmethod
    def log_query(
        query: str,
        address: str,
        driver: str,
        processing_status: Literal["start", "finish"],
    ):
        LOGGER.info(
            {
                "query": query,
                "address": address,
                "driver": driver,
                "processing_status": processing_status,
            },
        )

    @staticmethod
    def query(query: str, address: str, *args, **kwargs) -> Tuple[str, Any]:
        """Function runs query of single address

        Args:
        query (str): full query url
        address (str): address to look for

        Returns:
        Tuple[str, Any]: query response partitioned over query
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def format_raw_response(response: Dict[str, Any], *args, **kwargs) -> pd.DataFrame:
        """Performs formatting of response to migrate it from l1 cache to l2

        Args:
        response (Dict[str, Any]): raw api response need to be formatted

        Returns:
        pd.DataFrame: formatted dataframe
        """
        pass


class GenericFormattingDriver(object):
    @staticmethod
    def log_formatting_failure(
        driver: str,
        query: str,
        response: Any,
        exception_message: str,
    ):
        LOGGER.error(
            {
                "driver": driver,
                "query": query,
                "stage": "Formatting response",
                "response": response,
                "message": exception_message,
            },
        )
