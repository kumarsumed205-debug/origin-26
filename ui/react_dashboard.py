"""Embed the built React dashboard inside the Streamlit application."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import streamlit as st


DIST_DIR = Path(__file__).resolve().parent.parent / "react_dashboard" / "dist"


def _json_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_json_value(item) for item in value]
    return value


def build_dashboard_payload(
    profile: Mapping[str, Any] | None = None,
    weather: Mapping[str, Any] | None = None,
    aqi: Mapping[str, Any] | None = None,
    location: Any = None,
    risk: Mapping[str, Any] | None = None,
    advisory: Any = None,
    forecast: Sequence[Mapping[str, Any]] | None = None,
    trends: Sequence[Mapping[str, Any]] | None = None,
    status: str | None = None,
) -> dict[str, Any]:
    """Adapt existing Python values into the React display payload."""
    return {
        "user": {"profile": _json_value(profile or {})},
        "location": _json_value(location),
        "weather": _json_value(weather),
        "air_quality": _json_value(aqi),
        "risk": _json_value(risk),
        "advisory": _json_value(advisory),
        "forecast": _json_value(forecast or []),
        "trends": _json_value(trends or []),
        "status": status,
    }


def _read_asset(name: str) -> str:
    path = DIST_DIR / "assets" / name
    if not path.is_file():
        raise FileNotFoundError(f"React dashboard asset is missing: {path}")
    return path.read_text(encoding="utf-8")


def _load_built_assets() -> tuple[str, str]:
    index_path = DIST_DIR / "index.html"
    if not index_path.is_file():
        raise FileNotFoundError(
            "React dashboard build not found. Run `npm install` and `npm run build` "
            "inside react_dashboard."
        )

    index_html = index_path.read_text(encoding="utf-8")
    script_name = next(
        part.split('"')[0]
        for part in index_html.split('src="')[1:]
        if part.startswith("/assets/")
    )
    style_name = next(
        part.split('"')[0]
        for part in index_html.split('href="')[1:]
        if part.startswith("/assets/")
    )
    return _read_asset(Path(script_name).name), _read_asset(Path(style_name).name)


_REACT_SCRIPT, _REACT_STYLE = _load_built_assets()


def render_react_dashboard(payload: Mapping[str, Any] | None = None, height: int = 1500) -> None:
    """Render the production React document without deprecated component APIs."""
    payload_json = json.dumps(_json_value(payload or {}), ensure_ascii=True).replace("</", "<\\/")
    html = f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <style>{_REACT_STYLE}</style>
      </head>
      <body>
        <div id="root"></div>
        <script>window.__CLIMACARE_DATA__ = {payload_json};</script>
        <script type="module">{_REACT_SCRIPT}</script>
      </body>
    </html>
    """
    st.iframe(html, width="stretch", height=height)
