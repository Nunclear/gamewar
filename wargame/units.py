"""Unit definitions and movement handling."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from .map import Terrain, INF_MOVEMENT_COST, VEHICLE_MOVEMENT_COST


@dataclass
class UnitType:
    """Definition of a unit type including economic and movement stats."""

    name: str
    money_cost: int
    oil_cost: int
    tpm: float  # Oil consumption per movement point
    pm: int  # Movement points
    vehicle: bool = False


# Basic unit types based on GDD
UNIT_TYPES: Dict[str, UnitType] = {
    "INF_BASIC": UnitType("Infanteria basica", money_cost=60, oil_cost=0, tpm=0.0, pm=4, vehicle=False),
    "INF_HEAVY": UnitType("Infanteria pesada", money_cost=90, oil_cost=0, tpm=0.0, pm=3, vehicle=False),
    "RECON": UnitType("Reconocimiento", money_cost=80, oil_cost=20, tpm=1.0, pm=6, vehicle=True),
    "TANK_MEDIUM": UnitType("Tanque medio", money_cost=300, oil_cost=45, tpm=1.5, pm=5, vehicle=True),
}


@dataclass
class Unit:
    owner: str
    utype: UnitType
    position: Tuple[int, int]
    hp: int = 10

    def movement_cost(self, terrain: Terrain) -> float:
        table = VEHICLE_MOVEMENT_COST if self.utype.vehicle else INF_MOVEMENT_COST
        return table.get(terrain, float("inf"))
