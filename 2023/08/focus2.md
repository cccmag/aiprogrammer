# 詞法分析：正則表達式與 Lexer

## 詞法分析的角色

詞法分析（Lexical Analysis）是編譯器前端的第一個階段，負責將原始碼的字元序列轉換為具有語義的 Token 序列。這個過程也被稱為掃描（Scanning）。

詞法分析器的任務包括：
1. **識別 Token**：將字元分組為單詞或符號
2. **去除空白和註解**：忽略對語義無關的字元
3. **錯誤回報**：檢測非法字元

## Token 的種類

Token 是詞法分析的最小單元，通常包含型別和值：

```python
('IDENT', 'x')     # 識別字
('NUMBER', '42')   # 數字常數
('PLUS', '+')      # 運算子
('ASSIGN', ':=')   # 賦值符號
('LPAREN', '(')    # 左括號
('SEMI', ';')      # 分號
```

## 正則表達式

正則表達式（Regular Expression）是描述字串模式的強大工具，也是詞法分析器的理論基礎。每種 Token 都可以用一個正則表達式來描述：

| Token | 正則表達式 | 匹配範例 |
|---|---|---|
| NUMBER | `[0-9]+` | 42, 007 |
| IDENT | `[a-zA-Z_][a-zA-Z0-9_]*` | foo, bar_1 |
| PLUS | `\+` | + |
| ASSIGN | `:=` | := |

### 正則表達式的運算子

- **拼接**：`ab` 表示 a 後跟 b
- **聯集**：`a|b` 表示 a 或 b
- **閉包**：`a*` 表示零個或多個 a
- **正閉包**：`a+` 表示一個或多個 a
- **選擇**：`a?` 表示零個或一個 a
- **字元集**：`[abc]` 表示 a、b 或 c

## 有限狀態自動機

正則表達式可以等價地轉換為有限狀態自動機（Finite State Automaton, FSA）。根據轉換方式分為兩種：

### 確定性有限狀態自動機（DFA）

每個狀態在每種輸入下只有一個轉移：

```
狀態 0: 開始狀態
  遇到數字 → 狀態 1
狀態 1: 數字狀態（接受狀態）
  遇到數字 → 狀態 1
  遇到非數字 → 狀態 2
狀態 2: 結束（回傳 Token）
```

### 非確定性有限狀態自動機（NFA）

允許在相同輸入下有多個轉移，或空字串轉移。NFA 可以透過子集構造算法（Subset Construction）轉換為 DFA。

## Lexer 的實作方式

### 手動實作

最簡單的方式是使用正則表達式匹配所有 Token 種類：

```python
TOKEN_SPEC = [
    ('NUMBER',  r'\d+'),
    ('IDENT',   r'[a-zA-Z_]\w*'),
    ('ASSIGN',  r':='),
    ('PLUS',    r'\+'),
    ('MINUS',   r'-'),
]
```

然後逐字元掃描或使用正則引擎進行匹配。

### 使用 Lex/Flex

Lex（或 GNU 版本的 Flex）是專門的詞法分析器產生器。開發者只需用 DSL 描述 Token 規則，Flex 就會產生對應的 C 語言詞法分析器。

## 錯誤處理

詞法分析器遇到無法匹配的字元時，需要適當的錯誤處理策略：

- **恐慌模式**：跳過當前字元，繼續掃描
- **錯誤 Token**：產生特殊的錯誤 Token
- **立即回報**：拋出異常並停止

## 本期實作

在本期的迷你編譯器中，詞法分析器使用 Python 的 `re.finditer` 實現：

```python
TOKEN_RE = re.compile('|'.join(
    f'(?P<{n}>{p})' for n, p in TOKEN_SPEC
))
```

這種「一掃描」方式簡單有效，適合小型語言。

## 延伸閱讀

- [正則表達式教學](https://www.google.com/search?q=regular+expression+tutorial)
- [Lex 與 Flex 詞法分析器](https://www.google.com/search?q=Lex+Flex+lexical+analyzer+tutorial)
- [有限狀態自動機](https://www.google.com/search?q=finite+state+automaton+theory)

---

*本篇文章為「AI 程式人雜誌 2023 年 8 月號」編譯器理論系列之二。*
