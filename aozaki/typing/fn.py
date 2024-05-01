from typing import TYPE_CHECKING
from dataclasses import dataclass

from .type import Type

@dataclass
class Fn:
    params: tuple[Type, ...]
    ret: Type

    invertible: bool

__all__ = ["Fn"]
