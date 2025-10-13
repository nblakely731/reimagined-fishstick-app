from __future__ import annotations
import os
import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from version import __app_name__, __version__

MESSAGE_DEFAULT = os.getenv("APP_MESSAGE", "Automate all the things! 2")

app = FastAPI(title=__app_name__, version=__version__)

@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": __app_name__, "version": __version__}

@app.get("/api/v1/info")
def info():
    payload = {
        "message": MESSAGE_DEFAULT,
        "timestamp": int(time.time()),
    }
    return JSONResponse(payload)

@app.get("/")
def root():
    return {
        "service": __app_name__,
        "version": __version__,
        "endpoints": ["/api/v1/info", "/healthz"],
    }
