from aozaki.ast.algebra import AstAlgebra
from aozaki.ast.operator import Operator
from aozaki.typing.unknown import Unknown
from aozaki.ast.typedef import TypedefItem
from aozaki.ast.let_in_item import LetInItem

from .types import (
    AstNode,
    AstInt,
    AstString,
    AstBool,
    AstBinOp,
    AstApplication,
    AstVar,
    AstTypedef,
    AstLetIn,
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

    def application(self, what: AstNode, args: tuple[AstNode, ...]) -> AstNode:
        return AstApplication(what, args, Unknown())

    def let_in(self, items: tuple[LetInItem, ...], where: AstNode) -> AstNode:
        return AstLetIn(items, where)

    def binary(self, lhs: AstNode, rhs: AstNode, operator: Operator) -> AstNode:
        return AstBinOp(
            lhs=lhs,
            rhs=rhs,
            op=operator,
            result_tp=Unknown(),
        )

    def typedef(
        self,
        items: tuple[TypedefItem, ...],
        where: AstNode,
    ) -> AstNode:
        return AstTypedef(items, where)

