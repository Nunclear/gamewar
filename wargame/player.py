"""Player representation and economy handling."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple

from .map import Map, Terrain
from .units import Unit, UNIT_TYPES, UnitType


@dataclass
class Player:
    name: str
    money: int = 1000
    oil: int = 500
    stars: int = 0
    units: List[Unit] = field(default_factory=list)
    capital: Tuple[int, int] | None = None
    alive: bool = True

    def add_unit(self, utype: str, position: Tuple[int, int]) -> Unit:
        unit_type = UNIT_TYPES[utype]
        unit = Unit(owner=self.name, utype=unit_type, position=position)
        self.units.append(unit)
        return unit

    def remove_all_units(self) -> List[Unit]:
        units = self.units
        self.units = []
        return units
