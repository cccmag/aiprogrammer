# 程式模組化：為什麼需要 OOP？

## 複雜度爆炸的困境

假設你要寫一個簡單的文字編輯器。一開始只有開啟檔案、儲存檔案、編輯文字三個功能，用程序式程式設計可能只需要 200 行程式碼。但隨著需求增加——加入搜尋取代、語法高亮、外掛系統、多標籤頁——程式碼很快會膨脹到數萬行。

在沒有模組化的情況下，你會發現：

- **全域變數到處都是**：`current_file`、`cursor_position`、`highlight_mode` 散落在各處
- **函式參數爆炸**：每個函式都需要 5-8 個參數來傳遞狀態
- **修改一處壞一片**：一個全域變數的改動可能影響數十個函式

這就是「複雜度爆炸」的典型場景。OOP 正是為了解決這個問題而誕生的。

## 模組化的四大好處

### 1. 關注點分離

OOP 讓你把相關的資料與行為打包成類別。文字編輯器的功能可以被拆分為：

```python
class Document:
    def __init__(self):
        self._content = ""
        self._filepath = None

    def open(self, path): ...
    def save(self): ...
    def find_and_replace(self, old, new): ...

class SyntaxHighlighter:
    def highlight(self, code, language): ...

class TabManager:
    def add_tab(self, doc): ...
    def close_tab(self, index): ...
```

每個類別只關注自己的職責，互不干擾。

### 2. 資訊隱藏

類別可以隱藏內部實作細節，只暴露必要的介面。這意味著你可以隨時修改內部實作而不影響外部呼叫者：

```python
class Stack:
    def __init__(self):
        self._items = []  # 內部實作

    def push(self, item):
        self._items.append(item)

    def pop(self):
        return self._items.pop()
```

外部使用者只需要知道 `push` 和 `pop` 的用法，不需要理解 `_items` 的實作。

### 3. 可測試性

模組化的程式碼更容易測試。你可以單獨測試每個類別，而不需要設定整個系統：

```python
def test_stack():
    s = Stack()
    s.push(1)
    s.push(2)
    assert s.pop() == 2
    assert s.pop() == 1
```

### 4. 可重用性

一個設計良好的類別可以在不同專案中重複使用。例如 `Stack` 類別可以在計算器、編譯器、遊戲等任何需要後進先出資料結構的地方使用。

## OOP 的三大特性概覽

物件導向程式設計建立在三大核心特性之上：

**封裝（Encapsulation）**：將資料與操作資料的方法綁定在一起，隱藏內部細節。

```python
class BankAccount:
    def __init__(self):
        self._balance = 0  # 私有屬性

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount

    def get_balance(self):
        return self._balance
```

**繼承（Inheritance）**：從現有類別建立新類別，繼承其屬性和方法。

```python
class Animal:
    def speak(self): ...

class Dog(Animal):
    def speak(self):
        return "汪汪！"
```

**多型（Polymorphism）**：不同類別的物件可以透過相同的介面呼叫，展現不同的行為。

```python
def make_sound(animal):
    print(animal.speak())  # 任何有 speak() 的物件都可以

make_sound(Dog())
make_sound(Cat())
```

## 小結

模組化是管理程式複雜度的關鍵手段，而 OOP 提供了實現模組化的完善工具。封裝保護資料、繼承促進重用、多型增加彈性——三者結合，讓開發者可以建構出既有結構又富有彈性的系統。

## 延伸閱讀

- [模組化程式設計](https://www.google.com/search?q=modular+programming+concepts)
- [什麼是 OOP？](https://www.google.com/search?q=what+is+object+oriented+programming)
