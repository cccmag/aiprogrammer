# 用 Miri 與 Kani 驗證 Rust 系統程式碼

## 為什麼系統程式碼需要驗證

Rust 的所有權系統與借用檢查器已在編譯期杜絕了整類記憶體錯誤，然而一旦深入系統程式設計——自訂配置器、裸機驅動、內聯組合語言、`unsafe` 區塊——編譯器就無法再保證安全性。

系統程式碼常直接操作原始指標、呼叫 C ABI、或繞過標準配置器。這些行為在 Rust 的安全超集合中屬於 `unsafe`，但 `unsafe` 不表示「錯誤」，而是「編譯器不檢查，我手動擔保」。手動擔保可能出錯，而錯誤的後果是未定義行為（UB）：程式可能崩潰、資料損毀、或產生安全漏洞。

靜態驗證的工具鏈因此至關重要。Rust 生態中有兩套互補的工具尤為突出：**Miri** 與 **Kani**。

## Miri：Rust 的借用檢查器模擬器

Miri（Mid-level Intermediate Representation Interpreter）是一個 Rust 虛擬機，它在 LLVM 層級之上逐步解釋執行 Rust 中間表示（MIR），並在執行過程中動態追蹤記憶體狀態與借用規則。

Miri 的核心能力是**檢測未定義行為**，包括：

- 超出邊界的記憶體訪問
- 違反別名規則（違背 `noalias` 合約）
- 未初始化記憶體的讀取
- 不合法的指標算術
- 違反 `UnsafeCell` 的使用規則

安裝與使用非常簡單：

```bash
rustup +nightly component add miri
cargo +nightly miri test
```

在 `unsafe` 程式碼的測試上加上 `#[test]`，然後用 Miri 執行，就能在測試期間捕捉到任何 UB。

```rust
use std::mem;

#[test]
fn test_raw_vec() {
    let mut v = Vec::with_capacity(4);
    let ptr = v.as_mut_ptr();
    // 錯誤：未初始化記憶體就被讀取
    unsafe {
        let val = ptr.read(); // Miri 會在此處報告 UB
        v.set_len(1);
    }
}
```

Miri 會指出哪一行違反了哪條規則，並附上完整的借用棧回溯。

## 使用 Miri 發現未定義行為（UB）

考慮一個常見的陷阱——從已經移動的 `Box` 中讀取指標：

```rust
fn dangling_pointer() -> *const i32 {
    let b = Box::new(42);
    let p = &*b as *const i32;
    drop(b); // 釋放記憶體
    p       // 懸空指標
}

#[test]
fn test_dangling() {
    let p = dangling_pointer();
    unsafe {
        println!("{}", *p); // Miri：懸空指標使用！
    }
}
```

執行 `cargo +nightly miri test` 後 Miri 會輸出類似：

```
error: Undefined Behavior: pointer to alloc1 was freed
```

這類錯誤在一般測試中未必會觸發（記憶體可能未被覆寫），但 Miri 總是能發現。

Miri 的另一強項是檢測**不正確的 `UnsafeCell` 使用**。在多執行緒或自訂同步原語中，若違反了 Rust 的別名模型，Miri 會立即告警。

## Kani：Rust 的形式化驗證工具

如果 Miri 是**動態分析**，Kani 就是**靜態形式化驗證**。Kani 由 Amazon Web Services 開發，基於模型檢測（model checking）技術，將 Rust 程式碼翻譯成 SAT/SMT 約束，然後窮舉所有可能的輸入來證明或反駁指定的性質。

```bash
cargo kani
```

Kani 的核心概念是 **proof harness**——類似測試函數，但接受任意輸入：

```rust
use kani::cover;

#[kani::proof]
fn verify_vec_reserve() {
    let cap: usize = kani::any();
    kani::assume(cap < 1024);
    let mut v = Vec::with_capacity(cap);
    v.push(1);
    v.push(2);
    // Kani 會驗證容量在 push 後至少為 2
    assert!(v.capacity() >= 2);
}
```

不同於傳統測試，Kani 不只測一組數據，而是用符號執行探索所有滿足前提的輸入路徑。

## 使用 Kani 證明正確性

Kani 適合證明**函數式正確性**——不僅是「不崩潰」，而是「行為符合規格」。

```rust
fn bounded_add(a: u8, b: u8) -> Option<u8> {
    a.checked_add(b)
}

#[kani::proof]
#[kani::unwind(3)]
fn check_bounded_add() {
    let a: u8 = kani::any();
    let b: u8 = kani::any();
    if let Some(sum) = bounded_add(a, b) {
        assert!(sum as u16 == a as u16 + b as u16);
        assert!(sum >= a && sum >= b);
    }
}
```

Kani 的 `kani::any()` 會產生符號值，而 `kani::assume()` 加上前提。上例中 Kani 會走遍所有 65536 種輸入組合——不靠枚舉，而是靠 SMT 求解器一次性驗證。

對於包含迴圈的程式，需要 `#[kani::unwind(N)]` 指定展開深度，或使用 `kani::forge_loop` 驗證帶有迴圈不變量的程式。

```rust
fn find_index(slice: &[i32], target: i32) -> Option<usize> {
    for (i, &v) in slice.iter().enumerate() {
        if v == target {
            return Some(i);
        }
    }
    None
}

#[kani::proof]
fn check_find_index() {
    const N: usize = 4;
    let arr: [i32; N] = kani::any();
    let target: i32 = kani::any();
    let result = find_index(&arr, target);
    if let Some(idx) = result {
        assert!(idx < N);
        assert_eq!(arr[idx], target);
    }
}
```

## Miri 與 Kani 的互補性

Miri 與 Kani 的定位並不重疊，而是互補：

