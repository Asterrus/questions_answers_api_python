from datetime import datetime
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
import pytest_asyncio
from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.fastapi import setup_dishka
from fastapi.testclient import TestClient

from app.app_factory import create_app
from app.application.dtos.answer import AnswerResponseDTO
from app.application.use_cases.get_answer import GetAnswerUseCase


class MockUseCaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_use_case(self) -> GetAnswerUseCase:
        mock_use_case = Mock()
        mock_use_case.execute = AsyncMock(
            return_value=AnswerResponseDTO(
                id=uuid4(),
                question_id=uuid4(),
                user_id=uuid4(),
                text="1",
                created_at=datetime.now(),
            )
        )
        return mock_use_case


@pytest_asyncio.fixture
async def container():
    container = make_async_container(MockUseCaseProvider())
    yield container
    await container.close()


@pytest_asyncio.fixture
async def use_case(container) -> Mock:
    return await container.get(GetAnswerUseCase)


@pytest.fixture
def client(container):
    app = create_app()
    setup_dishka(container, app)
    with TestClient(app) as client:
        yield client


@pytest.mark.asyncio
async def test_get_answer(client: TestClient, use_case: Mock):
    answer_id = str(uuid4())
    response = client.get(f"/answers/{answer_id}")
    assert response.status_code == 200
    use_case.execute.assert_called_once()
