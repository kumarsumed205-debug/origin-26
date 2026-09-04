"""Presentation components for backend-provided risk and advisory data."""

from collections.abc import Mapping, Sequence
from typing import Any

import streamlit as st

from ui.theme import render_empty_state


def _risk_level(risk: Any) -> str | None:
    if not isinstance(risk, Mapping):
        return None
    level = risk.get("level")
    if level is None:
        return None
    return str(level)


def _risk_class(level: str | None) -> str:
    if level is None:
        return "pending"
    normalized_level = level.strip().upper()
    if normalized_level == "LOW":
        return "low"
    if normalized_level == "MODERATE":
        return "moderate"
    if normalized_level == "HIGH":
        return "high"
    if normalized_level == "VERY HIGH":
        return "very-high"
    return "provided"


def render_risk_card(risk: Any = None) -> None:
    """Render the backend-provided risk level without calculating or changing it."""
    level = _risk_level(risk)
    if level is None:
        render_empty_state("Preparing your health assessment", "Your personal risk will appear here once today’s environmental data is ready.")
        return

    risk_class = _risk_class(level)
    st.markdown(
        f"""
        <div class="clima-risk risk-{risk_class}">
            <div class="clima-risk-label">Your personal health risk</div>
            <div class="clima-risk-level">{level}</div>
            <div class="clima-risk-copy">
                Current conditions may present an exposure risk based on your profile.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_advisory_section(title: str, content: Any) -> None:
    if isinstance(content, Sequence) and not isinstance(content, (str, bytes)):
        for item in content:
            st.markdown(f"- {item}")
        return
    st.markdown(str(content))


def render_advisory_card(advisory: Any = None, risk: Any = None) -> None:
    """Render plain-text or structured advisory content from the backend."""
    st.subheader("Your Personalized Advisory")
    level = _risk_level(risk)
    if level is not None:
        st.caption(f"Risk status: {level}")

    if advisory is None:
        render_empty_state("Your personalized guidance will appear here", "Recommendations will be ready once today’s environmental data is available.")
        return

    if isinstance(advisory, Mapping):
        rendered_section = False
        for title, content in advisory.items():
            if content is None:
                continue
            rendered_section = True
            st.markdown(f"#### {title}")
            _render_advisory_section(str(title), content)
        if not rendered_section:
            render_empty_state("Your personalized guidance will appear here", "Recommendations will be ready once today’s environmental data is available.")
        return

    st.markdown(str(advisory))


def render_risk_explanation(risk: Any = None) -> None:
    """Render only reasons supplied by the risk engine in an expandable section."""
    with st.expander("🔍 Why am I seeing this risk?"):
        reasons = risk.get("reasons") if isinstance(risk, Mapping) else None
        if isinstance(reasons, Sequence) and not isinstance(reasons, (str, bytes)):
            if reasons:
                for reason in reasons:
                    st.markdown(f"- {reason}")
                return
        elif reasons:
            st.markdown(str(reasons))
            return
        render_empty_state("Explanation coming soon", "The reasons behind your assessment will appear here when the health assessment is ready.")
