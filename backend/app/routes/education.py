"""Education endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/education", tags=["Education"])


@router.get("", response_model=list[schemas.EducationOut], summary="List education history")
def read_education(db: Session = Depends(get_db)):
    return crud.list_education(db)
