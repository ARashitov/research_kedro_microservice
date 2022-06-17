from typing import Dict, List, Union
import pytest


@pytest.fixture(scope="module")
def geodata_gov_hk_address() -> str:
    return "屯門 屯門 龍門居 16座 11樓 B室"


@pytest.fixture(scope="module")
def geodata_gov_hk_query() -> str:
    return "https://geodata.gov.hk/gs/api/v1.0.0/locationSearch?" "q=屯門 屯門 龍門居 16座 11樓 B室"


@pytest.fixture(scope="module")
def geodata_gov_hk_response() -> List[Dict[str, Union[int, str]]]:
    return [
        {
            "addressZH": "龍門居",
            "nameZH": "龍門居第十六座",
            "x": 814640,
            "y": 827220,
            "nameEN": "Lung Mun Oasis Block 16",
            "addressEN": "LUNG MUN OASIS",
        },
    ]


@pytest.fixture(scope="module")
def geodata_gov_hk_driver_params() -> List[Dict[str, Union[int, str]]]:
    return {
        "rename_columns": {
            "addressZH": "formatted_address",
        },
        "output_columns": [
            "search_address",
            "lat",
            "lng",
            "formatted_address",
            "api",
        ],
    }
