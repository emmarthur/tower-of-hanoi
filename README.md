# Tower of Hanoi (catalog #519)

Puzzle from Al Sweigart’s *The Big Book of Small Python Projects* (Project #74). Logic in `tower_of_hanoi_core.py`.

## Run the web demo (port 3030)

```powershell
Set-Location "c:\Users\emmak\Desktop\Content\CodingProjects\PortProjects\demos\tower-of-hanoi\web"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 3030
```

Open http://localhost:3030

Provenance: [BOOK_DIRECTIONS.md](./BOOK_DIRECTIONS.md).
