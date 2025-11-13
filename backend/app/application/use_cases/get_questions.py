from dataclasses import dataclass

from app.application.dtos.question import QuestionResponseDTO
from app.application.interfaces.mappers import QuestionEntityToDtoMapper
from app.application.interfaces.repositories.question_repository import QuestionReader


@dataclass(frozen=True, slots=True)
class GetQuestionsUseCase:
    question_repository: QuestionReader
    question_mapper: QuestionEntityToDtoMapper

    async def execute(self) -> list[QuestionResponseDTO]:
        questions = await self.question_repository.get_all()
        return [self.question_mapper.to_dto(question) for question in questions]
