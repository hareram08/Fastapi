"""Skills endpoints."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/skills", tags=["Skills"])


@router.get("", response_model=list[schemas.SkillOut], summary="List skills")
def read_skills(
    category: str | None = Query(None, description="Filter by category (case-insensitive)"),
    db: Session = Depends(get_db),
):
    return crud.list_skills(db, category=category)


@router.get(
    "/categories",
    response_model=list[schemas.SkillCategoryOut],
    summary="List skills grouped by category",
)
def read_skill_categories(db: Session = Depends(get_db)):
    return crud.group_skills(crud.list_skills(db))
