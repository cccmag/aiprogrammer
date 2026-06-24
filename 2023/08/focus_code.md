# 迷你編譯器實作

## 前言

本實作用不到 200 行的 Python 程式碼，實現一個完整的編譯器流程：從詞法分析（Tokenizer）、語法分析（Parser）、抽象語法樹（AST）建構到程式碼生成（Code Generator）。這個迷你編譯器支援變數賦值、算術表達式和運算子優先級。

---

## 原始碼

完整的 Python 實作請參考：[_code/compiler.py](_code/compiler.py)

```python
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
        if kind == 'SKIP': continue
        if kind == 'MISMATCH':
            raise SyntaxError(f'Unexpected char: {val!r}')
        tokens.append((kind, val))
    tokens.append(('EOF', ''))
    return tokens
```

Tokenizer 使用具名群組的正則表達式，將字元流轉換為 Token 序列。

```python
# ─── Recursive Descent Parser ──────────────────────────────
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self): return self.tokens[self.pos]

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

    def parse_expr(self): return self.parse_term()

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
```

Parser 是遞迴下降解析器，每個語法規則對應一個方法。它正確處理了運算子優先級。

```python
# ─── Code Generator ─────────────────────────────────────────
class CodeGen:
    def __init__(self):
        self.lines = []
        self.label_num = 0

    def new_label(self): ...

    def emit(self, *parts):
        self.lines.append('  ' + ' '.join(str(p) for p in parts))

    def generate(self, ast):
        if ast.nodetype == 'Program':
            for stmt in ast.stmts: self.generate(stmt)
        elif ast.nodetype == 'Assign':
            val_reg = self.generate(ast.value)
            self.emit(f'STORE {ast.name} {val_reg}')
        elif ast.nodetype == 'BinOp':
            left_reg = self.generate(ast.left)
            right_reg = self.generate(ast.right)
            op_map = {'+':'ADD','-':'SUB','*':'MUL','/':'DIV'}
            result = f'R{self.label_num}'; self.label_num += 1
            self.emit(f'{op_map[ast.op]} {result} {left_reg} {right_reg}')
            return result
        elif ast.nodetype == 'Number':
            r = f'R{self.label_num}'; self.label_num += 1
            self.emit(f'LOADI {r} {ast.value}')
            return r
        elif ast.nodetype == 'Ident':
            r = f'R{self.label_num}'; self.label_num += 1
            self.emit(f'LOAD {r} {ast.name}')
            return r
        return None
```

CodeGen 走訪 AST 並生成類似三地址碼的目標指令。

## 執行結果

```
=== Source ===
x := 3 + 4 * 2;
y := x - 1;
z := x * y + 5;

=== Generated Code ===
  LOADI R0 3
  LOADI R1 4
  LOADI R2 2
  MUL R3 R1 R2
  ADD R4 R0 R3
  STORE x R4
  LOAD R5 x
  LOADI R6 1
  SUB R7 R5 R6
  STORE y R7
  LOAD R8 x
  LOAD R9 y
  MUL R10 R8 R9
  LOADI R11 5
  ADD R12 R10 R11
  STORE z R12
```

## 總結

這個迷你編譯器展示了編譯器的核心概念：從原始碼到目標程式碼的轉換過程中，Tokenization、Parsing、AST、Code Generation 四個階段的協作。你可以修改原始碼或擴充語言特性來加深理解。

## 延伸閱讀

- [迷你編譯器完整程式碼](_code/compiler.py)
- [編譯器設計](https://www.google.com/search?q=compiler+design+principles+techniques+tools)
- [Let's Build a Compiler](https://www.google.com/search?q=Let%27s+Build+a+Compiler+Jack+Crenshaw)

---

*本篇文章為「AI 程式人雜誌 2023 年 8 月號」編譯器理論系列補充文章。*
