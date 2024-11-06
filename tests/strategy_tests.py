from functools import partial
from powerplantapp.api.services.strategy import merit_order
from powerplantapp.domain.model import PayLoad


def test_merit_order(get_example_payloads, get_example_responses):
    for payload in [get_example_payloads[2]]:
        payload = PayLoad(**payload)
        sorted_powerplants = sorted(payload.powerplants, key=partial(merit_order, fuels=payload.fuels))
        assert all(answer_pp["name"] == response_pp.name for answer_pp, response_pp in zip(get_example_responses[0], sorted_powerplants))
    