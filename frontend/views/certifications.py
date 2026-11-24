"""Certifications page: cards rendered dynamically from GET /api/certifications."""
from html import escape

import streamlit as st

import api_client as api
from components import card, empty_state, footer, grid, load, page_header

certifications = load("certifications", api.get_certifications)

page_header(
    "Certifications",
    "Verified credentials and completed courses.",
    eyebrow="Credentials",
)

if not certifications:
    empty_state(
        "🏅",
        "No certifications listed yet",
        "Verified certifications will appear here as they are earned. "
        "In the meantime, see the Learning Journey for what I'm currently studying.",
    )
    st.write("")
    st.page_link("views/learning.py", label="View Learning Journey", icon=":material/route:")
else:
    cards = []
    for c in certifications:
        meta = " · ".join(x for x in (c["issuer"], c.get("issue_date")) if x)
        extra = ""
        if c.get("credential_id"):
            extra += f'<p style="font-size:.85rem">Credential ID: {escape(c["credential_id"])}</p>'
        if c.get("credential_url"):
            extra += (f'<p><a href="{escape(c["credential_url"])}" target="_blank" '
                      f'rel="noopener">Verify credential ↗</a></p>')
        cards.append(card(c["title"], meta=meta, icon="🏅", chip_items=c.get("skills", []), extra_html=extra))
    grid(cards, min_width=280)

footer()
