"""Configuration helpers for setting up a game."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .player import Player
from .game import Game


@dataclass
class GameConfig:
    """Convenience dataclass holding game setup parameters.

    Attributes
    ----------
    width, height:
        Dimensions of the hex map.
    seed:
        Random seed used by the map generator.  The same seed results in
        identical maps which enables reproducible matches.
    players:
        List of player names participating in the match.  The length of the
        list decides the number of players.  Between 2 and 4 players are
        supported by the current map generator.
    money, oil:
        Starting resources for each player.
    """

    width: int = 10
    height: int = 10
    seed: Optional[int] = None
    players: List[str] = field(default_factory=lambda: ["Player1", "Player2"])
    money: int = 1000
    oil: int = 500

    def create_game(self) -> Game:
        """Create a :class:`Game` instance based on this configuration."""
        player_objs = [Player(name=p, money=self.money, oil=self.oil) for p in self.players]
        return Game.create(player_objs, width=self.width, height=self.height, seed=self.seed)