| 面向 | Miri | Kani |
|------|------|------|
| 分析類型 | 動態（實際執行） | 靜態（模型檢測） |
| 輸入範圍 | 測試提供的數據 | 全部可能輸入 |
| 檢測目標 | UB、記憶體錯誤 | 斷言、性質違反 |
| 執行速度 | 慢（解釋執行） | 中（SMT 求解） |
| 誤報率 | 零（真 UB 才報） | 可能因迴圈 unwinding 有假陽性 |
| 適用階段 | 開發、測試 | CI、合規審查 |

實務中建議的流程：

1. 開發時用 `cargo test` 測試功能正確性
2. 用 `cargo miri test` 檢查所有測試有無 UB
3. 對關鍵函數寫 Kani proof harness，證明邊界條件與不變量
4. CI 中同時執行兩者

## 實際案例：用 Miri 和 Kani 驗證自訂配置器

以下是一個簡化的自訂配置器，管理固定大小的記憶體池：

```rust
use std::alloc::{GlobalAlloc, Layout};
use std::cell::UnsafeCell;
use std::ptr::NonNull;

pub struct BumpPool {
    pool: UnsafeCell<NonNull<u8>>,
    size: usize,
    offset: UnsafeCell<usize>,
}

unsafe impl GlobalAlloc for BumpPool {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        let off = *self.offset.get();
        let align = layout.align();
        let aligned_off = (off + align - 1) & !(align - 1);
        let new_off = aligned_off + layout.size();
        if new_off > self.size {
            return std::ptr::null_mut();
        }
        let ptr = self.pool.get().as_ptr().add(aligned_off);
        *self.offset.get() = new_off;
        ptr
    }

    unsafe fn dealloc(&self, _ptr: *mut u8, _layout: Layout) {
        // Bump 配置器不支援個別釋放
    }
}
```

### 用 Miri 檢查 UB

```rust
#[test]
fn miri_check_bump_alloc() {
    let mut storage = [0u8; 1024];
    let pool = BumpPool {
        pool: UnsafeCell::new(NonNull::new(storage.as_mut_ptr()).unwrap()),
        size: 1024,
        offset: UnsafeCell::new(0),
    };
    unsafe {
        let p = pool.alloc(Layout::new::<u64>());
        assert!(!p.is_null());
        *(p as *mut u64) = 42;
        // Miri 會驗證此寫入不超出配置範圍
        let q = pool.alloc(Layout::new::<u64>());
        assert!(!q.is_null());
        assert_eq!((q as usize) - (p as usize), 8);
    }
}
```

執行 `cargo +nightly miri test`，Miri 會確認無別名衝突、無重疊寫入。

### 用 Kani 證明配置器不變量

```rust
#[kani::proof]
#[kani::unwind(10)]
fn kani_bump_pool_safety() {
    let mut storage = [0u8; 256];
    let pool = BumpPool {
        pool: UnsafeCell::new(NonNull::new(storage.as_mut_ptr()).unwrap()),
        size: 256,
        offset: UnsafeCell::new(0),
    };
    // kani::any() 生成任意合法的配置請求
    let align: usize = kani::any();
    let size: usize = kani::any();
    kani::assume(align.is_power_of_two());
    kani::assume(align <= 64);
    kani::assume(size > 0 && size <= 128);

    unsafe {
        let ptr = pool.alloc(Layout::from_size_align(size, align).unwrap());
        if ptr.is_null() {
            // 若配置失敗，剩餘空間必須不足
            let off = *pool.offset.get();
            let remaining = pool.size - off;
            assert!(remaining < size); // 即配置器正確報告失敗
        } else {
            // 若配置成功，指標必須在池範圍內且對齊
            let base = pool.pool.get().as_ptr() as usize;
            let ptr_addr = ptr as usize;
            assert!(ptr_addr >= base);
            assert!(ptr_addr + size <= base + pool.size);
            assert_eq!(ptr_addr % align, 0);
        }
    }
}
```

這個 harness 讓 Kani 檢查所有可能的 `size` 和 `align` 組合，證明配置器在任何合法參數下都不會返回超出範圍或未對齊的指標。

## 在 CI 中整合驗證工具

將驗證整合進 CI pipeline 是讓工具發揮最大效益的關鍵。以下是一個 GitHub Actions 範例：

```yaml
name: Verify

on: [push, pull_request]

jobs:
  miri:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@nightly
        with:
          components: miri
      - run: cargo miri test
        env:
          MIRIFLAGS: -Zmiri-strict-provenance

  kani:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: model-checking/kani-github-action@v1
        with:
          args: cargo kani --tests
```

在 `MIRIFLAGS` 中啟用 `-Zmiri-strict-provenance` 會強制執行指標來源追蹤（Strict Provenance），確保不依賴指標的整數表示——這對未來 Rust 的記憶體模型演進至關重要。

大型專案如 `rustc` 本身、`hyper`、和 `tokio` 的某些關鍵模組都已採用類似流程。即便你的專案規模不大，在自訂配置器、FFI 綁定或底層資料結構中加入 Miri 和 Kani 的驗證，也能將「我相信這是对的」變成「我知道這是对的」。

## 結語

Miri 與 Kani 分別從動態與靜態兩個面向補足了 Rust 編譯器無法覆蓋的安全缺口。Miri 像一位嚴格的監察官，逐行執行你的測試並揪出每一處 UB；Kani 則像數學家，用形式化方法證明你的程式在所有情況下都符合預期。

系統程式碼的驗證不該是選配——當你的程式運行在數百萬台裝置上，或是嵌入在關鍵基礎設施中，Miri 和 Kani 是讓你夜裡安睡的兩道保險。
