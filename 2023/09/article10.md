# 程式語言比較：型別系統觀點

## Python、TypeScript、Rust、Haskell

### 比較維度

本期的最後一篇從型別系統的角度比較四種代表性語言。理解它們的設計取捨，有助於在實際專案中做出更明智的選擇。

### Python：動態型別的靈活性

```python
# 動態型別：型別在執行時決定
x = 42
x = "hello"  # 完全合法
x = [1, 2, 3]

# 3.5+ 型別提示（僅供檢查，不強制）
def greet(name: str) -> str:
    return "Hello, " + name
```

- **型別強度**：強
- **型別檢查**：動態（可選的靜態檢查 via mypy/pyright）
- **泛型**：3.12+ 支援泛型類別
- **多型**：鴨子型別、繼承

### TypeScript：JavaScript 的型別層

```typescript
// 結構子型別（structural subtyping）
interface Point {
    x: number;
    y: number;
}

function distance(p: Point): number {
    return Math.sqrt(p.x ** 2 + p.y ** 2);
}

// 只要結構匹配即可
distance({x: 3, y: 4, z: 0});  // 合法！
```

- **型別強度**：中等（any 逃脫）
- **型別檢查**：靜態（完全擦除，執行期無型別）
- **泛型**：豐富的泛型系統
- **多型**：結構子型別、聯合型別、交類型別

### Rust：所有權 + 強型別

```rust
// 所有權系統是型別系統的一部分
fn process(data: Vec<i32>) -> i32 {
    data.iter().sum()
    // data 在此被 drop（所有權轉移）
}

fn main() {
    let v = vec![1, 2, 3];
    let sum = process(v);
    // println!("{:?}", v);  // 編譯錯誤！v 已移動
}
```

- **型別強度**：極強（無隱式轉換）
- **型別檢查**：靜態（零成本抽象）
- **泛型**：trait bound、關聯型別
- **多型**：trait（類似 typeclass）

### Haskell：純函數式 + 全域推斷

```haskell
-- 全域型別推斷，函數簽名可省略
quicksort :: Ord a => [a] -> [a]
quicksort [] = []
quicksort (x:xs) =
    quicksort [y | y <- xs, y <= x]
    ++ [x] ++
    quicksort [y | y <- xs, y > x]
```

- **型別強度**：極強（無 side effect）
- **型別檢查**：靜態（全域推斷）
- **泛型**：typeclass + 高階多型
- **多型**：參數多型 + typeclass

### 比較總結

| 維度 | Python | TypeScript | Rust | Haskell |
|------|--------|-----------|------|---------|
| 型別強度 | 強 | 中 | 極強 | 極強 |
| 檢查時機 | 動態 | 靜態 | 靜態 | 靜態 |
| 推斷能力 | 無 | 區域 | 區域 | 全域 |
| 泛型 | 弱 | 強 | 強 | 極強 |
| 學習曲線 | 低 | 中 | 高 | 高 |
| 原型速度 | 快 | 中 | 慢 | 中 |
| 生產可靠 | 低 | 中 | 高 | 高 |

### 選擇建議

- **資料科學／腳本**：Python
- **Web 前端**：TypeScript
- **系統程式設計**：Rust
- **演算法競賽／概念驗證**：Haskell

### 延伸閱讀

- [型別系統比較](https://www.google.com/search?q=type+system+comparison+programming+languages)
- [Rust vs Haskell 型別系統](https://www.google.com/search?q=Rust+vs+Haskell+type+system)
