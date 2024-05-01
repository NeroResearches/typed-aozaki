from __future__ import annotations

from typing import TypeAlias
from dataclasses import dataclass
from frozendict import frozendict

from aozaki.typing.type import Type
from aozaki.ast.operator import Operator

from ..typedef import TypedefItem

@dataclass
class AstInt:
    value: int

@dataclass
class AstString:
    value: str

@dataclass
class AstBool:
    value: bool

@dataclass
class AstBinOp:
    lhs: AstNode
    rhs: AstNode
    op: Operator

    result_tp: Type

@dataclass
class AstVar:
    name: str

@dataclass
class AstApplication:
    what: AstNode
    args: tuple[AstNode, ...]
    
    result_tp: Type

@dataclass
class AstTypedef:
    items: tuple[TypedefItem, ...]
    where: AstNode

AstNode: TypeAlias = (
    Operator
    | AstInt
    | AstString
    | AstBool
    | AstBinOp
    | AstVar
    | AstApplication
    | AstTypedef
)


