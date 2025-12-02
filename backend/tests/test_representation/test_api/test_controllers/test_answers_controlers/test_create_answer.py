from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
import pytest_asyncio
from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.fastapi import setup_dishka
from fastapi.testclient import TestClient

from app.app_factory import create_app
from app.application.use_cases.create_answer import CreateAnswerUseCase


class MockUseCaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_use_case(self) -> CreateAnswerUseCase:
        mock_use_case = Mock()
        mock_use_case.execute = AsyncMock(return_value=uuid4())
        return mock_use_case


@pytest_asyncio.fixture
async def container():
    container = make_async_container(MockUseCaseProvider())
    yield container
    await container.close()


@pytest_asyncio.fixture
async def use_case(container) -> Mock:
    return await container.get(CreateAnswerUseCase)


@pytest.fixture
def client(container):
    app = create_app()
    setup_dishka(container, app)
    with TestClient(app) as client:
        yield client


@pytest.mark.asyncio
async def test_create_answer(client: TestClient, use_case: Mock):
    question_id = str(uuid4())
    data = {"text": "test"}
    response = client.post(f"questions/{question_id}/answers/", json=data)
    assert response.status_code == 201
    use_case.execute.assert_called_once()
