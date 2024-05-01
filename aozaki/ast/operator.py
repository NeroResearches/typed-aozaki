from enum import StrEnum

class Operator(StrEnum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    DOT = "."
    APPLY = "$"


__all__ = ["Operator"]

