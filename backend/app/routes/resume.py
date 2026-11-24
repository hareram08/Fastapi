"""Resume download.

Serves the PDF at RESUME_PATH (default: app/static/resume.pdf) when present.
Otherwise generates a printable HTML resume from the same database content,
so the download always reflects real portfolio data.
"""
from html import escape

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.orm import Session

from .. import crud
from ..config import get_settings
from ..database import get_db
from .profile import build_profile

router = APIRouter(prefix="/api", tags=["Resume"])

_CSS = """
body{font-family:Georgia,'Times New Roman',serif;color:#1f2933;max-width:820px;margin:40px auto;padding:0 24px;line-height:1.55}
h1{font-size:30px;margin:0}h2{font-size:15px;letter-spacing:.12em;text-transform:uppercase;color:#4338ca;
border-bottom:1px solid #d9dce3;padding-bottom:4px;margin-top:28px}.headline{color:#52606d;margin:4px 0 8px}
.links a{color:#4338ca;margin-right:14px}ul{padding-left:18px}.item{margin-bottom:10px}.muted{color:#616e7c}
@media print{body{margin:0}}
"""


def _li(items) -> str:
    return "".join(f"<li>{escape(i)}</li>" for i in items)


def render_resume_html(db: Session) -> str:
    p = build_profile(db)
    links = " ".join(
        f'<a href="{escape(url)}">{label}</a>'
        for label, url in (("LinkedIn", p.linkedin_url), ("GitHub", p.github_url))
        if url
    )
    if p.email:
        links += f' <a href="mailto:{escape(p.email)}">{escape(p.email)}</a>'

    skills = "".join(
        f"<li><b>{escape(g['category'])}:</b> {escape(', '.join(s.name for s in g['skills']))}</li>"
        for g in crud.group_skills(crud.list_skills(db))
    )
    education = "".join(
        f'<div class="item"><b>{escape(e.degree)}'
        f'{" — " + escape(e.field_of_study) if e.field_of_study else ""}</b><br>'
        f'<span class="muted">{escape(e.institution)}</span></div>'
        for e in crud.list_education(db)
    )
    projects = "".join(
        f'<div class="item"><b>{escape(pr.title)}</b> '
        f'<span class="muted">({escape(", ".join(pr.tech_stack))})</span><br>{escape(pr.summary)}</div>'
        for pr in crud.list_projects(db)
    )
    experience = "".join(
        f'<div class="item"><b>{escape(x.role)}</b>, {escape(x.organization)}<br>{escape(x.description)}</div>'
        for x in crud.list_experience(db)
    )
    certs = _li(f"{c.title} — {c.issuer}" for c in crud.list_certifications(db))

    sections = [
        ("Profile", f"<p>{escape(p.summary)}</p>"),
        ("Career Objective", f"<p>{escape(p.career_objective)}</p>"),
        ("Skills", f"<ul>{skills}</ul>"),
        ("Education", education),
        ("Projects", projects),
    ]
    if experience:
        sections.append(("Experience", experience))
    if certs:
        sections.append(("Certifications", f"<ul>{certs}</ul>"))

    body = "".join(f"<h2>{title}</h2>{content}" for title, content in sections)
    return (
        f"<!doctype html><html><head><meta charset='utf-8'><title>{escape(p.full_name)} — Resume</title>"
        f"<style>{_CSS}</style></head><body><h1>{escape(p.full_name)}</h1>"
        f"<p class='headline'>{escape(p.headline)}</p><div class='links'>{links}</div>{body}</body></html>"
    )


@router.get(
    "/resume",
    summary="Download resume",
    response_class=HTMLResponse,
    responses={200: {"content": {"application/pdf": {}, "text/html": {}}}},
)
def download_resume(db: Session = Depends(get_db)):
    """Returns the uploaded PDF resume if available, otherwise a generated HTML resume."""
    path = get_settings().resume_path
    if path.is_file():
        return FileResponse(path, media_type="application/pdf", filename="Hare_Ram_Resume.pdf")
    return HTMLResponse(
        render_resume_html(db),
        headers={"Content-Disposition": 'attachment; filename="Hare_Ram_Resume.html"'},
    )
