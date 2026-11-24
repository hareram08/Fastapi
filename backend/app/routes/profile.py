"""Profile and learning-journey endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..config import get_settings
from ..database import get_db

router = APIRouter(prefix="/api", tags=["Profile"])


def build_profile(db: Session) -> schemas.ProfileOut:
    profile = crud.get_profile(db)
    if profile is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Profile has not been configured yet.")
    data = schemas.ProfileOut.model_validate(profile)
    settings = get_settings()
    # Environment variables take precedence so links can change without reseeding.
    overrides = {
        "linkedin_url": settings.linkedin_url,
        "github_url": settings.github_url,
        "email": settings.contact_email,
    }
    return data.model_copy(update={k: v for k, v in overrides.items() if v})


@router.get(
    "/profile",
    response_model=schemas.ProfileOut,
    summary="Get profile",
    responses={404: {"model": schemas.ErrorResponse}},
)
def read_profile(db: Session = Depends(get_db)):
    """Name, headline, summary, academic background, statistics focus and career objective."""
    return build_profile(db)


@router.get("/journey", response_model=list[schemas.JourneyStepOut], summary="Get learning journey")
def read_journey(db: Session = Depends(get_db)):
    """Ordered milestones of the learning journey."""
    return crud.list_journey(db)
