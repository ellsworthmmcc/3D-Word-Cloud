# 3D-Word-Cloud

Generates interactive 3D word clouds from Wikipedia article URLs using topic modeling.
Paste a Wikipedia URL and the app scrapes the article, runs BERTopic analysis, and renders
the top 64 topic words as an explorable 3D sphere — sized and colored by relevance.

---

## Tech Stack & Libraries

### Backend
- **Python 3.12**
- **FastAPI** – API framework
- **SQLAlchemy (async)** – Database ORM
- **aiosqlite** – Async SQLite
- **BERTopic** – Topic modeling for word scoring
- **BeautifulSoup & httpx** – HTML scraping
- **uv** – Package management

### Frontend
- **React 19** + **TypeScript**
- **Three.js / @react-three/fiber / @react-three/drei** – 3D rendering
- **TailwindCSS** – Styling
- **Vite** – Dev server and bundler
- **Axios** – HTTP requests

---

## Prerequisites

- Python 3.12
- Node.js 18+
- [uv](https://docs.astral.sh/uv/) (`pip install uv`)

---

## Setup & Running

### 1. Backend
```bash
cd backend
uv venv .venv
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```
**macOS/Linux:**
```bash
source .venv/bin/activate
```

```bash
uv pip install -e .
fastapi dev main.py
```

### 2. Frontend
In a separate terminal:
```bash
cd frontend
npm install
npm run dev
```

---

### URLs
| Service  | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend  | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/analyze` | Submit a Wikipedia URL for analysis |
| `GET` | `/analyze` | List all analyzed article IDs |
| `GET` | `/analyze/{id}` | Get analysis for a specific article |
| `PATCH` | `/analyze/{id}` | Re-analyze an existing article |
| `DELETE` | `/analyze/{id}` | Delete an article analysis |


---

Notes
- The 3D cloud is interactive — click and drag to rotate, scroll to zoom
- Only Wikipedia URLs are currently supported — other sites may work but are untested
- No validation that the submitted URL is actually from Wikipedia