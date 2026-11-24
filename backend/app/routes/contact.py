"""Contact form endpoint."""
import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/contact", tags=["Contact"])
logger = logging.getLogger(__name__)


@router.post(
    "",
    response_model=schemas.ContactResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a contact message",
    responses={422: {"description": "Validation error"}},
)
def submit_contact(payload: schemas.ContactCreate, db: Session = Depends(get_db)):
    """Validate and store a message from the portfolio contact form."""
    message = crud.create_contact_message(db, payload)
    logger.info("Contact message %s received", message.id)
    return schemas.ContactResponse(
        id=message.id,
        detail="Thank you! Your message has been received.",
        created_at=message.created_at,
    )
