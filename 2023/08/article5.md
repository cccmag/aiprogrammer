# 符號表管理

## 前言

符號表（Symbol Table）是編譯器用來追蹤程式中所有識別字資訊的資料結構。從變數、函式到型別，每個命名實體都有自己的符號表條目。符號表管理的品質直接影響編譯器的正確性和效率。

## 符號表條目

每個符號表條目通常包含以下資訊：

```python
class Symbol:
    def __init__(self, name, kind, typeinfo):
        self.name = name       # 識別字名稱
        self.kind = kind       # 變數、函式、型別等
        self.typeinfo = typeinfo  # 型別資訊
        self.scope_level = 0   # 範圍層級
        self.offset = 0        # 記憶體偏移
        self.is_initialized = False  # 是否已初始化
```

## 範圍管理

### 巢狀範圍

大多數程式語言支援巢狀範圍（詞法作用域）：

```python
{
    int x = 1;      # 外層範圍
    {
        int y = 2;  # 內層範圍
        x = y + 1;  # 可以存取外層的 x
    }
    # y = 3;       # 錯誤！y 不可見
}
```

### 使用堆疊管理範圍

```python
class SymbolTable:
    def __init__(self):
        self.scopes = [{}]        # 範圍堆疊
        self.scope_stack = [0]    # 範圍層級追蹤
    
    def enter_scope(self):
        self.scopes.append({})
        self.scope_stack.append(len(self.scope_stack))
    
    def exit_scope(self):
        self.scopes.pop()
        self.scope_stack.pop()
    
    def declare(self, name, symbol):
        if name in self.scopes[-1]:
            raise ValueError(f'Duplicate: {name}')
        symbol.scope_level = self.scope_stack[-1]
        self.scopes[-1][name] = symbol
    
    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None  # 未宣告
```

## 符號表實作

### 雜湊表實作

雜湊表是符號表最常見的底層實作：

```python
class HashSymbolTable:
    def __init__(self, size=211):
        self.size = size
        self.table = [[] for _ in range(size)]
    
    def _hash(self, name):
        h = 0
        for c in name:
            h = (h * 31 + ord(c)) % self.size
        return h
    
    def insert(self, name, symbol):
        idx = self._hash(name)
        for existing, sym in self.table[idx]:
            if existing == name:
                raise ValueError(f'Duplicate: {name}')
        self.table[idx].append((name, symbol))
    
    def lookup(self, name):
        idx = self._hash(name)
        for existing, sym in self.table[idx]:
            if existing == name:
                return sym
        return None
```

### 二元搜尋樹實作

對於較小的符號表，也可以使用二元搜尋樹，方便有序輸出。

## 進階功能

### 函式多載

支援函式多載的語言需要在符號表中區分同名函式：

```python
class OverloadedSymbol:
    def __init__(self, name):
        self.name = name
        self.overloads = {}  # (參數型別) → Symbol
    
    def add_overload(self, param_types, symbol):
        key = tuple(param_types)
        if key in self.overloads:
            raise ValueError(f'Duplicate overload')
        self.overloads[key] = symbol
    
    def resolve(self, arg_types):
        key = tuple(arg_types)
        return self.overloads.get(key)
```

### 名稱修飾（Name Mangling）

C++ 等支援多載的語言使用名稱修飾來編碼型別資訊：

```
int foo(int, float) → _Z3fooi
int foo(int, double) → _Z3foid
```

## 與 Type Checker 的協作

符號表與型別檢查器緊密協作：

```python
class TypeChecker:
    def __init__(self, symtable):
        self.symtable = symtable
    
    def check_assign(self, node):
        sym = self.symtable.lookup(node.name)
        if not sym:
            raise NameError(f'Undefined: {node.name}')
        value_type = self.check_expr(node.value)
        if sym.typeinfo != value_type:
            raise TypeError(f'Type mismatch: {node.name}')
    
    def check_expr(self, node):
        if node.nodetype == 'Ident':
            sym = self.symtable.lookup(node.name)
            if not sym:
                raise NameError(f'Undefined: {node.name}')
            return sym.typeinfo
```

## 結語

符號表是編譯器前端的關鍵基礎設施。好的符號表設計使得語意分析、型別檢查和程式碼生成更容易實作。從簡單的堆疊式符號表開始，逐步加入多載、模板等高階功能，是學習編譯器開發的必經之路。

## 延伸閱讀

- [符號表在編譯器中的角色](https://www.google.com/search?q=symbol+table+compiler+design)
- [詞法作用域](https://www.google.com/search?q=lexical+scoping+nested+scopes)

---

*本篇文章為「AI 程式人雜誌 2023 年 8 月號」編譯器理論系列文章。*
