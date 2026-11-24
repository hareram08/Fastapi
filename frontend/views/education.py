"""Education page: academic timeline."""
from html import escape

import api_client as api
from components import card, chips, footer, load, page_header, timeline

education = load("education", api.get_education)

page_header(
    "Education",
    "A strong quantitative foundation in statistics from Patna University.",
    eyebrow="Academics",
)

items = []
for e in education:
    years = "–".join(str(y) for y in (e.get("start_year"), e.get("end_year")) if y)
    meta = " · ".join(x for x in (e["level"], years) if x)
    subtitle = " · ".join(x for x in (e.get("field_of_study"), e["institution"]) if x)
    extra = chips([e["field_of_study"]], "teal") if e.get("field_of_study") else ""
    items.append(card(e["degree"], body=e.get("description") or "", meta=meta,
                      extra_html=f'<p style="margin-top:-.2rem"><b>{escape(subtitle)}</b></p>{extra}'
                      if subtitle else extra))

timeline(items)
footer()
