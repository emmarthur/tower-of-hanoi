const statsText = document.getElementById("stats-text");
const resultText = document.getElementById("result-text");
const errorEl = document.getElementById("error-text");
const newBtn = document.getElementById("btn-new");
const boardEl = document.getElementById("board");
const moveHint = document.getElementById("move-hint");
const towerButtons = document.querySelectorAll(".tower-btn");

const SESSION_KEY = "tower-of-hanoi-v1";

let state = null;
let selectedFrom = null;

function persistState() {
  if (state) AppSession.save(SESSION_KEY, state);
}

function restoreState() {
  const saved = AppSession.load(SESSION_KEY);
  if (!saved?.towers) return false;
  state = saved;
  render();
  return true;
}

AppSession.wireHelpSave(SESSION_KEY, () => state);

function setError(message) {
  errorEl.hidden = !message;
  errorEl.textContent = message || "";
}

function diskColors(size) {
  const hues = [200, 280, 340, 30, 160];
  const h = hues[(size - 1) % hues.length];
  return {
    bg: `hsl(${h}, 70%, 48%)`,
    border: `hsl(${h}, 80%, 65%)`,
  };
}

function render() {
  if (!state) return;
  const n = state.total_disks ?? 5;
  boardEl.innerHTML = "";

  ["A", "B", "C"].forEach((name) => {
    const col = document.createElement("div");
    col.className = "tower-col";
    col.dataset.tower = name;

    const peg = document.createElement("div");
    peg.className = "peg";
    col.appendChild(peg);

    const stack = document.createElement("div");
    stack.className = "disk-stack";
    const disks = state.towers[name] || [];
    disks.forEach((size) => {
      const disk = document.createElement("div");
      disk.className = "disk";
      const widthPct = 30 + (size / n) * 70;
      disk.style.width = `${widthPct}%`;
      const colors = diskColors(size);
      disk.style.background = colors.bg;
      disk.style.borderColor = colors.border;
      disk.textContent = size;
      stack.appendChild(disk);
    });
    col.appendChild(stack);

    const label = document.createElement("span");
    label.className = "tower-label";
    label.textContent = name;
    col.appendChild(label);

    if (selectedFrom === name) {
      col.classList.add("is-selected");
    }

    boardEl.appendChild(col);
  });

  towerButtons.forEach((btn) => {
    const t = btn.dataset.tower;
    btn.classList.toggle("is-selected", t === selectedFrom);
    btn.disabled = state.status === "won";
  });

  const optimal = state.optimal_moves ?? 31;
  statsText.textContent = `Moves: ${state.moves} · Perfect: ${optimal}`;

  if (state.status === "won") {
    resultText.hidden = false;
    resultText.textContent = `Solved in ${state.moves} moves!`;
    moveHint.textContent = "Puzzle complete — start a new game.";
  } else {
    resultText.hidden = true;
    moveHint.textContent = selectedFrom
      ? `Moving from tower ${selectedFrom} — pick destination.`
      : "Select a source tower, then a destination.";
  }
}

async function resetGame() {
  setError(null);
  selectedFrom = null;
  try {
    const res = await fetch("/api/reset", { method: "POST" });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Could not reset.");
    AppSession.clear(SESSION_KEY);
    state = data;
    render();
    persistState();
  } catch (err) {
    setError(err.message || "Could not reset.");
  }
}

async function tryMove(from, to) {
  setError(null);
  try {
    const res = await fetch("/api/move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        state: {
          towers: state.towers,
          moves: state.moves,
          status: state.status,
        },
        from_tower: from,
        to_tower: to,
      }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || "Invalid move.");
    state = data;
    selectedFrom = null;
    render();
    persistState();
  } catch (err) {
    setError(err.message || "Invalid move.");
    selectedFrom = null;
    render();
  }
}

function onTowerPick(name) {
  if (!state || state.status === "won") return;
  setError(null);
  const disks = state.towers[name] || [];
  if (!selectedFrom) {
    if (!disks.length) {
      setError("That tower has no disks.");
      return;
    }
    selectedFrom = name;
    render();
    return;
  }
  if (selectedFrom === name) {
    selectedFrom = null;
    render();
    return;
  }
  tryMove(selectedFrom, name);
}

towerButtons.forEach((btn) => {
  btn.addEventListener("click", () => onTowerPick(btn.dataset.tower));
});

boardEl.addEventListener("click", (event) => {
  const col = event.target.closest(".tower-col");
  if (!col) return;
  onTowerPick(col.dataset.tower);
});

newBtn.addEventListener("click", () => resetGame());

if (!restoreState()) resetGame();
