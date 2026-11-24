"""Pydantic schemas for request validation and response serialization."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ---------- Read models ----------
class ProfileOut(ORMModel):
    id: int
    full_name: str
    headline: str
    summary: str
    location: str | None = None
    email: str | None = None
    linkedin_url: str | None = None
    github_url: str | None = None
    academic_background: str
    statistics_overview: str
    statistics_topics: list[str] = []
    career_objective: str


class SkillOut(ORMModel):
    id: int
    name: str
    category: str
    description: str
    tools: list[str] = []


class SkillCategoryOut(BaseModel):
    category: str
    skills: list[SkillOut]


class EducationOut(ORMModel):
    id: int
    degree: str
    field_of_study: str | None = None
    institution: str
    level: str
    description: str | None = None
    start_year: int | None = None
    end_year: int | None = None


class ProjectSummaryOut(ORMModel):
    id: int
    title: str
    category: str
    summary: str
    tech_stack: list[str] = []
    featured: bool = False


class ProjectOut(ProjectSummaryOut):
    description: str
    objectives: list[str] = []
    repository_url: str | None = None
    live_url: str | None = None


class ExperienceOut(ORMModel):
    id: int
    role: str
    organization: str
    location: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    description: str
    highlights: list[str] = []


class CertificationOut(ORMModel):
    id: int
    title: str
    issuer: str
    issue_date: str | None = None
    credential_id: str | None = None
    credential_url: str | None = None
    skills: list[str] = []


class JourneyStepOut(ORMModel):
    id: int
    phase: str
    title: str
    description: str
    focus_areas: list[str] = []


# ---------- Contact ----------
class ContactCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, examples=["Priya Sharma"])
    email: EmailStr = Field(..., examples=["priya@example.com"])
    subject: str | None = Field(None, max_length=150, examples=["Data Analyst opportunity"])
    message: str = Field(
        ..., min_length=10, max_length=5000, examples=["Hi Hare Ram, I'd like to discuss a role."]
    )

    @field_validator("name", "message", mode="before")
    @classmethod
    def strip_required(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value

    @field_validator("subject", mode="before")
    @classmethod
    def strip_optional(cls, value: object) -> object:
        if isinstance(value, str):
            value = value.strip()
            return value or None
        return value


class ContactResponse(BaseModel):
    id: int
    status: str = "received"
    detail: str
    created_at: datetime


# ---------- Misc ----------
class APIInfo(BaseModel):
    name: str
    version: str
    status: str
    docs_url: str
    endpoints: list[str]


class HealthOut(BaseModel):
    status: str
    database: str


class ErrorResponse(BaseModel):
    detail: str
