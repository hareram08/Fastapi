"""HTTP client for the portfolio FastAPI backend.

The frontend never touches the database: every piece of portfolio content is
fetched here via REST. GET responses are cached briefly; failures raise
APIError, which pages turn into friendly messages (exceptions are never cached).
"""
from __future__ import annotations

import os
import re
from typing import Any

import requests
import streamlit as st

API_BASE_URL = os.getenv("PORTFOLIO_API_URL", "http://127.0.0.1:8000").rstrip("/")
TIMEOUT_SECONDS = float(os.getenv("PORTFOLIO_API_TIMEOUT", "8"))
CACHE_TTL_SECONDS = int(os.getenv("PORTFOLIO_CACHE_TTL", "120"))


class APIError(Exception):
    """Raised when the backend is unreachable or returns an error response."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        errors: list[dict] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.errors = errors or []

    @property
    def is_connection_error(self) -> bool:
        return self.status_code is None


def _request(method: str, path: str, **kwargs: Any) -> requests.Response:
    url = f"{API_BASE_URL}{path}"
    try:
        response = requests.request(method, url, timeout=TIMEOUT_SECONDS, **kwargs)
    except requests.exceptions.ConnectionError as exc:
        raise APIError(f"Cannot reach the portfolio API at {API_BASE_URL}.") from exc
    except requests.exceptions.Timeout as exc:
        raise APIError(f"The portfolio API did not respond within {TIMEOUT_SECONDS:g}s.") from exc
    except requests.exceptions.RequestException as exc:
        raise APIError(f"Request to the portfolio API failed: {exc}") from exc

    if response.status_code >= 400:
        try:
            body = response.json()
        except ValueError:
            body = {}
        detail = body.get("detail") if isinstance(body, dict) else None
        raise APIError(
            detail if isinstance(detail, str) else f"API returned HTTP {response.status_code}.",
            status_code=response.status_code,
            errors=body.get("errors") if isinstance(body, dict) else None,
        )
    return response


def _get_json(path: str, params: dict | None = None) -> Any:
    try:
        return _request("GET", path, params=params).json()
    except ValueError as exc:
        raise APIError("The portfolio API returned an invalid response.") from exc


# ---------- Cached read endpoints ----------
@st.cache_data(ttl=CACHE_TTL_SECONDS, show_spinner=False)
def get_profile() -> dict:
    return _get_json("/api/profile")


@st.cache_data(ttl=CACHE_TTL_SECONDS, show_spinner=False)
def get_skills() -> list[dict]:
    return _get_json("/api/skills")


@st.cache_data(ttl=CACHE_TTL_SECONDS, show_spinner=False)
def get_skill_categories() -> list[dict]:
    return _get_json("/api/skills/categories")


@st.cache_data(ttl=CACHE_TTL_SECONDS, show_spinner=False)
def get_education() -> list[dict]:
    return _get_json("/api/education")


@st.cache_data(ttl=CACHE_TTL_SECONDS, show_spinner=False)
def get_projects() -> list[dict]:
    return _get_json("/api/projects")


@st.cache_data(ttl=CACHE_TTL_SECONDS, show_spinner=False)
def get_project(project_id: int) -> dict:
    return _get_json(f"/api/projects/{int(project_id)}")


@st.cache_data(ttl=CACHE_TTL_SECONDS, show_spinner=False)
def get_experience() -> list[dict]:
    return _get_json("/api/experience")


@st.cache_data(ttl=CACHE_TTL_SECONDS, show_spinner=False)
def get_certifications() -> list[dict]:
    return _get_json("/api/certifications")


@st.cache_data(ttl=CACHE_TTL_SECONDS, show_spinner=False)
def get_journey() -> list[dict]:
    return _get_json("/api/journey")


@st.cache_data(ttl=CACHE_TTL_SECONDS, show_spinner=False)
def get_resume() -> dict:
    """Returns {'data': bytes, 'mime': str, 'filename': str}."""
    response = _request("GET", "/api/resume")
    mime = response.headers.get("content-type", "application/octet-stream").split(";")[0]
    match = re.search(r'filename="?([^";]+)"?', response.headers.get("content-disposition", ""))
    default = "Hare_Ram_Resume.pdf" if mime == "application/pdf" else "Hare_Ram_Resume.html"
    return {"data": response.content, "mime": mime, "filename": match.group(1) if match else default}


@st.cache_data(ttl=15, show_spinner=False)
def check_health() -> bool:
    try:
        return _request("GET", "/health").json().get("status") == "ok"
    except (APIError, ValueError):
        return False


# ---------- Write endpoints (never cached) ----------
def submit_contact(name: str, email: str, message: str, subject: str | None = None) -> dict:
    payload = {"name": name, "email": email, "message": message, "subject": subject or None}
    return _request("POST", "/api/contact", json=payload).json()


def clear_cache() -> None:
    st.cache_data.clear()
