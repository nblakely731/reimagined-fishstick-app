from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_info_shape_and_timestamp():
    r = client.get("/api/v1/info")
    assert r.status_code == 200
    body = r.json()
    assert set(body.keys()) == {"message", "timestamp"}
    assert isinstance(body["timestamp"], int)
    assert isinstance(body["message"], str)