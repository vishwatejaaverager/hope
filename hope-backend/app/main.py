from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import payment, payout

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="Hope Backend")
app.include_router(payment.router)
app.include_router(payout.router)


@app.get("/")
def root():
    return {"status": "ok", "app": "Hope"}


@app.get("/donate", include_in_schema=False)
def donate_page():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/beneficiary", include_in_schema=False)
def beneficiary_page():
    return FileResponse(STATIC_DIR / "beneficiary.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
