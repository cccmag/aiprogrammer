# Monad 與 Functor

## 計算的抽象化

### Functor（函子）

Functor 是實現了 `fmap`（或 `map`）操作的型別類別，允許在容器內部應用函數：

```python
# Python 中的 Functor
numbers = [1, 2, 3]
doubled = list(map(lambda x: x * 2, numbers))
# [2, 4, 6]

# Functor 定律：
# 1. fmap id = id（單位律）
# 2. fmap (f . g) = fmap f . fmap g（組合律）
```

```rust
// Rust 中的 Functor：Option::map
let x = Some(3);
let y = x.map(|v| v + 1); // Some(4)
```

Functor 的概念很簡單：**在上下文中應用純函數**。上下文可能是可選值（Option）、錯誤處理（Result）、列表（非確定性）或未來值（Promise）。

### Monad（單子）

Monad 是 Functor 的超集，增加了 `bind`（或 `flat_map` / `>>= `）操作：

```python
# Maybe Monad 的 bind
def safe_div(x, y):
    return Maybe.just(x // y) if y != 0 else Maybe.nothing()

result = (Maybe.just(10)
          .bind(lambda x: safe_div(x, 2)))
# Just(5)

# 鏈式操作
result = (Maybe.just(10)
          .bind(lambda x: safe_div(x, 2))
          .bind(lambda y: safe_div(y, 5)))
# Just(1)
```

### Monad 定律

1. **左單位律**：`pure(a) >>= f` 等價於 `f(a)`
2. **右單位律**：`m >>= pure` 等價於 `m`
3. **結合律**：`(m >>= f) >>= g` 等價於 `m >>= (λx. f(x) >>= g)`

### 常見的 Monad

```python
# Maybe Monad：處理可能失敗的計算
# List Monad：非確定性計算
# Either Monad：帶錯誤訊息的計算
# State Monad：有狀態的計算
# IO Monad：帶副作用的計算
# Reader Monad：共享環境
# Writer Monad：日誌記錄
```

### Monad 的實務應用

```python
# Rust 的 Result 是 Monad
fn process(input: i32) -> Result<i32, String> {
    Ok(input)
        .and_then(|x| {
            if x > 0 { Ok(x) }
            else { Err("negative".into()) }
        })
        .and_then(|x| Ok(x * 2))
}
```

```python
# Python 中 asyncio 的 await 類似 Monadic 操作
async def fetch_data():
    data = await fetch_from_api()   # 類似 bind
    processed = await process(data)  # 鏈式操作
    return processed
```

### Monad 不等於難懂

Monad 的聲譽讓初學者望而生畏，但其實每天都在用：

- **Optional chaining**（`?.`）：Maybe Monad
- **Promise/then**：Future Monad
- **Error propagation**（`?` 運算符）：Result/Either Monad
- **List comprehension**：List Monad

### 延伸閱讀

- [Functor 與 Monad 解釋](https://www.google.com/search?q=functor+monad+explained+simply)
- [Monad 定律](https://www.google.com/search?q=monad+laws+programming)
