"""Experience endpoints. Returns an empty list until real experience is added."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/experience", tags=["Experience"])


@router.get("", response_model=list[schemas.ExperienceOut], summary="List work experience")
def read_experience(db: Session = Depends(get_db)):
    return crud.list_experience(db)
