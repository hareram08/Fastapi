"""Endpoint tests for the portfolio API."""


def test_root_lists_endpoints(client):
    res = client.get("/")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "ok"
    assert "/api/profile" in body["endpoints"]
    assert "/api/projects/{project_id}" in body["endpoints"]


def test_health(client):
    assert client.get("/health").json() == {"status": "ok", "database": "connected"}


def test_profile(client):
    res = client.get("/api/profile")
    assert res.status_code == 200
    data = res.json()
    assert data["full_name"] == "Hare Ram"
    assert "Statistics" in data["academic_background"]
    assert data["statistics_topics"]


def test_skills_and_categories(client):
    skills = client.get("/api/skills").json()
    names = {s["name"] for s in skills}
    for expected in ["Python", "SQL", "Excel", "Power BI", "Statistics",
                     "Pandas & NumPy", "FastAPI", "AWS Fundamentals"]:
        assert expected in names
    groups = client.get("/api/skills/categories").json()
    assert sum(len(g["skills"]) for g in groups) == len(skills)
    filtered = client.get("/api/skills", params={"category": "backend & cloud"}).json()
    assert {s["name"] for s in filtered} == {"FastAPI", "AWS Fundamentals"}


def test_education(client):
    edu = client.get("/api/education").json()
    assert [e["institution"] for e in edu] == [
        "Patna University", "Patna University", "Rajkiye Kshtriya High School"]
    assert edu[0]["field_of_study"] == "Statistics"


def test_projects_list_and_filters(client):
    projects = client.get("/api/projects").json()
    assert len(projects) == 4
    assert "description" not in projects[0]  # summary model only
    aws = client.get("/api/projects", params={"technology": "aws lambda"}).json()
    assert [p["title"] for p in aws] == ["AWS S3 → Lambda → RDS Pipeline"]
    analysis = client.get("/api/projects", params={"category": "Data Analysis"}).json()
    assert len(analysis) == 2


def test_project_detail(client):
    first_id = client.get("/api/projects").json()[0]["id"]
    res = client.get(f"/api/projects/{first_id}")
    assert res.status_code == 200
    assert res.json()["objectives"]


def test_project_not_found_and_invalid_id(client):
    res = client.get("/api/projects/9999")
    assert res.status_code == 404
    assert "not found" in res.json()["detail"]
    assert client.get("/api/projects/0").status_code == 422
    assert client.get("/api/projects/abc").status_code == 422


def test_experience_and_certifications_start_empty(client):
    # No employment or certifications are invented; they appear once real data is added.
    assert client.get("/api/experience").json() == []
    assert client.get("/api/certifications").json() == []


def test_journey(client):
    steps = client.get("/api/journey").json()
    assert [s["title"] for s in steps][1] == "Government Examination Preparation"


def test_contact_success(client):
    payload = {"name": "  Test User ", "email": "test@example.com",
               "message": "Hello, I would like to connect about a role."}
    res = client.post("/api/contact", json=payload)
    assert res.status_code == 201
    body = res.json()
    assert body["status"] == "received" and body["id"] >= 1


def test_contact_validation(client):
    res = client.post("/api/contact", json={"name": "A", "email": "bad", "message": "short"})
    assert res.status_code == 422
    fields = {e["field"] for e in res.json()["errors"]}
    assert fields == {"name", "email", "message"}


def test_resume_html_fallback(client, monkeypatch, tmp_path):
    from app.config import get_settings
    monkeypatch.setattr(get_settings(), "resume_path", tmp_path / "missing.pdf")
    res = client.get("/api/resume")
    assert res.status_code == 200
    assert res.headers["content-type"].startswith("text/html")
    assert "Hare Ram" in res.text and "Patna University" in res.text


def test_resume_pdf_served_when_present(client, monkeypatch, tmp_path):
    from app.config import get_settings
    pdf = tmp_path / "resume.pdf"
    pdf.write_bytes(b"%PDF-1.4 test")
    monkeypatch.setattr(get_settings(), "resume_path", pdf)
    res = client.get("/api/resume")
    assert res.status_code == 200
    assert res.headers["content-type"] == "application/pdf"
    assert res.content == b"%PDF-1.4 test"
