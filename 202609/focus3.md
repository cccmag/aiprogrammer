# unsafe Rust

## 何時與如何使用 unsafe（2015-2026）

### 前言

unsafe 是 Rust 中最被誤解的特性。初學者視它為禁忌，經驗不足的開發者濫用它，而在系統程式設計中，它是不可或缺的工具。

unsafe 的核心信念：**編譯器無法證明所有事情是安全的，但開發者可以（在有限的範圍內）**。

### unsafe 的五種超能力

Rust 的 unsafe 關鍵字啟用五種在安全 Rust 中不允許的操作：

```rust
// 1. 解引用裸指標
let ptr = &x as *const i32;
unsafe { println!("{}", *ptr) };

// 2. 呼叫 unsafe 函式
unsafe fn dangerous() {}
unsafe { dangerous() };

// 3. 存取可變靜態變數
static mut COUNTER: u32 = 0;
unsafe { COUNTER += 1 };

// 4. 實作 unsafe trait
unsafe trait Foo {}
unsafe impl Foo for MyType {}

// 5. 存取 union 欄位
union MyUnion { i: i32, f: f32 }
unsafe { let f = u.f };
```

### unsafe 不是「關閉安全檢查」

這是最常見的誤解。unsafe 並沒有關閉借用檢查器、型別檢查或任何安全機制：

```rust
// 即使在不安全的區塊中，借用檢查器仍然有效！
unsafe {
    let mut v = vec![1, 2, 3];
    let ptr = &v[0] as *const i32;
    v.push(4);  // 編譯錯誤！不可變引用存在時不能可變借用
    println!("{}", *ptr);
}
```

unsafe 只允許**特定**的低階操作，但 Rust 的安全規則仍然適用。

### 安全抽象模式

系統程式設計的核心模式是「內部 unsafe，外部安全」：

```rust
/// 安全的高階 API
pub fn split_at_mut<T>(slice: &mut [T], mid: usize) -> (&mut [T], &mut [T]) {
    let len = slice.len();
    let ptr = slice.as_mut_ptr();
    
    assert!(mid <= len);
    
    // unsafe 被封裝在安全函式中
    unsafe {
        (
            from_raw_parts_mut(ptr, mid),
            from_raw_parts_mut(ptr.add(mid), len - mid),
        )
    }
}
// 呼叫者不需要 unsafe！
```

**標準庫中到處都是這種模式**——Vec、String、HashMap 的核心實作都使用 unsafe，但透過安全 API 暴露。

### 常見的 unsafe 使用場景

**1. 自訂資料結構**：

```rust
pub struct MyVec<T> {
    ptr: *mut T,
    len: usize,
    cap: usize,
}

impl<T> MyVec<T> {
    pub fn push(&mut self, value: T) {
        if self.len == self.cap {
            self.grow();
        }
        unsafe {
            // 寫入未初始化的記憶體
            self.ptr.add(self.len).write(value);
            self.len += 1;
        }
    }
    
    pub fn pop(&mut self) -> Option<T> {
        if self.len == 0 {
            None
        } else {
            self.len -= 1;
            unsafe {
                // 讀取並銷毀
                Some(self.ptr.add(self.len).read())
            }
        }
    }
}
```

**2. FFI 綁定**：

```rust
use std::ffi::CStr;
use std::os::raw::c_char;

extern "C" {
    fn strlen(s: *const c_char) -> usize;
}

fn safe_strlen(s: &str) -> usize {
    let c_str = std::ffi::CString::new(s).unwrap();
    unsafe { strlen(c_str.as_ptr()) }
}
```

**3. 記憶體映射 I/O**：

```rust
const GPIO_BASE: usize = 0x4002_0000;

fn set_led(on: bool) {
    unsafe {
        core::ptr::write_volatile(GPIO_BASE as *mut u32, if on { 1 } else { 0 });
    }
}
```

**4. 高效能最佳化**：

```rust
// 跳過邊界檢查（僅在確定安全時使用）
fn get_unchecked(slice: &[u8], idx: usize) -> u8 {
    unsafe { *slice.get_unchecked(idx) }
}
```

### unsafe 的規則

Rust 的安全文檔（Rustonomicon）列出了 unsafe Rust 必須遵守的規則：

1. **資料競爭**：不可變和可變引用不能同時存在
2. **別名違反**：&mut 引用必須是唯一的
3. **未定義行為**：禁止 UB（緩衝區溢位、use-after-free 等）
4. **生命週期**：指標必須在存取的資料生命週期內有效
5. **對齊**：指標必須正確對齊
6. **初始化**：讀取的記憶體必須已初始化

### 違規的後果

違反 unsafe 規則不一定會立即崩潰——這就是問題所在：

```rust
// 災難範例：use-after-free
fn disaster() {
    let ptr = {
        let v = vec![1, 2, 3];
        let ptr = v.as_ptr();
        // v 在這裡被釋放！
        ptr
    };
    // ptr 是懸空指標！
    unsafe { println!("{}", *ptr) };  // 未定義行為！
}
```

### unsafe 的審查清單

在使用 unsafe 前，檢查以下幾點：

- [ ] 指標是否有效（非空、已對齊、指向已初始化的有效記憶體）？
- [ ] 指標是否在存取的資料生命週期內有效？
- [ ] 是否違反了借用規則？
- [ ] 是否有可能導致資料競爭？
- [ ] 是否有安全的替代方案？

### Rust 2026 的 unsafe 改進

Rust 2026 Edition 引入了多項 unsafe 的改進：

**1. unsafe 區塊的追蹤**：

```rust
// 2026：unsafe 可以指定需要驗證的假設
unsafe {
    // 保證：ptr 有效且已對齊
    // 保證：idx < len
    *ptr.add(idx)
}
```

**2. unsafe 區塊的巢狀控制**：

```rust
let ptr = ...;
// 只在最內層使用 unsafe
let val = unsafe {
    let raw = unsafe { ptr.as_ref() }.unwrap();
    raw.value
};
```

### 小結

unsafe Rust 是系統程式設計的核心技能。它不是一個需要害怕的功能，而是一個需要**理解和尊重**的工具。

**unsafe 哲學總結**：
- 安全 Rust 是預設——只有在必要時才使用 unsafe
- 最小化 unsafe 的作用域——越小越好
- 封裝 unsafe——提供安全的 API 介面
- 文件化假設——清楚地記錄 unsafe 程式碼的前置條件
- 測試 unsafe——用測試驗證安全抽象的正確性

---

**下一步**：[FFI 與 C 互動](focus4.md)

## 延伸閱讀

- [Rustonomicon: The Unsafe Book](https://www.google.com/search?q=Rustonomicon+unsafe+book)
- [Unsafe Rust Guidelines](https://www.google.com/search?q=unsafe+Rust+guidelines)
- [Rust 安全抽象模式](https://www.google.com/search?q=Rust+safe+abstraction+unsafe)
