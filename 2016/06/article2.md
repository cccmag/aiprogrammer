# 編譯器的詞彙分析

## 前言

詞彙分析（Lexical Analysis）是編譯器的第一階段，負責將原始程式碼轉換為詞彙單元（Token）序列。這一階段正是正規語言理論的直接應用。

## 詞彙分析的基礎

### Token 類型

```python
from enum import Enum, auto

class TokenType(Enum):
    KEYWORD = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    OPERATOR = auto()
    PUNCTUATION = auto()
    STRING = auto()
    COMMENT = auto()
    WHITESPACE = auto()
    EOF = auto()


class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"
```

### 正規表達式描述 Token

```python
TOKEN_PATTERNS = [
    (TokenType.KEYWORD, r"\b(if|else|while|for|return|int|float|void)\b"),
    (TokenType.IDENTIFIER, r"[a-zA-Z_][a-zA-Z0-9_]*"),
    (TokenType.NUMBER, r"\d+(\.\d+)?"),
    (TokenType.OPERATOR, r"[+\-*/%=<>!&|^~]"),
    (TokenType.PUNCTUATION, r"[{}()\[\];,.]"),
    (TokenType.STRING, r'"(?:[^"\\]|\\.)*"'),
    (TokenType.COMMENT, r"//.*|/\*[\s\S]*?\*/"),
    (TokenType.WHITESPACE, r"\s+"),
]

import re

class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    def tokenize(self):
        while self.pos < len(self.source):
            matched = False

            for token_type, pattern in TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.source, self.pos)
                if match:
                    value = match.group(0)

                    if token_type != TokenType.WHITESPACE and token_type != TokenType.COMMENT:
                        self.tokens.append(Token(token_type, value, self.line, self.column))

                    self.pos = match.end()
                    self.column += len(value)
                    matched = True
                    break

            if not matched:
                raise SyntaxError(f"Unexpected character at {self.line}:{self.column}")

        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
```

## 使用 NFA 進行詞彙分析

### 正規表達式 → NFA → DFA

```python
def build_nfa_from_regex(regex):
    """使用 Thompson 構造法"""
    pass  # See focus_code.md

def build_dfa_from_nfa(nfa):
    """使用子集構造法"""
    pass  # See focus_code.md
```

### 實際的詞彙分析器生成器

```python
class LexerGenerator:
    def __init__(self):
        self.patterns = []

    def add_pattern(self, name, pattern):
        self.patterns.append((name, pattern))
        return self

    def generate(self):
        """生成確定的有限自動機"""
        nfa = None

        for name, pattern in self.patterns:
            pattern_nfa = build_nfa_from_regex(pattern)
            if nfa is None:
                nfa = pattern_nfa
            else:
                nfa = union_nfa(nfa, pattern_nfa)

        return build_dfa_from_nfa(nfa)
```

## 實際範例：Python 簡單詞彙分析器

```python
def demo_lexer():
    source = """
    int main() {
        int x = 42;
        float y = 3.14;
        if (x > y) {
            return x + y;
        }
        return 0;
    }
    """

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    print("Tokens:")
    for token in tokens:
        print(f"  {token}")

demo_lexer()
```

## 詞彙分析的挑戰

### 1. 最長匹配原則

```python
def longest_match():
    """當多個模式都可能匹配時，選擇最長的"""
    source = "abc123"

    patterns = [
        (TokenType.IDENTIFIER, r"[a-z]+"),
        (TokenType.NUMBER, r"\d+"),
    ]

    for pattern_type, pattern in patterns:
        regex = re.compile(pattern)
        match = regex.match(source)
        if match:
            print(f"Longest match: {match.group(0)} (type: {pattern_type.name})")
            break

longest_match()
```

### 2. 優先級

```python
def priority_handling():
    """關鍵字優先於識別符"""
    source = "if"

    # 關鍵字（優先）
    keyword_pattern = r"\b(if|else|while)\b"
    # 識別符
    id_pattern = r"[a-z]+"

    keyword_regex = re.compile(keyword_pattern)
    id_regex = re.compile(id_pattern)

    kw_match = keyword_regex.match(source)
    if kw_match:
        print(f"Keyword: {kw_match.group(0)}")
    else:
        id_match = id_regex.match(source)
        if id_match:
            print(f"Identifier: {id_match.group(0)}")

priority_handling()
```

### 3. 巢狀註解

正規語言無法處理巢狀結構，但可以透過堆疊或輔助狀態來處理。

```python
def comment_state_machine():
    """使用狀態機處理巢狀註解"""
    # 這需要上下文無關文法，無法用純正規表達式處理
    # 通常需要特殊處理或分割成多個階段
    pass
```

## 效能優化

### 1. DFA 跳過

```python
def dfa_jump():
    """預計算 DFA 的跳轉表以加速"""
    pass
```

### 2. 字元類

```python
def char_classes():
    """將常見字元群組化為類以減少狀態"""
    # [a-zA-Z] 比列舉每個字元更高效
    pass
```

## 小結

詞彙分析是正規語言理論在編譯器中的經典應用。雖然現代編譯器通常使用工具（如 Lex、Flex）自動生成詞彙分析器，但理解其背後的理論——從正規表達式到 NFA 再到 DFA——對於編譯器設計和最佳化至關重要。

---

**延伸閱讀**

- [Lex and Flex documentation](https://www.google.com/search?q=lex+flex+lexer+generator)
- [Compilers: Principles, Techniques, and Tools (Dragon Book)](https://www.google.com/search?q=Dragon+Book+compilers)
- [Writing a Simple Lexer in Python](https://www.google.com/search?q=writing+simple+lexer+python+tutorial)