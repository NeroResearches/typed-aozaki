from dataclasses import dataclass
from typing import Callable

from .type import Type

@dataclass
class Kinded:
    requires_args: int
    f: Callable[[tuple[Type, ...]], Type]

@dataclass
class Application:
    tp: Type
    args: tuple[Type, ...]


__all__ = ["Application", "Kinded"]

