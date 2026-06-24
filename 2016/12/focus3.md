# 主題三：Rust 程式語言

## Rust 簡介

Rust 是一種系統程式語言，專注於安全性、並發性和效能。由 Mozilla 主導開發，首版於 2010 年發布，1.0 版本於 2015 年發布。

### Rust 的核心價值

```rust
// Rust 的三大核心原則
fn main() {
    // 1. 記憶體安全 - 編譯時杜絕記憶體錯誤
    // 2. 零成本抽象 - 抽象不帶來執行期開銷
    // 3. 並發安全 - 防止資料競態
}
```

### Rust vs 其他語言

```python
comparison = {
    'C/C++': '記憶體不安全，需要手動管理',
    'Java/Go': '有垃圾回收，犧牲效能',
    'Rust': '記憶體安全，無 GC，並發安全，零成本抽象',
}
```

## 安裝和工具鏈

```bash
# 安裝 Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 更新
rustup update

# 建構工具
rustc --version
cargo --version

# 文件
rustup doc
```

## 基本語法

### Hello World

```rust
fn main() {
    println!("Hello, world!");
}
```

### 變數和可變性

```rust
fn main() {
    // 不可變變數
    let x = 5;
    println!("x = {}", x);

    // 可變變數
    let mut y = 5;
    y += 1;
    println!("y = {}", y);

    // 型別推斷
    let z: i32 = 5;

    // 常量
    const MAX_POINTS: i32 = 100_000;
}
```

### 資料型別

```rust
fn main() {
    // 整數
    let a: i32 = 42;
    let b: u32 = 42;
    let c: isize = 42;
    let d: usize = 42;

    // 浮點數
    let f: f64 = 3.14;

    // 布林
    let b: bool = true;

    // 字元
    let c: char = 'A';

    // 元組
    let tuple: (i32, f64, u8) = (500, 6.4, 1);
    let (x, y, z) = tuple;

    // 陣列
    let arr: [i32; 5] = [1, 2, 3, 4, 5];
    let first = arr[0];
}
```

### 函式

```rust
fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

fn main() {
    println!("{}", add(1, 2));
    println!("{}", greet("World"));
}
```

### 流程控制

```rust
fn main() {
    // if 表達式
    let x = 5;
    if x > 0 {
        println!("positive");
    } else if x < 0 {
        println!("negative");
    } else {
        println!("zero");
    }

    // if let
    let option: Option<i32> = Some(5);
    if let Some(value) = option {
        println!("value = {}", value);
    }

    // match 表達式
    match x {
        1 => println!("one"),
        2 => println!("two"),
        _ => println!("other"),
    }

    // 迴圈
    for i in 0..5 {
        println!("i = {}", i);
    }

    let mut counter = 0;
    while counter < 5 {
        counter += 1;
    }

    loop {
        if counter > 10 {
            break;
        }
        counter += 1;
    }
}
```

## 所有權系統

### 所有權規則

```rust
fn main() {
    // Rust 的所有權規則：
    // 1. 每個值有一個所有者
    // 2. 一次只有一個所有者
    // 3. 當所有者離開作用域，值被 drop

    let s1 = String::from("hello");
    let s2 = s1; // s1 被移動到 s2
    // println!("{}", s1); // 錯誤：s1 不再有效
    println!("{}", s2); // 正確

    // Clone
    let s3 = s2.clone();
    println!("{} {}", s2, s3);
}
```

### 借用

```rust
fn main() {
    let s = String::from("hello");

    // 不可變借用
    let len = calculate_length(&s);
    println!("Length of '{}' is {}", s, len);

    // 可變借用
    let mut s2 = String::from("hello");
    change(&mut s2);
    println!("{}", s2);
}

fn calculate_length(s: &String) -> usize {
    s.len()
}

fn change(s: &mut String) {
    s.push_str(", world!");
}
```

### 生命週期

```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

struct Important<'a> {
    excerpt: &'a str,
}

impl<'a> Important<'a> {
    fn announce_and_return(&self, announcement: &str) -> &str {
        println!("Attention: {}", announcement);
        self.excerpt
    }
}
```

## 結構體和列舉

### 結構體

```rust
struct User {
    username: String,
    email: String,
    sign_in_count: u64,
    active: bool,
}

impl User {
    fn new(email: String, username: String) -> User {
        User {
            email,
            username,
            sign_in_count: 0,
            active: true,
        }
    }

    fn问候(&self) {
        println!("Hello, {}!", self.username);
    }
}

fn main() {
    let user = User::new(
        String::from("user@example.com"),
        String::from("username"),
    );
    user.greet();
}
```

### 列舉

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

impl Message {
    fn call(&self) {
        match self {
            Message::Write(text) => println!("{}", text),
            Message::Move { x, y } => println!("move to {}, {}", x, y),
            _ => println!("other"),
        }
    }
}

fn main() {
    let m = Message::Write(String::from("hello"));
    m.call();
}
```

## 錯誤處理

```rust
use std::fs::File;
use std::io::Read;

fn read_file() -> Result<String, std::io::Error> {
    let mut f = File::open("hello.txt")?;
    let mut s = String::new();
    f.read_to_string(&mut s)?;
    Ok(s)
}

fn main() {
    match read_file() {
        Ok(contents) => println!("{}", contents),
        Err(e) => eprintln!("Error: {}", e),
    }
}
```

## 併發

###執行緒

```rust
use std::thread;
use std::time::Duration;

fn main() {
    let handle = thread::spawn(|| {
        for i in 0..5 {
            println!("spawned thread: {}", i);
            thread::sleep(Duration::from_millis(1));
        }
    });

    for i in 0..3 {
        println!("main thread: {}", i);
    }

    handle.join().unwrap();
}
```

### 訊息傳遞

```rust
use std::sync::mpsc;

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        tx.send(42).unwrap();
    });

    println!("Received: {}", rx.recv().unwrap());
}
```

## 小結

Rust 語言為系統程式設計帶來了革命性的改變。透過所有權系統和借用檢查器，Rust 在編譯時就杜絕了記憶體錯誤，同時保持零成本抽象和優異的效能。對於需要高效能和安全的系統程式設計，Rust 是極佳的選擇。

---

**延伸閱讀**

- [The Rust Programming Language Book](https://www.google.com/search?q+Rust+programming+language+book)
- [Rust By Example](https://www.google.com/search?q=Rust+by+example)
- [Rust Error Handling](https://www.google.com/search?q=Rust+error+handling+result+option)