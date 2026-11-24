"""Reusable UI building blocks shared by every page."""
from __future__ import annotations

from collections.abc import Callable, Iterable
from html import escape
from typing import Any

import streamlit as st

import api_client as api
from styles import THEMES, build_css


# ---------- Theme ----------
def is_dark() -> bool:
    return bool(st.session_state.get("dark_mode", True))


def inject_css() -> None:
    st.markdown(build_css(is_dark()), unsafe_allow_html=True)


def html(markup: str) -> None:
    # Strip indentation so Markdown never mistakes indented HTML for a code block.
    flat = "\n".join(line.strip() for line in markup.splitlines() if line.strip())
    st.markdown(flat, unsafe_allow_html=True)


def plotly_layout(**overrides: Any) -> dict:
    t = THEMES["dark" if is_dark() else "light"]
    layout = {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"family": "Inter, sans-serif", "color": t["text"], "size": 13},
        "margin": {"l": 10, "r": 10, "t": 10, "b": 10},
    }
    layout.update(overrides)
    return layout


def theme_colors() -> dict:
    return THEMES["dark" if is_dark() else "light"]


# ---------- Data loading ----------
def load(label: str, fetcher: Callable[..., Any], *args: Any) -> Any:
    """Fetch data with a loading spinner; on failure render an error card and stop the page."""
    try:
        with st.spinner(f"Loading {label}…"):
            return fetcher(*args)
    except api.APIError as exc:
        api_error(exc, label)
        st.stop()


def api_error(exc: api.APIError, label: str = "data") -> None:
    if exc.is_connection_error:
        html(
            f"""<div class="hr-error hr-fade">
              <h3>Backend unavailable</h3>
              <p>{escape(exc.message)} The portfolio {escape(label)} could not be loaded.</p>
              <p>Start the API from the <code>backend/</code> folder:
              <code>uvicorn app.main:app --reload --port 8000</code></p>
            </div>"""
        )
    else:
        html(
            f"""<div class="hr-error hr-fade">
              <h3>Could not load {escape(label)}</h3>
              <p>{escape(exc.message)} (HTTP {exc.status_code})</p>
            </div>"""
        )
    st.write("")
    if st.button("Retry", icon=":material/refresh:", type="primary", key=f"retry-{label}"):
        api.clear_cache()
        st.rerun()


# ---------- Layout primitives ----------
def page_header(title: str, subtitle: str = "", eyebrow: str = "") -> None:
    eyebrow_html = f'<div class="hr-eyebrow">{escape(eyebrow)}</div>' if eyebrow else ""
    sub_html = f"<p>{escape(subtitle)}</p>" if subtitle else ""
    html(f'<div class="hr-page-header hr-fade">{eyebrow_html}<h1>{escape(title)}</h1>{sub_html}</div>')


def section_title(text: str, icon: str = "") -> None:
    html(f'<div class="hr-section-title">{escape(icon)} {escape(text)}</div>')


def chips(items: Iterable[str], variant: str = "") -> str:
    cls = f"hr-chip {variant}".strip()
    return '<div class="hr-chips">' + "".join(
        f'<span class="{cls}">{escape(str(i))}</span>' for i in items
    ) + "</div>"


def card(
    title: str,
    body: str = "",
    meta: str = "",
    icon: str = "",
    chip_items: Iterable[str] | None = None,
    chip_variant: str = "",
    bullets: Iterable[str] | None = None,
    accent: bool = True,
    extra_html: str = "",
) -> str:
    """Return card HTML. Text is escaped; extra_html is trusted markup built by callers."""
    parts = [f'<div class="hr-card {"accent-top" if accent else ""} hr-fade">']
    if icon:
        parts.append(f'<div class="hr-icon">{escape(icon)}</div>')
    if meta:
        parts.append(f'<div class="hr-meta">{escape(meta)}</div>')
    parts.append(f"<h3>{escape(title)}</h3>")
    if body:
        parts.append(f"<p>{escape(body)}</p>")
    if bullets:
        parts.append("<ul>" + "".join(f"<li>{escape(b)}</li>" for b in bullets) + "</ul>")
    if chip_items:
        parts.append(chips(chip_items, chip_variant))
    parts.append(extra_html)
    parts.append("</div>")
    return "".join(parts)


def grid(cards_html: Iterable[str], min_width: int = 260) -> None:
    html(f'<div class="hr-grid" style="--min:{min_width}px">' + "".join(cards_html) + "</div>")


def stats(items: Iterable[tuple[str, str]]) -> None:
    html(
        '<div class="hr-stats hr-fade">'
        + "".join(
            f'<div class="hr-stat"><div class="v">{escape(v)}</div><div class="l">{escape(l)}</div></div>'
            for v, l in items
        )
        + "</div>"
    )


def timeline(items: Iterable[str]) -> None:
    """items: inner card HTML for each step."""
    blocks = "".join(
        f'<div class="hr-tl-item"><div class="hr-tl-dot">{i}</div>{body}</div>'
        for i, body in enumerate(items, start=1)
    )
    html(f'<div class="hr-timeline">{blocks}</div>')


def empty_state(icon: str, title: str, text: str) -> None:
    html(
        f'<div class="hr-empty hr-fade"><div class="e-icon">{escape(icon)}</div>'
        f"<h3>{escape(title)}</h3><p>{escape(text)}</p></div>"
    )


def callout(text: str, label: str = "") -> None:
    prefix = f"<b>{escape(label)}</b> " if label else ""
    html(f'<div class="hr-callout hr-fade">{prefix}{escape(text)}</div>')


def footer() -> None:
    html(
        '<div class="hr-footer">Hare Ram · Data Analytics Portfolio · '
        "Built with Streamlit & FastAPI</div>"
    )


# ---------- Actions ----------
def profile_links(profile: dict, key_prefix: str = "") -> None:
    """LinkedIn / GitHub buttons; disabled with a hint if a link is not configured."""
    cols = st.columns(2)
    for col, (label, field, icon) in zip(
        cols,
        (("LinkedIn", "linkedin_url", ":material/work:"), ("GitHub", "github_url", ":material/code:")),
    ):
        url = profile.get(field)
        with col:
            if url:
                st.link_button(label, url, icon=icon, width="stretch")
            else:
                st.button(
                    label, icon=icon, disabled=True, width="stretch",
                    key=f"{key_prefix}{field}",
                    help=f"{label} link not configured yet (set PORTFOLIO_{field.upper()} in .env)",
                )


def resume_button(key: str = "resume") -> None:
    try:
        resume = api.get_resume()
    except api.APIError as exc:
        st.button("Download Resume", icon=":material/download:", disabled=True,
                  width="stretch", key=key, help=exc.message)
        return
    st.download_button(
        "Download Resume", data=resume["data"], file_name=resume["filename"], mime=resume["mime"],
        icon=":material/download:", type="primary", width="stretch", key=key,
    )


def api_status() -> None:
    ok = api.check_health()
    html(
        f'<div class="hr-status"><span class="hr-dot {"ok" if ok else "down"}"></span>'
        f'{"API connected" if ok else "API offline"}</div>'
    )
