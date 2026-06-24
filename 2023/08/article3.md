# 遞迴下降解析器實作

## 前言

遞迴下降解析器（Recursive Descent Parser）是實現編譯器語法分析最直覺的方式。每個非終結符對應一個方法，方法之間透過相互呼叫來實現文法的遞迴結構。本文實作一個完整的遞迴下降解析器。

## 文法設計

我們的目標語言是簡單的賦值語句和算術表達式：

```
program  → stmt*
stmt     → assign | expr_stmt
assign   → IDENT := expr ;
expr_stmt → expr ;
expr     → term {+ term}
term     → factor {* factor}
factor   → NUMBER | IDENT | ( expr )
```

這個文法正確處理了運算子優先級：乘法優先於加法，括號可以改變優先級。

## Parser 結構

```python
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens      # Token 序列
        self.pos = 0              # 當前位置
    
    def peek(self):
        return self.tokens[self.pos]
    
    def consume(self, kind=None):
        """消費當前 Token，可選地檢查型別"""
        tok = self.peek()
        if kind and tok.kind != kind:
            raise SyntaxError(f'Expected {kind}, got {tok.kind}')
        self.pos += 1
        return tok
```

## 解析方法

### 程式

```python
def parse_program(self):
    stmts = []
    while self.peek().kind != TokenKind.EOF:
        stmts.append(self.parse_stmt())
    return AST('Program', stmts=stmts)
```

### 陳述式

```python
def parse_stmt(self):
    """判斷是賦值還是表達式陳述式"""
    tok = self.peek()
    # 前瞻兩個 Token：IDENT + ASSIGN → 賦值
    if tok.kind == TokenKind.IDENT and \
       self.tokens[self.pos+1].kind == TokenKind.ASSIGN:
        return self.parse_assign()
    return self.parse_expr_stmt()
```

### 賦值

```python
def parse_assign(self):
    name = self.consume(TokenKind.IDENT).value
    self.consume(TokenKind.ASSIGN)
    value = self.parse_expr()
    self.consume(TokenKind.SEMI)
    return AST('Assign', name=name, value=value)
```

### 表達式

```python
def parse_expr(self):
    left = self.parse_term()
    while self.peek().kind in (TokenKind.PLUS, TokenKind.MINUS):
        op = self.consume().value
        right = self.parse_term()
        left = AST('BinOp', op=op, left=left, right=right)
    return left
```

### 項

```python
def parse_term(self):
    left = self.parse_factor()
    while self.peek().kind in (TokenKind.STAR, TokenKind.SLASH):
        op = self.consume().value
        right = self.parse_factor()
        left = AST('BinOp', op=op, left=left, right=right)
    return left
```

### 因子（基礎表達式）

```python
def parse_factor(self):
    tok = self.peek()
    if tok.kind == TokenKind.NUMBER:
        self.consume()
        return AST('Number', value=int(tok.value))
    elif tok.kind == TokenKind.IDENT:
        self.consume()
        return AST('Ident', name=tok.value)
    elif tok.kind == TokenKind.LPAREN:
        self.consume()
        expr = self.parse_expr()
        self.consume(TokenKind.RPAREN)
        return expr
    raise SyntaxError(f'Unexpected: {tok}')
```

## 完整解析流程

```python
def parse(self, tokens):
    self.tokens = tokens
    self.pos = 0
    return self.parse_program()
```

對於輸入 `x := 3 + 4 * 2;`，解析器會產生以下 AST：

```
Program:
  Assign:
    name = 'x'
    value:
      BinOp(+):
        Number(3)
        BinOp(*):
          Number(4)
          Number(2)
```

注意乘法的優先級被正確保留：`4 * 2` 是 `BinOp(*)` 的子樹，作為 `+` 的右運算元。

## 常見問題與處理

### 左遞迴

遞迴下降解析器不能處理左遞迴。文法需要改寫：

```
# 左遞迴（無法處理）
E → E + T | T

# 改寫為右遞迴（可處理）
E → T E'
E' → + T E' | ε
```

或者使用疊代方式（如本文使用 while 循環）。

### 回溯

嚴格的 LL(1) 解析器需要避免回溯，但實務上可以透過前瞻多個 Token 來解決歧義。

## 結語

遞迴下降解析器是編譯器開發的必備技能。實作簡單、易於理解和除錯，是教學和生產環境的常見選擇。掌握每個非終結符對應一個方法的設計模式後，你可以輕鬆實現任何程式的語法分析器。

## 延伸閱讀

- [遞迴下降解析技術](https://www.google.com/search?q=recursive+descent+parsing+techniques)
- [ANTLR 與訪客模式](https://www.google.com/search?q=ANTLR+visitor+pattern+parse+tree)

---

*本篇文章為「AI 程式人雜誌 2023 年 8 月號」編譯器理論系列文章。*
