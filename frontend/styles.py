"""Theme tokens and global CSS. Both themes share one stylesheet driven by CSS variables."""

THEMES = {
    "dark": {
        "bg": "#0a0f1e",
        "bg_glow_1": "rgba(124, 140, 255, 0.16)",
        "bg_glow_2": "rgba(45, 212, 191, 0.10)",
        "surface": "#111831",
        "surface_2": "#18213f",
        "border": "rgba(148, 163, 209, 0.16)",
        "text": "#e7eaf6",
        "muted": "#9aa3c2",
        "accent": "#8b97ff",
        "accent_2": "#2dd4bf",
        "accent_soft": "rgba(139, 151, 255, 0.14)",
        "accent_2_soft": "rgba(45, 212, 191, 0.13)",
        "shadow": "0 10px 30px rgba(0, 0, 0, 0.35)",
        "input_bg": "#0e1530",
    },
    "light": {
        "bg": "#f5f7fc",
        "bg_glow_1": "rgba(79, 70, 229, 0.08)",
        "bg_glow_2": "rgba(13, 148, 136, 0.07)",
        "surface": "#ffffff",
        "surface_2": "#eef1fb",
        "border": "#e0e4f0",
        "text": "#141a33",
        "muted": "#5a6382",
        "accent": "#4f46e5",
        "accent_2": "#0d9488",
        "accent_soft": "rgba(79, 70, 229, 0.09)",
        "accent_2_soft": "rgba(13, 148, 136, 0.10)",
        "shadow": "0 10px 28px rgba(20, 26, 51, 0.08)",
        "input_bg": "#ffffff",
    },
}


