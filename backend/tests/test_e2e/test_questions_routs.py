import pytest
from fastapi.testclient import TestClient

from app.app_factory import create_production_app


@pytest.fixture
def client():
    app = create_production_app()
    with TestClient(app) as c:
        yield c


@pytest.mark.asyncio
async def test_crud_questions(client: TestClient):
    create_resp = client.post("/questions/", json={"text": "Test question"})
    assert create_resp.status_code == 201
    created_id = create_resp.json()

    response = client.get("/questions/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(item["id"] == created_id and item["text"] == "Test question" for item in data)

    delete_resp = client.delete(f"/questions/{created_id}")
    assert delete_resp.status_code == 204

    response = client.get("/questions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert not any(item["id"] == created_id and item["text"] == "Test question" for item in data)
