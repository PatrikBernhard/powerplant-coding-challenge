import json
import os
import re
import pytest
from pathlib import Path

from powerplantapp.domain.model import Fuel, PayLoad, PowerPlant

@pytest.fixture
def resources() -> Path:
    return Path.cwd() / "example_payloads"

@pytest.fixture
def get_example_payloads(resources):
    payloads = {re.sub("\D", "", pl): json.loads((root / pl).read_bytes()) for root, _, pls in resources.walk() for pl in pls if "payload" in pl}
    return payloads

@pytest.fixture
def get_example_responses(resources):
    responses = {re.sub("\D", "", rs): json.loads((root / rs).read_bytes()) for root, _, rss in resources.walk() for rs in rss if "response" in rs}
    return responses

@pytest.fixture()
def generate_payload():
    return PayLoad(
        load=1,
        fuels={Fuel.GAS: 1},
        powerplants=[
            PowerPlant(name="test", type="gasfired", efficiency=0.3, pmin=10, pmax=30)
        ],
    )