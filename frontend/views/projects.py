"""Projects page: filterable project cards with a details dialog (GET /api/projects/{id})."""
import streamlit as st

import api_client as api
from components import api_error, card, chips, footer, html, load, page_header

projects = load("projects", api.get_projects)

page_header(
    "Projects",
    "Hands-on work across data analysis, data engineering and cloud analytics.",
    eyebrow="Portfolio",
)

ICONS = {"Data Analysis": "📊", "Data Engineering": "🔁", "Cloud Analytics": "☁️"}


@st.dialog("Project details", width="large")
def show_project(project_id: int) -> None:
    try:
        with st.spinner("Loading project…"):
            p = api.get_project(project_id)
    except api.APIError as exc:
        api_error(exc, "project")
        return
    html(f'<div class="hr-eyebrow">{p["category"]}</div>')
    st.subheader(p["title"])
    st.write(p["description"])
    if p.get("objectives"):
        st.markdown("**What the project covers**")
        for obj in p["objectives"]:
            st.markdown(f"- {obj}")
    st.markdown("**Tech stack**")
    html(chips(p["tech_stack"]))
    links = [(label, p.get(field)) for label, field in (("Source code", "repository_url"), ("Live demo", "live_url"))]
    links = [(label, url) for label, url in links if url]
    if links:
        st.write("")
        for col, (label, url) in zip(st.columns(len(links)), links):
            col.link_button(label, url, width="stretch")


categories = sorted({p["category"] for p in projects})
technologies = sorted({t for p in projects for t in p["tech_stack"]})

f1, f2 = st.columns([1.2, 1], gap="medium")
with f1:
    chosen_cats = st.pills("Category", categories, selection_mode="multi", default=None)
with f2:
    chosen_tech = st.multiselect("Technology", technologies, placeholder="Any technology")

filtered = [
    p for p in projects
    if (not chosen_cats or p["category"] in chosen_cats)
    and (not chosen_tech or set(chosen_tech) & set(p["tech_stack"]))
]

st.caption(f"Showing {len(filtered)} of {len(projects)} projects")

if not filtered:
    html('<div class="hr-empty"><h3>No matching projects</h3><p>Try clearing a filter.</p></div>')
else:
    for row_start in range(0, len(filtered), 2):
        cols = st.columns(2, gap="medium")
        for col, p in zip(cols, filtered[row_start:row_start + 2]):
            with col:
                html(card(p["title"], p["summary"], meta=p["category"],
                          icon=ICONS.get(p["category"], "📁"), chip_items=p["tech_stack"]))
                if st.button("View details", key=f"project-{p['id']}", icon=":material/open_in_full:",
                             width="stretch"):
                    show_project(p["id"])
        st.write("")

footer()
