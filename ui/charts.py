"""Presentation components for local assessment history and trends."""

from collections.abc import Mapping, Sequence
from typing import Any

import pandas as pd
import streamlit as st

from ui.theme import render_empty_state


def _history_frame(history: Sequence[Mapping[str, Any]] | None) -> pd.DataFrame:
    if not history:
        return pd.DataFrame()
    frame = pd.DataFrame(history).copy()
    if "timestamp" not in frame:
        frame["timestamp"] = pd.NaT
    frame["parsed_timestamp"] = pd.to_datetime(frame["timestamp"], errors="coerce", utc=True)
    for column in ("temperature", "aqi", "pm25", "pm10"):
        if column in frame:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
        else:
            frame[column] = pd.NA
    return frame.sort_values("parsed_timestamp", na_position="last")


def render_history(history: Sequence[Mapping[str, Any]] | None = None) -> None:
    """Render recent stored assessments without accessing SQLite directly."""
    st.markdown("### Assessment History")
    if not history:
        render_empty_state("No assessment history yet", "Your saved environmental check-ins will appear here.")
        return

    frame = _history_frame(history)
    display_frame = pd.DataFrame(
        {
            "Date / Time": frame["timestamp"],
            "Location": frame.get("location"),
            "Temperature": frame["temperature"],
            "AQI": frame["aqi"],
            "PM2.5": frame["pm25"],
            "Risk Level": frame.get("risk_level"),
        }
    )
    st.dataframe(display_frame, hide_index=True, width="stretch")


def _recent_frame(history: Sequence[Mapping[str, Any]] | None) -> pd.DataFrame:
    frame = _history_frame(history)
    valid_dates = frame["parsed_timestamp"].dropna()
    if valid_dates.empty:
        return frame.iloc[0:0]
    latest_date = valid_dates.max().normalize()
    first_date = latest_date - pd.Timedelta(days=6)
    return frame[
        frame["parsed_timestamp"].between(first_date, latest_date + pd.Timedelta(days=1), inclusive="left")
    ]


def _render_line_chart(frame: pd.DataFrame, label: str, column: str) -> None:
    chart_frame = frame[["parsed_timestamp", column]].dropna(subset=["parsed_timestamp", column])
    if chart_frame.empty:
        render_empty_state(f"No {label} trend yet", "More saved assessments are needed to show this trend.")
        return
    chart_frame = chart_frame.set_index("parsed_timestamp")
    st.line_chart(chart_frame[column].rename(label), width="stretch")


def _render_risk_trend(frame: pd.DataFrame) -> None:
    risk_frame = frame[["parsed_timestamp", "risk_level"]].dropna(
        subset=["parsed_timestamp", "risk_level"]
    )
    risk_frame = risk_frame[risk_frame["risk_level"].astype(str).str.upper().isin(
        {"LOW", "MODERATE", "HIGH", "VERY HIGH"}
    )]
    if risk_frame.empty:
        render_empty_state("No risk trend yet", "More saved assessments are needed to show this trend.")
        return

    risk_order = {"LOW": 1, "MODERATE": 2, "HIGH": 3, "VERY HIGH": 4}
    risk_frame = risk_frame.copy()
    risk_frame["risk_position"] = risk_frame["risk_level"].map(
        lambda value: risk_order.get(str(value).upper())
    )
    risk_frame = risk_frame.dropna(subset=["risk_position"]).set_index("parsed_timestamp")
    st.line_chart(risk_frame["risk_position"].rename("Risk level (visual scale)"), width="stretch")
    st.caption("Visualization scale: LOW 1, MODERATE 2, HIGH 3, VERY HIGH 4.")


def render_trends(history: Sequence[Mapping[str, Any]] | None = None) -> None:
    """Render recent environmental and risk trends from supplied history."""
    st.markdown("### 7-Day Environmental Trends")
    if not history:
        render_empty_state("Your trends are getting ready", "Saved environmental assessments will build this view over time.")
        return

    frame = _recent_frame(history)
    if frame.empty:
        render_empty_state("Your trends are getting ready", "Saved environmental assessments will build this view over time.")
        return

    _render_line_chart(frame, "AQI", "aqi")
    _render_line_chart(frame, "Temperature", "temperature")
    _render_line_chart(frame, "PM2.5", "pm25")
    _render_risk_trend(frame)


def render_trends_placeholder() -> None:
    """Compatibility wrapper for callers that have not supplied history yet."""
    render_trends([])
