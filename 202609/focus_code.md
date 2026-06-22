# mini-rt：自訂記憶體配置器、FFI 與低階抽象

## 概述

mini-rt 是一個展示 Rust 系統程式設計核心概念的小型專案。它實作了三個典型的系統程式設計模式：

1. **自訂全域配置器（Bump Allocator）**——透過 `GlobalAlloc` trait 實作
2. **安全的 FFI 封裝**——將 libc 函式包裝在安全的 Rust API 中
3. **低階記憶體操作**——MMIO 暫存器、Ring Buffer、裸指標管理

## 核心概念

### 1. Bump 配置器

Bump（Arena）配置器是最簡單的記憶體配置器：

```rust
pub struct BumpAllocator {
    offset: AtomicUsize,
}

unsafe impl GlobalAlloc for BumpAllocator {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        // 1. 計算對齊後的偏移量
        // 2. 檢查是否有足夠空間
        // 3. 移動偏移量並返回指標
    }
    unsafe fn dealloc(&self, _ptr: *mut u8, _layout: Layout) {
        // Bump allocator 的 dealloc 是空操作
        // 記憶體在 reset() 時一次釋放
    }
}
```

**關鍵點**：
- `GlobalAlloc` 是 unsafe trait——實作者必須保證正確性
- `dealloc` 是空操作——這限制了使用場景（僅適用於短期分配）
- 使用 `AtomicUsize` 實現基本的執行緒安全
- `#[global_allocator]` 靜態設定全域配置器

### 2. 安全 FFI 封裝模式

```rust
// 底層：unsafe FFI 宣告（在 sys 模組中隔離）
mod sys {
    extern "C" {
        pub fn getpid() -> i32;
        pub fn gethostname(name: *mut c_char, len: size_t) -> i32;
    }
}

// 上層：安全 Rust API
pub fn get_process_id() -> u32 {
    unsafe { libc::getpid() as u32 }
}

pub fn get_hostname() -> Result<String, std::io::Error> {
    let mut buf = vec![0u8; 256];
    let result = unsafe {
        libc::gethostname(buf.as_mut_ptr() as *mut c_char, buf.len())
    };
    // 錯誤處理 + 字串轉換
}
```

**關鍵模式**：
1. 所有 unsafe 集中在 FFI 邊界
2. 安全 API 處理錯誤、記憶體管理和型別轉換
3. `Result` 型別將 C 的錯誤碼轉換為 Rust 的錯誤處理

### 3. MMIO 暫存器抽象

```rust
#[derive(Clone, Copy)]
pub struct MappedRegister<T> {
    address: usize,
    _phantom: PhantomData<T>,
}

impl<T: Copy> MappedRegister<T> {
    pub unsafe fn new(address: usize) -> Self { ... }
    pub fn read(&self) -> T {
        unsafe { read_volatile(self.address as *const T) }
    }
    pub fn write(&self, value: T) {
        unsafe { write_volatile(self.address as *mut T, value) }
    }
}
```

### 4. Ring Buffer（環形緩衝區）

```rust
pub struct RingBuffer<T: Copy + Default> {
    buffer: *mut T,
    capacity: usize,
    head: usize,
    tail: usize,
    full: bool,
}
```

## unsafe 的使用邊界

mini-rt 中的 unsafe 使用遵循「最小化作用域」原則：

| 元件 | unsafe 位置 | 安全保證 |
|------|-----------|---------|
| BumpAllocator | `alloc` 的指標運算 | 邊界檢查 + 對齊保證 |
| FFI 封裝 | FFI 函式呼叫 | 輸入驗證 + 錯誤檢查 |
| MappedRegister | `read_volatile`/`write_volatile` | 由呼叫者保證位址有效 |
| RingBuffer | `alloc` 和指標運算 | Layout 驗證 + 邊界檢查 |

## 測試結果

```
running 6 tests
test tests::test_bump_allocator ... ok
test tests::test_ring_buffer ... ok
test tests::test_ring_buffer_overwrite ... ok
test tests::test_hostname ... ok
test tests::test_mmio ... ok
test tests::test_pid ... ok
test result: ok. 6 passed; 0 failed
```

## 執行結果

```
=== mini-rt: Systems Programming Demo ===

PID: 52141
Hostname: cccimacdeiMac.local

--- Ring Buffer Demo ---
Buffer len: 3
Pop: 10
Pop: 20

--- MMIO Register Demo ---
Register read: 42
After write: 100

--- Bump Allocator Demo ---
Vec from bump allocator: [1, 2, 3]
Allocated: 2036 bytes
```

## mini-rt 教會我們的事

### 1. unsafe 不是關閉安全檢查

即使在 unsafe 區塊中，Rust 的借用檢查器仍然有效。unsafe 只允許特定的低階操作，但不解除安全保證。

### 2. 安全的 FFI 需要三層架構

```
C 函式 → unsafe FFI 宣告 → 安全封裝 → Rust API
```

### 3. 系統程式設計的核心是抽象

裸指標 → 安全封裝 → 高階 API——每一層都在提供更高的安全保證。

### 4. 測試是系統程式碼的生命線

系統程式設計中的錯誤可能導致崩潰或安全漏洞——測試是確保正確性的最後防線。

---

## 延伸閱讀

- [完整程式碼](_code/src/main.rs)
- [Rust GlobalAlloc trait](https://www.google.com/search?q=Rust+GlobalAlloc+trait)
- [Rustonomicon: FFI](https://www.google.com/search?q=Rustonomicon+FFI)
- [Rust 中的 volatile 存取](https://www.google.com/search?q=Rust+volatile+memory+access)
