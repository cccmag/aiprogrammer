# Rust 與 C 的互相操作實戰

## 前言

C 語言仍是系統程式的 lingua franca——作業系統 API、嵌入式韌體、數字運算函式庫多以 C 撰寫。Rust 若無法與 C 順暢互通，就難以在真實世界落地。本文從實戰角度探討 Rust ↔ C 互相操作的七個核心領域。

## extern "C" 與 ABI 相容性

Rust 透過 `extern "C"` 使用 C ABI 呼叫外部函式：

```rust
use std::ffi::{c_char, c_int, c_void};

extern "C" {
    fn malloc(size: usize) -> *mut c_void;
    fn free(ptr: *mut c_void);
    fn puts(s: *const c_char) -> c_int;
}
```

所有 FFI 呼叫必須在 `unsafe` 區塊中——Rust 無法驗證 C 程式碼的安全性：

```rust
fn safe_puts(s: &str) -> i32 {
    let c_str = std::ffi::CString::new(s).unwrap();
    unsafe { puts(c_str.as_ptr()) }
}
```

跨 FFI 邊界的結構體必須使用 `#[repr(C)]`，確保 Rust 編譯器不重新排列欄位：

```rust
#[repr(C)]
struct Point {
    x: f64,
    y: f64,
}
```

型別對應方面，`int` → `c_int`（i32）、`double` → `c_double`（f64）、`void*` → `*mut c_void`、`size_t` → `usize`。

## 使用 bindgen 自動生成 FFI 綁定

手動撰寫 FFI 綁定容易出錯。`bindgen` 從 C 頭文件自動產生 Rust 程式碼：

```c
// libimage.h
typedef struct {
    unsigned char *data;
    int width, height, channels;
} Image;

Image *image_load(const char *path);
void image_free(Image *img);
```

```bash
bindgen libimage.h -o src/bindings.rs
```

輸出綁定節錄：

```rust
#[repr(C)]
pub struct Image {
    pub data: *mut u8,
    pub width: ::std::os::raw::c_int,
    pub height: ::std::os::raw::c_int,
    pub channels: ::std::os::raw::c_int,
}

extern "C" {
    pub fn image_load(path: *const ::std::os::raw::c_char) -> *mut Image;
    pub fn image_free(img: *mut Image);
}
```

搭配 `build.rs` 可在每次建置時自動重新生成綁定：

```rust
fn main() {
    println!("cargo:rustc-link-lib=image");
    let bindings = bindgen::Builder::default()
        .header("wrapper.h")
        .generate().expect("bindgen failed");
    bindings.write_to_file("src/bindings.rs").unwrap();
}
```

## 使用 cbindgen 從 Rust 生成 C 頭文件

當 Rust 程式碼需要被 C 呼叫時，`cbindgen` 自動生成對應 `.h` 檔：

```rust
#[no_mangle]
pub extern "C" fn greet(name: *const c_char) -> *mut c_char {
    let name = unsafe { CStr::from_ptr(name) }
        .to_str().unwrap_or("world");
    let greeting = format!("Hello, {}!", name);
    CString::new(greeting).unwrap().into_raw()
}

#[no_mangle]
pub extern "C" fn free_string(s: *mut c_char) {
    if !s.is_null() {
        unsafe { let _ = CString::from_raw(s); }
    }
}
```

```bash
cbindgen --lang c --output rust_greet.h
```

產生的 `rust_greet.h`：

```c
char *greet(const char *name);
void free_string(char *s);
```

關鍵元素：`#[no_mangle]` 防止符號名稱被改編，`extern "C"` 指定 C ABI。

## 從 C 呼叫 Rust（回呼函式）

C 函式庫常透過函式指標註冊回呼。Rust 可透過 trampoline 函式將閉包傳遞給 C：

```rust
type Callback = unsafe extern "C" fn(*mut c_void, i32);

extern "C" {
    fn register_timer_cb(cb: Callback, user_data: *mut c_void);
}

unsafe extern "C" fn trampoline<F: FnMut(i32)>(
    data: *mut c_void, value: i32,
) {
    let cb: &mut F = &mut *(data as *mut F);
    cb(value);
}

pub fn set_timer_callback<F: FnMut(i32) + 'static>(f: F) {
    let boxed = Box::into_raw(Box::new(f));
    unsafe { register_timer_cb(trampoline::<F>, boxed as *mut c_void) };
}
```

`Box::into_raw` 將所有權移交給 C，防止 Rust 提早釋放。C 端必須保證在適當時機呼叫回呼，否則會造成記憶體洩漏。

## 從 Rust 呼叫 C（動態載入）

靜態連結需要編譯期決定函式庫。`libloading` crate 提供執行期動態載入：

```toml
[dependencies]
libloading = "0.8"
```

