#!/usr/bin/env python3
"""ToyLang - A tiny programming language interpreter"""

import sys
from dataclasses import dataclass
from enum import Enum
from typing import Any

# =====================
# Token Types
# =====================

class TokenType(Enum):
    INTEGER   = 'INTEGER'
    PLUS      = 'PLUS'
    MINUS     = 'MINUS'
    MUL       = 'MUL'
    DIV       = 'DIV'
    LPAREN    = 'LPAREN'
    RPAREN    = 'RPAREN'
    LBRACE    = 'LBRACE'
    RBRACE    = 'RBRACE'
    SEMI      = 'SEMI'
    ASSIGN    = 'ASSIGN'
    EQ        = 'EQ'
    NEQ       = 'NEQ'
    LT        = 'LT'
    GT        = 'GT'
    LEQ       = 'LEQ'
    GEQ       = 'GEQ'
    IF        = 'IF'
    ELSE      = 'ELSE'
    WHILE     = 'WHILE'
    FUNC      = 'FUNC'
    RETURN    = 'RETURN'
    ID        = 'ID'
    NUMBER    = 'NUMBER'
    COMMA     = 'COMMA'
    EOF       = 'EOF'

@dataclass
class Token:
    type: TokenType
    value: Any
    lineno: int
    col: int

# =====================
# Lexer
# =====================

KEYWORDS = {
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'while': TokenType.WHILE,
    'func': TokenType.FUNC,
    'return': TokenType.RETURN,
}

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.lineno = 1
        self.col = 1

    def error(self, msg: str):
        raise SyntaxError(f"Lexer error at line {self.lineno}, col {self.col}: {msg}")

    def peek(self) -> str | None:
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]

    def advance(self) -> str:
        ch = self.text[self.pos]
        self.pos += 1
        if ch == '\n':
            self.lineno += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def skip_whitespace(self):
        while self.peek() is not None and self.peek() in ' \t\n\r':
            self.advance()

    def skip_comment(self):
        self.advance()
        while self.peek() is not None and self.peek() != '\n':
            self.advance()

    def read_number(self):
        lineno, col = self.lineno, self.col
        num = ''
        while self.peek() is not None and self.peek().isdigit():
            num += self.advance()
        return Token(TokenType.NUMBER, int(num), lineno, col)

    def read_identifier(self):
        lineno, col = self.lineno, self.col
        ident = ''
        while self.peek() is not None and (self.peek().isalnum() or self.peek() == '_'):
            ident += self.advance()
        ttype = KEYWORDS.get(ident, TokenType.ID)
        return Token(ttype, ident, lineno, col)

    def tokenize(self) -> list[Token]:
        tokens = []
        while self.peek() is not None:
            ch = self.peek()
            if ch in ' \t\n\r':
                self.skip_whitespace()
                continue
            if ch == '#':
                self.skip_comment()
                continue
            if ch.isdigit():
                tokens.append(self.read_number())
                continue
            if ch.isalpha() or ch == '_':
                tokens.append(self.read_identifier())
                continue
            lineno, col = self.lineno, self.col
            if ch == '+': self.advance(); tokens.append(Token(TokenType.PLUS, '+', lineno, col))
            elif ch == '-': self.advance(); tokens.append(Token(TokenType.MINUS, '-', lineno, col))
            elif ch == '*': self.advance(); tokens.append(Token(TokenType.MUL, '*', lineno, col))
            elif ch == '/': self.advance(); tokens.append(Token(TokenType.DIV, '/', lineno, col))
            elif ch == '(': self.advance(); tokens.append(Token(TokenType.LPAREN, '(', lineno, col))
            elif ch == ')': self.advance(); tokens.append(Token(TokenType.RPAREN, ')', lineno, col))
            elif ch == '{': self.advance(); tokens.append(Token(TokenType.LBRACE, '{', lineno, col))
            elif ch == '}': self.advance(); tokens.append(Token(TokenType.RBRACE, '}', lineno, col))
            elif ch == ';': self.advance(); tokens.append(Token(TokenType.SEMI, ';', lineno, col))
            elif ch == ',': self.advance(); tokens.append(Token(TokenType.COMMA, ',', lineno, col))
            elif ch == '=':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    tokens.append(Token(TokenType.EQ, '==', lineno, col))
                else:
                    tokens.append(Token(TokenType.ASSIGN, '=', lineno, col))
            elif ch == '!':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    tokens.append(Token(TokenType.NEQ, '!=', lineno, col))
                else:
                    self.error("Expected '=' after '!'")
            elif ch == '<':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    tokens.append(Token(TokenType.LEQ, '<=', lineno, col))
                else:
                    tokens.append(Token(TokenType.LT, '<', lineno, col))
            elif ch == '>':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    tokens.append(Token(TokenType.GEQ, '>=', lineno, col))
                else:
                    tokens.append(Token(TokenType.GT, '>', lineno, col))
            else:
                self.error(f"Unexpected character: {ch}")
        tokens.append(Token(TokenType.EOF, None, self.lineno, self.col))
        return tokens

