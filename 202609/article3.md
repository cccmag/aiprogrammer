# unSAFE Rust 實戰：正確使用 unsafe 的 10 條規則

> **系列文第 3 篇**｜Rust 的 `unsafe` 關鍵字是雙面刃：它賦予開發者底層控制能力，卻也繞過了編譯器的安全保證。本文歸納 10 條實戰規則，幫助你在必要時安全地使用 unsafe。

---

## 為什麼需要 unsafe？

Rust 的所有權與借用系統能在編譯期排除記憶體錯誤，但某些場景——例如呼叫 C 函式庫、操作裸指標、或實作底層資料結構——仍需要繞過編譯器的限制。`unsafe` 賦予你四種能力：解參考裸指標、呼叫 unsafe 函式、存取可變靜態變數、以及實作 unsafe trait。但權力越大，責任越大。

---

## 規則 1：最小化 unsafe 的作用域

將 `unsafe` 區塊縮到最小，避免整函式標記為 `unsafe`。

```rust
// 壞寫法：整個函式 unsafe
unsafe fn bad_example(buf: *mut u8, len: usize) {
    for i in 0..len {
        *buf.add(i) = 0;
    }
}

// 好寫法：只包裝必要的操作
fn good_example(buf: *mut u8, len: usize) {
    for i in 0..len {
        unsafe { *buf.add(i) = 0; }
    }
}
```

每一行 `unsafe` 程式碼都應該被獨立審查。區塊越小，出錯時越容易定位問題。

---

## 規則 2：所有 unsafe 必須有 Safety 文件

任何 `unsafe` 函式或 trait 都必須附上 `# Safety` 文件，說明呼叫者需滿足的前置條件。

```rust
/// 將 src 複製到 dst，兩者不可重疊。
///
/// # Safety
/// - `dst` 必須指向長度至少 `count` 的可寫記憶體。
/// - `src` 必須指向長度至少 `count` 的可讀記憶體。
/// - 兩指標必須有效且對齊。
unsafe fn copy_unchecked(dst: *mut u8, src: *const u8, count: usize) {
    for i in 0..count {
        *dst.add(i) = *src.add(i);
    }
}
```

這份文件是 unsafe 合約的核心：呼叫者負責滿足前置條件，實作者負責其餘部分。

---

## 規則 3：封裝 unsafe 在安全的 API 中

提供安全抽象層，將 unsafe 隱藏在經過驗證的公開介面之下。

```rust
/// 安全的 Ring Buffer 封裝，內部使用 unsafe
pub struct RingBuffer<T> {
    buffer: Vec<MaybeUninit<T>>,
    head: usize,
    tail: usize,
    capacity: usize,
}

impl<T> RingBuffer<T> {
    pub fn push(&mut self, value: T) -> Result<(), T> {
        if self.is_full() {
            return Err(value);
        }
        unsafe {
            let slot = self.buffer.get_unchecked_mut(self.tail);
            slot.as_mut_ptr().write(value);
        }
        self.tail = (self.tail + 1) % self.capacity;
        Ok(())
    }

    pub fn pop(&mut self) -> Option<T> {
        if self.is_empty() {
            return None;
        }
        let value = unsafe {
            let slot = self.buffer.get_unchecked_mut(self.head);
            slot.as_ptr().read()
        };
        self.head = (self.head + 1) % self.capacity;
        Some(value)
    }
}
```

使用者透過安全的 `push` / `pop` 操作，完全不需要接觸 unsafe。

---

## 規則 4：優先使用標準庫的安全替代方案

在引入 unsafe 之前，先確認標準庫是否已提供對應功能。

| 不安全作法 | 安全替代 |
|---|---|
| `slice::get_unchecked(i)` | `slice::get(i)` |
| `mem::transmute::<A, B>(v)` | `From` / `Into` / `TryFrom` |
| `ptr::read` / `ptr::write` | `std::mem::replace` / `take` |
| 手動配置記憶體 | `Vec` / `Box` / `Arc` |

```rust
// 避免：手動指標操作
unsafe { *ptr = new_val; }

// 偏好：安全抽象
*box_val = new_val;      // Box 自動管理
vec.push(new_val);       // Vec 自動擴展
```

標準庫的實作經過無數測試與審查，遠比自己手寫 unsafe 可靠。

---

## 規則 5：驗證指標有效性（非空、對齊、初始化）

操作裸指標前，必須確保它滿足三項條件：

- **非空**：指標不為 `null`
- **對齊**：符合型別的對齊要求
- **初始化**：指向的記憶體已正確初始化

```rust
unsafe fn write_aligned(ptr: *mut u32, val: u32) {
    // 檢查對齊：u32 需要 4-byte 對齊
    debug_assert!(!ptr.is_null(), "ptr must not be null");
    debug_assert!(
        (ptr as usize) % align_of::<u32>() == 0,
        "ptr must be aligned"
    );
    ptr.write(val);
}
```

生產環境建議使用 `debug_assert!`，在開發期捕捉違規而不影響發行版效能。

---

## 規則 6：注意生命週期和所有權

unsafe 程式碼不會自動繼承 Rust 的生命週期保護。指標的有效性取決於你維護的正確性。

