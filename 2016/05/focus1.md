# 主題一：類型系統導論

## 什麼是類型系統？

類型系統（Type System）是程式語言中定義、操作和檢查類型的規則集合。類型系統告訴程式：

- 資料的種類（數字、字串、布林值等）
- 可以對資料進行的操作
- 如何存儲和表示資料

```python
# 類型告訴我們：
# 1. 這是什麼種類的資料
# 2. 可以進行什麼操作

x = 5       # 整數，可以做加法
name = "Alice"  # 字串，可以做串聯
flag = True     # 布林值，可以做邏輯運算
```

## 靜態類型 vs 動態類型

### 靜態類型

類型在編譯時確定：

```java
// Java：靜態類型
int x = 5;           // x 是 int 類型
String name = "Bob"; // name 是 String 類型
// x = "hello";      // 編譯錯誤！
```

優點：
- 編譯時發現錯誤
- 更好的 IDE 支援
- 可能更好的效能（無需运行时檢查）

缺點：
- 需要更多程式碼（類型標注）
- 編譯時間較長

代表語言：Java、C++、C#、Rust、Go

### 動態類型

類型在執行時確定：

```python
# Python：動態類型
x = 5           # x 是整數
x = "hello"     # x 變成字串，完全合法
```

優點：
- 程式碼更簡潔
- 更靈活的程式設計
- 快速原型開發

缺點：
- 錯誤只在執行時發現
- 無法預先發現類型錯誤
- 執行時類型檢查有開銷

代表語言：Python、Ruby、JavaScript、PHP

### 漸進類型（Gradual Typing）

結合靜態和動態類型的優點：

```python
# TypeScript：漸進類型
let x: number = 5;
x = "hello";  // 錯誤：Type 'string' is not assignable to type 'number'

let y = 10;    // 推斷為 number
y = "world";   // 錯誤（嚴格模式）
```

## 強類型 vs 弱類型

### 強類型

語言強制執行類型規則，不允許隱式類型轉換：

```python
# Python：強類型
x = 5
y = "10"
# result = x + y  # 錯誤！不能將 str 和 int 相加
result = x + int(y)  # 必須明確轉換
```

優點：
- 更安全
- 行為更容易預測

缺點：
- 需要更多顯式轉換

代表語言：Python、Java、Rust、 Haskell

### 弱類型

允許隱式類型轉換，可能產生意外的行為：

```javascript
// JavaScript：弱類型
let x = 5;
let y = "10";
let result = x + y;  // "510"（數字被轉換為字串）
let z = "10" - 5;    // 5（字串被轉換為數字）
```

優點：
- 程式設計更彈性
- 有時更方便

缺點：
- 行為可能出人意料
- 更容易出錯

代表語言：JavaScript、PHP、C（某些情況）

## 類型推論

讓編譯器自動推斷類型：

```rust
// Rust：類型推論
let x = 5;        // 推斷為 i32
let y = 3.14;     // 推斷為 f64

// 明確標注
let x: i32 = 5;
let y: f64 = 3.14;
```

```scala
// Scala：類型推論
val x = 5           // Int
val y = List(1, 2, 3)  // List[Int]
val z = x.toString   // String
```

## 代數資料類型（ADT）

結合簡單類型形成複雜類型：

```haskell
-- Haskell：代數資料類型
data Shape = Circle Double           -- 圓（半徑）
           | Rectangle Double Double -- 長方形（寬、高）
           | Triangle Double Double Double -- 三角形

area :: Shape -> Double
area (Circle r) = pi * r * r
area (Rectangle w h) = w * h
area (Triangle a b c) = -- Heron's formula
    let s = (a + b + c) / 2
    in sqrt(s * (s - a) * (s - b) * (s - c))
```

```rust
// Rust：枚舉（ADT）
enum Shape {
    Circle(f64),
    Rectangle(f64, f64),
    Triangle(f64, f64, f64),
}

fn area(shape: &Shape) -> f64 {
    match shape {
        Shape::Circle(r) => std::f64::consts::PI * r * r,
        Shape::Rectangle(w, h) => w * h,
        Shape::Triangle(a, b, c) => {
            let s = (a + b + c) / 2.0;
            (s * (s - a) * (s - b) * (s - c)).sqrt()
        }
    }
}
```

## 泛型（Generics）

參數化類型，允許撰寫可復用程式碼：

```java
// Java：泛型
class Box<T> {
    private T value;
    public void set(T value) { this.value = value; }
    public T get() { return value; }
}

Box<Integer> intBox = new Box<>();
intBox.set(42);
Integer x = intBox.get();
```

```python
# Python：泛型（通過 TypeVar）
from typing import TypeVar, List

T = TypeVar('T')

def first(lst: List[T]) -> T:
    return lst[0]

x: int = first([1, 2, 3])
name: str = first(["a", "b", "c"])
```

## 指標類型與參考類型

### 指標

記憶體位址的抽象：

```c
// C：指標
int x = 5;
int *ptr = &x;    // ptr 儲存 x 的位址
*ptr = 10;        // 修改 x 為 10
printf("%d", x);  // 輸出 10
```

### 參考

指標的安全抽象：

```cpp
// C++：參考
int x = 5;
int &ref = x;  // ref 是 x 的參考
ref = 10;      // x 現在是 10
```

### 指標 vs 參考

| 特性 |指標 | 參考 |
|-----|-----|-----|
| 可為空 | 是 | 否（總是引用某物） |
| 可重新指定 | 是 | 否 |
| 算術運算 | 是 | 否 |
| 語法複雜度 | 較複雜 | 較簡單 |

## 小結

類型系統是程式語言設計的核心。理解靜態/動態、強/弱類型的權衡，有助於我們選擇適合的語言和設計更好的系統。