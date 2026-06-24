# 型別檢查系統

## 前言

型別檢查（Type Checking）是編譯器語意分析的核心。型別系統確保程式的運算元具有正確的型別，在編譯期捕獲大量潛在錯誤。本文探討型別檢查的理論、設計和實作。

## 型別的表示

型別在編譯器內部通常表示為一個資料結構：

```python
class Type:
    def __init__(self, kind):
        self.kind = kind  # 'int', 'float', 'bool', 'array', 'function'

class PrimitiveType(Type):
    def __init__(self, kind, size):
        super().__init__(kind)
        self.size = size  # 型別佔用的位元組數

class ArrayType(Type):
    def __init__(self, elem_type, length):
        super().__init__('array')
        self.elem_type = elem_type
        self.length = length

class FunctionType(Type):
    def __init__(self, param_types, return_type):
        super().__init__('function')
        self.param_types = param_types
        self.return_type = return_type
```

## 型別檢查的過程

型別檢查器（Type Checker）走訪 AST，為每個節點計算型別，並檢查型別相容性：

```python
class TypeChecker:
    def __init__(self, symtable):
        self.symtable = symtable
    
    def check(self, node):
        method = f'check_{node.nodetype}'
        if hasattr(self, method):
            return getattr(self, method)(node)
        raise NotImplementedError(f'{node.nodetype}')
```

### 數字常數

```python
def check_Number(self, node):
    # 整數常數的型別為 int
    node.type = PrimitiveType('int', 4)
    return node.type
```

### 識別字

```python
def check_Ident(self, node):
    sym = self.symtable.lookup(node.name)
    if not sym:
        raise NameError(f'Undefined variable: {node.name}')
    node.type = sym.typeinfo
    return node.type
```

### 二元運算

```python
def check_BinOp(self, node):
    left_type = self.check(node.left)
    right_type = self.check(node.right)
    
    # 型別相容性檢查
    if left_type.kind != right_type.kind:
        raise TypeError(f'Type mismatch: {left_type.kind} vs {right_type.kind}')
    
    # 型別升級（例如 int + float → float）
    node.type = self.coerce(left_type, right_type)
    return node.type

def coerce(self, t1, t2):
    # 簡單的型別升級規則
    if t1.kind == 'float' or t2.kind == 'float':
        return PrimitiveType('float', 4)
    return PrimitiveType('int', 4)
```

### 賦值陳述式

```python
def check_Assign(self, node):
    sym = self.symtable.lookup(node.name)
    if not sym:
        raise NameError(f'Undefined: {node.name}')
    value_type = self.check(node.value)
    if sym.typeinfo.kind != value_type.kind:
        raise TypeError(
            f'Cannot assign {value_type.kind} to {sym.typeinfo.kind}'
        )
```

## 多型與泛型

Hindley-Milner 型別推論系統支援參數化多型：

```python
# 在 ML 中
let f x = x
# f : 'a → 'a （對所有型別 a 通用）

let length lst = ...
# length : 'a list → int
```

## 型別安全

型別安全的語言保證程式不會執行非法操作：

```
Safe:   int + int           → int
Unsafe: int + string        → Type Error
Safe:   array[index]        → element
Unsafe: array[invalid_idx]  → 執行期錯誤（但非型別錯誤）
```

## 型別錯誤的範例

```python
# 型別錯誤案例
x := 42        # x 的型別為 int
y := "hello"   # y 的型別為 string
z := x + y     # ❌ 型別不匹配：int + string

# 未宣告錯誤
w := a + 1     # ❌ a 未宣告
```

## 結語

型別檢查是編譯器最重要的安全機制之一。一個健全的型別系統可以在編譯期捕獲大量錯誤，提高程式碼品質和開發效率。從簡單的靜態型別檢查到複雜的泛型和特設多型，型別系統的設計是程式語言設計的核心問題。

## 延伸閱讀

- [型別系統理論](https://www.google.com/search?q=type+system+programming+languages+theory)
- [Hindley-Milner 型別推論](https://www.google.com/search?q=Hindley+Milner+type+inference+algorithm)
- [Rust 所有權與型別](https://www.google.com/search?q=Rust+ownership+type+system)

---

*本篇文章為「AI 程式人雜誌 2023 年 8 月號」編譯器理論系列文章。*
