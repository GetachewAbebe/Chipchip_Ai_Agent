from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
import os

router = APIRouter()

@router.get("/logs", response_class=PlainTextResponse)
def read_logs(limit: int = 100):
    log_path = "logs/app.log"

    if not os.path.exists(log_path):
        raise HTTPException(status_code=404, detail="Log file not found")

    with open(log_path, "r") as f:
        lines = f.readlines()

    return "".join(lines[-limit:]) or "Log file is empty."
