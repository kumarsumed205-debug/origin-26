"""SQLite storage for environmental assessment history."""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DATABASE_PATH = Path(__file__).resolve().parent.parent / "climacare.db"


def _value(data: Any, key: str) -> Any:
	if isinstance(data, Mapping):
		return data.get(key)
	return None


def _advisory_value(advisory: Any) -> str | None:
	if advisory is None:
		return None
	if isinstance(advisory, (Mapping, list, tuple)):
		return json.dumps(advisory)
	return str(advisory)


def init_db() -> None:
	"""Create the database and assessments table if they do not exist."""
	with sqlite3.connect(DATABASE_PATH) as connection:
		connection.execute(
			"""
			CREATE TABLE IF NOT EXISTS assessments (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				timestamp TEXT NOT NULL,
				location TEXT,
				age_group TEXT,
				health_condition TEXT,
				occupation TEXT,
				temperature REAL,
				humidity REAL,
				aqi REAL,
				pm25 REAL,
				pm10 REAL,
				risk_level TEXT,
				advisory TEXT
			)
			"""
		)


def save_assessment(
	location: Any = None,
	profile: Any = None,
	weather: Any = None,
	aqi: Any = None,
	risk: Any = None,
	advisory: Any = None,
) -> int:
	"""Save supplied assessment values and return the new record id."""
	location_value = location
	if isinstance(location, Mapping):
		location_value = _value(location, "name") or _value(location, "city")
	if location_value is not None:
		location_value = str(location_value)

	with sqlite3.connect(DATABASE_PATH) as connection:
		cursor = connection.execute(
			"""
			INSERT INTO assessments (
				timestamp, location, age_group, health_condition, occupation,
				temperature, humidity, aqi, pm25, pm10, risk_level, advisory
			) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
			""",
			(
				datetime.now(timezone.utc).isoformat(),
				location_value,
				_value(profile, "age_group"),
				_value(profile, "health_condition"),
				_value(profile, "occupation"),
				_value(weather, "temperature"),
				_value(weather, "humidity"),
				_value(aqi, "aqi"),
				_value(aqi, "pm25"),
				_value(aqi, "pm10"),
				_value(risk, "level"),
				_advisory_value(advisory),
			),
		)
		return int(cursor.lastrowid)


def get_assessment_history(limit: int = 20) -> list[dict[str, Any]]:
	"""Return the newest saved assessments as frontend-friendly dictionaries."""
	if limit < 1:
		return []

	with sqlite3.connect(DATABASE_PATH) as connection:
		connection.row_factory = sqlite3.Row
		rows = connection.execute(
			"""
			SELECT id, timestamp, location, age_group, health_condition, occupation,
				   temperature, humidity, aqi, pm25, pm10, risk_level, advisory
			FROM assessments
			ORDER BY id DESC
			LIMIT ?
			""",
			(limit,),
		).fetchall()
	return [dict(row) for row in rows]


def clear_history() -> None:
	"""Delete all assessment records while keeping the database and table."""
	with sqlite3.connect(DATABASE_PATH) as connection:
		connection.execute("DELETE FROM assessments")
