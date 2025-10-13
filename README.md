# demo-app

A tiny **FastAPI** service that exposes a REST endpoint returning a static message and the current epoch timestamp.  
Built in Python 3.12, packaged as a container image, and published automatically to **AWS ECR** via GitHub Actions.

---

## Tooling

| Area | Tool |
|------|------|
| Language | Python 3.12 |
| Package / Env Mgr | [uv](https://github.com/astral-sh/uv) |
| Web Framework | FastAPI + Uvicorn |
| Container | Docker |
| CI/CD | GitHub Actions (tests + build + ECR push) |

---

## Endpoints

| Route | Description |
|-------|--------------|
| `GET /api/v1/info` | Returns `{ "message": "Automate all the things!", "timestamp": 1690000000 }` |
| `GET /healthz` | Basic health probe |
| `GET /` | Service metadata |

---

## Local Development

```bash
# Create venv and install
uv venv --python 3.12
. .venv/bin/activate
uv pip install -e app/.[dev]

# Run unit tests
uv run pytest

# Start API locally
uv run uvicorn main:app --reload --port 8080
curl localhost:8080/api/v1/info
