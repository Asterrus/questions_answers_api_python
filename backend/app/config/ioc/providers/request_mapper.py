from dishka import Provider, Scope, provide

from app.representation.api.rest.v1.mappers.questions import QuestionsListDtoToApiMapper

request_mapper_provider = Provider(scope=Scope.REQUEST)
request_mapper_provider.provide(QuestionsListDtoToApiMapper)
