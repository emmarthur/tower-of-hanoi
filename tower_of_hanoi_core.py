"""
Tower of Hanoi logic — shared by CLI and web.

Follows Al Sweigart's tower dicts, disk sizes, and move rules.
"""

from __future__ import annotations

import copy
from typing import Any, Literal

TOTAL_DISKS = 5
TOWER_NAMES: tuple[str, ...] = ("A", "B", "C")
COMPLETE_TOWER = list(range(TOTAL_DISKS, 0, -1))


def initial_state() -> dict[str, Any]:
    return {
        "towers": {"A": copy.copy(COMPLETE_TOWER), "B": [], "C": []},
        "moves": 0,
        "status": "playing",
    }


def is_solved(towers: dict[str, list[int]]) -> bool:
    return COMPLETE_TOWER in (towers["B"], towers["C"])


def apply_move(state: dict[str, Any], from_tower: str, to_tower: str) -> dict[str, Any]:
    if state.get("status") != "playing":
        raise ValueError("Puzzle already solved. Start a new game.")

    from_key = from_tower.upper()
    to_key = to_tower.upper()
    if from_key not in TOWER_NAMES or to_key not in TOWER_NAMES:
        raise ValueError("Towers must be A, B, or C.")
    if from_key == to_key:
        raise ValueError("Pick two different towers.")

    towers = copy.deepcopy(state["towers"])
    if not towers[from_key]:
        raise ValueError("That tower has no disks.")
    disk = towers[from_key][-1]
    if towers[to_key] and towers[to_key][-1] < disk:
        raise ValueError("Can't put larger disks on top of smaller ones.")

    towers[from_key].pop()
    towers[to_key].append(disk)

    next_state: dict[str, Any] = {
        "towers": towers,
        "moves": state["moves"] + 1,
        "status": "playing",
    }
    if is_solved(towers):
        next_state["status"] = "won"
    return next_state


def state_for_client(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "towers": state["towers"],
        "moves": state["moves"],
        "status": state["status"],
        "total_disks": TOTAL_DISKS,
        "optimal_moves": (2**TOTAL_DISKS) - 1,
    }
