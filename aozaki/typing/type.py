from typing import TypeAlias, TYPE_CHECKING

if TYPE_CHECKING:
    from .fn import Fn
    from .struct import Struct
    from .enum import Enum
    from .unknown import Unknown, UnresolvedName
    from .application import Application, Kinded
    from .assoc import AccessAssoc

Type: TypeAlias = """
(
  Fn
| Struct
| Enum
| Unknown
| Kinded
| Application
| AccessAssoc
)
"""

