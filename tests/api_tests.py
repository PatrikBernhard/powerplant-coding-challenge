import json
import os
import pytest
from pathlib import Path

from powerplantapp.domain.model import Fuel, PayLoad, PowerPlant
from powerplantapp.api.post import app

from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.fixture
def resources() -> Path:
    return Path.cwd() / "example_payloads"

@pytest.fixture
def get_example_payloads(resources):
    payloads = [json.loads((root / pl).read_bytes()) for root, _, pls in resources.walk() for pl in pls if "payload" in pl]
    return payloads

@pytest.fixture
def get_example_responses(resources):
    payloads = [json.loads((root / pl).read_bytes()) for root, _, pls in resources.walk() for pl in pls if "response" in pl]
    return payloads

@pytest.fixture()
def generate_payload():
    return PayLoad(
        load=1,
        fuels={Fuel.GAS: 1},
        powerplants=[
            PowerPlant(name="test", type="gasfired", efficiency=0.3, pmin=10, pmax=30)
        ],
    )


def test_api_set_up(get_example_payloads, get_example_responses):
    response = client.post("/productionplan", json=get_example_payloads[2])
    assert response.text == get_example_responses[0]