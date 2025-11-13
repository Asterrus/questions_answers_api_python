from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.application.use_cases.delete_answer import DeleteAnswerUseCase


class TestDeleteAnswerUseCase:
    @pytest.mark.asyncio
    async def test_delete_answer_success(self):
        mock_repo = AsyncMock()
        use_case = DeleteAnswerUseCase(answer_repository=mock_repo)
        answer_id = uuid4()
        await use_case.execute(answer_id)
        mock_repo.delete.assert_called_once_with(answer_id)
