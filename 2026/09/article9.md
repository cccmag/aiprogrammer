# 在 Linux 核心中寫 Rust：核心模組實戰

## 前言

Linux 核心長久以來以 C 語言為主宰，但隨著 Rust for Linux 專案的推進，2022 年底 Linux 6.1 正式引入了實驗性的 Rust 支援。這不僅是技術上的里程碑，更代表著核心開發進入記憶體安全的時代。

本文將從實戰角度出發，帶領讀者理解如何在 Linux 核心中使用 Rust 撰寫核心模組，探討其架構設計、與 C 程式的互動方式，以及目前的限制與未來展望。

## Linux 核心的 Rust 支援歷史

Linux 核心對 Rust 的支援始於 6.0 系列的 RFC 討論，並在 6.1 版本（2022 年 12 月）合併了初始基礎架構。後續版本逐漸擴充：

- **Linux 6.1**：引入 Rust 實驗性支援，包含核心 Rust 基礎設施與範例驅動程式。
- **Linux 6.7**：更新 Rust 工具鏈要求至 Rust 1.73+，並加入更多核心抽象層。
- **Linux 6.8-6.10**：持續擴充 Rust 的 PHYLIB、NET 與 GPU 子系統抽象。
- **Linux 6.12 起**：Rust 支援逐步穩定，開始被用於實際驅動程式中，如 ASIX 乙太網路 PHY 驅動。

截至 2026 年的 6.x 系列，雖然 Rust 核心支援仍標註為實驗性，但其基礎設施已經足夠支撐實際的核心模組開發。

## Rust for Linux 專案現狀

Rust for Linux（R4L）是由 Miguel Ojeda 發起的專案，目標是讓 Rust 成為 Linux 核心中 C 以外的第一級語言。目前專案主要成果包含：

- **核心抽象層（Kernel Abstractions）**：對核心基礎設施（如 mutex、spinlock、workqueue、定時器）的安全封裝。
- **bindgen 自動綁定**：透過 `bindgen` 工具自動產生 Rust FFI 綁定，讓 Rust 可以直接呼叫 C 核心函式。
- **自訂核心 crate**：如 `kernel` crate，提供 `Arc`、`Ref` 等核心安全型別，以及 `Device`、`FileOperations` 等 trait。
- **Kbuild 整合**：核心建置系統支援 Rust 原始碼的編譯，只需在 `Kconfig` 中設定 `depends on RUST`。

## 撰寫第一個 Rust 核心模組

一個最簡單的 Rust 核心模組結構如下：

```rust
// SPDX-License-Identifier: GPL-2.0

//! Rust 核心模組 — Hello World 範例

use kernel::prelude::*;

module! {
    type: HelloModule,
    name: "hello_rust",
    author: "AI Programmer Magazine",
    description: "一個簡單的 Rust 核心模組",
    license: "GPL",
}

struct HelloModule;

impl kernel::Module for HelloModule {
    fn init(_module: &'static ThisModule) -> Result<Self> {
        pr_info!("Hello, Rust kernel module!\n");
        Ok(HelloModule)
    }
}

impl Drop for HelloModule {
    fn drop(&mut self) {
        pr_info!("Goodbye, Rust kernel module!\n");
    }
}
```

### 建立 /proc 條目

若要建立 `/proc/hello_rust` 條目並支援讀取：

```rust
use kernel::prelude::*;
use kernel::file::Operations;
use kernel::proc;

module! {
    type: ProcModule,
    name: "hello_proc",
    author: "AI Programmer Magazine",
    description: "含 /proc 條目的 Rust 核心模組",
    license: "GPL",
}

struct ProcModule {
    _proc: Pin<Box<pin_init::PinData<proc::DirEntry>>>,
}

struct RustProc;

impl Operations for RustProc {
    const THIS_MODULE: ThisModule = ThisModule::new_unwrap();

    kernel::declare_file_operations!(read, write);

    fn read(
        _this: &kernel::file::File,
        _buf: &mut impl kernel::io_buffer::IoBufferWriter,
        _offset: u64,
    ) -> Result<usize> {
        let msg = b"Hello from Rust kernel module!\n";
        // 實作檔案讀取回呼
        Ok(msg.len())
    }

    fn write(
        _this: &kernel::file::File,
        _buf: &impl kernel::io_buffer::IoBufferReader,
        _offset: u64,
    ) -> Result<usize> {
        pr_info!("proc file written\n");
        Ok(_buf.len())
    }
}

impl kernel::Module for ProcModule {
    fn init(module: &'static ThisModule) -> Result<Self> {
        pr_info!("Hello proc module loaded\n");
        let proc = proc::create_proc_entry(
            "hello_rust",
            module,
            RustProc,
            kernel::module_param::Permission::ReadWrite,
        )?;
        Ok(ProcModule { _proc: proc })
    }
}
```

## Rust 核心模組的架構

### 核心抽象層

Rust for Linux 的設計哲學不是重新發明輪子，而是對既有的 C 核心 API 進行安全封裝。主要抽象層元件：

- **`kernel::sync`**：封裝 `spinlock_t`、`mutex` 等鎖機制，編譯時確保鎖的正確使用。
- **`kernel::workqueue`**：安全的工作佇列提交，確保回呼函式型別正確。
- **`kernel::timer`**：基於 Rust 閉包的計時器，避免回呼指標錯誤。
- **`kernel::file::Operations`**：檔案操作特徵（trait），對應 `struct file_operations`。

