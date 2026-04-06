# Render Deployment Guide

This project is a **Dash + Python** web app deployed as a Render Web Service.

## Required files in repo root

Make sure all of these are committed before deploying:

- `app.py`
- `state.py`
- `layout.py`
- `callbacks.py`
- `aggregations.py`
- `components.py`
- `config.py`
- `data_loader.py`
- `stock_logic.py`
- `logger.py`
- `requirements.txt`
- `render.yaml`
- `assets/styles.css`
- `data/lpg_stock_data.xlsx`

## How it works

| Config | Value |
|--------|-------|
| WSGI entrypoint | `app:server` |
| Data file | `data/lpg_stock_data.xlsx` (must be committed) |
| Python version | `3.11.11` |
| Start command | `gunicorn app:server --bind 0.0.0.0:$PORT --workers 1 --timeout 120` |

## Deployment steps (Blueprint — recommended)

1. Push all files to GitHub.
2. Open **Render Dashboard → New → Blueprint**.
3. Connect the repository and select the branch.
4. Render detects `render.yaml` automatically.
5. Click **Deploy Blueprint**.

## Local production test

**Linux / macOS:**
```bash
pip install -r requirements.txt
PORT=10000 gunicorn app:server --bind 0.0.0.0:$PORT --workers 1 --timeout 120
```

**Windows PowerShell:**
```powershell
pip install -r requirements.txt
$env:PORT = "10000"
python -m gunicorn app:server --bind 0.0.0.0:$env:PORT --workers 1 --timeout 120
```

## Common issues

### `FileNotFoundError: data/lpg_stock_data.xlsx`
- The Excel file was not committed to the repo.
- Check spelling and case — Linux is case-sensitive.

### `ModuleNotFoundError`
- A package is missing from `requirements.txt`.
- All versions are pinned with `==` — do not change to `>=`.

### App crashes immediately / no port detected
- The `--timeout 120` flag is required. Startup loads Excel + enriches
  rows which can exceed Gunicorn's 30s default timeout.

### Out of memory on free plan
- Keep `--workers 1`. Multiple workers will exhaust the free plan RAM.
