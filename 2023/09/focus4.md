# λ 演算與函數式程式設計

## 計算的數學基礎

### λ 演算是什麼？

λ 演算（Lambda Calculus）由 Alonzo Church 在 1930 年代提出，是函數式程式設計的理論基礎。在 λ 演算中，**一切皆函數**——數字、布林值、資料結構都可以用純函數表示。

### 語法

λ 演算只有三種表達式：

```
e ::= x                 (變數)
    | λx. e             (抽象：函數定義)
    | e1 e2             (應用：函數呼叫)
```

### Church 編碼

Church numerals 將自然數編碼為函數：

```python
# 數字 n 表示「將函數 f 應用 n 次」
0 = λf. λx. x
1 = λf. λx. f(x)
2 = λf. λx. f(f(x))

加法：add = λm. λn. λf. λx. m f (n f x)
乘法：mul = λm. λn. λf. m (n f) x
```

### 規約規則

- **α-轉換**：重新命名綁定變數
- **β-規約**：函數應用展開 `(λx. e1) e2 → e1[x:=e2]`
- **η-轉換**：`λx. f x → f`（當 x 不在 f 中自由出現）

### Y Combinator

Y combinator 在不使用語言內建遞迴的情況下實現遞迴：

```python
Y = λf. (λx. f (x x)) (λx. f (x x))

# 應用：階乘
fact = Y (λf. λn. if n==0 then 1 else n * f(n-1))
```

### 函數式程式設計的核心理念

1. **不可變性**：資料一旦建立就不會改變
2. **純函數**：相同輸入總是產生相同輸出，無副作用
3. **高階函數**：函數可作為參數傳遞和返回值
4. **遞迴**：取代迴圈的控制結構

### Python 中的函數式風格

```python
# 高階函數
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))

# 不可變性（避免原地修改）
from copy import deepcopy
new_list = old_list + [6]  # 建立新列表而非修改
```

### λ 演算對現代語言的影響

λ 演算看似純粹的數學，但其概念在現代語言中無所不在：

- **Python 的 lambda**：`lambda x: x + 1` 直接來自 λ 演算
- **JavaScript 的箭頭函數**：`(x) => x + 1` 是 λ 抽象
- **Rust 的閉包**：`|x| x + 1` 同樣源自 λ 演算
- **型別系統**：簡單型別 λ 演算（STLC）是一切型別系統的理論根源

Church 的 λ 演算與 Turing 機等價，證明了「可計算性」的統一性。這也是函數式程式設計與命令式程式設計能夠表達完全相同計算的理論基礎。

### 惰性求值

λ 演算的規約策略影響了語言的求值策略：

- **及早求值（Eager Evaluation）**：參數在傳入函數前就計算好（Python、C、Rust）
- **惰性求值（Lazy Evaluation）**：參數只在需要時才計算（Haskell）

```python
# Python 的惰性求值（透過 generator）
def infinite_sequence():
    n = 0
    while True:
        yield n
        n += 1
# 不會記憶體爆炸，因為是惰性的
```

### 延伸閱讀

- [λ 演算介紹](https://www.google.com/search?q=lambda+calculus+for+beginners)
- [Church 編碼](https://www.google.com/search?q=Church+encoding+lambda+calculus)
- [Y Combinator 解釋](https://www.google.com/search?q=Y+combinator+explained)

---

**下一篇**：[作用域與閉包](focus5.md)
