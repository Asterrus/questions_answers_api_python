from dishka import Provider, Scope

from app.application.use_cases.get_question_with_answers import (
    QuestionWithAnswersEntityToDtoMapper as QuestionWithAnswersEntityToDtoMapperInterface,
)
from app.application.use_cases.get_questions import (
    QuestionEntityToDtoMapper as QuestionEntityToDtoMapperInterface,
)
from app.infrastructure.mappers.question_mapper import (
    QuestionEntityToDtoMapper,
    QuestionWithAnswersEntityToDtoMapper,
)

mapper_provider = Provider(scope=Scope.REQUEST)
mapper_provider.provide(QuestionEntityToDtoMapper, provides=QuestionEntityToDtoMapperInterface)
mapper_provider.provide(
    QuestionWithAnswersEntityToDtoMapper, provides=QuestionWithAnswersEntityToDtoMapperInterface
)
