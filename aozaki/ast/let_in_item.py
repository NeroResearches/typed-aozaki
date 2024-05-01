from dataclasses import dataclass
from typing import Generic, TypeVar

from .pat import Pat
from ..typing.type import Type

T = TypeVar("T")

@dataclass
class LetInItem(Generic[T]):
    pattern: Pat
    tp: Type
    rhs: T

__all__ = ["LetInItem"]

