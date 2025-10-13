import time
from fastapi.testclient import TestClient
from main import app, MESSAGE_DEFAULT

client = TestClient(app)

def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    body = r.json()
    assert body.get("status") == "ok"
    assert "service" in body and "version" in body

def test_info_payload():
    r = client.get("/api/v1/info")
    assert r.status_code == 200
    body = r.json()
    assert set(body.keys()) == {"message", "timestamp"}
    assert body["message"] == MESSAGE_DEFAULT
    now = int(time.time())
    assert 0 <= (now - body["timestamp"]) <= 5  # within 5s of 'now'
