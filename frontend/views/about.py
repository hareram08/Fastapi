"""About page: academic background, statistics knowledge and career objective."""
import streamlit as st

import api_client as api
from components import callout, card, chips, footer, grid, html, load, page_header, section_title

profile = load("profile", api.get_profile)
education = load("education", api.get_education)
experience = load("experience", api.get_experience)

page_header(
    "About Me",
    "A statistician by training, building a career in data analytics.",
    eyebrow="Background",
)

left, right = st.columns([1.35, 1], gap="large")
with left:
    section_title("Academic background", "🎓")
    html(card("Statistics at Patna University", profile["academic_background"], icon="🎓"))
with right:
    section_title("Qualifications", "📜")
    grid(
        [
            card(
                e["degree"],
                meta=e["level"],
                body=" · ".join(x for x in (e.get("field_of_study"), e["institution"]) if x),
                accent=False,
            )
            for e in education
        ],
        min_width=220,
    )

section_title("Statistics knowledge", "📈")
html(card("How I think about data", profile["statistics_overview"], icon="🧮",
          chip_items=profile.get("statistics_topics", []), chip_variant="teal"))

section_title("Career objective", "🎯")
callout(profile["career_objective"], label="Objective —")

# Experience is shown only when real entries exist in the backend.
if experience:
    section_title("Experience", "💼")
    grid(
        [
            card(
                x["role"],
                x["description"],
                meta=" · ".join(v for v in (x["organization"], x.get("start_date"), x.get("end_date")) if v),
                bullets=x.get("highlights"),
            )
            for x in experience
        ],
        min_width=320,
    )

footer()
