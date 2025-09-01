import pytest

from wargame.map import Map, Terrain
from wargame.player import Player
from wargame.game import Game
from wargame.config import GameConfig


def test_map_determinism():
    m1 = Map(5, 5, seed=42, players=2)
    m2 = Map(5, 5, seed=42, players=2)
    for coord in m1.hexes:
        h1 = m1.hexes[coord]
        h2 = m2.hexes[coord]
        assert h1.terrain == h2.terrain
        assert h1.structure == h2.structure


def setup_income_scenario() -> Game:
    p1 = Player("A")
    p2 = Player("B")
    game = Game.create([p1, p2], width=10, height=10, seed=1)
    # clear map
    for h in game.game_map.hexes.values():
        h.owner = None
        h.structure = None
        h.terrain = Terrain.PLAIN
    game.game_map.capitals = [(0, 0)]
    cap = (0, 0)
    game.game_map.get_hex(cap).owner = "A"
    game.game_map.get_hex(cap).structure = Terrain.CITY_CAPITAL
    # City large and smalls
    large = (1, 0)
    small1 = (2, 0)
    small2 = (3, 0)
    game.game_map.get_hex(large).owner = "A"
    game.game_map.get_hex(large).structure = Terrain.CITY_LARGE
    game.game_map.get_hex(small1).owner = "A"
    game.game_map.get_hex(small1).structure = Terrain.CITY_SMALL
    game.game_map.get_hex(small2).owner = "A"
    game.game_map.get_hex(small2).structure = Terrain.CITY_SMALL
    # Oil wells and station
    well1 = (0, 1)
    well2 = (1, 1)
    station = (2, 1)
    for w in [well1, well2]:
        game.game_map.get_hex(w).owner = "A"
        game.game_map.get_hex(w).structure = Terrain.OIL_WELL
    game.game_map.get_hex(station).owner = "A"
    game.game_map.get_hex(station).structure = Terrain.STATION
    special = {cap, large, small1, small2, well1, well2, station}
    # Add 24 territory hexes
    count = 0
    for coord in game.game_map.hexes:
        if coord in special:
            continue
        game.game_map.get_hex(coord).owner = "A"
        count += 1
        if count == 24:
            break
    return game


def test_income_example():
    game = setup_income_scenario()
    player = game.players["A"]
    dinero, petroleo = game.calcular_ingresos(player)
    assert dinero == 182
    assert petroleo == 22


def test_move_consumes_oil_and_claims_territory():
    p1 = Player("A")
    p2 = Player("B")
    game = Game.create([p1, p2], width=5, height=5, seed=1)
    unit = p1.add_unit("RECON", p1.capital)
    path = [(p1.capital[0] + 1, p1.capital[1])]
    before_oil = p1.oil
    game.mover_unidad(p1, unit, path)
    assert unit.position == path[-1]
    assert p1.oil < before_oil
    assert game.game_map.get_hex(unit.position).owner == "A"


def test_capture_capital_transfers_units():
    p1 = Player("A")
    p2 = Player("B")
    game = Game.create([p1, p2], width=5, height=5, seed=1)
    defender_unit = p2.add_unit("INF_BASIC", (1, 1))
    attacker_unit = p1.add_unit("INF_BASIC", game.game_map.capitals[1])
    game.capturar_capital(attacker_unit)
    assert not p2.alive
    assert defender_unit in p1.units


def test_game_is_configurable():
    cfg = GameConfig(width=8, height=7, seed=99, players=["Alice", "Bob", "Carol"], money=500, oil=200)
    game = cfg.create_game()
    assert game.game_map.width == 8
    assert game.game_map.height == 7
    assert set(game.players.keys()) == {"Alice", "Bob", "Carol"}
    assert all(p.money == 500 and p.oil == 200 for p in game.players.values())
    # ensure correct number of capitals placed
    assert len(game.game_map.capitals) == 3
