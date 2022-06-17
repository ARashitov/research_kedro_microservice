import pytest


@pytest.fixture(scope="function")
def geocoding_v1_env_task_id() -> str:
    return "TruckRoutePlans_2022-03-25_IWS_1_small"


@pytest.fixture(scope="function")
def geocoding_v1_pipeline_name() -> str:
    return "geocoding.geodata_gov_hk.v1"
