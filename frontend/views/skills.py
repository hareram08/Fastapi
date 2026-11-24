"""Skills page: category sections, filter and a category map chart."""
import plotly.graph_objects as go
import streamlit as st

import api_client as api
from components import card, footer, grid, load, page_header, plotly_layout, section_title, theme_colors

categories = load("skills", api.get_skill_categories)

page_header(
    "Skills",
    "The toolkit I use to collect, analyse and communicate data — grouped by area.",
    eyebrow="Toolkit",
)

ICONS = {
    "Programming & Data": "🐍",
    "Analytics & BI": "📊",
    "Statistics & Analysis": "📐",
    "Backend & Cloud": "☁️",
}

names = [g["category"] for g in categories]
selected = st.pills("Filter by area", names, selection_mode="multi", default=None,
                    label_visibility="collapsed")
visible = [g for g in categories if not selected or g["category"] in selected]

chart_col, list_col = st.columns([1, 1.6], gap="large")

with chart_col:
    t = theme_colors()
    labels, parents, colors = ["Skills"], [""], [t["surface_2"]]
    palette = [t["accent"], t["accent_2"], "#f59e0b", "#ec4899", "#38bdf8"]
    for i, g in enumerate(visible):
        labels.append(g["category"]); parents.append("Skills"); colors.append(palette[i % len(palette)])
        for s in g["skills"]:
            labels.append(s["name"]); parents.append(g["category"]); colors.append(palette[i % len(palette)])
    fig = go.Figure(
        go.Sunburst(
            labels=labels, parents=parents, marker={"colors": colors, "line": {"color": t["bg"], "width": 2}},
            insidetextorientation="radial", hovertemplate="<b>%{label}</b><extra></extra>",
        )
    )
    fig.update_layout(**plotly_layout(height=420))
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    st.caption("Click a segment to zoom. The map shows how skills group together — not proficiency levels.")

with list_col:
    for g in visible:
        section_title(g["category"], ICONS.get(g["category"], "•"))
        grid(
            [card(s["name"], s["description"], chip_items=s.get("tools", []), chip_variant="outline")
             for s in g["skills"]],
            min_width=240,
        )

footer()
