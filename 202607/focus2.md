# 所有權模型

## Rust 的核心創新：Ownership、Borrowing、Lifetimes（2010-2015）

### 記憶體管理的三種典範

在 Rust 之前，系統程式語言處理記憶體的方式主要有兩種：

1. **手動管理（C/C++）**：程式設計師自己呼叫 `malloc`/`free` 或 `new`/`delete`。效能最高，但容易出錯——use-after-free、double free、memory leak……
2. **垃圾回收（Java/Go）**：執行時期自動回收不再使用的記憶體。安全性高，但有停頓時間（GC pause）和額外記憶體開銷。

Rust 提出了第三種方式：**所有權模型**——在編譯期檢查記憶體的安全性，不依賴垃圾回收，也不需手動管理。

### 所有權（Ownership）的三條規則

所有權模型的核心是三條規則：

1. **Rust 中的每個值都有一個所有者（owner）**
2. **一個值同時只能有一個所有者**
3. **當所有者離開作用域時，值會被丟棄**

```rust
{
    let s = String::from("hello"); // s 是 String 的所有者
    // 可以在這裡使用 s
} // 離開作用域，s 被自動釋放
```

這三條規則看似簡單，但帶來了深遠的影響：

```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1; // 所有權從 s1 轉移到 s2
    
    // println!("{}", s1); // 編譯錯誤！s1 的所有權已經轉移
    println!("{}", s2); // OK
}
```

### 借用（Borrowing）

當然，如果每次使用變數都必須轉移所有權，程式設計會變得非常困難。Rust 提供了**借用**機制——透過引用（reference）來存取值而不轉移所有權：

```rust
fn calculate_length(s: &String) -> usize { // 借用 String
    s.len()
} // s 離開作用域，但因為是借用，不會釋放 String

fn main() {
    let s = String::from("hello");
    let len = calculate_length(&s); // 傳入引用
    println!("The length of '{}' is {}.", s, len); // s 仍然可用
}
```

**借用規則**：
- 可以有多個不可變引用（`&T`）
- 同時只能有一個可變引用（`&mut T`）
- 不可變引用和可變引用不能同時存在

```rust
let mut s = String::from("hello");

let r1 = &s;   // OK
let r2 = &s;   // OK
// let r3 = &mut s; // 編譯錯誤！已有不可變引用

println!("{}, {}", r1, r2);
// r1, r2 在此之後不再使用

let r3 = &mut s; // OK，r1, r2 已不再使用
r3.push_str(" world");
```

### 生命週期（Lifetimes）

生命週期是 Rust 最複雜的概念。它確保引用在存取的資料有效時才能使用：

```rust
// 函式簽名中的 'a 是生命週期參數
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
```

這表示：回傳的引用至少與 `x` 和 `y` 中較短的那個一樣長。編譯器會在呼叫點檢查：

```rust
fn main() {
    let string1 = String::from("long string is long");
    let result;
    {
        let string2 = String::from("xyz");
        result = longest(&string1, &string2); // 編譯錯誤！
        // result 的生命週期不能超過 string2
    }
    // println!("{}", result); // 如果這裡能用就 UB 了
}
```

生命週期註解大多是編譯器可以自動推斷的（生命週期省略規則，lifetime elision）。開發者只需要在少數複雜情況下手動標註。

### 在 C++ 中實現類似 Rust 的記憶體安全

Rust 的所有權模型是否可以在 C++ 中模仿？理論上可以，但需要人工遵守約定：

```cpp
// C++ 中模仿 Rust 的所有權
class UniqueString {
    std::string* data;
public:
    // 類似 Rust 的所有權轉移（move）
    UniqueString(UniqueString&& other) : data(other.data) {
        other.data = nullptr; // 類似 Rust 的 move
    }
    ~UniqueString() { delete data; }
};
```

但 C++ 無法在編譯期強制這些規則——這就是為什麼 C++ 的智慧指標（unique_ptr、shared_ptr）雖有幫助，但仍然無法完全防止記憶體錯誤。

### 與 GC 語言的對比

| 特性 | Rust | Java/Go | C/C++ |
|------|------|---------|-------|
| 記憶體安全 | 編譯期保證 | 執行時期保證 | 無保證 |
| GC pause | 無 | 有 | 無 |
| 執行時期開銷 | 無 | GC + 記憶體開銷 | 無 |
| 學習曲線 | 陡峭 | 平緩 | 中等 |
| 控制力 | 精細 | 粗放 | 精細 |

### 所有權模型的代價

所有權模型雖然強大，但也有代價：

1. **學習曲線陡峭**：開發者需要理解所有權、借用、生命週期等新概念
2. **程式碼冗長**：有時需要額外的工作來滿足借用檢查器
3. **某些模式難以表達**：如雙向鏈結串列、圖結構等需要 `Rc<RefCell<T>>` 或 unsafe

但隨著時間推移，社群發現這些「代價」帶來的回報遠大於成本——**Rust 專案中的記憶體安全漏洞比其他系統語言少 70%**。

### 小結

所有權模型是 Rust 最核心的創新。它讓 Rust 在不依賴垃圾回收的情況下達到了 C 語言等級的效能，同時提供了媲美 Java 的記憶體安全保證。這個設計讓 Rust 在系統程式設計領域找到了獨特的定位——既能處理底層的記憶體操作，又能保證上層的安全性。

---

**下一步**：[編譯器與工具鏈](focus3.md)

## 延伸閱讀

- [The Rust Book: Ownership](https://www.google.com/search?q=Rust+book+ownership)
- [Rust 記憶體安全模型分析](https://www.google.com/search?q=Rust+memory+safety+model+analysis)
- [Understanding Rust Lifetimes](https://www.google.com/search?q=understanding+Rust+lifetimes)