```rust
use libloading::{Library, Symbol};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let lib = unsafe { Library::new("libcurl.dylib")? };
    let curl_version: Symbol<unsafe extern "C" fn() -> *const i8> =
        unsafe { lib.get(b"curl_version")? };
    let version = unsafe {
        std::ffi::CStr::from_ptr(curl_version()).to_str()?
    };
    println!("libcurl version: {}", version);
    Ok(())
}
```

適用場景：外掛系統、條件依賴、減少靜態連結體積。

## 所有權的跨語言傳遞

跨 FFI 邊界傳遞所有權是最大考驗。**分配與釋放必須在同一端**。

### Rust 分配，C 使用，Rust 釋放

```rust
use std::mem;

pub fn create_buffer(size: usize) -> *mut u8 {
    let mut buf = vec![0u8; size];
    let ptr = buf.as_mut_ptr();
    mem::forget(buf); // 阻止 Rust 自動釋放
    ptr
}

pub fn destroy_buffer(ptr: *mut u8, size: usize) {
    if !ptr.is_null() {
        unsafe { let _ = Vec::from_raw_parts(ptr, size, size); }
    }
}
```

### Box 與 raw pointer 轉換

```rust
#[repr(C)]
pub struct Config {
    pub timeout_ms: u32,
    pub retry_count: u32,
}

pub fn config_new(timeout: u32, retry: u32) -> *mut Config {
    Box::into_raw(Box::new(Config { timeout_ms: timeout, retry_count: retry }))
}

pub fn config_free(ptr: *mut Config) {
    if !ptr.is_null() {
        unsafe { drop(Box::from_raw(ptr)) };
    }
}
```

`config_free` 若不呼叫即造成記憶體洩漏——FFI 所有權管理最需警惕之處。

## 實戰案例：在 Rust 中整合 C 函式庫

以整合 `libzstd`（Zstandard 壓縮）為例，展示完整 FFI 流程。

### build.rs

```rust
fn main() {
    println!("cargo:rustc-link-lib=zstd");

    let bindings = bindgen::Builder::default()
        .header("wrapper.h")
        .allowlist_function("ZSTD_compress")
        .allowlist_function("ZSTD_decompress")
        .generate().expect("bindgen failed");

    bindings.write_to_file("src/bindings.rs").unwrap();
}
```

### 安全封裝

```rust
mod bindings { include!("bindings.rs"); }

pub fn compress(input: &[u8], level: i32) -> Vec<u8> {
    let bound = unsafe { bindings::ZSTD_compressBound(input.len()) };
    let mut dst = vec![0u8; bound];
    let size = unsafe {
        bindings::ZSTD_compress(
            dst.as_mut_ptr() as *mut c_void,
            dst.len(), input.as_ptr() as *const c_void,
            input.len(), level,
        )
    };
    if unsafe { bindings::ZSTD_isError(size) != 0 } {
        panic!("Compression failed");
    }
    dst.truncate(size);
    dst
}

pub fn decompress(compressed: &[u8]) -> Vec<u8> {
    let size = unsafe {
        bindings::ZSTD_getFrameContentSize(
            compressed.as_ptr() as *const c_void, compressed.len(),
        )
    };
    let mut dst = vec![0u8; size];
    let written = unsafe {
        bindings::ZSTD_decompress(
            dst.as_mut_ptr() as *mut c_void, dst.len(),
            compressed.as_ptr() as *const c_void, compressed.len(),
        )
    };
    dst.truncate(written);
    dst
}
```

### 測試

```rust
#[test]
fn roundtrip() {
    let original = b"Hello, Rust FFI with zstd!";
    let compressed = compress(original, 3);
    let decompressed = decompress(&compressed);
    assert_eq!(original.to_vec(), decompressed);
}
```

`allowlist_function` 精確控制只生成需要的綁定，避免 namespace 污染。安全封裝層將 unsafe 隔離在內部，對外提供純粹的 Rust API。

## 結語

Rust 與 C 的互操作是系統程式設計無可迴避的課題。掌握 `extern "C"`、`bindgen`、`cbindgen`、動態載入、回呼機制及跨語言所有權管理，就能運用廣大 C 生態系統，同時享受 Rust 的記憶體安全。核心原則：**將 unsafe 集中在 FFI 邊界層，在其上建立安全的 Rust API**。

## 延伸閱讀

- [Rust FFI Omnibus](https://www.google.com/search?q=Rust+FFI+Omnibus+examples)
- [bindgen 使用者指南](https://www.google.com/search?q=bindgen+user+guide+Rust)
- [cbindgen 文件](https://www.google.com/search?q=cbindgen+documentation)
- [libloading crate](https://www.google.com/search?q=libloading+Rust+crate)
- [The Rustonomicon - FFI](https://www.google.com/search?q=Rustonomicon+Foreign+Function+Interface)
