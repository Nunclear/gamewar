"""Core game logic implementing turn order and main mechanics."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Tuple, Iterable

from .map import Map, Terrain
from .player import Player
from .units import Unit


@dataclass
class Game:
    players: Dict[str, Player]
    game_map: Map
    turn_order: List[str]
    current_player_idx: int = 0

    @classmethod
    def create(cls, players: List[Player], width: int = 10, height: int = 10, seed: int | None = None) -> "Game":
        game_map = Map(width, height, seed, players=len(players))
        player_dict = {p.name: p for p in players}
        # Assign capitals
        for p, pos in zip(players, game_map.capitals):
            p.capital = pos
            game_map.get_hex(pos).owner = p.name
        turn_order = [p.name for p in players]
        return cls(player_dict, game_map, turn_order)

    @property
    def current_player(self) -> Player:
        return self.players[self.turn_order[self.current_player_idx]]

    def next_player(self) -> None:
        self.current_player_idx = (self.current_player_idx + 1) % len(self.turn_order)

    # --- Economy ---------------------------------------------------------
    def calcular_ingresos(self, player: Player) -> Tuple[int, int]:
        capitals = 0
        city_large = 0
        city_small = 0
        territory = 0
        oil_wells = 0
        stations = 0
        for coord, hex in self.game_map.hexes.items():
            if hex.owner != player.name:
                continue
            if hex.structure == Terrain.CITY_CAPITAL:
                capitals += 1
            elif hex.structure == Terrain.CITY_LARGE:
                city_large += 1
            elif hex.structure == Terrain.CITY_SMALL:
                city_small += 1
            elif hex.structure == Terrain.OIL_WELL:
                oil_wells += 1
            elif hex.structure == Terrain.STATION:
                stations += 1
            else:
                territory += 1
        dinero = 50 * capitals + 30 * city_large + 15 * city_small + 3 * territory
        petroleo_base = 10 * oil_wells
        petroleo = round(petroleo_base * (1 + 0.10 * stations))
        return dinero, petroleo

    def end_round(self) -> None:
        for player in self.players.values():
            d, p = self.calcular_ingresos(player)
            player.money += d
            player.oil += p

    # --- Movement --------------------------------------------------------
    def mover_unidad(self, player: Player, unit: Unit, path: Iterable[Tuple[int, int]]) -> None:
        """Move a unit along the given path.

        `path` is an iterable of coordinates excluding the unit's current position.
        The function calculates movement points and oil consumption according to
        terrain costs.
        """

        pm_usados = 0.0
        oil_necesario = 0.0
        current = unit.position
        for step in path:
            hex = self.game_map.get_hex(step)
            cost = unit.movement_cost(hex.terrain)
            pm_usados += cost
            oil_necesario += cost * unit.utype.tpm
            current = step
        if pm_usados > unit.utype.pm:
            raise ValueError("Movimiento excede PM disponible")
        if player.oil < oil_necesario:
            raise ValueError("Petróleo insuficiente")
        player.oil -= oil_necesario
        # Update position and ownership
        unit.position = current
        self.game_map.get_hex(current).owner = player.name

    # --- Capture ---------------------------------------------------------
    def capturar_capital(self, attacker: Unit) -> None:
        hex = self.game_map.get_hex(attacker.position)
        if hex.structure != Terrain.CITY_CAPITAL:
            return
        defender_name = hex.owner
        if defender_name is None or defender_name == attacker.owner:
            return
        defender = self.players[defender_name]
        # Transfer units
        transferred = defender.remove_all_units()
        for u in transferred:
            u.owner = attacker.owner
            self.players[attacker.owner].units.append(u)
        defender.alive = False
        hex.owner = attacker.owner

    # --- Utility ---------------------------------------------------------
    def players_alive(self) -> List[Player]:
        return [p for p in self.players.values() if p.alive]
