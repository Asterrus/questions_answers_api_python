from abc import abstractmethod
from typing import Protocol, TypeVar

T = TypeVar("T", contravariant=True)


class DbMapperProtocol(Protocol[T]):
    @abstractmethod
    def insert(self, model: T) -> None: ...

    @abstractmethod
    def update(self, model: T) -> None: ...

    @abstractmethod
    def delete(self, model: T) -> None: ...
