# 正則表達式引擎實作

## 簡介

正則表達式引擎是自動機理論最廣泛的應用之一。從 Python 的 re 模組到 JavaScript 的 RegExp，從 grep 到 sed——這些工具的核心都是一個基於自動機的匹配引擎。我們將用 Python 從零開始實作一個簡易但可運行的正則表達式引擎。

## 引擎架構

我們的正則表達式引擎由三個階段組成：

1. **解析 (Parsing)**：將正則表達式字串轉換為抽象語法樹 (AST)
2. **編譯 (Compilation)**：將 AST 轉換為 NFA（Thompson 建構）
3. **執行 (Execution)**：用 NFA 模擬進行字串匹配

## 詞法分析與語法分析

首先定義 AST 節點類型：

```python
class RegexNode:
    pass

class CharNode(RegexNode):      # 單一字元
    def __init__(self, c): self.c = c

class UnionNode(RegexNode):     # R|S
    def __init__(self, l, r): self.l, self.r = l, r

class ConcatNode(RegexNode):    # RS
    def __init__(self, l, r): self.l, self.r = l, r

class StarNode(RegexNode):      # R*
    def __init__(self, r): self.r = r
```

解析器使用遞迴下墜方式，處理優先級：字元 < 串接 < 聯集 < 星號。

## Thompson 建構

每個 AST 節點對應一個 NFA 片段：

```python
def compile(node):
    if isinstance(node, CharNode):
        # 兩個狀態，一個字元轉移
        s0, s1 = new_state(), new_state()
        add_transition(s0, node.c, s1)
        return NFASegment(s0, s1)
    elif isinstance(node, UnionNode):
        left = compile(node.l)
        right = compile(node.r)
        s0, s1 = new_state(), new_state()
        add_epsilon(s0, left.start)
        add_epsilon(s0, right.start)
        add_epsilon(left.accept, s1)
        add_epsilon(right.accept, s1)
        return NFASegment(s0, s1)
    elif isinstance(node, ConcatNode):
        left = compile(node.l)
        right = compile(node.r)
        add_epsilon(left.accept, right.start)
        return NFASegment(left.start, right.accept)
    elif isinstance(node, StarNode):
        inner = compile(node.r)
        s0, s1 = new_state(), new_state()
        add_epsilon(s0, inner.start)
        add_epsilon(s0, s1)
        add_epsilon(inner.accept, inner.start)
        add_epsilon(inner.accept, s1)
        return NFASegment(s0, s1)
```

## NFA 模擬匹配

匹配演算法使用 ε-閉包和狀態集合追蹤：

```python
def match(nfa, text):
    states = epsilon_closure({nfa.start})
    for ch in text:
        states = epsilon_closure(move(states, ch))
    return any(s in nfa.accepts for s in states)
```

## 功能擴展

基本的引擎可以擴展支援：
- **任意字元 `.`**：匹配任何字元
- **重複 `+`, `?`**：`R+` = `RR*`，`R?` = `R|ε`
- **字元集合 `[abc]`**：聯集的多個字元
- **錨點 `^`, `$`**：匹配行首和行尾

## 效能比較

| 方法 | 建構時間 | 匹配時間 | 記憶體 |
|------|---------|---------|--------|
| NFA 模擬 | O(m) | O(m × n) | O(m) |
| DFA 模擬 | O(2^m) | O(n) | O(2^m) |
| 回溯 (Backtracking) | O(m) | O(2^n) 最壞 | O(n) |

其中 m 是正則表達式長度，n 是文字長度。NFA 模擬在時間和空間之間取得良好平衡，是大多數實用引擎的選擇。

## 參考資料

- [https://www.google.com/search?q=regular+expression+engine+Thompson+construction](https://www.google.com/search?q=regular+expression+engine+Thompson+construction)
- [https://www.google.com/search?q=regex+NFA+simulation+Python+implementation](https://www.google.com/search?q=regex+NFA+simulation+Python+implementation)
- [https://www.google.com/search?q=正則表達式+NFA+Thompson](https://www.google.com/search?q=正則表達式+NFA+Thompson)
