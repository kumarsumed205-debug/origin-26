"""Adapter boundary for Saransh's backend services.

The backend capabilities are not present in this checkout yet. This module
keeps that absence explicit so the Streamlit app remains runnable without
inventing API calls or environmental values.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class BackendUnavailableError(RuntimeError):
	"""Raised when a requested backend capability is not implemented."""


def get_current_assessment(profile: Mapping[str, Any] | None = None) -> None:
	"""Define the integration boundary until Saransh exposes the service."""
	raise BackendUnavailableError(
		"No weather, AQI, location, risk, or advisory backend is available yet."
	)

# Future integration targets:
# from api.location import reverse_geocode
# from api.weather import get_current_weather, get_weather_forecast
# from api.aqi import get_aqi
# from ai.risk_engine import calculate_risk
# from ai.advisory import generate_advisory
