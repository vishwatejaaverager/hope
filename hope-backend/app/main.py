import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import auth, payment, payout

STATIC_DIR = Path(__file__).parent / "static"
DASHBOARD_URL = os.getenv("DASHBOARD_URL", "http://localhost:3000").rstrip("/")

app = FastAPI(title="Hope Backend")

# Enable CORS for credentials and cross-origin requests from Dashboard
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://hope-9dq5.onrender.com",
]
if DASHBOARD_URL and DASHBOARD_URL not in allowed_origins:
    allowed_origins.append(DASHBOARD_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(payment.router)
app.include_router(payout.router)


@app.get("/")
def root():
    return {"status": "ok", "app": "Hope"}


@app.get("/beneficiary", include_in_schema=False)
def beneficiary_page():
    return FileResponse(STATIC_DIR / "beneficiary.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
