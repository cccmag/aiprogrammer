#!/usr/bin/env python3
"""A tiny compiler: tokenizer, recursive descent parser, AST, code generator"""

import re

# ─── Tokenizer ───────────────────────────────────────────────
TOKEN_SPEC = [
    ('NUMBER',  r'\d+'),
    ('IDENT',   r'[a-zA-Z_]\w*'),
    ('ASSIGN',  r':='),
    ('PLUS',    r'\+'),
    ('MINUS',   r'-'),
    ('STAR',    r'\*'),
    ('SLASH',   r'/'),
    ('LPAREN',  r'\('),
    ('RPAREN',  r'\)'),
    ('SEMI',    r';'),
    ('SKIP',    r'[ \t\n]+'),
    ('MISMATCH', r'.'),
]
TOKEN_RE = re.compile('|'.join(f'(?P<{n}>{p})' for n, p in TOKEN_SPEC))

def tokenize(text):
    tokens = []
    for m in TOKEN_RE.finditer(text):
        kind = m.lastgroup
        val = m.group()
        if kind == 'SKIP':
            continue
        if kind == 'MISMATCH':
            raise SyntaxError(f'Unexpected char: {val!r}')
        tokens.append((kind, val))
    tokens.append(('EOF', ''))
    return tokens

# ─── AST Nodes ──────────────────────────────────────────────
class AST:
    def __init__(self, nodetype, **attrs):
        self.nodetype = nodetype
        self.__dict__.update(attrs)

    def __repr__(self):
        a = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items() if k != 'nodetype')
        return f'{self.nodetype}({a})'

# ─── Recursive Descent Parser ──────────────────────────────
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def consume(self, expected=None):
        tok = self.peek()
        if expected and tok[1] != expected and tok[0] != expected:
            raise SyntaxError(f'Expected {expected}, got {tok[1]}')
        self.pos += 1
        return tok

    def parse(self):
        stmts = []
        while self.peek()[0] != 'EOF':
            stmts.append(self.parse_stmt())
        return AST('Program', stmts=stmts)

    def parse_stmt(self):
        if self.peek()[0] == 'IDENT' and self.tokens[self.pos+1][0] == 'ASSIGN':
            return self.parse_assign()
        return self.parse_expr_stmt()

    def parse_assign(self):
        name = self.consume('IDENT')[1]
        self.consume('ASSIGN')
        val = self.parse_expr()
        self.consume('SEMI')
        return AST('Assign', name=name, value=val)

    def parse_expr_stmt(self):
        expr = self.parse_expr()
        if self.peek()[0] == 'SEMI':
            self.consume('SEMI')
        return AST('ExprStmt', expr=expr)

    def parse_expr(self):
        return self.parse_term()

    def parse_term(self):
        left = self.parse_factor()
        while self.peek()[1] in ('+', '-'):
            op = self.consume()[1]
            right = self.parse_factor()
            left = AST('BinOp', op=op, left=left, right=right)
        return left

    def parse_factor(self):
        left = self.parse_primary()
        while self.peek()[1] in ('*', '/'):
            op = self.consume()[1]
            right = self.parse_primary()
            left = AST('BinOp', op=op, left=left, right=right)
        return left

    def parse_primary(self):
        tok = self.peek()
        if tok[0] == 'NUMBER':
            self.consume()
            return AST('Number', value=int(tok[1]))
        if tok[0] == 'IDENT':
            self.consume()
            return AST('Ident', name=tok[1])
        if tok[1] == '(':
            self.consume('LPAREN')
            expr = self.parse_expr()
            self.consume('RPAREN')
            return expr
        raise SyntaxError(f'Unexpected token: {tok}')

# ─── Code Generator ─────────────────────────────────────────
class CodeGen:
    def __init__(self):
        self.lines = []
        self.label_num = 0

    def new_label(self):
        self.label_num += 1
        return f'L{self.label_num}'

    def emit(self, *parts):
        self.lines.append('  ' + ' '.join(str(p) for p in parts))

    def generate(self, ast):
        if ast.nodetype == 'Program':
            for stmt in ast.stmts:
                self.generate(stmt)
        elif ast.nodetype == 'Assign':
            val_reg = self.generate(ast.value)
            self.emit(f'STORE {ast.name} {val_reg}')
        elif ast.nodetype == 'ExprStmt':
            self.generate(ast.expr)
        elif ast.nodetype == 'BinOp':
            left_reg = self.generate(ast.left)
            right_reg = self.generate(ast.right)
            op_map = {'+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV'}
            result = f'R{self.label_num}'
            self.label_num += 1
            self.emit(f'{op_map[ast.op]} {result} {left_reg} {right_reg}')
            return result
        elif ast.nodetype == 'Number':
            r = f'R{self.label_num}'
            self.label_num += 1
            self.emit(f'LOADI {r} {ast.value}')
            return r
        elif ast.nodetype == 'Ident':
            r = f'R{self.label_num}'
            self.label_num += 1
            self.emit(f'LOAD {r} {ast.name}')
            return r
        return None

    def output(self):
        return '\n'.join(self.lines)

# ─── Demo ──────────────────────────────────────────────────
def demo():
    source = """
    x := 3 + 4 * 2;
    y := x - 1;
    z := x * y + 5;
    """
    print("=== Source ===")
    print(source.strip())

    tokens = tokenize(source)
    print("\n=== Tokens ===")
    for tok in tokens:
        print(f'  {tok}')

    parser = Parser(tokens)
    ast = parser.parse()
    print("\n=== AST ===")
    def show_ast(node, indent=0):
        prefix = '  ' * indent
        if isinstance(node, AST):
            attrs = {k: v for k, v in node.__dict__.items() if k != 'nodetype'}
            print(f'{prefix}{node.nodetype}:')
            for k, v in attrs.items():
                if isinstance(v, list):
                    print(f'{prefix}  {k}:')
                    for item in v:
                        show_ast(item, indent + 2)
                elif isinstance(v, AST):
                    print(f'{prefix}  {k}:')
                    show_ast(v, indent + 2)
                else:
                    print(f'{prefix}  {k} = {v!r}')
    show_ast(ast)

    cg = CodeGen()
    cg.generate(ast)
    print("\n=== Generated Code ===")
    print(cg.output())

if __name__ == '__main__':
    demo()
