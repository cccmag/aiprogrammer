# FFI 與 C 互動

## bindgen、cbindgen、ABI 相容性（2016-2026）

### 前言

FFI（Foreign Function Interface）是 Rust 系統程式設計的核心能力之一。現實世界中，大量的基礎設施程式碼是 C 寫的——作業系統 API、硬體驅動程式、嵌入式庫。Rust 需要與這些 C 程式碼無縫互動。

### extern "C"：ABI 橋樑

Rust 透過 `extern "C"` 區塊來宣告外部 C 函式：

```rust
// 宣告 C 標準庫函式
extern "C" {
    fn malloc(size: usize) -> *mut std::ffi::c_void;
    fn free(ptr: *mut std::ffi::c_void);
    fn strlen(s: *const std::ffi::c_char) -> usize;
}

// 使用
fn safe_malloc(size: usize) -> *mut std::ffi::c_void {
    unsafe { malloc(size) }
}
```

**關鍵點**：
- `extern "C"` 指定使用 C 的 ABI（呼叫慣例）
- 呼叫外部函式必須在 unsafe 區塊中
- Rust 不能保證 C 程式碼的安全性

### 型別對應

Rust 與 C 的型別對應：

| C 型別 | Rust 型別 |
|--------|----------|
| `char` | `i8` / `c_char` |
| `short` | `i16` / `c_short` |
| `int` | `i32` / `c_int` |
| `long long` | `i64` / `c_longlong` |
| `float` | `f32` / `c_float` |
| `double` | `f64` / `c_double` |
| `void*` | `*mut c_void` |
| `size_t` | `usize` |

### bindgen：自動生成 FFI 綁定

手動編寫 FFI 綁定繁瑣且容易出錯。`bindgen` 可以自動從 C 頭文件生成 Rust 綁定：

```bash
# 從 C 頭文件生成 Rust 綁定
bindgen input.h -o bindings.rs
```

**輸入（input.h）**：
```c
typedef struct {
    int x;
    int y;
} Point;

double distance(Point a, Point b);
int clamp(int value, int min, int max);
```

**輸出（bindings.rs）**：
```rust
#[repr(C)]
pub struct Point {
    pub x: ::std::os::raw::c_int,
    pub y: ::std::os::raw::c_int,
}

extern "C" {
    pub fn distance(a: Point, b: Point) -> f64;
    pub fn clamp(value: ::std::os::raw::c_int, min: ::std::os::raw::c_int, max: ::std::os::raw::c_int) -> ::std::os::raw::c_int;
}
```

### 安全的 FFI 封裝

自動生成的綁定是 unsafe 的。最佳實踐是將它們封裝在安全的 Rust API 中：

```rust
// 自動生成的綁定（放在 sys/ 模組中）
mod sys {
    include!("bindings.rs");
}

// 安全封裝
#[derive(Clone, Copy)]
pub struct Point {
    pub x: i32,
    pub y: i32,
}

pub fn distance(a: Point, b: Point) -> f64 {
    unsafe { sys::distance(
        sys::Point { x: a.x, y: a.y },
        sys::Point { x: b.x, y: b.y },
    )}
}

pub fn clamp(value: i32, min: i32, max: i32) -> i32 {
    unsafe { sys::clamp(value, min, max) }
}
```

### cbindgen：從 Rust 生成 C 頭文件

`cbindgen` 是 bindgen 的逆向操作——從 Rust 程式碼生成 C 頭文件：

```rust
// Rust 程式碼
#[no_mangle]
pub extern "C" fn rust_add(a: i32, b: i32) -> i32 {
    a + b
}

#[no_mangle]
pub extern "C" fn rust_greet(name: *const c_char) -> *mut c_char {
    let name = unsafe { CStr::from_ptr(name) }.to_str().unwrap();
    let greeting = format!("Hello, {}!", name);
    CString::new(greeting).unwrap().into_raw()
}
```

```bash
# 生成 C 頭文件
cbindgen --lang c --output mylib.h
```

```c
// 生成的 C 頭文件
int32_t rust_add(int32_t a, int32_t b);
char* rust_greet(const char* name);
```

### ABI 相容性

FFI 最棘手的問題是 ABI（Application Binary Interface）相容性。

**repr(C)**：

