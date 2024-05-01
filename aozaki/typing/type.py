from typing import TypeAlias, TYPE_CHECKING

if TYPE_CHECKING:
    from .fn import Fn
    from .struct import Struct
    from .enum import Enum
    from .unknown import Unknown

Type: TypeAlias = """
  Fn
| Struct
| Enum
| Unknown
"""

