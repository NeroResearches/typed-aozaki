from typing import TypeVar, Callable, overload

from .peco.peco import *

from .typing.enum import Enum
from .typing.struct import Struct
from .typing.unknown import Unknown
from .typing.fn import Fn

from .ast.algebra import AstAlgebra
from .ast.tree import AstNode, AstTreeAlgebra

from frozendict import frozendict
from string import hexdigits

hex_digit = one_of(hexdigits)
ws = many(space)
tok = lambda f: memo(seq(ws, f))
skip = lambda c: tok(sym(c))
repeat = lambda f, n: seq(*(f for _ in range(n)))

tp = lambda s: tp(s)

name_start = alt(letter, sym('_'))
name_rest = alt(name_start, one_of("'!?"))
comma = skip(',')

dquote = sym('"')
squote = sym("'")

def to_alg(f):
    n = f.__code__.co_argcount - 1
    if n < 0:
        raise ValueError
    def parse(s):
        pos = len(s.stack) - n
        return s._replace(stack=s.stack[:pos] + (f(s.glob['algebra'], *s.stack[pos:]),))
    return parse

map_esc = lambda symbol, map_to: seq(sym(symbol), to(lambda: map_to))

hex_escape = seq(
    repeat(hex_digit, 2),
    to(lambda l, r: chr(int(l + r, 16)))
)
string_escape = alt(
    seq(sym('x'), hex_escape),
    map_esc('n', '\n'),
    map_esc('t', '\t'),
    map_esc('r', '\r'),
)
string_char = alt(
    seq(sym('\\'), string_escape),
    cite(non(dquote)),
)
string_unmarked = seq(
    skip('"'),
    group(many(string_char)),
    skip('"'),
    to(lambda chars: ''.join(chars))
)
string = seq(
    string_unmarked,
    to_alg(lambda alg, s: alg.string(s))
)

name = alt(
    cite(seq(name_start, many(name_rest))),
    seq(skip('@'), string_unmarked)
)
var = seq(name, to_alg(lambda alg, n: alg.var(n)))

unknown_tp = seq(
    skip('?'),
    to(lambda: Unknown())
)

enum_variant = seq(
    tok(name),
    some(space),
    skip('of'),
    tp,
    to(lambda n, t: (n, t))
)
enum_tp = seq(
    skip('enum'),
    skip('{'),
    group(list_of(enum_variant, comma)),
    opt(comma),
    skip('}'),
    to(lambda variants: Enum(frozendict(variants)))
)

struct_field_tp = seq(
    tok(name),
    skip(':'),
    tp,
    to(lambda n, t: (n, t))
)
struct_tp = seq(
    skip('struct'),
    skip('{'),
    group(opt(list_of(struct_field_tp, comma))),
    opt(comma),
    skip('}'),
    to(lambda fields: Struct(frozendict(fields))),
)

maybe_invertible = alt(
    seq(skip("'"), to(lambda: True)),
    to(lambda: False),
)
fn_tp = seq(
    skip('fn'),
    maybe_invertible,
    skip('('),
    group(opt(list_of(tp, comma))),
    opt(comma),
    skip(')'),
    skip('->'),
    tp,
    to(lambda invertible, params, ret: Fn(params=params, ret=ret, invertible=invertible))
)

tp = alt(
    unknown_tp,
    struct_tp,
    fn_tp,
    enum_tp,
)

expr = alt(
    string,
    var,
)

Repr = TypeVar("Repr")
def parse(
    source: str,
    algebra: AstAlgebra[Repr],
    parser: Callable[[State], State] | None = None,
) -> Repr:
    if parser is None:
        parser = expr

    state = State(source, 0, True, (), {
        'pos': 0,
        'tab': {},
        'algebra': algebra,
    })
    result = parser(state)
    if not result.ok:
        raise SyntaxError(f"Failed to parse: {result!r}")

    return result.stack[0]

def parse_ast(
    source: str,
    parser: Callable[[State], State] | None = None,
) -> AstNode:
    return parse(source, AstTreeAlgebra(), parser)

