from ..typing.type import Type
from dataclasses import dataclass

@dataclass
class TypedefItem:
    # Type name
    name: str

    # Bound variables for type
    args: tuple[str, ...]

    # Type where substitute bound variables
    rhs: Type

__all__ = ["TypedefItem"]

