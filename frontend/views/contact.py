"""Contact page: form submitted to POST /api/contact."""
import re

import streamlit as st

import api_client as api
from components import card, footer, grid, html, page_header, load

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
FIELDS = ("contact_name", "contact_email", "contact_subject", "contact_message")

profile = load("profile", api.get_profile)

page_header(
    "Contact",
    "Have an opportunity, a project or a question? Send a message and I will get back to you.",
    eyebrow="Let's talk",
)


def validate(name: str, email: str, message: str) -> list[str]:
    errors = []
    if len(name.strip()) < 2:
        errors.append("Please enter your name (at least 2 characters).")
    if not EMAIL_RE.match(email.strip()):
        errors.append("Please enter a valid email address.")
    if len(message.strip()) < 10:
        errors.append("Your message should be at least 10 characters long.")
    return errors


def handle_submit() -> None:
    """Runs before the rerun, so it may safely clear the form fields on success."""
    s = st.session_state
    name, email = s.contact_name, s.contact_email
    subject, message = s.contact_subject, s.contact_message
    errors = validate(name, email, message)
    if errors:
        s.contact_result = ("error", errors)
        return
    try:
        result = api.submit_contact(name.strip(), email.strip(), message.strip(), subject.strip() or None)
    except api.APIError as exc:
        details = [f"{e['field']}: {e['message']}" for e in exc.errors] or [exc.message]
        s.contact_result = ("error", details)
        return
    s.contact_result = ("success", [result.get("detail", "Message sent.")])
    for key in FIELDS:
        s[key] = ""


form_col, info_col = st.columns([1.6, 1], gap="large")

with form_col:
    with st.form("contact-form", border=False):
        c1, c2 = st.columns(2)
        c1.text_input("Name", key="contact_name", placeholder="Your full name", max_chars=100)
        c2.text_input("Email", key="contact_email", placeholder="you@example.com", max_chars=255)
        st.text_input("Subject (optional)", key="contact_subject", placeholder="What's this about?",
                      max_chars=150)
        st.text_area("Message", key="contact_message", height=170, max_chars=5000,
                     placeholder="Write your message…")
        st.form_submit_button("Send message", type="primary", icon=":material/send:",
                              on_click=handle_submit, width="stretch")

    result = st.session_state.pop("contact_result", None)
    if result:
        kind, messages = result
        if kind == "success":
            st.success(messages[0], icon=":material/check_circle:")
            st.toast("Message sent!", icon="✅")
        else:
            st.error("\n".join(f"- {m}" for m in messages), icon=":material/error:")

with info_col:
    cards = [card("Response", "Messages are saved by the portfolio API and read personally.",
                  icon="✉️", accent=False)]
    links = [(label, profile.get(field)) for label, field in
             (("LinkedIn", "linkedin_url"), ("GitHub", "github_url"))]
    if profile.get("email"):
        links.insert(0, ("Email", f"mailto:{profile['email']}"))
    grid(cards, min_width=220)
    available = [(label, url) for label, url in links if url]
    if available:
        st.write("")
        st.markdown("**Other ways to connect**")
        for label, url in available:
            st.link_button(label, url, width="stretch")

footer()
