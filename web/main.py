"""
FastAPI app — Tower of Hanoi puzzle.

Run: uvicorn main:app --reload --port 3030
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

_DEMO_ROOT = Path(__file__).resolve().parent.parent
if str(_DEMO_ROOT) not in sys.path:
    sys.path.insert(0, str(_DEMO_ROOT))

from tower_of_hanoi_core import (  # noqa: E402
    apply_move,
    initial_state,
    state_for_client,
)

app = FastAPI(title="Tower of Hanoi")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")


class TowersState(BaseModel):
    towers: dict[str, list[int]]
    moves: int = 0
    status: Literal["playing", "won"] = "playing"


class MoveRequest(BaseModel):
    state: TowersState
    from_tower: str = Field(..., min_length=1, max_length=1)
    to_tower: str = Field(..., min_length=1, max_length=1)


def _state_from_client(body: TowersState) -> dict[str, Any]:
    return {
        "towers": body.towers,
        "moves": body.moves,
        "status": body.status,
    }


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html")


@app.get("/help", response_class=HTMLResponse)
async def help_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "help.html")


@app.post("/api/reset")
async def api_reset() -> JSONResponse:
    return JSONResponse(state_for_client(initial_state()))


@app.post("/api/move")
async def api_move(body: MoveRequest) -> JSONResponse:
    try:
        state = _state_from_client(body.state)
        new_state = apply_move(state, body.from_tower, body.to_tower)
        return JSONResponse(state_for_client(new_state))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
