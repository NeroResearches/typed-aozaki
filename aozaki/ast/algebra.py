from typing import Protocol, TypeVar

from .operator import Operator
from .typedef import TypedefItem
from .let_in_item import LetInItem

T = TypeVar("T")

class AstAlgebra(Protocol[T]):
    def int(self, value: int) -> T:
        ...

    def string(self, value: str) -> T:
        ...

    def bool(self, value: bool) -> T:
        ...

    def binary(self, lhs: T, rhs: T, op: Operator) -> T:
        ...

    def var(self, name: str) -> T:
        ...

    def application(self, what: T, args: tuple[T, ...]) -> T:
        ...

    def let_in(self, items: tuple[LetInItem, ...], where: T) -> T:
        ...

    def typedef(
        self,
        items: tuple[TypedefItem, ...],
        where: T,
    ) -> T: 
        ...


__all__ = ["AstAlgebra"]