### 安全封裝原則

核心模組採用三大安全原則：

1. **所有權模型**：Rust 的 ownership 機制確保核心資源（如配置的記憶體、開啟的檔案）在不再使用時自動釋放。
2. **型別安全**：FFI 邊界的 C 指標經過安全的包裝型別轉換，不暴露裸指標給模組開發者。
3. **Send/Sync 標記**：明確標記哪些型別可以安全地跨 CPU 傳送或共用，在編譯期避免資料競爭。

## 核心中的記憶體配置

核心環境的記憶體配置與使用者空間不同，必須使用核心專用的配置器：

```rust
use kernel::alloc::flags;

// 使用 GFP_KERNEL 配置記憶體
let buffer = kernel::alloc::vec![0u8; 4096; flags::GFP_KERNEL]?;

// 使用 KBox（核心版 Box）
let data = kernel::alloc::KBox::new(MyData::new(), flags::GFP_KERNEL)?;
```

Rust for Linux 提供了 `KBox`、`KVec`、`KString` 等核心感知型別，它們底層使用 `kmalloc` / `kfree`，並要求呼叫者指定 GFP flags。開發者不得使用標準庫的 `Box` 或 `Vec`，因為它們依賴使用者空間的配置器。

## 核心中的錯誤處理

核心模組的錯誤處理使用 Rust 標準的 `Result` 型別，但錯誤碼與核心的 errno 對應：

```rust
use kernel::error::{Error, code::*};

fn do_something() -> Result<(), Error> {
    let ptr = kernel::alloc::KBox::new(
        SomeData,
        flags::GFP_KERNEL,
    ).map_err(|_| Error::from_errno(ENOMEM))?;

    // 應用邏輯...
    Ok(())
}
```

核心 crate 提供：

- **`Error`**：封裝核心錯誤碼的新型別（newtype）。
- **`Result<T>`**：`core::result::Result<T, Error>` 的別名。
- **`Error::from_errno()`**：從 i32 核心錯誤碼（如 `-ENOMEM`、`-EINVAL`）建立錯誤。
- **程式碼產生**：在核心模組中，`?` 運算子可自動傳播錯誤，類似 C 語言中的 `goto out_err` 模式。

## Rust 與 C 核心程式碼的共存

Rust 核心模組並非孤立存在，而是必須與既有 C 子系統深度整合：

### FFI 邊界管理

透過 `extern "C"` 宣告以及 `bindgen` 產生綁定：

```rust
// 手動宣告 C 函式
extern "C" {
    fn printk(fmt: *const core::ffi::c_char, ...) -> i32;
}

// 使用 bindgen 產生的綁定（通常由核心建置系統自動處理）
```

### Kconfig 與 Makefile 整合

Rust 核心模組的 Kconfig 寫法：

```kconfig
config HELLO_RUST
    tristate "Hello Rust Module"
    depends on RUST
    help
      範例 Rust 核心模組
```

對應的 `Makefile`：

```makefile
obj-$(CONFIG_HELLO_RUST) += hello_rust.o
```

Rust 原始碼會自動被核心的編譯系統辨識並啟動 `rustc` 編譯。核心團隊維護了一份 `rustfmt.toml` 與 `clippy` 組態，確保程式碼風格一致。

### 共享資料結構

當 Rust 模組需要存取 C 端定義的資料結構（如 `sk_buff`、`net_device`）時，透過「零成本抽象」原則，Rust 型別直接對應到 C 結構體的記憶體佈局，不產生額外開銷：

```rust
#[repr(C)]
struct sk_buff {
    // ... 欄位對應核心標頭檔
}
```

## 目前限制與未來展望

### 當前限制

1. **工具鏈依賴**：需要特定版本的 `rustc` 與 `bindgen`，與發行版預裝版本可能不同。
2. **抽象層覆蓋率**：許多子系統（如網路、區塊層、PCIe）的 Rust 抽象尚未完整。
3. **unsafe 程式碼**：核心模組底層仍需使用 `unsafe` 來呼叫 C API，但應將其封裝在少數抽象層中。
4. **偵錯工具**：`kgdb`、`kprobe` 對 Rust 的支援仍在發展中，無法直接追蹤 Rust 的堆疊。
5. **模版化與泛型**：核心中過度使用 Rust 泛型可能導致編譯時間增長與二進位檔膨脹。

### 未來展望

- **更多子系統抽象**：社群正積極開發 GPU（DRM）、NVMe、USB 等子系統的安全抽象。
- **Rust for UEFI**：除了核心模組，Rust 也被用於核心開機階段的 EFI stub。
- **穩定標記**：預計在 Linux 6.x 後期版本中，Rust 支援將從「實驗性」升級為正式功能。
- **Asahi Linux**：Apple Silicon 平台的 Rust GPU 驅動程式展示了 Rust 核心開發的實際威力。

## 結語

在 Linux 核心中撰寫 Rust 不再是純粹的學術實驗。從 6.1 到 6.x，Rust for Linux 已經從原型階段成長為具備實用價值的開發選項。對於想要在記憶體安全與效能之間取得最佳平衡的驅動程式開發者而言，Rust 核心模組是一條值得投入的道路。

當然，學習曲線與生態系統的成熟度仍是挑戰——但正如 Linus Torvalds 在合併 Rust 支援時所說：「這只是個開始。」
