# Rust Atomics 與記憶體順序深入探討

## 前言

在現代多核心處理器時代，並行程式設計已成為系統程式設計師的必備技能。Rust 作為一款強調安全與效能的系統程式語言，提供了強大的原子操作（Atomic Operations）與記憶體順序（Memory Ordering）原語，讓我們能在無鎖（lock-free）程式設計中兼顧正確性與效能。本文將深入探討 Rust 中的原子操作與六種記憶體順序，並透過實作自旋鎖來加深理解。

## Atomic 操作的基本概念

原子操作是指不可中斷的單一操作——要麼完全執行，要麼完全不執行。在並行環境中，當多個執行緒同時讀寫同一個變數時，若無原子保證，可能會出現 data race，導致未定義行為。

Rust 標準庫中的 `std::sync::atomic` 模組提供了多種原子型別：

- `AtomicBool`
- `AtomicI8`, `AtomicI16`, `AtomicI32`, `AtomicI64`, `AtomicIsize`
- `AtomicU8`, `AtomicU16`, `AtomicU32`, `AtomicU64`, `AtomicUsize`
- `AtomicPtr<T>`

每個原子型別都提供 `load`、`store`、`swap`、`compare_and_swap`（或 `compare_exchange`）等操作方法，且這些方法都接受一個 `Ordering` 參數來指定記憶體順序。

## Rust 的六種記憶體順序

Rust 定義了五種標準記憶體順序，加上一種編譯屏障（compiler fence），共六種。

### 1. Relaxed（`Ordering::Relaxed`）

`Relaxed` 是最輕量的記憶體順序，只保證操作本身的原子性，不提供任何 happens-before 關係或同步保證。不同執行緒對同一變數的 Relaxed 操作可以任意重排。

```rust
use std::sync::atomic::{AtomicBool, Ordering};
use std::thread;

let flag = AtomicBool::new(false);

// 執行緒 A
thread::spawn(move || {
    flag.store(true, Ordering::Relaxed);
});

// 執行緒 B
thread::spawn(move || {
    if flag.load(Ordering::Relaxed) {
        // 不一定能看到 A 的寫入，即使看到，也不保證看到 A 的其他寫入
    }
});
```

**適用場景**：計數器、統計資料、progress flag 等不影響其他記憶體操作的場合。

### 2. Release 與 Acquire

這是最常用的配對記憶體順序，用於實作「釋放-獲取」（release-acquire）同步模式。

- **Release**：寫入操作使用。保證在此之前的**所有記憶體寫入**（包括非原子寫入）在執行 Release 操作之前已對其他執行緒可見。
- **Acquire**：讀取操作使用。保證在此之後的**所有記憶體讀取**都可以看到另一個執行緒在 Release 操作之前寫入的資料。

```rust
use std::sync::atomic::{AtomicBool, Ordering};
use std::thread;

static DATA: [i32; 3] = [0; 3];
static READY: AtomicBool = AtomicBool::new(false);

// 生產者執行緒
thread::spawn(|| {
    DATA[0] = 42;           // 普通寫入
    DATA[1] = 100;
    DATA[2] = 200;
    READY.store(true, Ordering::Release);  // Release 屏障
});

// 消費者執行緒
thread::spawn(|| {
    if READY.load(Ordering::Acquire) {    // Acquire 屏障
        // 保證能看到 DATA 的所有寫入
        assert_eq!(DATA[0], 42);
    }
});
```

**適用場景**：生產者-消費者模式、標誌位同步、鎖的實作。

### 3. AcqRel（`Ordering::AcqRel`）

`AcqRel` 是 Acquire 與 Release 的組合，用於同時需要讀取和寫入的操作，如 `compare_exchange` 和 `swap`。它對寫入方施加 Release 語義，對讀取方施加 Acquire 語義。

**適用場景**：read-modify-write（RMW）操作，如自旋鎖的嘗試取得鎖。

### 4. SeqCst（`Ordering::SeqCst`）

