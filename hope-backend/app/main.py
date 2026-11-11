import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import auth, case, email, payment, payout

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
    "https://hope-frontend-a15f.onrender.com",
]
if DASHBOARD_URL and DASHBOARD_URL not in allowed_origins:
    allowed_origins.append(DASHBOARD_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"^https:\/\/[\w-]+\.onrender\.com$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(payment.router)
app.include_router(payout.router)
app.include_router(email.router)
app.include_router(case.router)


@app.on_event("startup")
def _start_background_services() -> None:
    # Render starts this app directly with Uvicorn. Migrate its actual runtime
    # database before accepting requests, with bounded connection/query timeouts.
    if os.getenv("RENDER") or os.getenv("AUTO_MIGRATE") == "1":
        from app.db import engine
        from app.migrations import upgrade_database

        upgrade_database(engine)

    from app.services import imap_service, payout_reconciliation

    imap_service.start_poller()
    payout_reconciliation.start_poller()


@app.get("/")
def root():
    return {"status": "ok", "app": "Hope"}


@app.get("/beneficiary", include_in_schema=False)
def beneficiary_page():
    return FileResponse(STATIC_DIR / "beneficiary.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 10000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)

