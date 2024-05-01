from typing import TypeVar, Callable, overload

from .peco.peco import *

from .typing.enum import Enum
from .typing.struct import Struct
from .typing.unknown import Unknown, UnresolvedName
from .typing.fn import Fn
from .typing.application import Application
from .typing.assoc import AccessAssoc

from .ast.algebra import AstAlgebra
from .ast.tree import AstNode, AstTreeAlgebra
from .ast.typedef import TypedefItem
from .ast.operator import Operator
from .ast.let_in_item import LetInItem

from frozendict import frozendict
from string import hexdigits

hex_digit = one_of(hexdigits)
ws = many(space)
tok = lambda f: memo(seq(ws, f))
skip = lambda c: tok(sym(c))
repeat = lambda f, n: seq(*(f for _ in range(n)))
break_char = some(space)

kw = lambda f: memo(seq(ws, sym(f), break_char))

tp = lambda s: tp(s)

name_start = alt(letter, sym('_'))
name_rest = alt(name_start, digit, one_of("'!?"))
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

mkint = to_alg(lambda alg, val: alg.int(val))
number = alt(
    seq(sym('0x'), cite(some(hex_digit)), to(lambda x: int(x, 16))),
    seq(cite(some(digit)), to(lambda x: int(x))),
)
boolean = alt(
    seq(sym('true'), to_alg(lambda alg: alg.bool(True))),
    seq(sym('false'), to_alg(lambda alg: alg.bool(False))),
)

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
name_tp = seq(tok(name), to(lambda n: UnresolvedName(n)))
application_tp = seq(
    tp,
    skip('['),
    group(list_of(tp, comma)),
    opt(comma),
    skip(']'),
    to(lambda lhs, args: Application(lhs, args))
)
assoc_tp = seq(
    tp,
    skip('.'),
    name,
    to(lambda lhs, what: AccessAssoc(lhs, what))
)

tp = left(alt(
    unknown_tp,
    struct_tp,
    fn_tp,
    enum_tp,
    application_tp,
    assoc_tp,
    name_tp,
))

expr = lambda s: expr(s)

typedef_item_args = seq(
    skip('['),
    list_of(name, comma),
    opt(comma),
    skip(']'),
)
typedef_item = seq(
    tok(name),
    group(opt(typedef_item_args)),
    skip('='),
    tp,
    skip(';'),
    to(lambda n, args, rhs: TypedefItem(n, args, rhs))
)
typedef = seq(
    kw('type'),
    group(some(typedef_item)),
    kw('in'),
    expr,
    to_alg(lambda alg, items, where: alg.typedef(items, where))
)

factor = alt(
    tok(seq(number, mkint)),
    tok(boolean),
    tok(var),
    tok(string),
    seq(
        skip('('),
        expr,
        skip(')'),
    ),
)
mkbop = lambda op: to_alg(lambda alg, lhs, rhs: alg.binary(lhs, rhs, op))

pat = tok(name)

dot_op = lambda s: dot_op(s)
dot_op = left(alt(
    seq(dot_op, skip('.'), name, to_alg(lambda alg, lhs, rhs: alg.binary(lhs, alg.string(rhs), Operator.DOT))),
    factor,
))

application = seq(
    dot_op,
    some(space),
    group(list_of(dot_op, some(space))),
    to_alg(lambda alg, what, args: alg.application(what, args))
)

let_in_item_rhs_type = alt(
    seq(skip(':'), tp),
    to(lambda: Unknown())
)
let_in_item = seq(
    pat,
    let_in_item_rhs_type,
    skip('='),
    expr,
    skip(';'),
    to(lambda p, rhs_tp, val: LetInItem(p, rhs_tp, val))
)
let_in = seq(
    kw('let'),
    group(some(let_in_item)),
    kw('in'),
    expr,
    to_alg(lambda alg, items, where: alg.let_in(items, where))
)

special = alt(
    let_in,
    application,
    dot_op,
)

term = lambda s: term(s)
term = left(alt(
    seq(term, skip('*'), special, mkbop(Operator.MUL)),
    seq(term, skip('/'), special, mkbop(Operator.DIV)),
    special,
))

addsub = lambda s: term(s)
addsub = left(alt(
    seq(addsub, skip('+'), term, mkbop(Operator.ADD)),
    seq(addsub, skip('-'), term, mkbop(Operator.SUB)),
    term,
))

pre_lowest = addsub
# Lowest priority
apply_op = lambda s: apply_op(s)
apply_op = alt(
    seq(pre_lowest, skip('$'), apply_op, mkbop(Operator.APPLY)),
    pre_lowest,
)

expr = alt(
    typedef,
    apply_op,
)

Repr = TypeVar("Repr")
def parse(
    source: str,
    algebra: AstAlgebra[Repr],
    parser: Callable[[State], State] | None = None,
) -> Repr:
    if parser is None:
        parser = let_in

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

