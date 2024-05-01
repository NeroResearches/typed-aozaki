from dataclasses import dataclass

from .type import Type

@dataclass
class AccessAssoc:
    lhs: Type
    name: str

__all__ = ["AccessAssoc"]
