import pytest

from app.application.interfaces.uow import UnitOfWorkProtocol
from tests.fakes.fake_uow import FakeUnitOfWork


@pytest.fixture
def fake_uow() -> UnitOfWorkProtocol:
    return FakeUnitOfWork()
