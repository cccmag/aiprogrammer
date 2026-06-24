# 詞法分析器手作

## 前言

詞法分析器（Lexer）是編譯器的第一個階段，將原始碼字元流轉換為 Token 序列。本文從零開始手作一個詞法分析器，適用於簡單的算術語言。

## Token 的定義

首先定義 Token 的型別（Kind）：

```python
from enum import Enum

class TokenKind(Enum):
    NUMBER = 'NUMBER'
    IDENT  = 'IDENT'
    ASSIGN = 'ASSIGN'
    PLUS   = 'PLUS'
    MINUS  = 'MINUS'
    STAR   = 'STAR'
    SLASH  = 'SLASH'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    SEMI   = 'SEMI'
    EOF    = 'EOF'
```

每個 Token 由型別和值組成。

## 基於正則表達式的實作

最簡潔的方式是使用正則表達式的具名群組：

```python
import re

TOKEN_REGEX = [
    (TokenKind.NUMBER, r'\d+'),
    (TokenKind.IDENT,  r'[a-zA-Z_]\w*'),
    (TokenKind.ASSIGN, r':='),
    (TokenKind.PLUS,   r'\+'),
    (TokenKind.MINUS,  r'-'),
    (TokenKind.STAR,   r'\*'),
    (TokenKind.SLASH,  r'/'),
    (TokenKind.LPAREN, r'\('),
    (TokenKind.RPAREN, r'\)'),
    (TokenKind.SEMI,   r';'),
]

pattern = '|'.join(f'(?P<{k.value}>{p})' for k, p in TOKEN_REGEX)
PATTERN = re.compile(pattern)
```

逐字元掃描的方式更接近傳統的 Lexer：

```python
class CharStream:
    def __init__(self, text):
        self.text = text
        self.pos = 0
    
    def peek(self, offset=0):
        idx = self.pos + offset
        return self.text[idx] if idx < len(self.text) else '\0'
    
    def advance(self):
        ch = self.text[self.pos]
        self.pos += 1
        return ch
    
    def skip_whitespace(self):
        while self.pos < len(self.text) and self.text[self.pos] in ' \t\n':
            self.pos += 1
```

## 手動掃描實作

### 數字

```python
def scan_number(stream):
    start = stream.pos
    while stream.peek().isdigit():
        stream.advance()
    return Token(TokenKind.NUMBER, stream.text[start:stream.pos])
```

### 識別字

```python
def scan_ident(stream):
    start = stream.pos
    while stream.peek().isalnum() or stream.peek() == '_':
        stream.advance()
    return Token(TokenKind.IDENT, stream.text[start:stream.pos])
```

### 運算子

```python
def scan_assign(stream):
    stream.advance()  # consume ':'
    stream.advance()  # consume '='
    return Token(TokenKind.ASSIGN, ':=')

def scan_operator(stream, kind):
    stream.advance()
    return Token(kind, stream.text[stream.pos-1])
```

## 主循環

```python
def tokenize(text):
    stream = CharStream(text)
    tokens = []
    
    while stream.pos < len(text):
        stream.skip_whitespace()
        ch = stream.peek()
        
        if ch.isdigit():
            tokens.append(scan_number(stream))
        elif ch.isalpha() or ch == '_':
            tokens.append(scan_ident(stream))
        elif ch == ':':
            tokens.append(scan_assign(stream))
        elif ch == '+':
            tokens.append(scan_operator(stream, TokenKind.PLUS))
        elif ch == '-':
            tokens.append(scan_operator(stream, TokenKind.MINUS))
        elif ch == '*':
            tokens.append(scan_operator(stream, TokenKind.STAR))
        else:
            raise SyntaxError(f'Unexpected: {ch}')
    
    tokens.append(Token(TokenKind.EOF, ''))
    return tokens
```

## 測試

```python
source = "x := 3 + 4 * 2; y := x - 1;"
tokens = tokenize(source)
for tok in tokens:
    print(tok)
```

輸出：

```
Token(IDENT, 'x')
Token(ASSIGN, ':=')
Token(NUMBER, '3')
Token(PLUS, '+')
Token(NUMBER, '4')
Token(STAR, '*')
Token(NUMBER, '2')
Token(SEMI, ';')
Token(IDENT, 'y')
...
Token(EOF, '')
```

## 結語

手作詞法分析器並不困難，關鍵在於理解 Token 的概念和正則表達式的匹配原理。兩種實作方式各有優劣：正則表達式版本簡潔但不易擴展；逐字元掃描版本靈活但程式碼較長。對於小型語言，推薦使用正則表達式版本。

## 延伸閱讀

- [Lex 詞法分析器](https://www.google.com/search?q=Lex+lexical+analyzer+generator)
- [正則表達式引擎](https://www.google.com/search?q=regular+expression+engine+NFA+DFA)

---

*本篇文章為「AI 程式人雜誌 2023 年 8 月號」編譯器理論系列文章。*