def build_css(dark: bool) -> str:
    t = THEMES["dark" if dark else "light"]
    variables = "\n".join(f"  --{k.replace('_', '-')}: {v};" for k, v in t.items())
    return f"""
<style>
:root {{
{variables}
  --radius: 16px;
  --heading-font: "Space Grotesk", "Inter", system-ui, sans-serif;
}}

/* ---------- App shell ---------- */
.stApp, [data-testid="stAppViewContainer"] {{
  background:
    radial-gradient(900px 500px at 85% -10%, var(--bg-glow-1), transparent 60%),
    radial-gradient(700px 420px at -10% 30%, var(--bg-glow-2), transparent 60%),
    var(--bg) !important;
  color: var(--text);
}}
[data-testid="stHeader"] {{ background: transparent !important; }}
[data-testid="stAppDeployButton"], #MainMenu, footer {{ display: none !important; }}
.block-container {{ padding-top: 2.4rem; padding-bottom: 3rem; max-width: 1180px; }}
.stApp p, .stApp li, .stApp label, .stApp span, .stApp div {{ color: inherit; }}
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {{ color: var(--text) !important; font-family: var(--heading-font); }}
[data-testid="stMarkdownContainer"] p {{ color: var(--text); }}
[data-testid="stCaptionContainer"], .stCaption {{ color: var(--muted) !important; }}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {{
  background: var(--surface) !important;
  border-right: 1px solid var(--border);
}}
[data-testid="stSidebar"] * {{ color: var(--text); }}
[data-testid="stSidebarNav"] a {{ border-radius: 10px; margin: 2px 0; transition: background .2s ease; }}
[data-testid="stSidebarNav"] a:hover {{ background: var(--accent-soft) !important; }}
[data-testid="stSidebarNav"] a[aria-current="page"] {{ background: var(--accent-soft) !important; }}
[data-testid="stSidebarNav"] a[aria-current="page"] span {{ color: var(--accent) !important; font-weight: 600; }}
[data-testid="stNavSectionHeader"] {{ color: var(--muted) !important; letter-spacing: .08em; }}

/* ---------- Widgets ---------- */
.stButton button, .stDownloadButton button, .stFormSubmitButton button, .stLinkButton a {{
  border-radius: 12px !important;
  border: 1px solid var(--border) !important;
  background: var(--surface) !important;
  color: var(--text) !important;
  font-weight: 600 !important;
  transition: transform .15s ease, box-shadow .2s ease, border-color .2s ease !important;
}}
.stButton button:hover, .stDownloadButton button:hover, .stFormSubmitButton button:hover, .stLinkButton a:hover {{
  transform: translateY(-1px);
  border-color: var(--accent) !important;
  box-shadow: 0 6px 18px var(--accent-soft);
}}
.stButton button[kind="primary"], .stDownloadButton button[kind="primary"],
.stFormSubmitButton button[kind="primaryFormSubmit"], .stFormSubmitButton button[kind="primary"],
.stLinkButton a[kind="primary"] {{
  background: linear-gradient(135deg, var(--accent), var(--accent-2)) !important;
  border: none !important;
  color: #fff !important;
}}
.stButton button[kind="primary"] *, .stDownloadButton button[kind="primary"] *,
.stFormSubmitButton button *, .stLinkButton a[kind="primary"] * {{ color: #fff !important; }}
.stButton button:disabled, .stLinkButton a[disabled] {{ opacity: .45; transform: none; }}

[data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] > div, [data-baseweb="base-input"] {{
  background: var(--input-bg) !important;
  border-color: var(--border) !important;
  border-radius: 12px !important;
}}
[data-baseweb="input"] input, [data-baseweb="textarea"] textarea {{
  color: var(--text) !important;
  -webkit-text-fill-color: var(--text) !important;
  caret-color: var(--accent);
}}
[data-baseweb="input"] input, [data-baseweb="textarea"] textarea,
[data-baseweb="input"] > div, [data-baseweb="textarea"] > div {{ background: transparent !important; }}
[data-baseweb="select"] * {{ color: var(--text); }}
[data-baseweb="select"] svg {{ fill: var(--muted); }}
[data-baseweb="input"]:focus-within, [data-baseweb="textarea"]:focus-within {{ border-color: var(--accent) !important; }}
/* Streamlit >= 1.5x widget roots (no baseweb attributes) */
[data-testid="stTextInputRootElement"], [data-testid="stTextAreaRootElement"],
[data-testid="stMultiSelect"] div:has(> [data-testid="stMultiSelectTagsContainer"]),
[data-testid="stSelectbox"] div:has(> div > input) {{
  background: var(--input-bg) !important;
  border-color: var(--border) !important;
  border-radius: 12px !important;
}}
[data-testid="stTextInputRootElement"]:focus-within, [data-testid="stTextAreaRootElement"]:focus-within {{
  border-color: var(--accent) !important;
}}
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea,
[data-testid="stMultiSelect"] input, [data-testid="stMultiSelect"] div, [data-testid="stSelectbox"] div {{
  color: var(--text) !important; -webkit-text-fill-color: var(--text);
}}
[data-testid="stTextInput"] input::placeholder, [data-testid="stTextArea"] textarea::placeholder {{
  color: var(--muted) !important; -webkit-text-fill-color: var(--muted); opacity: 1;
}}
[data-testid="stMultiSelect"] svg {{ fill: var(--muted) !important; color: var(--muted) !important; }}
/* Dialogs render in a portal outside .stApp, so theme their text explicitly */
[role="dialog"] h1, [role="dialog"] h2, [role="dialog"] h3,
[role="dialog"] [data-testid="stMarkdownContainer"] p,
[role="dialog"] [data-testid="stMarkdownContainer"] li,
[role="dialog"] [data-testid="stMarkdownContainer"] strong {{ color: var(--text) !important; }}
[role="dialog"] button[aria-label="Close"] svg {{ color: var(--muted) !important; fill: var(--muted) !important; }}
.hr-eyebrow {{ color: var(--accent) !important; }}
/* Toggle track visibility in both themes */
[data-testid="stCheckbox"] label > div:first-child, .stToggle label > div:first-child {{ box-shadow: inset 0 0 0 1px var(--border); }}
[data-testid="stWidgetLabel"] p {{ color: var(--text) !important; font-weight: 500; }}
[data-testid="stForm"] {{
  background: var(--surface);
  border: 1px solid var(--border) !important;
  border-radius: var(--radius);
  padding: 1.6rem;
  box-shadow: var(--shadow);
}}
[data-baseweb="tag"] {{ background: var(--accent-soft) !important; }}
[data-baseweb="tag"] span {{ color: var(--accent) !important; }}
[data-baseweb="popover"] ul, [data-baseweb="menu"] {{ background: var(--surface) !important; }}
[data-baseweb="popover"] li {{ color: var(--text) !important; }}
[data-testid="stButtonGroup"] button[data-variant="pills"], [data-testid="stBaseButton-pills"] {{
  border-radius: 999px !important; border: 1px solid var(--border) !important;
  background: var(--surface) !important; color: var(--text) !important;
}}
[data-testid="stButtonGroup"] button[data-variant="pills"] * {{ color: var(--text) !important; }}
[data-testid="stButtonGroup"] button[aria-pressed="true"], [data-testid="stBaseButton-pillsActive"] {{
  background: var(--accent-soft) !important; border-color: var(--accent) !important;
}}
[data-testid="stButtonGroup"] button[aria-pressed="true"] * {{ color: var(--accent) !important; }}
[role="dialog"] {{ background: var(--surface) !important; color: var(--text) !important; border-radius: 20px !important; }}
[data-testid="stExpander"] details {{ background: var(--surface); border-color: var(--border) !important; border-radius: 14px; }}
[data-testid="stAlert"] {{ border-radius: 14px; }}
[data-testid="stAlert"] > div {{ background: var(--surface-2) !important; border: 1px solid var(--border); border-radius: 14px; }}
[data-testid="stAlert"] p, [data-testid="stAlert"] li {{ color: var(--text) !important; }}
[data-testid="stAlertContentSuccess"] svg, [data-testid="stAlertContentSuccess"] [data-testid="stIconMaterial"] {{ color: #22c55e !important; }}
[data-testid="stAlertContentError"] svg, [data-testid="stAlertContentError"] [data-testid="stIconMaterial"] {{ color: #ef4444 !important; }}
[data-testid="stToast"] {{ background: var(--surface) !important; border: 1px solid var(--border); box-shadow: var(--shadow); }}
[data-testid="stToast"] p, [data-testid="stToast"] div {{ color: var(--text) !important; }}
[data-testid="stSpinner"] {{ color: var(--muted); }}
hr {{ border-color: var(--border) !important; }}

/* ---------- Custom components ---------- */
.hr-eyebrow {{
  display: inline-flex; align-items: center; gap: .5rem;
  font-size: .78rem; font-weight: 600; letter-spacing: .14em; text-transform: uppercase;
  color: var(--accent); background: var(--accent-soft);
  padding: .38rem .8rem; border-radius: 999px; margin-bottom: 1rem;
}}
.hr-eyebrow::before {{ content: ""; width: 7px; height: 7px; border-radius: 50%; background: var(--accent-2); }}
.hr-hero h1 {{
  font-family: var(--heading-font); font-weight: 700; line-height: 1.02;
  font-size: clamp(2.6rem, 6vw, 4.4rem); margin: 0 0 .6rem 0; letter-spacing: -0.02em;
}}
.hr-gradient {{
  background: linear-gradient(120deg, var(--accent), var(--accent-2));
  -webkit-background-clip: text; background-clip: text; color: transparent !important;
  -webkit-text-fill-color: transparent;
}}
.hr-headline {{ font-size: clamp(1.05rem, 2vw, 1.3rem); color: var(--muted) !important; font-weight: 500; margin-bottom: 1rem; }}
.hr-lead {{ font-size: 1.05rem; line-height: 1.75; color: var(--text); max-width: 760px; }}

.hr-page-header {{ margin-bottom: 1.8rem; }}
.hr-page-header h1 {{
  font-family: var(--heading-font); font-size: clamp(2rem, 4.5vw, 2.9rem);
  margin: 0 0 .4rem 0; letter-spacing: -0.015em; padding: 0;
}}
.hr-page-header p {{ color: var(--muted) !important; font-size: 1.05rem; max-width: 720px; margin: 0; }}

.hr-section-title {{
  font-family: var(--heading-font); font-size: 1.35rem; font-weight: 600; color: var(--text);
  margin: 2.2rem 0 1rem 0; display: flex; align-items: center; gap: .6rem;
}}
.hr-section-title::after {{ content: ""; flex: 1; height: 1px; background: var(--border); margin-left: .6rem; }}

.hr-grid {{ display: grid; gap: 1.1rem; grid-template-columns: repeat(auto-fill, minmax(var(--min, 260px), 1fr)); }}
.hr-card {{
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 1.35rem 1.4rem; box-shadow: var(--shadow); height: 100%;
  transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease;
  position: relative; overflow: hidden;
}}
.hr-card:hover {{ transform: translateY(-3px); border-color: var(--accent); }}
.hr-card.accent-top::before {{
  content: ""; position: absolute; inset: 0 0 auto 0; height: 3px;
  background: linear-gradient(90deg, var(--accent), var(--accent-2));
}}
.hr-card h3 {{ font-family: var(--heading-font); font-size: 1.18rem; margin: .2rem 0 .45rem 0; padding: 0; color: var(--text); }}
.hr-card p {{ color: var(--muted) !important; line-height: 1.65; margin: 0 0 .8rem 0; font-size: .97rem; }}
.hr-card .hr-meta {{ font-size: .78rem; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; color: var(--accent-2) !important; }}
.hr-card ul {{ margin: .2rem 0 .8rem 1.1rem; padding: 0; color: var(--muted); }}
.hr-card li {{ margin-bottom: .3rem; color: var(--muted); }}
.hr-icon {{
  width: 42px; height: 42px; border-radius: 12px; display: grid; place-items: center;
  background: var(--accent-soft); color: var(--accent); font-size: 1.25rem; margin-bottom: .8rem;
}}

.hr-chips {{ display: flex; flex-wrap: wrap; gap: .4rem; }}
.hr-chip {{
  font-size: .8rem; font-weight: 500; padding: .28rem .7rem; border-radius: 999px;
  background: var(--accent-soft); color: var(--accent) !important; border: 1px solid transparent; white-space: nowrap;
}}
.hr-chip.teal {{ background: var(--accent-2-soft); color: var(--accent-2) !important; }}
.hr-chip.outline {{ background: transparent; border-color: var(--border); color: var(--muted) !important; }}

.hr-stats {{ display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); margin: 1.8rem 0 .6rem 0; }}
.hr-stat {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.1rem 1.2rem; }}
.hr-stat .v {{ font-family: var(--heading-font); font-size: 1.9rem; font-weight: 700; color: var(--text); line-height: 1.1; }}
.hr-stat .l {{ font-size: .85rem; color: var(--muted) !important; margin-top: .2rem; }}

.hr-callout {{
  border-radius: var(--radius); padding: 1.5rem 1.6rem;
  background: linear-gradient(135deg, var(--accent-soft), var(--accent-2-soft));
  border: 1px solid var(--border); color: var(--text); line-height: 1.75; font-size: 1.04rem;
}}
.hr-callout b {{ color: var(--accent); }}

.hr-timeline {{ position: relative; margin-left: .6rem; padding-left: 2rem; border-left: 2px solid var(--border); }}
.hr-tl-item {{ position: relative; margin-bottom: 1.3rem; }}
.hr-tl-dot {{
  position: absolute; left: calc(-2rem - 13px); top: 1.25rem; width: 24px; height: 24px; border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), var(--accent-2)); color: #fff !important;
  font-size: .75rem; font-weight: 700; display: grid; place-items: center; box-shadow: 0 0 0 5px var(--bg);
}}

.hr-empty {{
  text-align: center; padding: 3rem 1.5rem; border: 1px dashed var(--border); border-radius: var(--radius);
  background: var(--surface);
}}
.hr-empty .e-icon {{ font-size: 2.2rem; margin-bottom: .6rem; }}
.hr-empty h3 {{ font-family: var(--heading-font); margin: 0 0 .4rem 0; color: var(--text); }}
.hr-empty p {{ color: var(--muted) !important; max-width: 520px; margin: 0 auto; }}

.hr-error {{
  border-radius: var(--radius); padding: 1.6rem; border: 1px solid rgba(248, 113, 113, .45);
  background: rgba(248, 113, 113, .08);
}}
.hr-error h3 {{ margin: 0 0 .4rem 0; color: #f87171 !important; font-family: var(--heading-font); }}
.hr-error p {{ color: var(--text) !important; margin: .2rem 0; }}
.hr-error code {{ background: var(--surface-2); color: var(--text); padding: .1rem .4rem; border-radius: 6px; }}

.hr-status {{ display: flex; align-items: center; gap: .5rem; font-size: .85rem; color: var(--muted) !important; }}
.hr-dot {{ width: 9px; height: 9px; border-radius: 50%; }}
.hr-dot.ok {{ background: #22c55e; box-shadow: 0 0 0 4px rgba(34,197,94,.18); }}
.hr-dot.down {{ background: #ef4444; box-shadow: 0 0 0 4px rgba(239,68,68,.18); }}
.hr-footer {{ margin-top: 3.5rem; padding-top: 1.2rem; border-top: 1px solid var(--border); color: var(--muted) !important; font-size: .85rem; text-align: center; }}

.hr-fade {{ animation: hrFade .45s ease both; }}
@keyframes hrFade {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}

@media (max-width: 640px) {{
  .block-container {{ padding-left: 1rem; padding-right: 1rem; padding-top: 3.4rem; }}
  .hr-card {{ padding: 1.1rem; }}
  .hr-timeline {{ padding-left: 1.5rem; }}
  .hr-tl-dot {{ left: calc(-1.5rem - 13px); }}
}}
</style>
"""
