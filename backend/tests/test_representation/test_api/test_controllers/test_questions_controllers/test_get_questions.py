from unittest.mock import AsyncMock, Mock

import pytest
import pytest_asyncio
from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.fastapi import setup_dishka
from fastapi.testclient import TestClient

from app.app_factory import create_app
from app.application.use_cases.get_questions import GetQuestionsUseCase


class MockUseCaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_use_case(self) -> GetQuestionsUseCase:
        mock_use_case = Mock()
        mock_use_case.execute = AsyncMock(return_value=[])
        return mock_use_case


@pytest_asyncio.fixture
async def container():
    container = make_async_container(MockUseCaseProvider())
    yield container
    await container.close()


@pytest.fixture
def client(container):
    app = create_app()
    setup_dishka(container, app)
    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture
async def use_case(container) -> Mock:
    return await container.get(GetQuestionsUseCase)


@pytest.mark.asyncio
async def test_get_questions(client: TestClient, use_case: Mock):
    response = client.get("/questions/")
    assert response.status_code == 200
    use_case.execute.assert_called_once()
