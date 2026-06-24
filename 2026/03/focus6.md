# Rust 與現代系統程式設計（2010s-2020s）

## Rust 的誕生

2006 年，Graydon Hoare 在 Mozilla 工作期間開始開發 Rust。這是一個旨在提供 C++ 的效能和控制力的語言，同時確保記憶體安全。

> 「Rust 是一個將現代語言理論與系統程式設計結合的實驗。」—— Graydon Hoare

### Rust 的設計目標

```
┌─────────────────────────────────────────────────────┐
│                   Rust 設計目標                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│    效能 ──────────────────────────────────► 記憶體安全│
│    ▲                                            ▲  │
│    │                                            │  │
│    │    零成本抽象    實用主義    融合兩者        │  │
│    │                                            │  │
│    └────────────────────────────────────────────┘  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 所有權系統：Rust 的核心創新

Rust 的革命性在於其所有權系統——這是一種在編譯時確保記憶體安全的機制，無需垃圾回收。

### 所有權規則

```rust
// Rust 的三條所有權規則：

// 規則 1：每個值有一個所有者
let s1 = String::from("hello");
let s2 = s1;  // s1 的所有權移動到 s2
// println!("{}", s1);  // 錯誤！s1 已無效

// 規則 2：同一時間只有一個所有者
let s1 = String::from("hello");
let s2 = s1;  // 所有權移動
// s1 和 s2 不能同時存在

// 規則 3：當所有者離開作用域，值被丟棄
{
    let s = String::from("hello");
}  // s 在這裡被 drop
```

### 借用檢查器

Rust 的借用檢查器確保記憶體安全：

```rust
fn main() {
    let mut s = String::from("hello");
    
    // 不可變借用
    let r1 = &s;
    let r2 = &s;
    println!("{} and {}", r1, r2);
    // r1 和 r2 在這裡不再使用，可以安全釋放
    
    // 可變借用
    let r3 = &mut s;
    r3.push_str(", world");
    println!("{}", r3);
    // r3 在這裡離開作用域，不再可變借用
}
```

### 生命週期

生命週期確保引用始終有效：

```rust
// 生命週期註解
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// 'a 表示返回的引用與輸入的引用有相同的生命週期

struct Important<'a> {
    part: &'a str,
}

impl<'a> Important<'a> {
    fn level(&self) -> i32 {
        3
    }
}
```

### 視覺化所有權

```
┌─────────────────────────────────────────────────────┐
│                   所有權示意                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  let s = String::from("hello");                   │
│    │                                               │
│    ▼                                               │
│  ┌─────────────┐                                   │
│  │  s: 0x1234  │                                 │
│  │  heap: "hello"                                 │
│  └─────────────┘                                   │
│                                                     │
│  let s2 = s;  // 移動                              │
│    │                                               │
│    ▼                                               │
│  ┌─────────────┐                                   │
│  │  s2: 0x1234  │  (s 失效)                      │
│  │  heap: "hello"                                 │
│  └─────────────┘                                   │
│                                                     │
│  drop(s2);  // 釋放記憶體                          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Rust 的函式特性

Rust 的設計深受函式程式設計影響。

### 閉包

```rust
// 閉包語法
let add_one = |x| x + 1;
let add = |x, y| x + y;
let print_and_return = |x| { 
    println!("x = {}", x); 
    x 
};

// 閉包捕獲環境
let multiplier = 10;
let scaled = |x| x * multiplier;

// Fn, FnMut, FnOnce
fn apply<F>(f: F) where F: Fn(i32) -> i32 {
    f(5)
}

fn apply_mut<F>(mut f: F) where F: FnMut(i32) -> i32 {
    f(5)
}

fn consume<F>(f: F) where F: FnOnce(i32) -> i32 {
    f(5)
}
```

### Option 與 Result

```rust
// Option：處理可能為空的值
fn find_user(id: u32) -> Option<User> {
    if id == 1 { Some(User { name: "Alice" }) }
    else { None }
}

fn main() {
    match find_user(1) {
        Some(user) => println!("Found: {}", user.name),
        None => println!("User not found"),
    }
    
    // 或使用 ? 運算子
    let user = find_user(1)?;
    println!("Found: {}", user.name);
}

// Result：處理可能失敗的操作
fn read_file(path: &str) -> Result<String, std::io::Error> {
    std::fs::read_to_string(path)
}

fn main() {
    let content = read_file("config.txt")?;
    println!("{}", content);
}
```

