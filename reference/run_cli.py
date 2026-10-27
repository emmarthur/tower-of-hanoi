"""Terminal Tower of Hanoi — uses shared tower_of_hanoi_core logic."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from tower_of_hanoi_core import (  # noqa: E402
    TOTAL_DISKS,
    apply_move,
    initial_state,
    state_for_client,
)

print(
    """Tower of Hanoi

Move the stack from tower A to B or C. Only one disk at a time; no larger disk on a smaller one.
Enter moves like AB (A to B), or QUIT.
"""
)


def display(towers: dict[str, list[int]]) -> None:
    for level in range(TOTAL_DISKS, -1, -1):
        for name in ("A", "B", "C"):
            tower = towers[name]
            if level >= len(tower):
                print("  ||  ", end="")
            else:
                width = tower[level]
                print(f" {'@' * width:^{TOTAL_DISKS * 2 + 2}} ", end="")
        print()
    pad = " " * TOTAL_DISKS
    print(f"{pad} A{pad}{pad} B{pad}{pad} C\n")


state = initial_state()

while state["status"] == "playing":
    view = state_for_client(state)
    display(view["towers"])
    print(f"Moves: {view['moves']} (perfect play: {view['optimal_moves']})")
    raw = input("Move (e.g. AC) or QUIT:\n> ").strip().upper()
    if raw == "QUIT":
        print("Thanks for playing!")
        break
    if len(raw) != 2:
        print("Enter two tower letters, e.g. AB.")
        continue
    try:
        state = apply_move(state, raw[0], raw[1])
    except ValueError as exc:
        print(exc)

if state["status"] == "won":
    display(state["towers"])
    print(f"You solved it in {state['moves']} moves! Well done!")
