from dishka import Provider, Scope

from app.application.use_cases.create_question import QuestionWriter
from app.application.use_cases.get_questions import QuestionListReader
from app.infrastructure.db.repositories.question import SQLAlchemyQuestionRepository

repository_provider = Provider(scope=Scope.REQUEST)
repository_provider.provide(SQLAlchemyQuestionRepository, provides=QuestionListReader)
repository_provider.provide(SQLAlchemyQuestionRepository, provides=QuestionWriter)
