# Hare Ram — Resume & Portfolio

A full-stack resume and portfolio app with a **Streamlit** frontend and a **FastAPI** backend. The frontend has no data of its own: every name, skill, project and education entry is fetched from the REST API, which reads it from a database through SQLAlchemy.

```
Streamlit (views/*.py) ──► api_client.py ──HTTP/JSON──► FastAPI routes ──► crud.py ──► SQLAlchemy ──► SQLite / PostgreSQL
```

## Architecture

| Layer | Location | Responsibility |
|---|---|---|
| UI pages | `frontend/views/` | One file per page. Each one only renders data. |
| UI components | `frontend/components.py`, `styles.py` | Reusable cards, grids, timeline, chips, error and empty states, dark/light theme CSS |
| API client | `frontend/api_client.py` | Wraps `requests`, caches GETs (TTL), raises `APIError` on failure |
| Routes | `backend/app/routes/` | HTTP concerns: status codes, query params, Swagger metadata |
| Schemas | `backend/app/schemas.py` | Pydantic request validation and response shapes |
| Data access | `backend/app/crud.py` | All database queries |
| Models | `backend/app/models.py` | SQLAlchemy tables. Only portable types are used, so it runs on SQLite and PostgreSQL. |
| Content | `backend/app/data/portfolio.json` | **The single file to edit** for portfolio content. It is seeded into the DB. |

The two apps are independent. They share no code, and the frontend never imports backend modules or opens the database.

## Project structure

```
hareram-portfolio/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app, CORS, exception handlers, / and /health
│   │   ├── config.py          # settings from environment variables
│   │   ├── database.py        # engine, session, Base
│   │   ├── models.py          # SQLAlchemy models
│   │   ├── schemas.py         # Pydantic schemas
│   │   ├── crud.py            # data access functions
│   │   ├── seed.py            # loads data/portfolio.json into the DB
│   │   ├── data/portfolio.json
│   │   ├── static/            # put resume.pdf here (optional)
│   │   └── routes/            # profile, skills, education, projects, experience,
│   │                          # certifications, contact, resume
│   ├── tests/                 # pytest suite (isolated in-memory DB)
│   └── requirements.txt
├── frontend/
│   ├── app.py                 # page config, sidebar navigation, theme toggle
│   ├── api_client.py          # all HTTP calls to FastAPI
│   ├── components.py          # reusable UI components
│   ├── styles.py              # theme tokens + CSS
│   ├── views/                 # home, about, skills, projects, education,
│   │                          # learning, certifications, contact
│   ├── assets/                # logo / icon
│   ├── .streamlit/config.toml
│   └── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

> **Why `views/` and not `pages/`?** Streamlit auto-discovers a folder named `pages/` as legacy multipage pages. With `st.navigation`, that causes a bug: opening a deep link such as `/projects` on a freshly started server skips `app.py`, so the theme, logo and navigation are missing. Naming the folder `views/` avoids this.

## Setup

Requires Python 3.10 or newer. A virtual environment is recommended.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
cp .env.example .env             # then fill in your LinkedIn / GitHub URLs
```

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

On first start, the database is created and filled from `app/data/portfolio.json`.

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### 2. Frontend (in a second terminal)

```bash
cd frontend
pip install -r requirements.txt   # streamlit, requests, plotly
streamlit run app.py
```

Open http://localhost:8501.

If the backend runs somewhere else, set `PORTFOLIO_API_URL` before starting Streamlit, for example `export PORTFOLIO_API_URL=https://api.example.com`.

### 3. Run the tests

```bash
cd backend
pytest -q
```

## API reference

