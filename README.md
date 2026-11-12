# Capability Launcher

Backend prototype for managing and running isolated Python capabilities.

## Overview

This project is a central API that can discover capability metadata without importing each capability's implementation into the same Python process.

Each capability lives in its own folder under `backend/capabilities` and includes:
- `manifest.json`
- `main.py`
- `requirements.txt`

The API loads metadata from `manifest.json` and executes the capability in a separate virtual environment through a subprocess worker.

## Backend structure

- `backend/app` – FastAPI app, validation, catalog, config, and execution helpers
- `backend/capabilities` – example capability folders
- `backend/runner/worker.py` – subprocess worker used to call the capability `run(inputs)` function
- `backend/setup_capabilities.py` – creates a `.venv` for each capability and installs its dependencies
- `backend/tests` – API and catalog tests

## Example capabilities

The prototype includes three example capabilities:

- `url_inspector`
- `timezone_converter`
- `csv_cleaner`

## Frontend

The project also includes a small React + Vite frontend in `frontend/`.

It is intentionally generic: it reads capability metadata from the backend API and renders form fields dynamically instead of hard-coding one UI per capability.

Run it separately from the backend:

```bash
cd frontend
npm install
npm run dev
```

The frontend expects the API to be running at:
- `http://localhost:8000`

## Run locally

From the project root:

1. Create and activate the backend environment.
2. Install dependencies:
   ```bash
   cd backend
   python3 -m pip install -r requirements.txt
   ```
3. Prepare capability virtual environments:
   ```bash
   python3 setup_capabilities.py
   ```
4. Start the backend:
   ```bash
   PYTHONPATH=. python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

The API is then available at:
- `http://localhost:8000/health`
- `http://localhost:8000/api/capabilities`
- Swagger UI at `http://localhost:8000/docs`

## Useful API calls

List capabilities:
```bash
curl http://localhost:8000/api/capabilities
```

Run a capability:
```bash
curl -X POST http://localhost:8000/api/capabilities/url_inspector/run \
  -H "Content-Type: application/json" \
  -d '{"inputs":{"url":"https://example.com/path?x=1&y=2"}}'
```

## Tests

Run the backend tests:
```bash
cd backend
python3 -m pytest -q
```
