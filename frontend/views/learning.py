"""Learning Journey page: from statistics to data analytics."""
import api_client as api
from components import callout, card, footer, load, page_header, timeline

steps = load("learning journey", api.get_journey)

page_header(
    "Learning Journey",
    "How a statistics background, disciplined exam preparation and curiosity led me into data analytics.",
    eyebrow="Growth",
)

timeline(
    card(s["title"], s["description"], meta=s["phase"], chip_items=s.get("focus_areas", []))
    for s in steps
)
callout(
    "Every project in this portfolio is part of that journey — including this site itself, "
    "built as a Streamlit frontend talking to a FastAPI backend.",
    label="Still learning —",
)
footer()
