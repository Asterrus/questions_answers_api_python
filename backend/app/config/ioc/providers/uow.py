from dishka import Provider, Scope

from app.application.interfaces.uow import UnitOfWork
from app.infrastructure.db.uow import SQLAlchemyUnitOfWork

uow_provider = Provider(scope=Scope.REQUEST)
uow_provider.provide(SQLAlchemyUnitOfWork, provides=UnitOfWork)
