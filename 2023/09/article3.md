# 型別推斷

## 編譯器自動推導型別

### 什麼是型別推斷？

型別推斷（Type Inference）是編譯器自動推導表達式型別的機制，讓開發者不需要明確標註每個變數的型別。最著名的型別推斷演算法是 **Hindley-Milner（HM）**，最初用於 ML 語言。

### Hindley-Milner 推斷

HM 演算法基於三個核心步驟：

**1. 收集約束**：遍歷 AST，為每個表達式產生型別變數和約束條件。

```python
# 函數 f(x) = x + 1
# 1. x 的型別 = α（型別變數）
# 2. 1 的型別 = Int
# 3. + 要求 α = Int（因為 + 需要兩個 Int）
# 4. 結果型別 = Int
# 5. f 的型別 = Int -> Int
```

**2. 單一化（Unification）**：解約束方程組，找到所有型別變數的一致賦值。

**3. 泛化**：未受約束的型別變數被泛化為多型型別。

```haskell
-- Haskell 的全域推斷
-- x 的型別被推斷為：x :: Num a => a -> a -> a
x = (+) :: Num a => a -> a -> a
```

### 區域推斷 vs 全域推斷

**全域推斷**（Haskell、OCaml）：不需要任何型別註記，編譯器推斷所有表達式的型別。

```haskell
-- 完全不需要型別宣告
factorial n = if n == 0 then 1 else n * factorial (n - 1)
-- 推斷結果：factorial :: (Eq a, Num a) => a -> a
```

**區域推斷**（Java 10+、C++ auto、Rust）：僅在區域變數中推斷，函數簽名仍需明確標註。

```python
# Rust：區域推斷
let x = 10;       // 推斷為 i32
let y = 3.14;     // 推斷為 f64
let z = x + y;    // 推斷為 f64（x 被轉為 f64）

# 函數簽名仍需明確
fn add(x: i32, y: i32) -> i32 { x + y }
```

### 各語言的型別推斷能力

| 語言 | 推斷範圍 | 需要註記的場景 |
|------|---------|------------|
| Haskell | 全域 | 頂層多型型別（可選） |
| Rust | 區域 | 函數參數和回傳型別 |
| TypeScript | 區域 | 函數參數（可選） |
| Kotlin | 區域 | 函數參數和回傳型別（可選） |
| Java | 區域（var） | 所有宣告 |
| Python | 無（3.5+ 提示） | 所有宣告（提示非強制） |

### 型別推斷的優缺點

優點：
- **減少樣板程式碼**：不需要重複書明顯而易見的型別
- **提高抽象層次**：專注於邏輯而非型別細節
- **泛型更易使用**：型別參數自動推導

缺點：
- **錯誤訊息可能令人困惑**：型別推斷失敗時，錯誤訊息難以理解
- **調試難度增加**：隱式型別不如顯式宣告直觀
- **編譯時間增加**：推斷演算法需要更多計算

### 延伸閱讀

- [Hindley-Milner 型別推斷](https://www.google.com/search?q=Hindley+Milner+type+inference)
- [型別推斷簡介](https://www.google.com/search?q=type+inference+programming+languages)
