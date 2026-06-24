# 模式匹配

## 結構化解構資料

### 什麼是模式匹配？

模式匹配（Pattern Matching）是根據資料的結構來進行分支判斷的機制。與傳統的 `if/else` 和 `switch` 不同，模式匹配可以**解構**資料結構，同時提取內部值。

### 基本語法

```python
# Python 3.10+ 的 match 語句
def describe(value):
    match value:
        case 0:
            return "零"
        case 1 | 2 | 3:
            return "小數字"
        case int(n) if n > 100:
            return "大數字"
        case str(s):
            return f"字串: {s}"
        case _:
            return "其他"
```

### 模式匹配 vs Switch

```rust
// Rust 的模式匹配（窮舉檢查）
enum Coin { Penny, Nickel, Dime, Quarter }

fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => 1,
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter => 25,
        // 編譯器檢查所有變體都已處理
    }
}
```

### 模式類型

**字面值模式**：匹配特定值
```python
match x:
    case 42: print("答案")
```

**解構模式**：提取內部的值
```python
match point:
    case (0, 0): print("原點")
    case (x, 0): print(f"x 軸上 {x}")
    case (0, y): print(f"y 軸上 {y}")
    case (x, y): print(f"({x}, {y})")
```

**守衛條件**：加上條件判斷
```python
match number:
    case n if n < 0: print("負數")
    case n if n == 0: print("零")
    case n: print("正數")
```

**綁定模式**：用 `as` 綁定到變數
```python
match result:
    case Ok(value) as r if value > 0:
        print(f"正數: {value}")
```

### 窮舉檢查

模式匹配的重要保證是**窮舉性（exhaustiveness）**——編譯器檢查是否所有可能的情況都被覆蓋：

```rust
// Rust 的 match 必須窮舉
fn is_positive(x: i32) -> bool {
    match x {
        0 => false,
        _ if x > 0 => true,
        _ => false,  // 必須處理
    }
}
```

### 模式匹配的應用

- **錯誤處理**：`Result` 和 `Option` 的模式匹配
- **資料序列化**：解構 JSON、XML 等結構化資料
- **文法分析**：匹配 AST 節點
- **DOM 操作**：匹配 HTML 元素結構

### 延伸閱讀

- [Python match 語句](https://www.google.com/search?q=Python+match+statement+pattern+matching)
- [Rust match 模式](https://www.google.com/search?q=Rust+match+pattern+matching)
