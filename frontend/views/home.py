"""Home page: hero, quick actions, snapshot statistics and highlights."""
from html import escape

import streamlit as st

import api_client as api
from components import card, chips, footer, grid, html, load, profile_links, resume_button, section_title, stats

profile = load("profile", api.get_profile)
projects = load("projects", api.get_projects)
categories = load("skills", api.get_skill_categories)
education = load("education", api.get_education)

hero_left, hero_right = st.columns([1.65, 1], gap="large", vertical_alignment="center")

with hero_left:
    html(
        f"""<div class="hr-hero hr-fade">
        <div class="hr-eyebrow">Data Analytics · Statistics</div>
        <h1>Hi, I'm <span class="hr-gradient">{escape(profile["full_name"])}</span></h1>
        <div class="hr-headline">{escape(profile["headline"])}</div>
        <div class="hr-lead">{escape(profile["summary"])}</div>
        </div>"""
    )
    st.write("")
    c1, c2 = st.columns([1, 2])
    with c1:
        resume_button("home-resume")
    with c2:
        profile_links(profile, key_prefix="home-")

with hero_right:
    top_degree = education[0] if education else None
    degree_line = (
        f'{top_degree["degree"]} — {top_degree["field_of_study"]}' if top_degree and top_degree.get("field_of_study")
        else (top_degree["degree"] if top_degree else "")
    )
    core_stack = [s["name"] for g in categories for s in g["skills"]][:8]
    html(
        card(
            "Snapshot",
            meta="At a glance",
            icon="📊",
            bullets=[b for b in (degree_line, top_degree["institution"] if top_degree else "",
                                 "Career focus: Data Analytics") if b],
            chip_items=core_stack,
        )
    )

skill_count = sum(len(g["skills"]) for g in categories)
stats(
    [
        (str(len(projects)), "Portfolio projects"),
        (str(skill_count), "Core skills"),
        (str(len(categories)), "Skill areas"),
        (str(len(education)), "Education milestones"),
    ]
)

section_title("Featured projects", "🚀")
featured = [p for p in projects if p.get("featured")] or projects
grid(
    [card(p["title"], p["summary"], meta=p["category"], chip_items=p["tech_stack"][:4]) for p in featured[:4]],
    min_width=250,
)
st.write("")
st.page_link("views/projects.py", label="Explore all projects", icon=":material/arrow_forward:")

section_title("Skill areas", "🧭")
grid(
    [
        card(g["category"], chip_items=[s["name"] for s in g["skills"]], accent=False)
        for g in categories
    ],
    min_width=230,
)

st.write("")
html(
    '<div class="hr-callout hr-fade"><b>Open to Data Analyst opportunities.</b> '
    "Have a role, project or question in mind? I'd be glad to hear from you.</div>"
)
st.write("")
st.page_link("views/contact.py", label="Get in touch", icon=":material/mail:")
footer()
