# 代數資料型別

## Product Type 與 Sum Type

### 什麼是代數資料型別？

代數資料型別（Algebraic Data Type, ADT）是一種組合型別的方式，透過「乘積」（product）和「和」（sum）兩種運算組建複雜型別。ADT 是函數式語言（Haskell、OCaml、Rust）的核心特性。

### Product Type（乘積型別）

乘積型別是**多個型別的組合**——值同時包含所有欄位的資料。對應到結構體、Tuple 或 Record：

```python
# Python dataclass（乘積型別）
from dataclasses import dataclass
@dataclass
class Point:
    x: float
    y: float

# 值的數量 = |float| × |float|
```

```rust
// Rust 結構體（乘積型別）
struct Point {
    x: f64,
    y: f64,
}
```

### Sum Type（和型別）

和型別是**多個型別的選擇**——值只能是其中一個變體的資料。對應到枚舉（enum）：

```rust
// Rust 枚舉（和型別）
enum Shape {
    Circle(f64),           // 只有半徑
    Rectangle(f64, f64),   // 寬和長
    Triangle(f64, f64, f64), // 三邊長
}

// 值的數量 = |f64| + |f64×f64| + |f64×f64×f64|
```

### Python 中的 ADT 模擬

Python 沒有原生的 sum type，但可以用 Union 型別提示模擬：

```python
from typing import Union
from dataclasses import dataclass

@dataclass
class Circle:
    radius: float

@dataclass
class Rectangle:
    width: float
    height: float

Shape = Union[Circle, Rectangle]  # 和型別（模擬）

def area(shape: Shape) -> float:
    match shape:
        case Circle(r): return 3.14 * r * r
        case Rectangle(w, h): return w * h
```

### Option 與 Result

ADT 最實用的應用是 **Option** 和 **Result**：

```python
# Rust 的 Option<T>
# enum Option<T> { Some(T), None }

# Rust 的 Result<T, E>
# enum Result<T, E> { Ok(T), Err(E) }

# Python 中模擬
from typing import Optional, Union
# Optional[str] 等價於 Union[str, None]
```

### ADT 的數學基礎

ADT 的「代數」來自於型別組合的計數：

- `ab`（product）：`|A × B| = |A| × |B|`
- `a + b`（sum）：`|A + B| = |A| + |B|`
- `a^b`（指數）：`|B → A| = |A|^|B|`（函數型別）

### 為何 ADT 重要？

1. **窮舉檢查**：編譯器確保所有情況都被處理
2. **非法狀態不可表示**：型別系統排除無效組合
3. **型別安全**：不需要執行時期檢查就知道值的結構

### 延伸閱讀

- [代數資料型別解釋](https://www.google.com/search?q=algebraic+data+type+explained)
- [Rust 枚舉進階](https://www.google.com/search?q=Rust+enum+algebraic+data+type)
