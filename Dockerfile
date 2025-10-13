# syntax=docker/dockerfile:1.7-labs
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /svc

COPY app /svc/app
RUN pip install --upgrade pip && pip install -e /svc/app

EXPOSE 8080
CMD ["uvicorn", "demo_app.main:app", "--host", "0.0.0.0", "--port", "8080"]
