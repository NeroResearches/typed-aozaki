from argparse import ArgumentParser
from pprint import pprint

from .parser import parse_ast

parser = ArgumentParser(
    prog='aozaki',
    description='typed version of aozaki'
)
parser.add_argument('filename', nargs='?', help='run this file')

args = parser.parse_args()

if args.filename is None:
    raise NotImplementedError("REPL")

with open(args.filename) as fp:
    source = fp.read()

print('Text')
print('======================')
print(source)

print("\n", "AST")
print("======================")

ast = parse_ast(source)

pprint(ast)


