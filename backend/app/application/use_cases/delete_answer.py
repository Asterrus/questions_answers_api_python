from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


class AnswerDeleter(Protocol):
    async def delete(self, id: UUID) -> None: ...


@dataclass(frozen=True, slots=True)
class DeleteAnswerUseCase:
    answer_repository: AnswerDeleter

    async def execute(self, answer_id: UUID) -> None:
        await self.answer_repository.delete(answer_id)
