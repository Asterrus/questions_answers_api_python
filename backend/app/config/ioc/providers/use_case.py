from dishka import Provider, Scope, provide

from app.application.use_cases.get_questions import GetQuestionsUseCase

use_case_provider = Provider(scope=Scope.REQUEST)
use_case_provider.provide(GetQuestionsUseCase)
