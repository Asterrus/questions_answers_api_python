from datetime import datetime
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
import pytest_asyncio
from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.fastapi import setup_dishka
from fastapi.testclient import TestClient

from app.app_factory import create_app
from app.application.use_cases.get_answer import GetAnswerUseCase
from app.representation.api.rest.v1.mappers.answers import AnswerDtoToApiMapper
from app.representation.api.rest.v1.schemas.answers import GetAnswerResponseSchema


class MockUseCaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_use_case(self) -> GetAnswerUseCase:
        mock_use_case = Mock()
        mock_use_case.execute = AsyncMock(return_value=uuid4())
        return mock_use_case


class MockAnswerDtoToApiMapperProvider(Provider):
    @provide(scope=Scope.APP)
    def get_provider(self) -> AnswerDtoToApiMapper:
        mock_provider = Mock()
        mock_provider.to_response = Mock(
            return_value=GetAnswerResponseSchema(
                question_id=uuid4(),
                user_id=uuid4(),
                text="1",
                created_at=datetime.now(),
            )
        )
        return mock_provider


@pytest_asyncio.fixture
async def container():
    container = make_async_container(MockUseCaseProvider(), MockAnswerDtoToApiMapperProvider())
    yield container
    await container.close()


@pytest_asyncio.fixture
async def use_case(container) -> Mock:
    return await container.get(GetAnswerUseCase)


@pytest_asyncio.fixture
async def mapper(container) -> Mock:
    return await container.get(AnswerDtoToApiMapper)


@pytest.fixture
def client(container):
    app = create_app()
    setup_dishka(container, app)
    with TestClient(app) as client:
        yield client


@pytest.mark.asyncio
async def test_get_answer(client: TestClient, use_case: Mock, mapper: Mock):
    answer_id = str(uuid4())
    response = client.get(f"/answers/{answer_id}")
    assert response.status_code == 200
    use_case.execute.assert_called_once()
    mapper.to_response.assert_called_once()
