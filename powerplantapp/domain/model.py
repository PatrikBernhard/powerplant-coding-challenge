import json
from pathlib import Path
from pydantic import model_validator
from pydantic.dataclasses import dataclass
from enum import Enum

"""
The payload contains 3 types of data:
 - load: The load is the amount of energy (MWh) that need to be generated during one hour.
 - fuels: based on the cost of the fuels of each powerplant, the merit-order can be determined which is the starting point for deciding which powerplants should be switched on and how much power they will deliver.  Wind-turbine are either switched-on, and in that case generate a certain amount of energy depending on the % of wind, or can be switched off. 
   - gas(euro/MWh): the price of gas per MWh. Thus if gas is at 6 euro/MWh and if the efficiency of the powerplant is 50% (i.e. 2 units of gas will generate one unit of electricity), the cost of generating 1 MWh is 12 euro.
   - kerosine(euro/Mwh): the price of kerosine per MWh.
   - co2(euro/ton): the price of emission allowances (optionally to be taken into account).
   - wind(%): percentage of wind. Example: if there is on average 25% wind during an hour, a wind-turbine with a Pmax of 4 MW will generate 1MWh of energy.
 - powerplants: describes the powerplants at disposal to generate the demanded load. For each powerplant is specified:
   - name:
   - type: gasfired, turbojet or windturbine.
   - efficiency: the efficiency at which they convert a MWh of fuel into a MWh of electrical energy. Wind-turbines do not consume 'fuel' and thus are considered to generate power at zero price.
   - pmax: the maximum amount of power the powerplant can generate.
   - pmin: the minimum amount of power the powerplant generates when switched on. 
"""


class Fuel(Enum):
    GAS = "gas(euro/MWh)"
    KEROSINE = "kerosine(euro/MWh)"
    CO2 = "co2(euro/ton)"
    WIND = "wind(%)"

class PlantType(Enum):
    WIND = "windturbine"
    GAS = "gasfired"
    JET = "turbojet"



@dataclass
class PowerPlant:
    name: str
    type: PlantType
    efficiency: float
    pmin: int
    pmax: int


@dataclass
class PayLoad:
    load: int
    fuels: dict[Fuel, float]
    powerplants: list[PowerPlant]

    @classmethod
    def from_json(cls, path: Path):
        return cls(**json.loads(path.read_bytes()))

    @model_validator(mode='after')
    def set_new_efficiency_for_wind(self):
        """Immediately scale the p-value for wind to normalize calculations across powerplant types."""
        for pp in self.powerplants:
            if pp.type == PlantType.WIND:
                pp.pmin = pp.pmin*self.fuels[Fuel.WIND] / 100
                pp.pmax = pp.pmax*self.fuels[Fuel.WIND] / 100
        return self

@dataclass
class Response:
    name: str
    p: float