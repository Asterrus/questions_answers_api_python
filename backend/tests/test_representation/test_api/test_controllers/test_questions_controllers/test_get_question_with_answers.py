from datetime import datetime
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
import pytest_asyncio
from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.fastapi import setup_dishka
from fastapi.testclient import TestClient

from app.app_factory import create_app
from app.application.exceptions import QuestionNotFound
from app.application.use_cases.get_question_with_answers import GetQuestionWithAnswersUseCase
from app.representation.api.rest.error_handling import setup_exception_handlers
from app.representation.api.rest.v1.mappers.questions import QuestionWithAnswersDtoToApiMapper
from app.representation.api.rest.v1.schemas.questions import (
    AnswerListItem,
    GetQuestionWithAnswersResponseSchema,
)


class MockUseCaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_use_case(self) -> GetQuestionWithAnswersUseCase:
        mock_use_case = Mock()
        mock_use_case.execute = AsyncMock(return_value=[])
        return mock_use_case


class MockMapperProvider(Provider):
    @provide(scope=Scope.APP)
    def get_mapper(self) -> QuestionWithAnswersDtoToApiMapper:
        mock_mapper = Mock()
        value = GetQuestionWithAnswersResponseSchema(
            id=uuid4(),
            text="What is your favorite color?",
            created_at=datetime.now(),
            answers=[
                AnswerListItem(
                    id=uuid4(),
                    text="Blue",
                    created_at=datetime.now(),
                ),
            ],
        )
        mock_mapper.to_response = Mock(return_value=value)
        return mock_mapper


@pytest_asyncio.fixture
async def container():
    container = make_async_container(MockUseCaseProvider(), MockMapperProvider())
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


@pytest_asyncio.fixture
async def mapper(container) -> Mock:
    return await container.get(QuestionWithAnswersDtoToApiMapper)


@pytest.mark.asyncio
async def test_get_question_with_answers(client: TestClient, use_case: Mock, mapper: Mock):
    uuid = uuid4()
    response = client.get(f"/questions/{uuid}")
    assert response.status_code == 200
    use_case.execute.assert_called_once()
    mapper.to_response.assert_called_once()


@pytest.mark.asyncio
async def test_get_question_not_found(client, use_case: Mock):
    nonexistent_id = uuid4()
    use_case.execute = AsyncMock(side_effect=QuestionNotFound(nonexistent_id))

    response = client.get(f"/questions/{nonexistent_id}")
    assert response.status_code == 404
