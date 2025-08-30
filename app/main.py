from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .routes import router as api_router
from .ws_routes import router as ws_router

app = FastAPI(title="FastAPI Contacts Demo (Vite)")

# CORS (dev with Vite at 5173 by default)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API & WS
app.include_router(api_router)
app.include_router(ws_router)

# Production: serve built frontend if exists (frontend/dist)
dist_dir = Path(__file__).parent.parent / "frontend" / "dist"
if dist_dir.exists():
    app.mount("/", StaticFiles(directory=dist_dir, html=True), name="frontend")
#    app.mount("/app", StaticFiles(directory=dist_dir, html=True), name="frontend")
