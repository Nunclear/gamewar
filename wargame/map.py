"""Map generation and terrain handling for the strategy game."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import random
from typing import Dict, Tuple, Optional, List


class Terrain(Enum):
    """Basic terrain types used on the hex map."""

    PLAIN = "plain"
    HILL = "hill"
    MOUNTAIN = "mountain"
    FOREST = "forest"
    SWAMP = "swamp"
    RIVER = "river"
    ROAD = "road"
    RAIL = "rail"
    RUINS = "ruins"
    CITY_CAPITAL = "city_capital"
    CITY_LARGE = "city_large"
    CITY_SMALL = "city_small"
    OIL_WELL = "oil_well"
    STATION = "station"


# Movement cost (movement points) for infantry units. Vehicles have special cases
INF_MOVEMENT_COST: Dict[Terrain, float] = {
    Terrain.PLAIN: 1.0,
    Terrain.ROAD: 0.5,
    Terrain.HILL: 1.5,
    Terrain.FOREST: 2.0,
    Terrain.SWAMP: 3.0,
    Terrain.MOUNTAIN: 3.0,  # only some units can enter
    Terrain.RIVER: float("inf"),
}

VEHICLE_MOVEMENT_COST: Dict[Terrain, float] = {
    Terrain.PLAIN: 1.0,
    Terrain.ROAD: 0.5,
    Terrain.HILL: 1.5,
    Terrain.FOREST: 3.0,
    Terrain.SWAMP: 4.0,
    Terrain.MOUNTAIN: float("inf"),
    Terrain.RIVER: float("inf"),
}


@dataclass
class Hex:
    """Single hex tile on the map."""

    terrain: Terrain = Terrain.PLAIN
    owner: Optional[str] = None  # player's name
    structure: Optional[Terrain] = None  # e.g. city, oil well, station


class Map:
    """Hex map consisting of terrain and structures.

    The map uses axial coordinates (q, r) for hexes.  Generation is deterministic
    given a random seed so that the same seed results in the same map layout.
    """

    def __init__(self, width: int, height: int, seed: Optional[int] = None, players: int = 2):
        self.width = width
        self.height = height
        self.hexes: Dict[Tuple[int, int], Hex] = {}
        self.capitals: List[Tuple[int, int]] = []
        if seed is not None:
            random.seed(seed)
        self._generate(players)

    # Directions for axial coordinates (q, r)
    DIRECTIONS = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]

    def _generate(self, players: int) -> None:
        """Generate map terrain and place capitals.

        For simplicity the terrain is largely plains with some random features.
        Capitals are placed in symmetric positions based on the number of players.
        """

        terrains = [Terrain.PLAIN] * 6 + [Terrain.FOREST, Terrain.HILL, Terrain.SWAMP]

        for q in range(self.width):
            for r in range(self.height):
                self.hexes[(q, r)] = Hex(terrain=random.choice(terrains))

        # place capitals
        positions = {
            2: [(0, 0), (self.width - 1, self.height - 1)],
            3: [(0, 0), (self.width - 1, 0), (self.width // 2, self.height - 1)],
            4: [(0, 0), (self.width - 1, 0), (self.width - 1, self.height - 1), (0, self.height - 1)],
        }
        cap_positions = positions.get(players)
        if not cap_positions or len(cap_positions) < players:
            raise ValueError("Players must be between 2 and 4")
        for pos in cap_positions[:players]:
            self.hexes[pos].terrain = Terrain.CITY_CAPITAL
            self.hexes[pos].structure = Terrain.CITY_CAPITAL
            self.capitals.append(pos)

        # Randomly place oil wells and stations
        free_hexes = [coord for coord, h in self.hexes.items() if h.structure is None]
        random.shuffle(free_hexes)
        for i in range(max(1, self.width // 5)):
            if not free_hexes:
                break
            coord = free_hexes.pop()
            self.hexes[coord].terrain = Terrain.OIL_WELL
            self.hexes[coord].structure = Terrain.OIL_WELL
        for i in range(max(1, self.width // 6)):
            if not free_hexes:
                break
            coord = free_hexes.pop()
            self.hexes[coord].terrain = Terrain.STATION
            self.hexes[coord].structure = Terrain.STATION

    def get_hex(self, coord: Tuple[int, int]) -> Hex:
        return self.hexes[coord]

    def neighbors(self, coord: Tuple[int, int]) -> List[Tuple[int, int]]:
        q, r = coord
        result = []
        for dq, dr in self.DIRECTIONS:
            nq, nr = q + dq, r + dr
            if (nq, nr) in self.hexes:
                result.append((nq, nr))
        return result
