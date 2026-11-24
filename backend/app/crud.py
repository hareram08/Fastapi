"""Data-access functions. Routes call these; they never build queries themselves."""
from __future__ import annotations

from collections import OrderedDict

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


def get_profile(db: Session) -> models.Profile | None:
    return db.scalars(select(models.Profile).order_by(models.Profile.id)).first()


def list_skills(db: Session, category: str | None = None) -> list[models.Skill]:
    stmt = select(models.Skill).order_by(models.Skill.display_order, models.Skill.id)
    if category:
        stmt = stmt.where(models.Skill.category.ilike(category))
    return list(db.scalars(stmt))


def group_skills(skills: list[models.Skill]) -> list[dict]:
    grouped: OrderedDict[str, list[models.Skill]] = OrderedDict()
    for skill in skills:
        grouped.setdefault(skill.category, []).append(skill)
    return [{"category": cat, "skills": items} for cat, items in grouped.items()]


def list_education(db: Session) -> list[models.Education]:
    stmt = select(models.Education).order_by(models.Education.display_order, models.Education.id)
    return list(db.scalars(stmt))


def list_projects(
    db: Session,
    category: str | None = None,
    technology: str | None = None,
    featured: bool | None = None,
) -> list[models.Project]:
    stmt = select(models.Project).order_by(models.Project.display_order, models.Project.id)
    if category:
        stmt = stmt.where(models.Project.category.ilike(category))
    if featured is not None:
        stmt = stmt.where(models.Project.featured.is_(featured))
    projects = list(db.scalars(stmt))
    if technology:
        # JSON containment differs between SQLite and PostgreSQL; filter in Python for portability.
        needle = technology.lower()
        projects = [p for p in projects if any(needle == t.lower() for t in p.tech_stack or [])]
    return projects


def get_project(db: Session, project_id: int) -> models.Project | None:
    return db.get(models.Project, project_id)


def list_experience(db: Session) -> list[models.Experience]:
    stmt = select(models.Experience).order_by(models.Experience.display_order, models.Experience.id)
    return list(db.scalars(stmt))


def list_certifications(db: Session) -> list[models.Certification]:
    stmt = select(models.Certification).order_by(
        models.Certification.display_order, models.Certification.id
    )
    return list(db.scalars(stmt))


def list_journey(db: Session) -> list[models.JourneyStep]:
    stmt = select(models.JourneyStep).order_by(
        models.JourneyStep.display_order, models.JourneyStep.id
    )
    return list(db.scalars(stmt))


def create_contact_message(db: Session, payload: schemas.ContactCreate) -> models.ContactMessage:
    message = models.ContactMessage(
        name=payload.name,
        email=str(payload.email),
        subject=payload.subject,
        message=payload.message,
    )
    db.add(message)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
    db.refresh(message)
    return message
