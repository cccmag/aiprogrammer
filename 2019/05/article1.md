# Python 深入：生成器與迭代器

## 前言

生成器和迭代器是 Python 中處理大容量資料的重要工具，對於 AI 開發者處理大型資料集非常實用。

## 迭代器協議

```python
class Counter:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.limit:
            raise StopIteration
        value = self.current
        self.current += 1
        return value

for i in Counter(5):
    print(i)  # 0, 1, 2, 3, 4
```

## 生成器函數

```python
def fibonacci(n):
    """費波那契生成器"""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci(10):
    print(num)  # 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
```

## 生成器表達式

```python
# 記憶體效率高的方式
squares = (x**2 for x in range(1000000))

# 不會立即創建完整列表
for sq in squares:
    print(sq)
    if sq > 100:
        break
```

## 在 ML 中的應用

```python
def batch_generator(data, batch_size):
    """批次生成器"""
    for i in range(0, len(data), batch_size):
        yield data[i:i+batch_size]

# 使用
for batch in batch_generator(large_dataset, 32):
    train_step(model, batch)
```

## 延伸閱讀

- [Python 迭代器詳解](https://www.google.com/search?q=Python+iterators+generators+tutorial)