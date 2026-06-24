# 遞迴下推解析器

## 解析器的角色

在編譯器中，語法分析 (Parsing) 是將原始碼轉換為語法樹的過程。解析器接受詞法分析器產生的 Token 串流，根據文法規則建構語法樹。

遞迴下推解析器 (Recursive Descent Parser) 是最容易手寫實作的解析技術——對文法中的每個非終止符號編寫一個對應的遞迴函數。

## LL(1) 解析

遞迴下推解析器通常處理 LL(1) 文法——從左到右掃描 (Left-to-right)、最左推導 (Leftmost derivation)、向前看一個記號 (1 token lookahead)。

### 基本結構

考慮算術表達式的文法：
```
E → E + T | T
T → T * F | F
F → (E) | num
```

這不是 LL(1) 文法（左遞迴），我們需要改寫為：
```
E → T E'
E' → + T E' | ε
T → F T'
T' → * F T' | ε
F → (E) | num
```

### 解析函數

```python
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected=None):
        token = self.peek()
        if expected and token != expected:
            raise SyntaxError(f"Expected {expected}, got {token}")
        self.pos += 1
        return token

    def parse_E(self):       # E → T E'
        left = self.parse_T()
        return self.parse_E_prime(left)

    def parse_E_prime(self, left):  # E' → + T E' | ε
        if self.peek() == '+':
            self.consume('+')
            right = self.parse_T()
            return self.parse_E_prime(('+', left, right))
        return left

    def parse_T(self):       # T → F T'
        left = self.parse_F()
        return self.parse_T_prime(left)

    def parse_T_prime(self, left):  # T' → * F T' | ε
        if self.peek() == '*':
            self.consume('*')
            right = self.parse_F()
            return self.parse_T_prime(('*', left, right))
        return left

    def parse_F(self):       # F → (E) | num
        if self.peek() == '(':
            self.consume('(')
            expr = self.parse_E()
            self.consume(')')
            return expr
        return ('num', self.consume())
```

## 錯誤處理

遞迴下推解析器可以整合豐富的錯誤資訊：

1. **同步 (Synchronization)**：遇到錯誤時跳過 Token 直到找到一個「可靠」的符號（如 `;`、`}`）
2. **錯誤產生式**：在文法中加入產生式來捕獲常見錯誤模式
3. **最起碼恢復 (Minimal Recovery)**：插入或刪除最少數量的 Token

## 優點與缺點

**優點**：
- 直觀易懂，與文法結構對應
- 錯誤訊息可以很精確
- 容易加入語意動作

**缺點**：
- 不能處理左遞迴文法
- 需要 LL(1) 文法限制
- 對大型文法的維護較困難

## 實用工具

雖然遞迴下推解析器可以手寫，但對於複雜的文法，使用解析器生成器更有效率：

- **ANTLR**：支援 LL(*) 解析，可產生多種語言的解析器
- **Yacc/Bison**：LALR(1) 解析器生成器
- **lark-parser**：Python 的 EBNF 解析器

## 參考資料

- [https://www.google.com/search?q=recursive+descent+parser+implementation](https://www.google.com/search?q=recursive+descent+parser+implementation)
- [https://www.google.com/search?q=LL(1)+grammar+recursive+descent](https://www.google.com/search?q=LL(1)+grammar+recursive+descent)
- [https://www.google.com/search?q=遞迴下推解析器+實作](https://www.google.com/search?q=遞迴下推解析器+實作)
