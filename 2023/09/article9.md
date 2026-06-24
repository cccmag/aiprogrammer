# 巨集與元程式設計

## 寫程式的程式

### 什麼是元程式設計？

元程式設計（Metaprogramming）是指**撰寫能夠產生、操作或轉換其他程式碼的程式**。這讓開發者在編譯期或執行期動態地建立程式碼。

### 巨集（Macro）

巨集是元程式設計最古老的形式之一，在編譯期對程式碼進行文字轉換。

**Lisp 巨集（最強大的巨集系統）**：

```lisp
;; Lisp 巨集：程式碼即資料
(defmacro unless (condition body)
  `(if (not ,condition) ,body))

;; 使用
(unless (> x 10)
  (print "x is not greater than 10"))
```

**Rust 巨集（宣告式和程序式）**：

```rust
// Rust 宣告式巨集
macro_rules! vec {
    ( $( $x:expr ),* ) => {
        {
            let mut temp_vec = Vec::new();
            $(temp_vec.push($x);)*
            temp_vec
        }
    };
}

// Rust 程序式巨集
#[derive(Debug, Clone)]
struct Point { x: i32, y: i32 }
```

### Python 的元程式設計

Python 提供了多種元程式設計機制：

**裝飾器**：

```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_calls
def greet(name):
    return f"Hello, {name}"
```

**元類別（Metaclass）**：

```python
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    pass
```

**動態程式碼產生**：

```python
# exec/eval 執行動態產生的程式碼
code = "result = sum([1, 2, 3, 4, 5])"
exec(code)
print(result)  # 15

# 動態建立函數
def make_multiplier(n):
    # 動態產生 lambda
    return lambda x: x * n
```

### 各語言的元程式設計能力

| 語言 | 巨集類型 | 元程式設計機制 |
|------|---------|------------|
| Lisp | 最強：hygienic macro | 程式碼即資料（同像性） |
| Rust | 強：宣告式 + 程序式 | proc_macro crate |
| Python | 執行期 | 裝飾器、元類別、exec/eval |
| JavaScript | 弱 | Proxy、Reflect、eval |
| C | 非常弱 | 預處理器（文字替換） |
| C++ | template metaprogramming | SFINAE、constexpr |

### 何時使用元程式設計？

**適合使用**的場景：
- 減少樣板程式碼（derive 巨集）
- 領域特定語言（DSL）嵌入
- 自動產生序列化/反序列化程式碼
- 編譯期計算（const fn、模板元程式設計）

**應避免**的場景：
- 程式碼可讀性顯著下降
- 除錯變得極其困難
- 可以透過更簡單的抽象解決

### 延伸閱讀

- [Lisp 巨集](https://www.google.com/search?q=Lisp+macro+tutorial)
- [Rust 程序式巨集](https://www.google.com/search?q=Rust+procedural+macro)
- [Python 元程式設計](https://www.google.com/search?q=Python+metaprogramming+decorator+metaclass)