`SeqCst`（順序一致，Sequentially Consistent）是最強的記憶體順序。它保證所有執行緒看到完全一致的全局操作順序。換句話說，程式的執行結果等同於所有執行緒的操作以某種交錯（interleaving）方式依序執行。

```rust
use std::sync::atomic::{AtomicBool, Ordering};

let x = AtomicBool::new(false);
let y = AtomicBool::new(false);

// 執行緒 A
x.store(true, Ordering::SeqCst);

// 執行緒 B
y.store(true, Ordering::SeqCst);

// 執行緒 C
let a = x.load(Ordering::SeqCst);
let b = y.load(Ordering::SeqCst);
// 不可能出現 a == false && b == false 同時發生的情況
```

**適用場景**：需要嚴格全局一致的場景，如 Dekker's algorithm、 Peterson's algorithm 等經典並行演算法。

### 5. 編譯屏障（Compiler Fence）

除了上述五種標準記憶體順序外，Rust 還提供了 `compiler_fence`：

```rust
use std::sync::atomic::{compiler_fence, Ordering};

compiler_fence(Ordering::AcqRel);
```

`compiler_fence` 只阻止編譯器對指令重排，不產生任何 CPU 層級的記憶體屏障指令。這在與特定 CPU 指令（如 `pause`）配合使用，或在作業系統核心開發中非常有用。一般應用程式開發中較少使用。

**適用場景**：驅動程式、作業系統核心、嵌入式系統等底層程式設計。

## 用 Atomic 實作自旋鎖

理解上述概念後，讓我們用 `AtomicBool` 實作一個簡單的自旋鎖（spinlock）：

```rust
use std::sync::atomic::{AtomicBool, Ordering};
use std::cell::UnsafeCell;
use std::ops::{Deref, DerefMut};
use std::thread;
use std::time::Duration;
use std::hint;

pub struct SpinLock<T> {
    locked: AtomicBool,
    data: UnsafeCell<T>,
}

// UnsafeCell 不是 Send/Sync，但 SpinLock 提供執行緒安全保證
unsafe impl<T: Send> Send for SpinLock<T> {}
unsafe impl<T: Send> Sync for SpinLock<T> {}

impl<T> SpinLock<T> {
    pub fn new(value: T) -> Self {
        SpinLock {
            locked: AtomicBool::new(false),
            data: UnsafeCell::new(value),
        }
    }

    pub fn lock(&self) -> SpinLockGuard<'_, T> {
        // 忙等（busy-wait），直到成功取得鎖
        while self
            .locked
            .compare_exchange(false, true, Ordering::Acquire, Ordering::Relaxed)
            .is_err()
        {
            // 在 x86 上可加入 pause 指令，在 ARM 上則是 yield
            hint::spin_loop();
        }
        SpinLockGuard { lock: self }
    }

    pub fn try_lock(&self) -> Option<SpinLockGuard<'_, T>> {
        self.locked
            .compare_exchange(false, true, Ordering::Acquire, Ordering::Relaxed)
            .ok()
            .map(|_| SpinLockGuard { lock: self })
    }
}

pub struct SpinLockGuard<'a, T> {
    lock: &'a SpinLock<T>,
}

impl<T> Deref for SpinLockGuard<'_, T> {
    type Target = T;

    fn deref(&self) -> &T {
        unsafe { &*self.lock.data.get() }
    }
}

impl<T> DerefMut for SpinLockGuard<'_, T> {
    fn deref_mut(&mut self) -> &mut T {
        unsafe { &mut *self.lock.data.get() }
    }
}

impl<T> Drop for SpinLockGuard<'_, T> {
    fn drop(&mut self) {
        // 使用 Release 語義釋放鎖，保證臨界區的寫入在解鎖前被看到
        self.lock.locked.store(false, Ordering::Release);
    }
}

fn main() {
    let lock = SpinLock::new(0);
    let mut handles = vec![];

    for _ in 0..10 {
        let lock_ref = &lock;
        handles.push(thread::spawn(move || {
            for _ in 0..1000 {
                let mut guard = lock_ref.lock();
                *guard += 1;
            }
        }));
    }

    for h in handles {
        h.join().unwrap();
    }

    let result = lock.lock();
    println!("最終結果: {}", *result); // 應輸出 10000
}
```

