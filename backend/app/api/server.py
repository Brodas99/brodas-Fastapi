import json
from enum import Enum
from dataclasses import dataclass, field

from app.core import config, tasks  

from fastapi import FastAPI, HTTPException, Response
from starlette.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router

def get_application():
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix="/api")
    return app
app = get_application()