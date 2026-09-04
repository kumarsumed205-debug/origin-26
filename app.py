"""ClimaCare AI Streamlit entry point."""

from datetime import datetime
import json
from collections.abc import Mapping

import streamlit as st

from database.database import get_assessment_history, init_db, save_assessment
from services.backend_adapter import BackendUnavailableError, get_current_assessment
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
    st.session_state.setdefault("profile", {})
    st.session_state.setdefault("location", None)
    st.session_state.setdefault("weather", None)
    st.session_state.setdefault("aqi", None)
    st.session_state.setdefault("risk", None)
    st.session_state.setdefault("advisory", None)
    st.session_state.setdefault("assessment_status", "waiting")

    profile = render_profile()
    try:
        assessment = get_current_assessment(profile)
    except BackendUnavailableError:
        assessment = None
        st.session_state["assessment_status"] = "backend_unavailable"

    if isinstance(assessment, Mapping):
        st.session_state.update(assessment)
        required_values = (
            st.session_state.get("location"),
            st.session_state.get("weather"),
            st.session_state.get("aqi"),
            st.session_state.get("risk"),
            st.session_state.get("advisory"),
        )
        if all(value is not None for value in required_values):
            fingerprint = json.dumps(
                {"profile": profile, "assessment": assessment},
                sort_keys=True,
                default=str,
            )
            if fingerprint != st.session_state.get("last_saved_assessment"):
                save_assessment(
                    location=st.session_state["location"],
                    profile=profile,
                    weather=st.session_state["weather"],
                    aqi=st.session_state["aqi"],
                    risk=st.session_state["risk"],
                    advisory=st.session_state["advisory"],
                )
                st.session_state["last_saved_assessment"] = fingerprint
    elif assessment is not None:
        st.session_state["assessment_status"] = "invalid_backend_response"

    history = get_assessment_history(limit=100)
    payload = build_dashboard_payload(
        profile=profile,
        weather=st.session_state.get("weather"),
        aqi=st.session_state.get("aqi"),
        location=st.session_state.get("location"),
        risk=st.session_state.get("risk"),
        advisory=st.session_state.get("advisory"),
        trends=history,
        status=st.session_state.get("assessment_status"),
    )
    render_react_dashboard(payload)


if __name__ == "__main__":
    main()
