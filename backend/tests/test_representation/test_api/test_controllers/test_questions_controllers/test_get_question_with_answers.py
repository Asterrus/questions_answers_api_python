from datetime import datetime
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
import pytest_asyncio
from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.fastapi import setup_dishka
from fastapi.testclient import TestClient

from app.app_factory import create_app
from app.application.dtos.question import QuestionWithAnswersResponseDTO
from app.application.exceptions import QuestionNotFound
from app.application.use_cases.get_question_with_answers import GetQuestionWithAnswersUseCase
from app.representation.api.rest.error_handling import setup_exception_handlers


class MockUseCaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_use_case(self) -> GetQuestionWithAnswersUseCase:
        mock_use_case = Mock()
        mock_use_case.execute = AsyncMock(
            return_value=QuestionWithAnswersResponseDTO(
                id=uuid4(),
                text="What is your favorite color?",
                created_at=datetime.now(),
                answers=[],
            )
        )
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
    setup_exception_handlers(app)
    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture
async def use_case(container) -> Mock:
    return await container.get(GetQuestionWithAnswersUseCase)


@pytest.mark.asyncio
async def test_get_question_with_answers(client: TestClient, use_case: Mock):
    uuid = uuid4()
    response = client.get(f"/questions/{uuid}")
    assert response.status_code == 200
    use_case.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_question_not_found(client, use_case: Mock):
    nonexistent_id = uuid4()
    use_case.execute = AsyncMock(side_effect=QuestionNotFound(nonexistent_id))

    response = client.get(f"/questions/{nonexistent_id}")
    assert response.status_code == 404