### 實作重點說明

1. **compare_exchange 使用 `Acquire`**：成功取得鎖時，需要看到前一個持有者寫入的資料。
2. **store 使用 `Release`**：釋放鎖時，確保臨界區的寫入對下一個取得鎖的執行緒可見。
3. **compare_exchange 失敗時用 `Relaxed`**：因為失敗代表沒取得鎖，不需同步。
4. **`hint::spin_loop()`**：提示處理器這是旋轉等待，在 x86 上會產生 `PAUSE` 指令，在 ARM 上會產生 `YIELD`，可改善效能與功耗。

## 記憶體順序與 CPU 架構的關係

記憶體順序的開銷與底層 CPU 架構密切相關。理解這些差異有助於我們做出更好的設計決策。

### x86（Intel / AMD）

x86 架構使用 **TSO（Total Store Order）** 記憶體模型，本身就相當嚴格：

- 所有 `store` 操作都有類似 Release 的語義
- 所有 `load` 操作都有類似 Acquire 的語義
- 只有在 `SeqCst` 的 `store` 時才會插入 `MFENCE` 指令（或 `LOCK` 前綴）

這意味著在 x86 上，`Relaxed`、`Acquire`、`Release`、`AcqRel` 在編譯後的機器碼是一樣的——編譯器只確保不進行不當重排，但不會插入硬體屏障指令。只有 `SeqCst` 會產生真正的屏障開銷。

### ARM / ARM64

ARM 架構使用 **弱記憶體模型（Weak Memory Model）**：

- 處理器可以自由重排記憶體操作
- 每種記憶體順序都會產生對應的屏障指令（如 `DMB` Data Memory Barrier）
- ARMv8 的 `LDAR`（load-acquire）和 `STLR`（store-release）指令直接對應 Acquire/Release 語義

因此在 ARM 上，不同記憶體順序的效能差異更明顯，`Relaxed` 比 `SeqCst` 快得多。

### 架構對比總結

| 順序 | x86 開銷 | ARM 開銷 |
|:---|:---|:---|
| Relaxed | 無 | 無 |
| Acquire | 無（隱含） | `DMB` 或 `LDAR` |
| Release | 無（隱含） | `DMB` 或 `STLR` |
| AcqRel | 無 | `DMB` |
| SeqCst (load) | 無 | `DMB` 或 `LDAR` |
| SeqCst (store) | `MFENCE` | `DMB` + `STLR` |

因此，若你編寫跨平台程式碼，使用 `Acquire`/`Release` 而不是 `SeqCst` 可以在 ARM 上獲得更好的效能。

## C++20 與 Rust 記憶體模型的比較

Rust 的記憶體模型深受 C++11 的影響，兩者本質上非常相似，但存在一些關鍵差異：

### 相同點

- 六種記憶體順序的名稱與語義幾乎相同（C++ 的 `memory_order_relaxed` 對應 Rust 的 `Ordering::Relaxed`，依此類推）
- 都定義了 happens-before 關係
- 都支援 `compare_exchange_weak` 與 `compare_exchange_strong`
- 操作在 data race 情況下都是未定義行為（UB）

### 差異點

1. **安全性保證**：C++ 的 data race 是未定義行為，編譯器可能產生任何程式碼。Rust 的 type system 在編譯期就杜絕了 data race——只有 `unsafe` 程式碼中的原子操作需要手動保證正確性。

2. **預設順序**：C++20 的 `atomic<T>` 預設使用 `memory_order_seq_cst`；Rust 則要求你每次操作都顯式指定 `Ordering`，避免因遺忘而誤用錯誤的順序。

