from aozaki.ast.algebra import AstAlgebra
from aozaki.ast.operator import Operator
from aozaki.typing.unknown import Unknown

from .types import (
    AstNode,
    AstInt,
    AstString,
    AstBool,
    AstBinOp,
    AstVar,
)

class AstTreeAlgebra(AstAlgebra[AstNode]):
    def int(self, value: int) -> AstNode:
        return AstInt(value)

    def string(self, value: str) -> AstNode:
        return AstString(value)

    def bool(self, value: bool) -> AstNode:
        return AstBool(value)

    def var(self, value: str) -> AstNode:
        return AstVar(value)

    def binary(self, lhs: AstNode, rhs: AstNode, operator: Operator) -> AstNode:
        return AstBinOp(
            lhs=lhs,
            rhs=rhs,
            operator=operator,
            result_tp=Unknown(),
        )

