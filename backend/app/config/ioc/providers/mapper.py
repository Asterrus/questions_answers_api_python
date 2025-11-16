from dishka import Provider, Scope, provide

from app.application.use_cases.get_questions import (
    QuestionEntityToDtoMapper as QuestionEntityToDtoMapperInterface,
)
from app.infrastructure.mappers.question_mapper import QuestionEntityToDtoMapper

mapper_provider = Provider(scope=Scope.REQUEST)
mapper_provider.provide(QuestionEntityToDtoMapper, provides=QuestionEntityToDtoMapperInterface)
