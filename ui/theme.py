"""Shared visual system for the ClimaCare Streamlit interface."""

import streamlit as st


COLORS = {
    "navy": "#123B65",
    "teal": "#2A8C8C",
    "teal_soft": "#E7F5F3",
    "yellow": "#F4C95D",
    "ink": "#183247",
    "muted": "#607789",
    "surface": "#FFFFFF",
    "canvas": "#F5F9FB",
    "line": "#DCE8EE",
    "danger": "#C85C54",
    "success": "#3C896B",
}


def inject_styles() -> None:
    """Apply the shared health-app visual system once per Streamlit run."""
    st.markdown(
        """
        <style>
            :root {
                --clima-navy: #123B65;
                --clima-teal: #2A8C8C;
                --clima-teal-soft: #E7F5F3;
                --clima-yellow: #F4C95D;
                --clima-ink: #183247;
                --clima-muted: #607789;
                --clima-surface: #FFFFFF;
                --clima-canvas: #F5F9FB;
                --clima-line: #DCE8EE;
            }

            .stApp { background: var(--clima-canvas); color: var(--clima-ink); }
            .block-container { max-width: 1120px; padding: 2.25rem 1.25rem 4rem; }
            .clima-header { align-items: center; display: flex; justify-content: space-between; margin-bottom: 2rem; }
            .clima-brand { align-items: center; display: flex; gap: 0.7rem; }
            .clima-mark { align-items: center; background: var(--clima-navy); border-radius: 12px; color: white; display: flex; font-size: 1.15rem; font-weight: 800; height: 2.7rem; justify-content: center; width: 2.7rem; }
            .clima-brand-name { color: var(--clima-navy); font-size: 1.15rem; font-weight: 800; letter-spacing: 0.01em; }
            .clima-brand-note { color: var(--clima-muted); font-size: 0.78rem; margin-top: 0.12rem; }
            .clima-location { color: var(--clima-muted); font-size: 0.9rem; }
            .clima-greeting { color: var(--clima-navy); font-size: clamp(1.65rem, 3vw, 2.45rem); font-weight: 780; letter-spacing: 0; line-height: 1.12; margin: 0; }
            .clima-greeting-copy { color: var(--clima-muted); font-size: 1.05rem; margin: 0.55rem 0 2rem; }
            .section-heading { color: var(--clima-navy); font-size: 1.35rem; font-weight: 760; letter-spacing: 0; margin: 2rem 0 0.9rem; }
            .section-support { color: var(--clima-muted); font-size: 0.95rem; margin: -0.45rem 0 1rem; }
            .clima-card { background: var(--clima-surface); border: 1px solid var(--clima-line); border-radius: 16px; box-shadow: 0 8px 24px rgba(18, 59, 101, 0.06); padding: 1.15rem; }
            .clima-card-label { color: var(--clima-muted); font-size: 0.84rem; font-weight: 700; }
            .clima-card-value { color: var(--clima-navy); font-size: 1.7rem; font-weight: 780; margin-top: 0.45rem; }
            .clima-card-unit { color: var(--clima-muted); font-size: 0.86rem; font-weight: 600; }
            .clima-card-note { color: var(--clima-muted); font-size: 0.82rem; line-height: 1.35; margin-top: 0.4rem; }
            .clima-risk { background: var(--clima-surface); border: 1px solid var(--clima-line); border-left: 7px solid var(--clima-teal); border-radius: 16px; box-shadow: 0 10px 28px rgba(18, 59, 101, 0.08); padding: 1.4rem 1.5rem; }
            .clima-risk-label { color: var(--clima-muted); font-size: 0.82rem; font-weight: 750; letter-spacing: 0.04em; text-transform: uppercase; }
            .clima-risk-level { color: var(--clima-navy); font-size: 2.2rem; font-weight: 820; line-height: 1.1; margin: 0.4rem 0; }
            .clima-risk-copy { color: var(--clima-ink); line-height: 1.5; }
            .risk-low { border-left-color: var(--clima-success); }
            .risk-moderate { border-left-color: var(--clima-yellow); }
            .risk-high, .risk-very-high { border-left-color: var(--clima-danger); }
            .clima-empty { background: var(--clima-teal-soft); border: 1px solid #CBE9E5; border-radius: 14px; color: var(--clima-ink); padding: 1rem 1.1rem; }
            .clima-empty-title { color: var(--clima-navy); font-weight: 750; }
            .clima-advisory { background: var(--clima-surface); border: 1px solid var(--clima-line); border-radius: 16px; box-shadow: 0 8px 24px rgba(18, 59, 101, 0.05); padding: 1.3rem 1.4rem; }
            .placeholder-panel { background: var(--clima-surface); border: 1px solid var(--clima-line); border-radius: 14px; color: var(--clima-muted); padding: 1rem 1.1rem; }
            .placeholder-panel strong { color: var(--clima-ink); display: block; margin-bottom: 0.35rem; }
            .source-note { color: var(--clima-muted); font-size: 0.92rem; line-height: 1.55; }
            .stButton > button, .stSelectbox [data-baseweb="select"] { min-height: 2.8rem; }
            [data-testid="stExpander"] { background: var(--clima-surface); border: 1px solid var(--clima-line); border-radius: 14px; }
            [data-testid="stDataFrame"] { border-radius: 14px; overflow: hidden; }
            @media (max-width: 640px) {
                .block-container { padding: 1.35rem 0.9rem 3rem; }
                .clima-header { align-items: flex-start; flex-direction: column; gap: 0.75rem; }
                .clima-greeting-copy { margin-bottom: 1.35rem; }
                .clima-card, .clima-risk, .clima-advisory { border-radius: 13px; }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_card(label: str, value: str, unit: str = "", note: str = "") -> None:
    """Render a small shared metric card."""
    st.markdown(
        f"""
        <div class="clima-card">
            <div class="clima-card-label">{label}</div>
            <div class="clima-card-value">{value} <span class="clima-card-unit">{unit}</span></div>
            <div class="clima-card-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state(title: str, message: str) -> None:
    """Render an intentional, non-technical empty state."""
    st.markdown(
        f'<div class="clima-empty"><div class="clima-empty-title">{title}</div>{message}</div>',
        unsafe_allow_html=True,
    )
