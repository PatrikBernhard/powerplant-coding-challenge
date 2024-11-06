from powerplantapp.api.post import app

from fastapi.testclient import TestClient

client = TestClient(app)



def test_api_set_up(get_example_payloads, get_example_responses):
    response = client.post("/productionplan", json=get_example_payloads[2])
    assert response.text == get_example_responses[0]


def test_no_response_has_illegal_pvalue(get_example_payloads, get_example_responses):
    for payload in get_example_payloads:
         response = client.post("/productionplan", json=payload)
         sorted_payload = sorted(payload["powerplants"], key=lambda x: x["name"])
         sorted_response = sorted(response, key=lambda x: x["name"])
         assert all(re["p"] == 0 or pl["pmin"] <= re["p"] and pl["pmax"] >= re["p"] for pl, re in zip(sorted_payload, sorted_response))