"""Seed the database from data/portfolio.json.

Usage (from backend/):
    python -m app.seed           # seed only if the database is empty
    python -m app.seed --reset   # replace portfolio content with the JSON file
Contact messages are never deleted by a reset.
"""
from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from . import models
from .database import SessionLocal, init_db

logger = logging.getLogger(__name__)
DATA_FILE = Path(__file__).resolve().parent / "data" / "portfolio.json"

# JSON section -> ORM model (order matters only for readability).
SECTIONS: dict[str, type] = {
    "skills": models.Skill,
    "education": models.Education,
    "projects": models.Project,
    "experience": models.Experience,
    "certifications": models.Certification,
    "learning_journey": models.JourneyStep,
}


def load_data(path: Path = DATA_FILE) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def seed_database(db: Session, reset: bool = False, data: dict | None = None) -> bool:
    """Populate portfolio tables. Returns True if data was written."""
    if not reset and db.scalars(select(models.Profile)).first() is not None:
        return False

    data = data or load_data()
    if reset:
        for model in [models.Profile, *SECTIONS.values()]:
            db.execute(delete(model))

    db.add(models.Profile(**data["profile"]))
    for key, model in SECTIONS.items():
        for order, item in enumerate(data.get(key, [])):
            db.add(model(display_order=order, **item))
    db.commit()
    logger.info("Portfolio data seeded from %s", DATA_FILE.name)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed portfolio database")
    parser.add_argument("--reset", action="store_true", help="replace existing portfolio content")
    args = parser.parse_args()
    init_db()
    with SessionLocal() as db:
        written = seed_database(db, reset=args.reset)
    print("Database seeded." if written else "Database already contains data (use --reset).")


if __name__ == "__main__":
    main()
