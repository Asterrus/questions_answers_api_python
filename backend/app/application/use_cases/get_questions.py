from dataclasses import dataclass
from typing import Protocol

from app.application.dtos.question import QuestionsListResponseDTO
from app.application.interfaces.mappers import QuestionEntityToDtoMapper
from app.domain.entities.question import QuestionEntity


class QuestionListReader(Protocol):
    async def get_list(self) -> list[QuestionEntity]: ...


@dataclass(frozen=True, slots=True)
class GetQuestionsUseCase:
    question_repository: QuestionListReader
    question_mapper: QuestionEntityToDtoMapper

    async def execute(self) -> list[QuestionsListResponseDTO]:
        questions = await self.question_repository.get_list()
        return [self.question_mapper.to_dto(question) for question in questions]
