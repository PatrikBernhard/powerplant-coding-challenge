
from functools import partial
from powerplantapp.domain.model import Fuel, PayLoad, PlantType, Response, PowerPlant


def compute_response(payload: PayLoad) -> list[Response]:
    sorted_powerplants = sorted(payload.powerplants, key=partial(merit_order, fuels=payload.fuels))
    p_budget = payload.load
    response = []
    for pp in sorted_powerplants:
        desired_p = get_desired_p(pp, p_left=p_budget)
        response.append(Response(pp.name, desired_p))
        p_budget -= desired_p 
    return response

def get_desired_p(powerplant: PowerPlant, p_left: int):
    if p_left <= 0:
        return 0
    return max(powerplant.pmin, min(powerplant.pmax, p_left))


def merit_order(powerplant: PowerPlant, fuels: dict[Fuel, float]) -> int:
    """
    The merit-order can be determined which is the starting point for deciding which powerplants should be switched on
     and how much power they will deliver.

    Thus if gas is at 6 euro/MWh and if the efficiency of the powerplant is 50% 
    (i.e. 2 units of gas will generate one unit of electricity),
    the cost of generating 1 MWh is 12 euro.

    co2(euro/ton): the price of emission allowances (optionally to be taken into account).
    Taken into account that a gas-fired powerplant also emits CO2,
        for this challenge, you may take into account that each MWh generated creates 0.3 ton of CO2.
    """
    match powerplant.type:
        case PlantType.WIND:
            return 0
        case PlantType.GAS:
            return fuels[Fuel.GAS]/powerplant.efficiency + 0.3*fuels[Fuel.CO2]
        case PlantType.JET:
            return fuels[Fuel.KEROSINE]/powerplant.efficiency
    