"""Project endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/projects", tags=["Projects"])


@router.get("", response_model=list[schemas.ProjectSummaryOut], summary="List projects")
def read_projects(
    category: str | None = Query(None, description="Filter by category, e.g. 'Data Analysis'"),
    technology: str | None = Query(None, description="Filter by technology, e.g. 'Python'"),
    featured: bool | None = Query(None, description="Only featured / non-featured projects"),
    db: Session = Depends(get_db),
):
    return crud.list_projects(db, category=category, technology=technology, featured=featured)


@router.get(
    "/{project_id}",
    response_model=schemas.ProjectOut,
    summary="Get a project by ID",
    responses={404: {"model": schemas.ErrorResponse}},
)
def read_project(
    project_id: int = Path(..., ge=1, description="Numeric project ID"),
    db: Session = Depends(get_db),
):
    project = crud.get_project(db, project_id)
    if project is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Project {project_id} not found.")
    return project
