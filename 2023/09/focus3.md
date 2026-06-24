# 多型與泛型

## 同一程式碼，不同型別

### 什麼是多型？

多型（Polymorphism）允許同一段程式碼處理不同型別的資料。這是程式語言中最重要的抽象化機制之一。

### 三種多型

**1. 參數多型（Parametric Polymorphism）**

又稱泛型（Generics）。函數或資料結構的型別參數化：

```python
# Python 型別提示的泛型
from typing import TypeVar, List
T = TypeVar('T')
def first(items: List[T]) -> T:
    return items[0]
```

Rust 的泛型、Java 的泛型、C++ 的 template 都屬於參數多型。

**2. 特設多型（Ad-hoc Polymorphism）**

又稱多載（Overloading）。同一函數名稱在不同型別上有不同實作：

```python
# Rust 的 trait 實現特設多型
# trait Add { fn add(self, other: Self) -> Self; }
# impl Add for i32 { ... }
# impl Add for f64 { ... }
```

Haskell 的 typeclass、Rust 的 trait、Java 的 interface 都屬於此類。

**3. 子型別多型（Subtype Polymorphism）**

子類別可以取代父類別使用（Liskov 替換原則）：

```python
class Animal:
    def speak(self): pass
class Dog(Animal):
    def speak(self): return "Woof"

def make_sound(a: Animal): return a.speak()
make_sound(Dog())  # Dog 是 Animal 的子型別
```

### 泛型的實作方式

- **模板展開**（C++）：編譯期生成型別特化版本，程式碼膨脹但零成本
- **型別擦除**（Java）：編譯期移除型別參數，執行時期無泛型資訊
- **單態化**（Rust）：類似模板展開，但有限度最佳化

### 泛型約束

泛型參數可以加上約束（bounds），限制可使用的型別：

```python
# Rust: fn max<T: Ord>(a: T, b: T) -> T { ... }
# Haskell: max :: Ord a => a -> a -> a
```

約束讓泛型程式碼既能保持型別安全，又能利用型別特定的功能。例如 Rust 的 `Hash` trait 約束保證泛型雜湊表只能使用可雜湊的鍵類型。

### 存在量化 vs 全稱量化

- **全稱量化（Universal Quantification）**：`∀T. f(T) → T`——對所有型別 T 都適用
- **存在量化（Existential Quantification）**：`∃T. T`——存在某個型別 T

Rust 的 `dyn Trait` 是存在量化的體現——執行時期才知道具體型別，但保證實現了某個 trait。

### 實務應用

- **容器型別**：`List<T>`、`Option<T>`、`Result<T, E>`
- **演算法抽象**：排序、搜尋、迭代器鏈
- **依賴注入**：透過 trait bound 實現鬆散耦合

### 延伸閱讀

- [泛型程式設計](https://www.google.com/search?q=generic+programming+programming+languages)
- [參數多型 vs 特設多型](https://www.google.com/search?q=parametric+vs+ad+hoc+polymorphism)

---

**下一篇**：[λ 演算與函數式程式設計](focus4.md)
