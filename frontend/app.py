"""Hare Ram — Resume & Portfolio (Streamlit frontend).

Run from frontend/:  streamlit run app.py
All content is fetched from the FastAPI backend (see api_client.py).
"""
from pathlib import Path

import streamlit as st

ASSETS = Path(__file__).parent / "assets"

st.set_page_config(
    page_title="Hare Ram · Data Analytics Portfolio",
    page_icon=str(ASSETS / "icon.svg"),
    layout="wide",
    initial_sidebar_state="auto",
)

import api_client as api  # noqa: E402  (after set_page_config)
from components import api_status, inject_css  # noqa: E402

st.session_state.setdefault("dark_mode", True)

pages = {
    "Portfolio": [
        st.Page("views/home.py", title="Home", icon=":material/home:", default=True),
        st.Page("views/about.py", title="About Me", icon=":material/person:"),
        st.Page("views/skills.py", title="Skills", icon=":material/insights:"),
        st.Page("views/projects.py", title="Projects", icon=":material/folder_open:"),
        st.Page("views/education.py", title="Education", icon=":material/school:"),
        st.Page("views/learning.py", title="Learning Journey", icon=":material/route:"),
        st.Page("views/certifications.py", title="Certifications", icon=":material/workspace_premium:"),
    ],
    "Connect": [
        st.Page("views/contact.py", title="Contact", icon=":material/mail:"),
    ],
}

navigation = st.navigation(pages, position="sidebar")
st.logo(str(ASSETS / "logo.svg"), size="large", icon_image=str(ASSETS / "icon.svg"))

with st.sidebar:
    st.toggle("Dark mode", key="dark_mode")
    api_status()
    st.caption(f"API: {api.API_BASE_URL}")

inject_css()
navigation.run()
