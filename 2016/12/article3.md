# Rust 在系統程式設計的應用

## 前言

Rust 語言以其獨特的所有權系統和記憶體安全特性，正在成為系統程式設計的新選擇。本文探討 Rust 在各類系統程式設計場景中的應用。

## Rust 的核心優勢

```rust
// Rust 的記憶體安全
fn main() {
    // 編譯器在編譯時就防止記憶體錯誤
    let s1 = String::from("hello");
    let s2 = s1; // s1 被移動，這裡不再是有效的
    // println!("{}", s1); // 編譯錯誤！
    println!("{}", s2);

    // 借用檢查
    let mut s = String::from("hello");
    let r1 = &s;  // 不可變借用
    let r2 = &s;  // 可以有多個不可變借用
    println!("{} {}", r1, r2);
    // r1 和 r2 在這裡之後不再使用

    let r3 = &mut s; // 可變借用
    r3.push_str(", world");
    println!("{}", r3);
}
```

## 命令列工具

```rust
use clap::{Arg, App};

fn main() {
    let matches = App::new("My App")
        .version("1.0")
        .author("Author")
        .about("A simple CLI tool")
        .arg(Arg::with_name("input")
            .short("i")
            .long("input")
            .value_name("FILE")
            .help("Input file")
            .takes_value(true))
        .arg(Arg::with_name("verbose")
            .short("v")
            .long("verbose")
            .help("Enable verbose output"))
        .get_matches();

    if let Some(input) = matches.value_of("input") {
        println!("Input file: {}", input);
    }
}
```

## 網路程式設計

### 非同步 HTTP 客戶端

```rust
use reqwest;
use tokio;

#[tokio::main]
async fn main() -> Result<(), reqwest::Error> {
    let response = reqwest::get("https://api.example.com/data")
        .await?;

    println!("Status: {}", response.status());
    println!("Headers: {:?}", response.headers());

    let body = response.text().await?;
    println!("Body: {}", body);

    Ok(())
}
```

### TCP 伺服器

```rust
use std::net::{TcpListener, TcpStream};
use std::io::{Read, Write};

fn handle_client(mut stream: TcpStream) {
    let mut buffer = [0; 1024];
    stream.read(&mut buffer).unwrap();

    let response = b"HTTP/1.1 200 OK\r\n\r\nHello, World!";
    stream.write(response).unwrap();
}

fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:8080")?;
    println!("Server listening on port 8080");

    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                std::thread::spawn(|| {
                    handle_client(stream);
                });
            }
            Err(e) => eprintln!("Connection failed: {}", e),
        }
    }

    Ok(())
}
```

## 檔案處理

```rust
use std::fs::File;
use std::io::{self, BufRead, BufReader, Write};

fn read_file(path: &str) -> io::Result<Vec<String>> {
    let file = File::open(path)?;
    let reader = BufReader::new(file);
    Ok(reader.lines().filter_map(|l| l.ok()).collect())
}

fn write_file(path: &str, content: &[String]) -> io::Result<()> {
    let mut file = File::create(path)?;
    for line in content {
        writeln!(file, "{}", line)?;
    }
    Ok(())
}

fn main() {
    let lines = vec![
        String::from("Line 1"),
        String::from("Line 2"),
        String::from("Line 3"),
    ];

    write_file("output.txt", &lines).unwrap();
    let read_lines = read_file("output.txt").unwrap();
    println!("Read {} lines", read_lines.len());
}
```

## 並發程式設計

### Thread

```rust
use std::thread;
use std::sync::Arc;
use std::time::Duration;

fn main() {
    let data = vec![1, 2, 3, 4, 5];
    let data = Arc::new(data);

    let handles: Vec<_> = (0..3).map(|i| {
        let data = Arc::clone(&data);
        thread::spawn(move || {
            println!("Thread {} sees: {:?}", i, data);
        })
    }).collect();

    for handle in handles {
        handle.join().unwrap();
    }
}
```

### Mutex

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();
            *num += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Result: {}", *counter.lock().unwrap());
}
```

## 嵌入式系統

```rust
#![no_std]
#![no_main]

use panic_halt as _;

#[no_mangle]
pub extern "C" fn main() -> ! {
    // 嵌入式程式碼
    loop {
        // 等待中斷
    }
}
```

### 嵌入式框架

```rust
// 使用 embedded-hal
use embedded_hal::digital::v2::OutputPin;

fn toggle_led<G: OutputPin>(led: &mut G) {
    led.set_high().ok();
    // 延遲
    led.set_low().ok();
}
```

## 效能優化

### SIMD

```rust
#[cfg(target_arch = "x86_64")]
use std::arch::x86_64::*;

unsafe fn simd_sum(values: &[f32]) -> f32 {
    let mut sum = _mm256_setzero_ps();
    let chunks = values.chunks(8);

    for chunk in chunks {
        let mut arr = [0f32; 8];
        arr[..chunk.len()].copy_from_slice(chunk);
        let loaded = _mm256_loadu_ps(arr.as_ptr());
        sum = _mm256_add_ps(sum, loaded);
    }

    let mut result = [0f32; 8];
    _mm256_storeu_ps(result.as_mut_ptr(), sum);
    result.iter().sum()
}
```

### Benchmark

```rust
use criterion::{black_box, criterion_group, Criterion};

fn fibonacci(n: u64) -> u64 {
    match n {
        0 => 0,
        1 => 1,
        _ => fibonacci(n - 1) + fibonacci(n - 2),
    }
}

fn bench_fib(c: &mut Criterion) {
    c.bench_function("fibonacci_20", |b| {
        b.iter(|| fibonacci(black_box(20)));
    });
}

criterion_group!(benches, bench_fib);
```

## WebAssembly

```rust
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

#[wasm_bindgen]
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

```javascript
// JavaScript 调用
const result = Module.add(1, 2);
console.log(result);
```

## 小結

Rust 的記憶體安全保證、零成本抽象和優異的效能使其成為系統程式設計的理想選擇。從命令列工具到嵌入式系統，從網路程式設計到 WebAssembly，Rust 正在各個領域展現其價值。

---

**延伸閱讀**

- [The Rust Programming Language Book](https://www.google.com/search?q=Rust+programming+language+book)
- [Rust Embedded Book](https://www.google.com/search?q=Rust+embedded+systems+book)
- [Rust WebAssembly](https://www.google.com/search?q=Rust+webassembly+tutorial)