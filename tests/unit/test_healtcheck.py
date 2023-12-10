from fastapi.testclient import TestClient
from httpx import Response

from app.main import app

client = TestClient(app)


def test_healthcheck() -> None:
    response: Response = client.get("/api/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
