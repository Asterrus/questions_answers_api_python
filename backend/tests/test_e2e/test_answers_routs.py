import pytest
from fastapi.testclient import TestClient

from app.app_factory import create_production_app


@pytest.fixture
def client():
    app = create_production_app()
    with TestClient(app) as c:
        yield c


@pytest.mark.asyncio
async def test_crud_answers(client: TestClient):
    # create question
    create_resp = client.post("/questions/", json={"text": "Test question"})
    assert create_resp.status_code == 201
    question_id = create_resp.json()

    # create answer
    data = {"text": "test"}
    response = client.post(f"questions/{question_id}/answers/", json=data)
    assert response.status_code == 201
    answer_id = response.json()

    # get answer
    response = client.get(f"/answers/{answer_id}")
    assert response.status_code == 200

    # delete answer
    response = client.delete(f"/answers/{answer_id}")
    assert response.status_code == 204

    # check answer deleted
    response = client.get(f"/answers/{answer_id}")
    assert response.status_code == 404

    # delete question
    delete_resp = client.delete(f"/questions/{question_id}")
    assert delete_resp.status_code == 204
