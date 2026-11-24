"""Certification endpoints. Returns an empty list until verified certifications are added."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/certifications", tags=["Certifications"])


@router.get("", response_model=list[schemas.CertificationOut], summary="List certifications")
def read_certifications(db: Session = Depends(get_db)):
    return crud.list_certifications(db)
