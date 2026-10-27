# Book directions — Tower of Hanoi

**Catalog #519** · Al Sweigart, *The Big Book of Small Python Projects*, **Project #74** — Tower of Hanoi

- Invent with Python: [project74.html](https://inventwithpython.com/bigbookpython/project74.html)
- Upstream: [towerofhanoi.py](https://github.com/asweigart/the-big-book-of-small-python-projects/blob/main/towerofhanoi.py)
- Local reference: [`reference/towerofhanoi.py`](./reference/towerofhanoi.py)
- Shared logic: [`tower_of_hanoi_core.py`](./tower_of_hanoi_core.py)

## What the book asks you to build

A five-disk puzzle:

1. Towers **A**, **B**, **C** as lists (end of list = top).
2. Player moves one disk at a time with two-letter moves (**AB**, **AC**, …).
3. Cannot place a larger disk on a smaller one; empty towers accept any disk.
4. Win when the full stack sits on **B** or **C**.

## Web version (`web/` — FastAPI, port **3030**)

| Book step | Web equivalent |
|-----------|----------------|
| Move validation | `POST /api/move` |
| Win check | `tower_of_hanoi_core.apply_move` |
| Display | Colored disks + tap/click towers |

CLI: [`reference/run_cli.py`](./reference/run_cli.py)