| Method | Endpoint | Description | Status codes |
|---|---|---|---|
| GET | `/` | API info and endpoint list | 200 |
| GET | `/health` | Liveness and DB check | 200, 503 |
| GET | `/api/profile` | Name, headline, summary, academic background, statistics focus, career objective | 200, 404 |
| GET | `/api/skills` | Skills. Optional filter `?category=` | 200 |
| GET | `/api/skills/categories` | Skills grouped by category | 200 |
| GET | `/api/education` | Education history | 200 |
| GET | `/api/projects` | Project summaries. Optional filters `?category=`, `?technology=`, `?featured=` | 200 |
| GET | `/api/projects/{project_id}` | Full project details | 200, 404, 422 |
| GET | `/api/experience` | Work experience (empty until real entries are added) | 200 |
| GET | `/api/certifications` | Certifications (empty until verified entries are added) | 200 |
| GET | `/api/journey` | Learning-journey milestones | 200 |
| GET | `/api/resume` | `static/resume.pdf` if present, otherwise an HTML resume generated from the DB | 200 |
| POST | `/api/contact` | Saves a contact message | 201, 422, 503 |

Example contact request:

```bash
curl -X POST http://127.0.0.1:8000/api/contact \
  -H "Content-Type: application/json" \
  -d '{"name":"Priya Sharma","email":"priya@example.com","message":"Hello, I would like to connect."}'
```

Validation errors return a consistent shape:

```json
{"detail": "Validation failed.", "errors": [{"field": "email", "message": "value is not a valid email address"}]}
```

## Editing your content

1. Edit `backend/app/data/portfolio.json`.
2. Reload it into the database:
   ```bash
   cd backend
   python -m app.seed --reset
   ```
   Contact messages are kept.
3. Refresh the site. Streamlit caches API responses for 120 seconds; restart Streamlit to see changes immediately.

**Links:** set `PORTFOLIO_LINKEDIN_URL`, `PORTFOLIO_GITHUB_URL` and `PORTFOLIO_EMAIL` in `.env`. They override the JSON values without reseeding. Until they are set, the LinkedIn and GitHub buttons appear disabled with a hint.

**Resume:** drop a PDF at `backend/app/static/resume.pdf` and the Download Resume button serves it. Until then, it downloads a printable HTML resume built from the same API data.

**Certifications and experience** are intentionally empty. Add entries to the `certifications` and `experience` arrays in the JSON and reseed; the cards appear automatically. Example certification:

```json
{"title": "…", "issuer": "…", "issue_date": "2025-06", "credential_id": null,
 "credential_url": "https://…", "skills": ["SQL"]}
```

> Content rule: only add facts that are true and verifiable. Leave unknown dates as `null`; the UI hides missing fields.

## Viewing contact messages

Messages are stored in the `contact_messages` table. They are not emailed. With the default SQLite database:

```bash
cd backend
python -c "import sqlite3; [print(r) for r in sqlite3.connect('portfolio.db').execute('select created_at, name, email, message from contact_messages order by id desc')]"
```

## Production notes (PostgreSQL)

- Set `DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DBNAME` in your host's secret store, never in code. The legacy `postgres://` scheme is accepted too. `psycopg2-binary` is already in `requirements.txt`.
- Tables are created automatically on startup. For schema changes over time, consider adding Alembic migrations.
- Set `CORS_ORIGINS` to your deployed frontend URL and `PORTFOLIO_API_URL` on the frontend to your deployed API URL.
- Run the API with several workers, for example `uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2`.
- The contact endpoint has no rate limiting or CAPTCHA. Add one (a reverse proxy rule or middleware) before heavy public exposure.

## Features

- Eight pages with sidebar navigation: Home, About Me, Skills, Projects, Education, Learning Journey, Certifications, Contact
- Dark and light themes (sidebar toggle), custom typography (Inter and Space Grotesk), card and timeline components, hover animations
- Responsive layout: grids reflow, columns stack on phones, and the sidebar collapses automatically on small screens
- Interactive Plotly skill map. It shows how skills are grouped, **not** proficiency scores, so no levels are made up.
- Project filters (category and technology) and a details dialog backed by `GET /api/projects/{id}`
- Loading spinners, cached responses, a live API status light, and a friendly "backend unavailable" card with Retry
- Contact form with client-side validation, server-side Pydantic validation, and per-field error messages
