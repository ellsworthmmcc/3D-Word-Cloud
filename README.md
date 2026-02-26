# 3D-Word-Cloud-Ellsworth

This project generates 3D word clouds from article URLs. 
It uses a FastAPI backend for scraping and processing text, 
and a React + Three.js frontend to render interactive 3D visualizations.

---

## Tech Stack & Libraries

### Backend
- **Python 3.12**
- **FastAPI** – API framework
- **SQLAlchemy (async)** – Database ORM
- **aiosqlite** – Async SQLite
- **BERTopic** – Topic modeling for word scoring
- **BeautifulSoup & requests** – HTML scraping

### Frontend
- **React 19**
- **TypeScript**
- **Three.js** – 3D rendering
- **@react-three/fiber & @react-three/drei** – React bindings for Three.js
- **TailwindCSS** – Styling
- **Vite** – Development server and bundler
- **Axios** – HTTP requests

---

## Setup Script Instructions
```
./setup.sh
```

---

## Manual Setup Instructions

### 1. Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Frontend
```bash
cd frontend
npm install
```

### 3. Running the Project
#### Activate backend venv and start backend
source backend/.venv/bin/activate
uvicorn backend.main:app --reload --port 8000

#### In another terminal, start frontend
cd frontend
npm run dev

Backend API is available at: http://localhost:8000/analyze
Frontend is available at: http://localhost:5173 (Vite default)

---

Notes
- Use Python 3.12 for compatibility.
- 3D cloud is interactive

Known Issues
- Scraper sometimes jumbles certain words together