# =====================
# AST Nodes
# =====================

class ASTNode: pass

@dataclass
class Program(ASTNode): statements: list

@dataclass
class Number(ASTNode): value: int

@dataclass
class BinOp(ASTNode): left: ASTNode; op: str; right: ASTNode

@dataclass
class UnaryOp(ASTNode): op: str; expr: ASTNode

@dataclass
class Var(ASTNode): name: str

@dataclass
class Assign(ASTNode): name: str; expr: ASTNode

@dataclass
class If(ASTNode): condition: ASTNode; then_branch: list; else_branch: list | None = None

@dataclass
class While(ASTNode): condition: ASTNode; body: list

@dataclass
class FuncDef(ASTNode): name: str; params: list[str]; body: list

@dataclass
class Return(ASTNode): expr: ASTNode

@dataclass
class FuncCall(ASTNode): name: str; args: list

@dataclass
class Block(ASTNode): statements: list

# =====================
# Parser
# =====================

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def advance(self) -> Token:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, ttype: TokenType) -> Token:
        tok = self.peek()
        if tok.type != ttype:
            raise SyntaxError(f"Expected {ttype}, got {tok.type} at line {tok.lineno}")
        return self.advance()

    def parse(self) -> Program:
        statements = []
        while self.peek().type != TokenType.EOF:
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self) -> ASTNode:
        tok = self.peek()
        if tok.type == TokenType.FUNC:
            return self.parse_funcdef()
        if tok.type == TokenType.IF:
            return self.parse_if()
        if tok.type == TokenType.WHILE:
            return self.parse_while()
        if tok.type == TokenType.RETURN:
            return self.parse_return()
        if tok.type == TokenType.LBRACE:
            return self.parse_block()
        return self.parse_assign_or_expr()

    def parse_block(self) -> Block:
        self.expect(TokenType.LBRACE)
        statements = []
        while self.peek().type != TokenType.RBRACE:
            statements.append(self.parse_statement())
        self.expect(TokenType.RBRACE)
        return Block(statements)

    def parse_funcdef(self) -> FuncDef:
        self.expect(TokenType.FUNC)
        name = self.expect(TokenType.ID).value
        self.expect(TokenType.LPAREN)
        params = []
        while self.peek().type != TokenType.RPAREN:
            params.append(self.expect(TokenType.ID).value)
            if self.peek().type == TokenType.COMMA:
                self.advance()
        self.expect(TokenType.RPAREN)
        body = self.parse_block().statements
        return FuncDef(name, params, body)

    def parse_if(self) -> If:
        self.expect(TokenType.IF)
        condition = self.parse_expression()
        then_branch = self.parse_block().statements
        else_branch = None
        if self.peek().type == TokenType.ELSE:
            self.advance()
            if self.peek().type == TokenType.IF:
                else_branch = [self.parse_if()]
            else:
                else_branch = self.parse_block().statements
        return If(condition, then_branch, else_branch)

    def parse_while(self) -> While:
        self.expect(TokenType.WHILE)
        condition = self.parse_expression()
        body = self.parse_block().statements
        return While(condition, body)

    def parse_return(self) -> Return:
        self.expect(TokenType.RETURN)
        expr = self.parse_expression()
        self.expect(TokenType.SEMI)
        return Return(expr)

    def parse_assign_or_expr(self) -> ASTNode:
        tok = self.peek()
        if tok.type == TokenType.ID:
            saved_pos = self.pos
            self.advance()
            if self.peek().type == TokenType.ASSIGN:
                self.advance()
                expr = self.parse_expression()
                self.expect(TokenType.SEMI)
                return Assign(tok.value, expr)
            self.pos = saved_pos
        expr = self.parse_expression()
        self.expect(TokenType.SEMI)
        return expr

    PRECEDENCE = {
        TokenType.EQ: 10, TokenType.NEQ: 10,
        TokenType.LT: 20, TokenType.GT: 20, TokenType.LEQ: 20, TokenType.GEQ: 20,
        TokenType.PLUS: 30, TokenType.MINUS: 30,
        TokenType.MUL: 40, TokenType.DIV: 40,
    }

    def parse_expression(self) -> ASTNode:
        return self.parse_binary(0)

    def parse_binary(self, min_prec: int) -> ASTNode:
        left = self.parse_atom()
        while True:
            tok = self.peek()
            if tok.type not in self.PRECEDENCE:
                break
            prec = self.PRECEDENCE[tok.type]
            if prec < min_prec:
                break
            op = self.advance().value
            right = self.parse_binary(prec + 1)
            left = BinOp(left, op, right)
        return left

    def parse_atom(self) -> ASTNode:
        tok = self.peek()
        if tok.type == TokenType.NUMBER:
            self.advance()
            return Number(tok.value)
        if tok.type == TokenType.ID:
            self.advance()
            if self.peek().type == TokenType.LPAREN:
                return self.parse_call(tok.value)
            return Var(tok.value)
        if tok.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        if tok.type == TokenType.MINUS:
            self.advance()
            return UnaryOp('-', self.parse_atom())
        raise SyntaxError(f"Unexpected token: {tok.type} at line {tok.lineno}")

    def parse_call(self, name: str) -> FuncCall:
        self.expect(TokenType.LPAREN)
        args = []
        while self.peek().type != TokenType.RPAREN:
            args.append(self.parse_expression())
            if self.peek().type == TokenType.COMMA:
                self.advance()
        self.expect(TokenType.RPAREN)
        return FuncCall(name, args)

