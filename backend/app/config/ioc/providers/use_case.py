from dishka import Provider, Scope

from app.application.use_cases.create_question import CreateQuestionUseCase
from app.application.use_cases.get_questions import GetQuestionsUseCase

use_case_provider = Provider(scope=Scope.REQUEST)
use_case_provider.provide(GetQuestionsUseCase)
use_case_provider.provide(CreateQuestionUseCase)
