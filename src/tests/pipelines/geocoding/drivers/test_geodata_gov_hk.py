import pandas as pd

# pylint: disable=import-error
from src.pipelines.pipelines.geocoding.drivers.geodata_gov_hk import GeodataGovHK


class TestGeodataGovHK:
    def __assert_query_schema(self, response):
        assert "x" in response
        assert "y" in response
        assert "addressEN" in response
        assert "addressZH" in response
        assert "nameZH" in response
        assert "nameEN" in response

    def test_query(self, geodata_gov_hk_address: str, geodata_gov_hk_query: str):
        query_response = GeodataGovHK.query(
            query=geodata_gov_hk_query,
            address=geodata_gov_hk_address,
        )
        response = query_response
        assert geodata_gov_hk_address == response[0]
        self.__assert_query_schema(response[1][0])

    def __assert_formatted_schema(self, df: pd.DataFrame):
        assert "search_address" in df.columns
        assert "lat" in df.columns
        assert "lng" in df.columns
        assert "formatted_address" in df.columns
        assert "api" in df.columns

    def test_empty_formatting(self, geodata_gov_hk_address, geodata_gov_hk_driver_params):
        reformatted_response = GeodataGovHK.format_raw_response(
            query=geodata_gov_hk_address,
            responses=[],
            params=geodata_gov_hk_driver_params,
        )
        assert type(reformatted_response) == pd.DataFrame
        self.__assert_formatted_schema(reformatted_response)

    def test_non_empty_formatting(self, geodata_gov_hk_address, geodata_gov_hk_response, geodata_gov_hk_driver_params):
        reformatted_response = GeodataGovHK.format_raw_response(
            query=geodata_gov_hk_address,
            responses=geodata_gov_hk_response,
            params=geodata_gov_hk_driver_params,
        )
        assert type(reformatted_response) == pd.DataFrame
        self.__assert_formatted_schema(reformatted_response)
