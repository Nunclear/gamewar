"""Core package for turn-based WWII strategy game."""

from .game import Game
from .player import Player
from .units import Unit, UnitType, UNIT_TYPES
from .map import Map, Terrain, Hex
from .config import GameConfig

__all__ = [
    "Game",
    "Player",
    "Unit",
    "UnitType",
    "UNIT_TYPES",
    "Map",
    "Terrain",
    "Hex",
    "GameConfig",
]
