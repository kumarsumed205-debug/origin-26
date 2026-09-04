"""Data-ready environmental dashboard components."""

from collections.abc import Mapping, Sequence
from typing import Any

import streamlit as st

from ui.theme import render_card, render_empty_state


def _safe_get(data: Any, keys: Sequence[str]) -> Any:
    """Return the first present value from a mapping without raising errors."""
    if not isinstance(data, Mapping):
        return None
    for key in keys:
        value = data.get(key)
        if value is not None:
            return value
    return None


def _format_value(value: Any, suffix: str = "") -> str:
    if value is None:
        return "--"
    return f"{value}{suffix}"


def _render_metrics(data: Any, metrics: Sequence[tuple[str, Sequence[str], str]]) -> None:
    available_metrics = []
    for label, keys, suffix in metrics:
        value = _safe_get(data, keys)
        if value is not None:
            available_metrics.append((label, _format_value(value, suffix)))

    if not available_metrics:
        render_empty_state("Waiting for weather data", "Weather details will appear here once today’s conditions are ready.")
        return

    columns = st.columns(min(len(available_metrics), 3))
    for column, (label, value) in zip(columns, available_metrics):
        with column:
            render_card(label, value)


def render_dashboard(weather: Any = None, aqi: Any = None, location: Any = None) -> None:
    """Render current environmental data without making backend assumptions."""
    st.markdown("#### Environment at a glance")
    location_label = _safe_get(location, ("name", "city", "label", "display_name"))
    if location_label is None:
        location_label = location if isinstance(location, str) else "Location pending"
    st.caption(f"📍 {location_label}")

    if weather is None and aqi is None:
        render_empty_state("Waiting for weather data", "Today’s temperature and air quality will appear here once environmental data is ready.")

    kpi_columns = st.columns(4)
    kpis = (
        ("Temperature", weather, ("temperature", "temp"), "°C"),
        ("Humidity", weather, ("humidity", "relative_humidity"), "%"),
        ("AQI", aqi, ("aqi", "air_quality_index"), ""),
        ("PM2.5", aqi, ("pm25", "pm2.5", "pm_2_5", "particulate_matter_2_5"), " µg/m³"),
    )
    for column, (label, data, keys, suffix) in zip(kpi_columns, kpis):
        with column:
            value = _safe_get(data, keys)
            note = "Waiting for live data" if value is None else "Current reading"
            render_card(label, _format_value(value), suffix, note)

    st.markdown("#### Weather summary")
    _render_metrics(
        weather,
        (
            ("Temperature", ("temperature", "temp"), "°C"),
            ("Feels Like", ("feels_like", "feels_like_temperature", "apparent_temperature"), "°C"),
            ("Humidity", ("humidity", "relative_humidity"), "%"),
            ("Wind Speed", ("wind_speed", "windspeed"), " km/h"),
            ("UV Index", ("uv_index", "uv"), ""),
            ("Rain Probability", ("rain_probability", "precipitation_probability"), "%"),
        ),
    )

    st.markdown("#### Air quality summary")
    _render_metrics(
        aqi,
        (
            ("AQI", ("aqi", "air_quality_index"), ""),
            ("PM2.5", ("pm25", "pm2.5", "pm_2_5", "particulate_matter_2_5"), " µg/m³"),
            ("PM10", ("pm10", "pm_10", "particulate_matter_10"), " µg/m³"),
            ("O3", ("o3", "ozone"), " µg/m³"),
            ("NO2", ("no2", "nitrogen_dioxide"), " µg/m³"),
        ),
    )


def render_environment_placeholder() -> None:
    """Show an empty state until live environment data is available."""
    st.info("Live weather and air-quality data will be connected in a later step.")


def render_risk_placeholder() -> None:
    """Show an empty state until Saransh's risk engine is integrated."""
    st.info("Personal health risk will appear after profile and backend integration.")