```rust
fn dangling_pointer() -> *const i32 {
    let x = 42;
    &x as *const i32  // 危險！x 會在函式結束時釋放
}                     // 回傳的指標是懸空指標

fn valid_pattern() {
    let x = 42;
    let ptr: *const i32 = &x;
    unsafe {
        println!("{}", *ptr); // 安全：x 仍在作用域內
    }
}
```

當 unsafe 區塊與資源的生命週期交錯時，使用註解明確標記誰擁有什麼。

---

## 規則 7：使用工具驗證 unsafe（Miri、Loom、Kani）

Rust 生態系提供多種工具自動偵測 unsafe 的未定義行為。

**Miri** — 解譯執行，檢測 UB：
```bash
cargo +nightly miri test
```
可檢測：越界記憶體存取、未對齊存取、違反別名規則等。

**Loom** — 並發模型檢查：
```rust
// 使用 loom 代替 std 進行執行緒安全驗證
use loom::sync::atomic::AtomicUsize;
use loom::thread;
```

**Kani** — 形式化驗證：
```bash
cargo kani
```
透過符號執行窮舉所有可能的程式路徑，證明 unsafe 程式碼的正確性。

每當你變更 unsafe 區塊，至少先用 Miri 全數通過測試。

---

## 規則 8：測試不安全程式碼的邊界條件

對 unsafe 程式碼的測試必須涵蓋邊界情況：空指標、零長度、最大容量、別名區域。

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_copy_zero_bytes() {
        let src = [1u8, 2, 3];
        let mut dst = [0u8; 3];
        unsafe {
            copy_unchecked(dst.as_mut_ptr(), src.as_ptr(), 0);
        }
        // 零長度複製不應改動任何內容
        assert_eq!(dst, [0, 0, 0]);
    }

    #[test]
    fn test_copy_full_buffer() {
        let src = [1u8, 2, 3];
        let mut dst = [0u8; 3];
        unsafe {
            copy_unchecked(dst.as_mut_ptr(), src.as_ptr(), 3);
        }
        assert_eq!(dst, [1, 2, 3]);
    }

    #[test]
    fn test_copy_overlapping() {
        // 故意測試重疊區域
        let mut buf = [1u8, 2, 3, 4];
        let ptr = buf.as_mut_ptr();
        unsafe {
            // 這可能會 UB，測試應該要捕捉到
            copy_unchecked(ptr.add(1), ptr, 3);
        }
    }
}
```

編寫測試時思考：「哪種輸入會讓這個 unsafe 程式碼出錯？」然後寫下對應測試。

---

## 規則 9：審查 Send/Sync 的實作

手動實作 `Send` 或 `Sync` 等 unsafe trait 時，必須證明型別在跨執行緒使用時是安全的。

```rust
/// 內部可變指標包裝器，非執行緒安全
struct PtrWrapper<T> {
    ptr: *mut T,
}

// 危險的實作：讓 !Send 型別變成 Send
unsafe impl<T: Send> Send for PtrWrapper<T> {}
unsafe impl<T: Sync> Sync for PtrWrapper<T> {}

// 安全實作範例：使用 AtomicPtr
use std::sync::atomic::AtomicPtr;

struct SafeWrapper<T> {
    ptr: AtomicPtr<T>,
}

unsafe impl<T: Send> Send for SafeWrapper<T> {}
unsafe impl<T: Sync> Sync for SafeWrapper<T> {}
```

判斷標準很簡單：這個型別在兩個執行緒間共用（Sync）或轉移（Send）時，會導致資料競爭嗎？確認後再用文件說明理由。

---

## 規則 10：記錄每個 unsafe 的安全假設

每一處 unsafe 都依賴某些外部假設——這些假設必須被白紙黑字記錄下來。

```rust
/// 將給定的 fd 包裝為 File。
/// # Safety
/// - `fd` 必須是有效的、已開啟的檔案描述符。
/// - 呼叫者必須擁有該 fd 的所有權。
/// - 此函式消耗 fd，呼叫者不應再關閉它。
unsafe fn from_raw_fd(fd: i32) -> File {
    File::from_raw_fd(fd)
}
```

建議在專案根目錄維護一份 `UNSAFE.md`，彙整所有 unsafe 的使用位置與安全論證，便於程式碼審查與後續維護。

```markdown
# UNSAFE 使用清單

## src/ring_buffer.rs:42
- 行號：42
- 原因：使用 get_unchecked_mut 跳過邊界檢查
- 假設：tail 總是 < capacity
- 驗證方式：Miri 測試通過

## src/ffi.rs:15
- 行號：15
- 原因：呼叫 C 函式庫 malloc
- 假設：回傳值非 null
- 驗證方式：呼叫後立即檢查 null
```

---

## 結語

unsafe Rust 並非應該避免的禁忌，而是經過深思熟慮後才動用的工具。這 10 條規則的核心精神只有一句話：**用紀律取代編譯器做不到的檢查**。當你遵守這些規則時，unsafe 區塊不僅不會削弱程式的可靠性，反而讓不安全成為經過審計、可驗證的例外——這正是 Rust 最重要的設計哲學。

記住：unsafe 不代表程式碼有 bug，但寫 unsafe 時的你，必須比編譯器更嚴格。

---

*本系列下篇預告：「Rust 非同步程式設計：從 Future 到 async/await 的底層原理」*