```rust
// 預設：Rust 可以重新排列欄位（最佳化）
struct PointRust {
    x: f64,
    y: f64,
}

// repr(C)：遵循 C 的佈局規則
#[repr(C)]
struct PointC {
    x: f64,
    y: f64,
}
```

**複雜型別的傳遞**：

```rust
// 透過指標傳遞結構體（避免 ABI 問題）
extern "C" {
    fn process_point(p: *const Point) -> f64;
}

fn safe_process_point(p: &Point) -> f64 {
    unsafe { process_point(p as *const Point) }
}
```

### 回呼函式

從 C 呼叫 Rust 函式（回呼）：

```rust
// Rust 端：定義可以被 C 呼叫的函式
extern "C" fn callback(data: *mut c_void, value: i32) {
    let data = unsafe { &mut *(data as *mut MyData) };
    data.on_event(value);
}

// 註冊回呼
extern "C" {
    fn register_callback(
        cb: extern "C" fn(*mut c_void, i32),
        data: *mut c_void,
    );
}

// 安全封裝
pub fn set_callback<F: FnMut(i32)>(f: F) {
    let data = Box::into_raw(Box::new(MyData { callback: Box::new(f) }));
    unsafe {
        register_callback(Some(callback), data as *mut c_void);
    }
}
```

### 錯誤處理

C 語言沒有 Result 型別，錯誤通常透過回傳值或 errno 來表示：

```rust
// C 風格的錯誤處理
extern "C" {
    fn c_function(arg: i32) -> i32;  // 回傳 0 表示成功
}

#[derive(Debug)]
enum MyError {
    InvalidArg,
    Unknown(i32),
}

fn safe_c_function(arg: i32) -> Result<(), MyError> {
    let result = unsafe { c_function(arg) };
    match result {
        0 => Ok(()),
        -1 => Err(MyError::InvalidArg),
        n => Err(MyError::Unknown(n)),
    }
}
```

### 所有權的傳遞

FFI 中所有權的處理是最困難的部分：

```rust
// Rust 分配，C 使用，Rust 釋放
fn create_buffer(size: usize) -> *mut u8 {
    let mut buf = vec![0u8; size];
    let ptr = buf.as_mut_ptr();
    std::mem::forget(buf);  // 防止 Rust 釋放！
    ptr
}

fn free_buffer(ptr: *mut u8, size: usize) {
    unsafe {
        // 重新取得所有權並釋放
        let _ = Vec::from_raw_parts(ptr, size, size);
    }
}
```

### 實戰：libcurl 綁定

```rust
use std::ffi::{CStr, CString};

mod ffi {
    include!("bindings/curl.rs");
}

pub struct Easy {
    handle: *mut ffi::CURL,
}

impl Easy {
    pub fn new() -> Result<Self, String> {
        let handle = unsafe { ffi::curl_easy_init() };
        if handle.is_null() {
            Err("Failed to initialize curl".into())
        } else {
            Ok(Easy { handle })
        }
    }
    
    pub fn set_url(&mut self, url: &str) -> Result<(), String> {
        let c_url = CString::new(url).map_err(|_| "Invalid URL")?;
        let result = unsafe {
            ffi::curl_easy_setopt(
                self.handle,
                ffi::CURLOPT_URL,
                c_url.as_ptr(),
            )
        };
        if result == 0 { Ok(()) } else { Err("Failed to set URL".into()) }
    }
}

impl Drop for Easy {
    fn drop(&mut self) {
        unsafe { ffi::curl_easy_cleanup(self.handle) };
    }
}
```

### 小結

FFI 是 Rust 系統程式設計的橋樑——讓 Rust 可以使用廣大的 C 生態系統：

- **bindgen**：從 C 自動生成 Rust 綁定
- **cbindgen**：從 Rust 生成 C 頭文件
- **repr(C)**：確保記憶體佈局相容
- **安全封裝**：將 unsafe 的 FFI 包裝在安全 API 中

關鍵原則：**將 unsafe 集中於 FFI 邊界，在其上建立安全的 Rust API**。

---

**下一步**：[即時作業系統](focus5.md)

## 延伸閱讀

- [Rust FFI Guide](https://www.google.com/search?q=Rust+FFI+guide)
- [bindgen 官方文件](https://www.google.com/search?q=bindgen+Rust)
- [cbindgen 官方文件](https://www.google.com/search?q=cbindgen+Rust)
