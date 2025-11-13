from dataclasses import dataclass

from app.application.dtos.question import QuestionsListResponseDTO
from app.application.interfaces.mappers import QuestionEntityToDtoMapper
from app.application.interfaces.repositories.question_repository import QuestionListReader


@dataclass(frozen=True, slots=True)
class GetQuestionsUseCase:
    question_repository: QuestionListReader
    question_mapper: QuestionEntityToDtoMapper

    async def execute(self) -> list[QuestionsListResponseDTO]:
        questions = await self.question_repository.get_list()
        return [self.question_mapper.to_dto(question) for question in questions]
