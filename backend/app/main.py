"""FastAPI application entry point.

Run from backend/:  uvicorn app.main:app --reload --port 8000
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from . import schemas
from .config import get_settings
from .database import SessionLocal, get_db, init_db
from .routes import certifications, contact, education, experience, profile, projects, resume, skills
from .seed import seed_database

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("portfolio")
settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    if settings.seed_on_startup:
        with SessionLocal() as db:
            if seed_database(db):
                logger.info("Seeded empty database with portfolio content.")
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "REST API powering Hare Ram's resume & portfolio. "
        "All portfolio content displayed by the Streamlit frontend is served from here."
    ),
    lifespan=lifespan,
    contact={"name": "Hare Ram"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# ---------- Exception handlers ----------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    errors = [
        {
            "field": ".".join(str(p) for p in err.get("loc", [])[1:]) or "body",
            "message": err.get("msg", "Invalid value"),
        }
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": "Validation failed.", "errors": errors}),
    )


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(_: Request, exc: SQLAlchemyError):
    logger.exception("Database error: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "The database is temporarily unavailable. Please try again later."},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception):
    logger.exception("Unhandled error: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred."},
    )


# ---------- Routers ----------
for router_module in (profile, skills, education, projects, experience, certifications, contact, resume):
    app.include_router(router_module.router)


@app.get("/", response_model=schemas.APIInfo, tags=["Meta"], summary="API information")
def root():
    return schemas.APIInfo(
        name=settings.app_name,
        version=settings.app_version,
        status="ok",
        docs_url="/docs",
        # Derived from the OpenAPI schema so it works however routers are mounted.
        endpoints=sorted(p for p in app.openapi()["paths"] if p.startswith("/api")),
    )


@app.get("/health", response_model=schemas.HealthOut, tags=["Meta"], summary="Health check")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return schemas.HealthOut(status="ok", database="connected")
