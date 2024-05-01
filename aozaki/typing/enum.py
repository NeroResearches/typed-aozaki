from dataclasses import dataclass
from frozendict import frozendict

from .type import Type

@dataclass
class Enum:
    variants: frozendict[str, Type]

__all__ = ["Enum"]

