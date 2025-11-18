
from dishka import Provider, Scope

from app.application.interfaces.uow import UnitOfWorkProtocol
from app.infrastructure.db.uow import UnitOfWorkSQLAlchemy

uow_provider = Provider(scope=Scope.REQUEST)
uow_provider.provide(UnitOfWorkSQLAlchemy, provides=UnitOfWorkProtocol)