### 模式匹配

```rust
// match 表達式
match value {
    Some(x) => println!("{}", x),
    None => println!("nothing"),
}

// if let 簡化
if let Some(x) = find_user(1) {
    println!("Found: {}", x.name);
}

// while let 迴圈
while let Some(line) = lines.next() {
    println!("{}", line);
}

// 哨兵模式
match x {
    Some(ref n) if *n > 0 => println!("positive: {}", n),
    Some(ref n) if *n < 0 => println!("negative: {}", n),
    Some(0) => println!("zero"),
    None => println!("none"),
    _ => println!("other"),
}
```

---

## Iterator 與 combinator

Rust 的 Iterator 是函式程式設計的完美體現。

### 基本操作

```rust
// 鏈式呼叫
let result: i32 = (1..1000)
    .filter(|x| x % 3 == 0 || x % 5 == 0)  // 過濾
    .map(|x| x * x)                        // 轉換
    .sum();                                 // 聚合

// collect 收集為不同類型
let vec: Vec<i32> = (1..10).collect();
let set: HashSet<i32> = (1..10).collect();
let string: String = (b'A'..=b'Z')
    .map(|c| c as char)
    .collect();
```

### 惰性求值

Iterator 是惰性的——什麼都不計算，直到你消費它：

```rust
// 這不會立即執行任何操作！
let iter = (1..1000)
    .filter(|x| x % 2 == 0)
    .map(|x| x * x);

// 只有在這裡才開始計算
let first_five: Vec<_> = iter.take(5).collect();

// 如果不收集，迭代器不會執行
// 這對於處理無限序列特別有用
let fibs = (0i64..)
    .scan((0, 1), |state, _| {
        *state = (state.1, state.0 + state.1);
        Some(state.0)
    });

let first_10: Vec<_> = fibs.take(10).collect();
// [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### combinator 方法

```rust
// 常見 combinator
let numbers = vec![1, 2, 3, 4, 5];

// map
let doubled: Vec<_> = numbers.iter().map(|x| x * 2).collect();

// filter
let evens: Vec<_> = numbers.iter().filter(|x| *x % 2 == 0).collect();

// filter_map
let parsed: Vec<_> = ["1", "two", "3", "four"]
    .iter()
    .filter_map(|s| s.parse::<i32>().ok())
    .collect();

// flat_map
let words = vec!["hello", "world"];
let chars: Vec<_> = words.iter().flat_map(|s| s.chars()).collect();

// take_while, skip_while
let first_positive = numbers.iter().skip_while(|x| **x <= 0).next();

// fold
let sum = numbers.iter().fold(0, |acc, x| acc + x);
let product = numbers.iter().product();

// reduce
let max = numbers.iter().cloned().reduce(|a, b| if a > b { a } else { b });
```

### 自定義 Iterator

```rust
struct Counter {
    count: u32,
    max: u32,
}

impl Counter {
    fn new(max: u32) -> Counter {
        Counter { count: 0, max }
    }
}

impl Iterator for Counter {
    type Item = u32;
    
    fn next(&mut self) -> Option<Self::Item> {
        if self.count < self.max {
            self.count += 1;
            Some(self.count)
        } else {
            None
        }
    }
}

// 使用自定義 Iterator
let counter = Counter::new(5);
let sum: u32 = counter.sum();
println!("Sum: {}", sum);  // 15
```

### 迭代器適配器鏈

```
┌─────────────────────────────────────────────────────┐
│               Iterator 適配器鏈                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  (1..1000)  ──► filter(even)  ──► map(*2)  ──► sum │
│   Iterator      Iterator       Iterator      i32    │
│                                                     │
│  惰性 ──────────────────────────────────────────► │
│                                                     │
│  只有在呼叫 .sum() 時才開始計算！                   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 錯誤處理模式

Rust 的錯誤處理是函式式的：

### Option  combinator

