from dishka import Provider, Scope

from app.infrastructure.db.mappers.question_db_mapper import QuestionDbMapper

db_mapper_provider = Provider(scope=Scope.REQUEST)
db_mapper_provider.provide(QuestionDbMapper)
