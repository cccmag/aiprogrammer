#!/usr/bin/env python3
"""MiniSQL - A minimal in-memory SQL database engine"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import re

# =====================
# Token Types
# =====================

class TokenType(Enum):
    CREATE = 'CREATE'
    TABLE = 'TABLE'
    INSERT = 'INSERT'
    INTO = 'INTO'
    VALUES = 'VALUES'
    SELECT = 'SELECT'
    FROM = 'FROM'
    WHERE = 'WHERE'
    AND = 'AND'
    OR = 'OR'
    DELETE = 'DELETE'
    DROP = 'DROP'
    INT = 'INT'
    TEXT = 'TEXT'
    FLOAT = 'FLOAT'
    ID = 'ID'
    NUMBER = 'NUMBER'
    STRING = 'STRING'
    STAR = 'STAR'
    COMMA = 'COMMA'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    SEMI = 'SEMI'
    EQ = 'EQ'
    NEQ = 'NEQ'
    LT = 'LT'
    GT = 'GT'
    LE = 'LE'
    GE = 'GE'
    EOF = 'EOF'

@dataclass
class Token:
    type: TokenType
    value: Any
    lineno: int
    col: int

# =====================
# Keywords
# =====================

KEYWORDS = {
    'create': TokenType.CREATE, 'table': TokenType.TABLE,
    'insert': TokenType.INSERT, 'into': TokenType.INTO,
    'values': TokenType.VALUES, 'select': TokenType.SELECT,
    'from': TokenType.FROM, 'where': TokenType.WHERE,
    'and': TokenType.AND, 'or': TokenType.OR,
    'delete': TokenType.DELETE, 'drop': TokenType.DROP,
    'int': TokenType.INT, 'text': TokenType.TEXT,
    'float': TokenType.FLOAT,
}

# =====================
# Lexer
# =====================

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.lineno = 1
        self.col = 1

    def advance(self):
        if self.pos < len(self.text):
            ch = self.text[self.pos]
            self.pos += 1
            if ch == '\n':
                self.lineno += 1
                self.col = 1
            else:
                self.col += 1
            return ch
        return ''

    def peek(self):
        if self.pos < len(self.text):
            return self.text[self.pos]
        return ''

    def skip_whitespace(self):
        while self.pos < len(self.text) and self.text[self.pos] in ' \t\n\r':
            self.advance()

    def read_identifier(self):
        ch = self.advance()
        ident = ch
        while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == '_'):
            ident += self.advance()
        lower = ident.lower()
        ttype = KEYWORDS.get(lower, TokenType.ID)
        return Token(ttype, ident, self.lineno, self.col - len(ident))

    def read_number(self):
        num = ''
        while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == '.'):
            num += self.advance()
        if '.' in num:
            return Token(TokenType.NUMBER, float(num), self.lineno, self.col - len(num))
        return Token(TokenType.NUMBER, int(num), self.lineno, self.col - len(num))

    def read_string(self):
        quote = self.advance()
        s = ''
        while self.pos < len(self.text) and self.text[self.pos] != quote:
            s += self.advance()
        self.advance()
        return Token(TokenType.STRING, s, self.lineno, self.col - len(s) - 2)

    def tokenize(self):
        tokens = []
        while self.pos < len(self.text):
            ch = self.text[self.pos]
            if ch in ' \t\n\r':
                self.skip_whitespace()
                continue
            if ch.isalpha() or ch == '_':
                tokens.append(self.read_identifier())
            elif ch.isdigit():
                tokens.append(self.read_number())
            elif ch in '"\'':
                tokens.append(self.read_string())
            elif ch == '*':
                tokens.append(Token(TokenType.STAR, '*', self.lineno, self.col))
                self.advance()
            elif ch == ',':
                tokens.append(Token(TokenType.COMMA, ',', self.lineno, self.col))
                self.advance()
            elif ch == '(':
                tokens.append(Token(TokenType.LPAREN, '(', self.lineno, self.col))
                self.advance()
            elif ch == ')':
                tokens.append(Token(TokenType.RPAREN, ')', self.lineno, self.col))
                self.advance()
            elif ch == ';':
                tokens.append(Token(TokenType.SEMI, ';', self.lineno, self.col))
                self.advance()
            elif ch == '=':
                tokens.append(Token(TokenType.EQ, '=', self.lineno, self.col))
                self.advance()
            elif ch == '!':
                self.advance()
                if self.pos < len(self.text) and self.text[self.pos] == '=':
                    tokens.append(Token(TokenType.NEQ, '!=', self.lineno, self.col))
                    self.advance()
                else:
                    raise SyntaxError(f"Unexpected character ! at line {self.lineno}")
            elif ch == '<':
                self.advance()
                if self.pos < len(self.text) and self.text[self.pos] == '=':
                    tokens.append(Token(TokenType.LE, '<=', self.lineno, self.col))
                    self.advance()
                else:
                    tokens.append(Token(TokenType.LT, '<', self.lineno, self.col))
            elif ch == '>':
                self.advance()
                if self.pos < len(self.text) and self.text[self.pos] == '=':
                    tokens.append(Token(TokenType.GE, '>=', self.lineno, self.col))
                    self.advance()
                else:
                    tokens.append(Token(TokenType.GT, '>', self.lineno, self.col))
            else:
                raise SyntaxError(f"Unexpected character {ch} at line {self.lineno}")
        tokens.append(Token(TokenType.EOF, None, self.lineno, self.col))
        return tokens

# =====================
# AST Nodes
# =====================

@dataclass
class ColumnDef:
    name: str
    col_type: str

@dataclass
class CreateTable:
    table_name: str
    columns: list

@dataclass
class InsertInto:
    table_name: str
    values: list

@dataclass
class Select:
    columns: list
    table_name: str
    where: Any = None

@dataclass
class BinOp:
    op: str
    left: Any
    right: Any

@dataclass
class Literal:
    value: Any

@dataclass
class Column:
    name: str

# =====================
# Parser
# =====================

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, ttype):
        tok = self.peek()
        if tok.type != ttype:
            raise SyntaxError(f"Expected {ttype}, got {tok.type} ({tok.value}) at line {tok.lineno}")
        return self.advance()

    def parse(self):
        stmt = None
        tok = self.peek()
        if tok.type == TokenType.CREATE:
            stmt = self.parse_create()
        elif tok.type == TokenType.INSERT:
            stmt = self.parse_insert()
        elif tok.type == TokenType.SELECT:
            stmt = self.parse_select()
        elif tok.type == TokenType.DELETE:
            stmt = self.parse_delete()
        elif tok.type == TokenType.DROP:
            stmt = self.parse_drop()
        else:
            raise SyntaxError(f"Unexpected token {tok.type} at line {tok.lineno}")
        self.expect(TokenType.SEMI)
        return stmt

    def parse_create(self):
        self.expect(TokenType.CREATE)
        self.expect(TokenType.TABLE)
        table_name = self.expect(TokenType.ID).value
        self.expect(TokenType.LPAREN)
        columns = []
        while self.peek().type != TokenType.RPAREN:
            col_name = self.expect(TokenType.ID).value
            type_tok = self.advance()
            if type_tok.type == TokenType.INT:
                col_type = 'INT'
            elif type_tok.type == TokenType.TEXT:
                col_type = 'TEXT'
            elif type_tok.type == TokenType.FLOAT:
                col_type = 'FLOAT'
            else:
                raise SyntaxError(f"Expected type, got {type_tok.type}")
            columns.append(ColumnDef(col_name, col_type))
            if self.peek().type == TokenType.COMMA:
                self.advance()
        self.expect(TokenType.RPAREN)
        return CreateTable(table_name, columns)

    def parse_insert(self):
        self.expect(TokenType.INSERT)
        self.expect(TokenType.INTO)
        table_name = self.expect(TokenType.ID).value
        self.expect(TokenType.VALUES)
        self.expect(TokenType.LPAREN)
        values = []
        while self.peek().type != TokenType.RPAREN:
            tok = self.advance()
            if tok.type == TokenType.NUMBER:
                values.append(Literal(tok.value))
            elif tok.type == TokenType.STRING:
                values.append(Literal(tok.value))
            else:
                raise SyntaxError(f"Unexpected token in values: {tok.type}")
            if self.peek().type == TokenType.COMMA:
                self.advance()
        self.expect(TokenType.RPAREN)
        return InsertInto(table_name, values)

    def parse_select(self):
        self.expect(TokenType.SELECT)
        columns = []
        if self.peek().type == TokenType.STAR:
            self.advance()
            columns.append('*')
        else:
            col = self.expect(TokenType.ID).value
            columns.append(col)
            while self.peek().type == TokenType.COMMA:
                self.advance()
                col = self.expect(TokenType.ID).value
                columns.append(col)
        self.expect(TokenType.FROM)
        table_name = self.expect(TokenType.ID).value
        where = None
        if self.peek().type == TokenType.WHERE:
            self.advance()
            where = self.parse_condition()
        return Select(columns, table_name, where)

    def parse_condition(self):
        left = Column(self.expect(TokenType.ID).value)
        op_tok = self.advance()
        op_map = {
            TokenType.EQ: '=', TokenType.NEQ: '!=',
            TokenType.LT: '<', TokenType.GT: '>',
            TokenType.LE: '<=', TokenType.GE: '>=',
        }
        op = op_map.get(op_tok.type)
        if op is None:
            raise SyntaxError(f"Expected comparison operator, got {op_tok.type}")
        right_tok = self.advance()
        if right_tok.type == TokenType.NUMBER:
            right = Literal(right_tok.value)
        elif right_tok.type == TokenType.STRING:
            right = Literal(right_tok.value)
        elif right_tok.type == TokenType.ID:
            right = Column(right_tok.value)
        else:
            raise SyntaxError(f"Unexpected token: {right_tok.type}")
        node = BinOp(op, left, right)
        while self.peek().type in (TokenType.AND, TokenType.OR):
            log_op = 'AND' if self.advance().type == TokenType.AND else 'OR'
            right_cond = self.parse_condition()
            node = BinOp(log_op, node, right_cond)
        return node

    def parse_delete(self):
        self.expect(TokenType.DELETE)
        self.expect(TokenType.FROM)
        table_name = self.expect(TokenType.ID).value
        where = None
        if self.peek().type == TokenType.WHERE:
            self.advance()
            where = self.parse_condition()
        return Delete(table_name, where)

    def parse_drop(self):
        self.expect(TokenType.DROP)
        self.expect(TokenType.TABLE)
        table_name = self.expect(TokenType.ID).value
        return DropTable(table_name)

@dataclass
class Delete:
    table_name: str
    where: Any = None

@dataclass
class DropTable:
    table_name: str

# =====================
# Database Engine
# =====================

class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns
        self.rows = []

class Database:
    def __init__(self):
        self.tables = {}

    def execute(self, stmt):
        if isinstance(stmt, CreateTable):
            return self._create_table(stmt)
        elif isinstance(stmt, InsertInto):
            return self._insert(stmt)
        elif isinstance(stmt, Select):
            return self._select(stmt)
        elif isinstance(stmt, Delete):
            return self._delete(stmt)
        elif isinstance(stmt, DropTable):
            return self._drop_table(stmt)
        raise ValueError(f"Unknown statement: {type(stmt)}")

    def _create_table(self, stmt):
        if stmt.table_name in self.tables:
            return f'Error: Table "{stmt.table_name}" already exists'
        self.tables[stmt.table_name] = Table(stmt.table_name, stmt.columns)
        return f'OK: Table "{stmt.table_name}" created'

    def _insert(self, stmt):
        table = self.tables.get(stmt.table_name)
        if not table:
            return f'Error: Table "{stmt.table_name}" not found'
        if len(stmt.values) != len(table.columns):
            return f'Error: Expected {len(table.columns)} values, got {len(stmt.values)}'
        row = []
        for val, col in zip(stmt.values, table.columns):
            v = val.value
            if col.col_type == 'INT':
                v = int(v)
            elif col.col_type == 'FLOAT':
                v = float(v)
            elif col.col_type == 'TEXT':
                v = str(v)
            row.append(v)
        table.rows.append(row)
        return f'OK: 1 row inserted into "{stmt.table_name}"'

    def _eval_condition(self, cond, row, table):
        if isinstance(cond, BinOp):
            if cond.op in ('AND', 'OR'):
                left = self._eval_condition(cond.left, row, table)
                right = self._eval_condition(cond.right, row, table)
                if cond.op == 'AND':
                    return left and right
                return left or right
            left = self._get_value(cond.left, row, table)
            right = self._get_value(cond.right, row, table)
            if cond.op == '=':
                return left == right
            elif cond.op == '!=':
                return left != right
            elif cond.op == '<':
                return left < right
            elif cond.op == '>':
                return left > right
            elif cond.op == '<=':
                return left <= right
            elif cond.op == '>=':
                return left >= right
        return True

    def _get_value(self, node, row, table):
        if isinstance(node, Column):
            for i, col in enumerate(table.columns):
                if col.name == node.name:
                    return row[i]
            raise ValueError(f"Column {node.name} not found")
        if isinstance(node, Literal):
            return node.value
        return None

    def _select(self, stmt):
        table = self.tables.get(stmt.table_name)
        if not table:
            return f'Error: Table "{stmt.table_name}" not found'
        result = []
        if stmt.columns == ['*']:
            col_names = [c.name for c in table.columns]
            for row in table.rows:
                if stmt.where and not self._eval_condition(stmt.where, row, table):
                    continue
                result.append(row)
        else:
            col_names = stmt.columns
            col_indices = []
            for c in stmt.columns:
                found = False
                for i, col in enumerate(table.columns):
                    if col.name == c:
                        col_indices.append(i)
                        found = True
                        break
                if not found:
                    return f'Error: Column "{c}" not found'
            for row in table.rows:
                if stmt.where and not self._eval_condition(stmt.where, row, table):
                    continue
                selected = [row[i] for i in col_indices]
                result.append(selected)
        return QueryResult(col_names, result, table)

    def _delete(self, stmt):
        table = self.tables.get(stmt.table_name)
        if not table:
            return f'Error: Table "{stmt.table_name}" not found'
        before = len(table.rows)
        if stmt.where:
            table.rows = [r for r in table.rows
                          if not self._eval_condition(stmt.where, r, table)]
        else:
            table.rows = []
        deleted = before - len(table.rows)
        return f'OK: {deleted} rows deleted from "{stmt.table_name}"'

    def _drop_table(self, stmt):
        if stmt.table_name not in self.tables:
            return f'Error: Table "{stmt.table_name}" not found'
        del self.tables[stmt.table_name]
        return f'OK: Table "{stmt.table_name}" dropped'

@dataclass
class QueryResult:
    columns: list
    rows: list
    table: Table = None

    def __str__(self):
        if not self.rows:
            return '(0 rows)'
        col_widths = []
        for i, name in enumerate(self.columns):
            data_widths = [len(str(r[i])) for r in self.rows] if self.rows else [0]
            col_widths.append(max(len(name), max(data_widths)))
        sep = '+' + '+'.join('-' * (w + 2) for w in col_widths) + '+'
        header = '|' + '|'.join(f' {c:<{w}} ' for c, w in zip(self.columns, col_widths)) + '|'
        lines = [sep, header, sep]
        for row in self.rows:
            line = '|' + '|'.join(f' {str(row[i]):<{col_widths[i]}} ' for i in range(len(self.columns))) + '|'
            lines.append(line)
        lines.append(sep)
        lines.append(f'({len(self.rows)} rows)')
        return '\n'.join(lines)

# =====================
# REPL
# =====================

def repl():
    db = Database()
    print("MiniSQL v1.0")
    print("Enter SQL statements (end with ;). Type 'exit' to quit.")
    print()
    buffer = ''
    while True:
        try:
            line = input('sql> ' if not buffer else '...> ')
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if line.lower() in ('exit', 'quit'):
            break
        buffer += line + ' '
        if ';' not in line:
            continue
        try:
            lexer = Lexer(buffer)
            tokens = lexer.tokenize()
            pos = 0
            while pos < len(tokens) - 1:
                token_slice = tokens[pos:]
                parser = Parser(token_slice)
                stmt = parser.parse()
                pos += parser.pos
                result = db.execute(stmt)
                print(result)
                print()
            buffer = ''
        except (SyntaxError, ValueError) as e:
            print(f'Error: {e}')
            print()
            buffer = ''

# =====================
# Test
# =====================

def test():
    db = Database()
    sqls = [
        "CREATE TABLE employee (id INT, name TEXT, salary INT);",
        "INSERT INTO employee VALUES (1, 'Alice', 75000);",
        "INSERT INTO employee VALUES (2, 'Bob', 68000);",
        "INSERT INTO employee VALUES (3, 'Charlie', 82000);",
        "INSERT INTO employee VALUES (4, 'Diana', 95000);",
        "INSERT INTO employee VALUES (5, 'Eve', 72000);",
        "SELECT * FROM employee;",
        "SELECT name, salary FROM employee WHERE salary > 75000;",
        "SELECT name FROM employee WHERE salary >= 72000 AND salary <= 82000;",
        "DELETE FROM employee WHERE name = 'Eve';",
        "SELECT * FROM employee;",
        "DROP TABLE employee;",
    ]
    for sql in sqls:
        print(f"SQL: {sql}")
        lexer = Lexer(sql)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        stmt = parser.parse()
        result = db.execute(stmt)
        print(result)
        print()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'repl':
        repl()
    else:
        test()
