from dataclasses import dataclass

@dataclass
class Unknown:
    ...

@dataclass
class UnresolvedName:
    name: str


__all__ = ["Unknown", "UnresolvedName"]

