# 作用域與閉包

## 變數的可視範圍

### 作用域

**作用域（Scope）** 定義了程式中變數的可視範圍。每當變數被引用時，程式語言需要決定這個名稱對應的是哪個變數。

### 詞法作用域 vs 動態作用域

**詞法作用域（Lexical Scoping）**：變數的綁定由程式碼的詞法結構決定——函數內部可以存取其定義時可存取的變數。也稱為靜態作用域。

**動態作用域（Dynamic Scoping）**：變數的綁定由執行時期的呼叫棧決定——當一個變數被引用時，會在呼叫棧上尋找最近綁定的值。

```python
# 詞法作用域：x 由定義時的上下文決定
x = 1
def outer():
    x = 2
    def inner():
        return x  # 這裡的 x 是 outer 中的 x，值為 2
    return inner()
print(outer())  # 2
```

大多數現代語言（Python、JavaScript、Rust、Haskell）都使用詞法作用域。

### 閉包（Closure）

**閉包** 是捕捉了自由變數的函數。閉包「記住」了它被定義時的環境：

```python
def make_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

c1 = make_counter()
print(c1())  # 1
print(c1())  # 2
c2 = make_counter()
print(c2())  # 1 (獨立的捕獲環境)
```

### 閉包的實作

編譯器將閉包實作為一個結構體，包含：
- 函數指標（指向函數程式碼）
- 捕獲的變數（從環境中複製或引用）

Python 的 `__closure__` 屬性可以檢視閉包捕獲的變數：

```python
def f():
    x = 10
    def g(): return x
    return g
print(f().__closure__[0].cell_contents)  # 10
```

### 變數捕獲的陷阱

```python
# Python 經典陷阱：延遲綁定
funcs = []
for i in range(3):
    funcs.append(lambda: i)
print([f() for f in funcs])  # [2, 2, 2] (i 被共享)

# 修正：使用預設參數
funcs = []
for i in range(3):
    funcs.append(lambda i=i: i)
print([f() for f in funcs])  # [0, 1, 2]
```

### 閉包的應用

- **回呼函數**：GUI 事件處理、非同步操作
- **裝飾器**：在不修改原始碼的前提下擴充功能
- **部分應用**：固定函數的部分參數
- **封裝**：模擬私有變數（模組模式）

### 延伸閱讀

- [閉包概念](https://www.google.com/search?q=closure+programming+concept)
- [詞法 vs 動態作用域](https://www.google.com/search?q=lexical+scoping+vs+dynamic+scoping)

---

**下一篇**：[控制流程與 continuation](focus6.md)