3. **`std::atomic_ref`**：C++20 引入了 `atomic_ref`，允許對非原子變數進行原子操作。Rust 標準庫目前沒有直接對應，但可透過 `AtomicPtr` 或第三方 crate（如 `atomic`）實現類似功能。

4. **`compare_exchange` 的 weak/strong**：C++ 分為 `compare_exchange_weak`（可在 spurious fail 時返回 false）和 `compare_exchange_strong`。Rust 的 `compare_exchange` 等同於 `strong`，而 `compare_exchange_weak` 則對應 `weak` 版本。在循環中使用 `weak` 在 ARM 上可獲得更好效能。

5. **編譯屏障**：Rust 的 `compiler_fence` 在 C++ 中沒有直接對應物（C++ 的 `atomic_signal_fence` 概念類似但用於 signal handler）。

## 常見錯誤與最佳實踐

### 常見錯誤

**錯誤 1：在 Relaxed 之外假設操作順序**

```rust
// 錯誤示範：用 Relaxed 實作 flag 同步
static READY: AtomicBool = AtomicBool::new(false);
static DATA: AtomicI32 = AtomicI32::new(0);

// 執行緒 A
DATA.store(42, Ordering::Relaxed);
READY.store(true, Ordering::Relaxed);  // 可能被重排到 DATA.store 之前！

// 執行緒 B
if READY.load(Ordering::Relaxed) {
    // 可能看到 DATA 還是 0！
    println!("{}", DATA.load(Ordering::Relaxed));
}
```

**錯誤 2：在 compare_exchange 中混用錯誤順序**

```rust
// 低效但正確：Acquire 和 Release 分開指定
lock.compare_exchange(false, true, Ordering::Acquire, Ordering::Relaxed);

// 可能過度保守：成功和失敗都用 AcqRel
lock.compare_exchange(false, true, Ordering::AcqRel, Ordering::AcqRel);
```

**錯誤 3：SeqCst 依賴**

過度使用 `SeqCst` 不僅在 ARM 上造成效能損失，還可能隱藏設計問題。如果無法用 `Acquire`/`Release` 推理程式的正確性，往往代表設計本身有缺陷。

### 最佳實踐

1. **從 Relaxed 開始，按需強化**：先使用最弱的記憶體順序滿足功能，再用測試和形式化驗證確保正確性。

2. **使用 Acquire/Release 而非 SeqCst**：除非需要嚴格的全局一致順序（如三執行緒以上的複雜同步），否則 `Acquire`/`Release` 已足夠。

3. **為 compare_exchange 指定合適的失敗順序**：失敗順序可以是 `Relaxed` 或 `Acquire`，但絕不應是 `Release` 或 `AcqRel`——因為失敗時沒有任何寫入需要釋放。

4. **優先使用高層同步原語**：除非需要極致效能，否則優先使用 `Mutex`、`RwLock`、`Barrier`、`Channel` 等高層抽象，它們內部已正確處理記憶體順序。

5. **撰寫 loom 測試**：[loom](https://crates.io/crates/loom) 是 Rust 生態系中的並行測試工具，它透過排列組合所有可能的執行順序來驗證無鎖資料結構的正確性。

6. **文件化記憶體順序的意圖**：使用 `Acquire`/`Release` 時，在註解中說明哪個操作與哪個操作同步，幫助後續維護者理解。

## 結語

Rust 的原子操作與記憶體順序看似複雜，但掌握其核心概念後，就能寫出既安全又高效的低階並行程式碼。最重要的是記住：**使用最弱且足夠的記憶體順序**，並在高層抽象不足時才手動操作原子變數。隨著無鎖資料結構與無阻塞演算法在高效能系統中的需求增加，這些知識將成為 Rust 系統程式設計師不可或缺的技能。

下一篇文章將探討 Rust 的非同步程式設計模型與 async/await 的內部實作，敬請期待。
