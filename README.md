<<<<<<< HEAD
# origin-26
=======
# ClimaCare AI

**Developer:** SUMED — Frontend  
**Current stage:** Step 1–3 — Streamlit architecture + app shell

ClimaCare AI is a personalized weather and air-quality health advisory project.

## Frontend responsibilities

- Streamlit UI
- Profile
- Dashboard
- Advisory presentation
- SQLite history
- Charts
- Integration

## Backend responsibilities

Saransh owns the weather API, AQI API, automatic location backend, risk engine,
LLM integration, and backend functions. Those implementations are intentionally
not included in this Step 1–3 shell.

## Current architecture

The shell is organized around this future flow:

`Browser location → Streamlit app → Profile UI → backend adapter → Dashboard → SQLite history → 7-day charts`

`services/backend_adapter.py` is the integration boundary for Saransh's future
functions. The `api/` and `ai/` directories are reserved for his backend files.

## Run the current shell

From the project root:

```powershell
pip install -r requirements-frontend.txt
streamlit run app.py
```

The current screen contains UI placeholders only. It does not detect a real
location, call backend services, create SQLite history, render charts, or provide
medical advice.
>>>>>>> 3e139df (Initial commit - ClimaCare AI project)
