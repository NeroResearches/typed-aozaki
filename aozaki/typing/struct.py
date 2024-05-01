from dataclasses import dataclass
from frozendict import frozendict

from .type import Type

@dataclass
class Struct:
    fields: frozendict[str, Type]

__all__ = ["Struct"]


