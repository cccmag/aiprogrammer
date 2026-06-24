# 實作簡化 Ruby 直譯器：打造 MiniRuby

## 簡介

本期程式實作將帶領讀者從頭實作一個簡化的 Ruby 直譯器 MiniRuby，幫助理解程式語言直譯的基本概念。

## 程式碼

```python
#!/usr/bin/env python3
"""
MiniRuby - A simplified Ruby interpreter demo

這個程式演示了直譯器的基本概念：
1. 詞法分析
2. 語法解析
3. 執行環境
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class TokenType(Enum):
    NUMBER = "NUMBER"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    ASSIGN = "ASSIGN"
    EQ = "EQ"
    DEF = "DEF"
    END = "END"
    RETURN = "RETURN"
    IF = "IF"
    WHILE = "WHILE"
    PRINT = "PRINT"
    EOF = "EOF"


@dataclass
class Token:
    type: TokenType
    value: Any


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0

    def tokenize(self) -> List[Token]:
        tokens = []
        while self.pos < len(self.source):
            self.skip_whitespace()
            if self.pos >= len(self.source):
                break
            char = self.source[self.pos]
            if char.isdigit():
                tokens.append(self.read_number())
            elif char.isalpha() or char == '_':
                tokens.append(self.read_identifier())
            elif char == '+':
                tokens.append(Token(TokenType.PLUS, '+'))
                self.pos += 1
            elif char == '-':
                tokens.append(Token(TokenType.MINUS, '-'))
                self.pos += 1
            elif char == '*':
                tokens.append(Token(TokenType.STAR, '*'))
                self.pos += 1
            elif char == '/':
                tokens.append(Token(TokenType.SLASH, '/'))
                self.pos += 1
            elif char == '(':
                tokens.append(Token(TokenType.LPAREN, '('))
                self.pos += 1
            elif char == ')':
                tokens.append(Token(TokenType.RPAREN, ')'))
                self.pos += 1
            elif char == '=':
                if self.peek(1) == '=':
                    tokens.append(Token(TokenType.EQ, '=='))
                    self.pos += 2
                else:
                    tokens.append(Token(TokenType.ASSIGN, '='))
                    self.pos += 1
            else:
                self.pos += 1
        tokens.append(Token(TokenType.EOF, None))
        return tokens

    def skip_whitespace(self):
        while self.pos < len(self.source) and self.source[self.pos].isspace():
            self.pos += 1

    def read_number(self) -> Token:
        num = ''
        while self.pos < len(self.source) and self.source[self.pos].isdigit():
            num += self.source[self.pos]
            self.pos += 1
        return Token(TokenType.NUMBER, int(num))

    def read_identifier(self) -> Token:
        ident = ''
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            ident += self.source[self.pos]
            self.pos += 1
        keywords = {'def', 'end', 'return', 'if', 'while', 'print'}
        if ident in keywords:
            return Token(TokenType(ident.upper()), ident)
        return Token(TokenType.IDENTIFIER, ident)

    def peek(self, offset: int) -> str:
        if self.pos + offset < len(self.source):
            return self.source[self.pos + offset]
        return ''


class Interpreter:
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, dict] = {}

    def evaluate(self, tokens: List[Token]) -> Any:
        self.tokens = tokens
        self.pos = 0
        result = None
        while self.current_token().type != TokenType.EOF:
            result = self.statement()
        return result

    def current_token(self) -> Token:
        return self.tokens[self.pos]

    def advance(self):
        self.pos += 1

    def statement(self) -> Any:
        token = self.current_token()
        if token.type == TokenType.PRINT:
            return self.print_statement()
        elif token.type == TokenType.DEF:
            return self.function_def()
        elif token.type == TokenType.IDENTIFIER:
            return self.assignment_or_expr()
        elif token.type == TokenType.RETURN:
            return self.return_statement()
        else:
            return self.expr()

    def print_statement(self) -> Any:
        self.advance()
        value = self.expr()
        print(value)
        return value

    def function_def(self) -> None:
        self.advance()  # skip 'def'
        name = self.current_token().value
        self.advance()  # skip function name
        params = []
        if self.current_token().type == TokenType.IDENTIFIER:
            params.append(self.current_token().value)
            self.advance()
        self.advance()  # skip ')'
        body = []
        while self.current_token().type != TokenType.END:
            body.append(self.current_token())
            self.advance()
        self.advance()  # skip 'end'
        self.functions[name] = {'params': params, 'body': body}
        return None

    def assignment_or_expr(self) -> Any:
        name = self.current_token().value
        self.advance()
        if self.current_token().type == TokenType.ASSIGN:
            self.advance()
            value = self.expr()
            self.variables[name] = value
            return value
        else:
            return self.function_call(name)

    def return_statement(self) -> Any:
        self.advance()
        return self.expr()

    def expr(self) -> Any:
        left = self.term()
        while self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token().type
            self.advance()
            right = self.term()
            if op == TokenType.PLUS:
                left = left + right
            else:
                left = left - right
        return left

    def term(self) -> Any:
        left = self.factor()
        while self.current_token().type in (TokenType.STAR, TokenType.SLASH):
            op = self.current_token().type
            self.advance()
            right = self.factor()
            if op == TokenType.STAR:
                left = left * right
            else:
                left = left // right
        return left

    def factor(self) -> Any:
        token = self.current_token()
        if token.type == TokenType.NUMBER:
            self.advance()
            return token.value
        elif token.type == TokenType.IDENTIFIER:
            self.advance()
            if self.current_token().type == TokenType.LPAREN:
                return self.function_call(token.value)
            return self.variables.get(token.value, 0)
        elif token.type == TokenType.LPAREN:
            self.advance()
            value = self.expr()
            self.advance()  # skip ')'
            return value
        return 0

    def function_call(self, name: str) -> Any:
        if name not in self.functions:
            return self.variables.get(name, 0)
        func = self.functions[name]
        self.advance()  # skip '('
        args = []
        while self.current_token().type != TokenType.RPAREN:
            args.append(self.expr())
        self.advance()  # skip ')'
        # Simple: just execute body and return last expression
        old_pos = self.pos
        result = None
        for token in func['body']:
            if token.type == TokenType.RETURN:
                continue
            result = self.expr()
        return result


def demo():
    print("\n" + "#" * 60)
    print("# MiniRuby - Ruby Interpreter Demo")
    print("#" * 60 + "\n")

    interpreter = Interpreter()

    # Simple arithmetic
    code = "x = 10 + 5 * 2"
    print(f"Evaluating: {code}")
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    result = interpreter.evaluate(tokens)
    print(f"Result: {result}")

    # Print statement
    code = "print 42"
    print(f"\nEvaluating: {code}")
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    interpreter.evaluate(tokens)


if __name__ == "__main__":
    demo()
```

## 測試方式

```bash
python3 _code/ruby_demo.py
```

## 實作重點

1. **Lexer**：將 Ruby 程式碼轉換為 Token 流
2. **Interpreter**：遍歷 Token 並執行
3. **變數儲存**：簡單的符號表
4. **函數定義**：基本的函數支援

---

*本期程式實作到此結束。*