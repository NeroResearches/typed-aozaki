from enum import StrEnum

class Operator(StrEnum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    ATTR = "."
    APPLY = "$"


__all__ = ["Operator"]

