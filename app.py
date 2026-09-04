"""ClimaCare AI Streamlit entry point."""

from datetime import datetime

import streamlit as st

from database.database import get_assessment_history, init_db
from ui.advisory_card import (
    render_advisory_card,
    render_risk_card,
    render_risk_explanation,
)
from ui.charts import render_history, render_trends
from ui.dashboard import render_dashboard, render_risk_placeholder
from ui.profile import render_profile
from ui.react_dashboard import build_dashboard_payload, render_react_dashboard
from ui.theme import inject_styles


st.set_page_config(
    page_title="ClimaCare AI",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_db()


def get_current_location_placeholder() -> None:
    """Compatibility placeholder for future browser geolocation."""
    return None


def get_greeting() -> str:
    """Return a familiar greeting without depending on backend data."""
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    if hour < 18:
        return "Good afternoon"
    return "Good evening"


def render_section_heading(title: str) -> None:
    """Compatibility helper retained for the existing Streamlit UI modules."""
    st.markdown(f"### {title}")


def render_data_sources_placeholder() -> None:
    """Compatibility placeholder for the pre-React presentation layer."""
    st.info("Connected data sources will appear after backend integration.")


def render_disclaimer_placeholder() -> None:
    """Compatibility placeholder for the existing medical disclaimer."""
    st.info("ClimaCare AI provides environmental health information and does not replace professional medical advice.")


def main() -> None:
    """Render the built React presentation layer with Python-owned data."""
    history = get_assessment_history(limit=100)
    payload = build_dashboard_payload(
        profile=st.session_state.get("profile"),
        weather=None,
        aqi=None,
        location=None,
        risk=None,
        advisory=None,
        trends=history,
    )
    render_react_dashboard(payload)


if __name__ == "__main__":
    main()