# =====================
# Interpreter
# =====================

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Interpreter:
    def __init__(self):
        self.globals: dict[str, Any] = {}
        self.functions: dict[str, FuncDef] = {}

    def interpret(self, program: Program):
        for stmt in program.statements:
            if isinstance(stmt, FuncDef):
                self.functions[stmt.name] = stmt
        for stmt in program.statements:
            if not isinstance(stmt, FuncDef):
                self.eval(stmt, {})

    def eval(self, node: ASTNode, env: dict[str, Any]):
        if isinstance(node, Number):
            return node.value
        if isinstance(node, Var):
            if node.name in env:
                return env[node.name]
            if node.name in self.globals:
                return self.globals[node.name]
            raise NameError(f"Undefined variable: {node.name}")
        if isinstance(node, UnaryOp):
            return -self.eval(node.expr, env)
        if isinstance(node, BinOp):
            left = self.eval(node.left, env)
            right = self.eval(node.right, env)
            if node.op == '+': return left + right
            if node.op == '-': return left - right
            if node.op == '*': return left * right
            if node.op == '/':
                if right == 0: raise ZeroDivisionError("Division by zero")
                return left // right
            if node.op == '==': return 1 if left == right else 0
            if node.op == '!=': return 1 if left != right else 0
            if node.op == '<': return 1 if left < right else 0
            if node.op == '>': return 1 if left > right else 0
            if node.op == '<=': return 1 if left <= right else 0
            if node.op == '>=': return 1 if left >= right else 0
            raise RuntimeError(f"Unknown operator: {node.op}")
        if isinstance(node, Assign):
            val = self.eval(node.expr, env)
            self.globals[node.name] = val
            return val
        if isinstance(node, If):
            if self.eval(node.condition, env):
                for stmt in node.then_branch: self.eval(stmt, env)
            elif node.else_branch:
                for stmt in node.else_branch: self.eval(stmt, env)
            return
        if isinstance(node, While):
            while self.eval(node.condition, env):
                for stmt in node.body: self.eval(stmt, env)
            return
        if isinstance(node, Block):
            for stmt in node.statements: self.eval(stmt, env)
            return
        if isinstance(node, Return):
            raise ReturnException(self.eval(node.expr, env))
        if isinstance(node, FuncCall):
            if node.name in self.functions:
                func = self.functions[node.name]
                args = [self.eval(a, env) for a in node.args]
                local_env = dict(zip(func.params, args))
                try:
                    for stmt in func.body:
                        self.eval(stmt, local_env)
                except ReturnException as ret:
                    return ret.value
                return None
            if node.name == 'print':
                print(self.eval(node.args[0], env))
                return None
            raise NameError(f"Undefined function: {node.name}")
        if isinstance(node, Program):
            for stmt in node.statements: self.eval(stmt, env)
            return
        raise RuntimeError(f"Unknown node type: {type(node)}")

# =====================
# REPL
# =====================

def repl():
    interp = Interpreter()
    print("ToyLang REPL (type 'exit' to quit)")
    while True:
        try:
            text = input('>> ')
            if text.strip() == 'exit':
                break
            lexer = Lexer(text)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()
            interp.interpret(program)
        except (SyntaxError, NameError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nBye!")
            break

def run_file(path: str):
    with open(path) as f:
        text = f.read()
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    interp = Interpreter()
    interp.interpret(program)

# =====================
# Test
# =====================

def test():
    code = """
    func fib(n) {
        if n <= 1 {
            return n;
        }
        return fib(n-1) + fib(n-2);
    }
    print(fib(10));
    func factorial(n) {
        if n <= 1 {
            return 1;
        }
        return n * factorial(n-1);
    }
    print(factorial(5));
    x = 100;
    y = 200;
    print(x + y);
    func gcd(a, b) {
        if b == 0 {
            return a;
        }
        return gcd(b, a - b * (a / b));
    }
    print(gcd(48, 18));
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    interp = Interpreter()
    interp.interpret(program)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        test()