```rust
// 鏈式操作
fn get_city(user: &User) -> Option<&str> {
    user.address
        .as_ref()
        .and_then(|addr| addr.city.as_deref())
}

// unwrap_or, unwrap_or_else
let value = maybe_number.unwrap_or(0);
let value = maybe_number.unwrap_or_else(|| expensive_default());

// map
let upper = maybe_string.map(|s| s.to_uppercase());

// ok_or：轉換為 Result
let result: Result<i32, ()> = 
    maybe_number.ok_or(());

// and_then
fn parse_and_double(s: &str) -> Option<i32> {
    s.parse::<i32>().ok().map(|n| n * 2)
}
```

### Result combinator

```rust
// map
fn parse_and_format(s: &str) -> Result<String, ParseError> {
    s.parse::<i32>()
        .map(|n| format!("Number: {}", n))
}

// map_err
fn read_config(path: &str) -> Result<Config, io::Error> {
    fs::read_to_string(path)
        .and_then(|content| {
            content.parse::<Config>()
                   .map_err(|e| io::Error::new(
                       io::ErrorKind::InvalidData, e))
        })
}

// or_else：處理錯誤後返回新 Result
fn read_or_default(path: &str) -> Result<String, io::Error> {
    read_file(path).or_else(|_| Ok(DEFAULT_CONTENT))
}
```

### ? 運算子

```rust
// ? 運算子是錯誤傳播的語法糖
fn read_and_parse(path: &str) -> Result<Config, Box<dyn Error>> {
    let content = fs::read_to_string(path)?;  // 可能返回 Err
    let config = content.parse::<Config>()?;  // 可能返回 Err
    Ok(config)
}

// 展開後相當於：
fn read_and_parse(path: &str) -> Result<Config, Box<dyn Error>> {
    let content = match fs::read_to_string(path) {
        Ok(c) => c,
        Err(e) => return Err(e.into()),
    };
    let config = match content.parse::<Config>() {
        Ok(c) => c,
        Err(e) => return Err(e.into()),
    };
    Ok(config)
}
```

---

## Rust 對函式編程的影響

### 與 Haskell 的對比

| Haskell | Rust |
|---------|------|
| Maybe a | Option<T> |
| Either e a | Result<T, E> |
| Monad | ? 運算子, combinator |
| 惰性列表 | Iterator |
| 類別系統 | Trait |
| Lazy evaluation | 預設 eager, Iterator 惰性 |

### Rust 特有的創新

```rust
// 非同步編程
#[tokio::main]
async fn main() {
    let data = fetch_from_api().await?;
    process(data);
}

// 特性物件
trait Draw {
    fn draw(&self);
}

fn draw_all(drawables: Vec<Box<dyn Draw>>) {
    for d in drawables {
        d.draw();
    }
}

// 內聯組合
let result = (1..1000)
    .filter(|x| x % 2 == 0)
    .map(|x| x * x)
    .take(10)
    .collect::<Vec<_>>();
```

---

## Rust 的現狀與未來

### Rust 的成就

- 2021 年起連續多年獲得 Stack Overflow「最受喜愛語言」
- 被用於 Linux 核心開發
- 成為雲端基礎設施的主流語言
- WebAssembly 生態的重要組成部分

### Rust 2024 Edition

Rust 2024 Edition 將帶來更多函式特性的增強：

```rust
// 未來可能支援的語法
// 更好的 async/await
// 增強的模式匹配
// 更強的型別推斷
```

---

## 結語

Rust 展示了如何將函式程式設計的精華應用於系統程式設計：

1. **所有權系統**：純函式的記憶體管理
2. **Iterator**：惰性求值和函式組合
3. **Result 和 Option**：類型安全的錯誤處理
4. **Pattern matching**：強大的控制流抽象

Rust 的成功證明：函式編程的概念不僅適用於高階應用，也可以應用於需要精確控制的底層系統。

---

## 延伸閱讀

- [Rust 官方書籍](https://www.google.com/search?q=The+Rust+Programming+Language+book)
- [Iterator 文件](https://www.google.com/search?q=Rust+Iterator+documentation)
- [所有權系統深入](https://www.google.com/search?q=Rust+ownership+system+explained)

---

*本篇文章為「AI 程式人雜誌 2026 年 3 月號」歷史回顧系列之六。*
