from typing import Protocol, TypeVar

from .operator import Operator

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


__all__ = ["AstAlgebra"]


