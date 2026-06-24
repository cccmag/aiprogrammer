# 本期焦點

## 用 Rust 寫 Linux 驅動程式 — 從核心模組到安全驅動

### 引言

Linux 核心是世界上最大的開源專案之一，數十年來主要用 C 語言開發。隨著 Linux 核心 8.0 在 2026 年正式將 Rust 支援標記為穩定，撰寫核心驅動程式的方式正在發生根本性的改變。

Rust 的記憶體安全保證——所有權、借用檢查、生命週期——恰好擊中了核心開發中最頭痛的問題：緩衝區溢位、釋放後使用、雙重釋放。這些在 C 驅動程式中屢見不鮮的錯誤，在 Rust 中可以在編譯期被杜絕。

本期將帶你從零開始，學習如何在 Linux 核心中撰寫 Rust 驅動程式。我們不假設你有核心開發經驗，而是從最基礎的字元設備開始，逐步深入到 PCI、網路、GPU 等真實驅動程式的開發模式。

---

## 大綱

* [程式：實作 mini-kmod — 從零開始的 Rust 核心模組](focus_code.md)
   - 核心模組的生命週期
   - 字元設備操作
   - 平台驅動程式模型

1. [核心模組基礎（2021-2026）](focus1.md)
   - Rust for Linux 專案歷史
   - 核心 API 的 Rust 綁定
   - 模組初始化與卸載

2. [字元設備驅動程式（2021-2026）](focus2.md)
   - file_operations 結構
   - read/write/ioctl 實作
   - 與使用者空間溝通

3. [平台驅動程式與裝置樹（2022-2026）](focus3.md)
   - platform_driver 抽象
   - Device Tree 匹配
   - 電源管理整合

4. [PCI 與 USB 驅動程式（2022-2026）](focus4.md)
   - PCI 列舉與 BAR 空間
   - USB 裝置識別與驅動綁定
   - DMA 操作

5. [網路驅動程式（2023-2026）](focus5.md)
   - NAPI 與網路佇列
   - net_device_ops
   - 硬體卸載與 XDP

6. [GPU 與 DRM 驅動程式（2023-2026）](focus6.md)
   - Direct Rendering Manager 架構
   - GEM 緩衝區管理
   - 顯示控制器驅動

7. [AI 輔助驅動程式開發（2024-2026）](focus7.md)
   - 用 LLM 生成核心模組框架
   - 自動化 bindings 生成
   - 形式化驗證與模型檢查

---

## 核心驅動程式層次

```
使用者空間 (ioctl, mmap, read/write)
      │
字元設備層 (file_operations / miscdevice)
      │
核心驅動層 (platform_driver / pci_driver)
      │
硬體抽象層 (DMA / 中斷 / MMIO)
      │
硬體層 (PCI / USB / I2C / SPI 匯流排)
```

## 濃縮回顧

### Rust for Linux 的關鍵里程碑

Rust 進入 Linux 核心經歷了漫長的道路：

- **2020**：Google 與 ISRG（Internet Security Research Group）宣布支援 Rust for Linux
- **2021**：初始 RFC 貼上 Linux 核心郵件列表
- **2022**：初步的 Rust 支援合入 Linux 6.1
- **2024**：更多驅動程式用 Rust 改寫（NVMe、GPU）
- **2026**：Linux 8.0 宣布 Rust 支援正式穩定

### 為什麼核心開發者擁抱 Rust？

Linux 核心中約有 66% 的安全漏洞來自記憶體安全問題。Rust 在編譯期消除整類漏洞：

| 漏洞類型 | C 語言 | Rust |
|---------|--------|------|
| 緩衝區溢位 | 常見 | 編譯期檢查 |
| 釋放後使用 | 常見 | 借用檢查 |
| 雙重釋放 | 常見 | 所有權唯一 |
| 空指標解引用 | 常見 | Option 強制檢查 |
| 資料競爭 | 難以偵測 | Send/Sync 檢查 |

### 核心模組的基本結構

Rust 核心模組的核心抽象是 `Module` trait：

```rust
#[module]
struct MyDriver {
    name: CString,
    irq: i32,
}

impl Module for MyDriver {
    fn init(module: &'static ModuleInfo) -> Result<Self> {
        let name = CString::new("mydriver")?;
        pr_info!("mydriver: loaded\n");
        Ok(MyDriver { name, irq: 0 })
    }
}

impl Drop for MyDriver {
    fn drop(&mut self) {
        pr_info!("mydriver: unloaded\n");
    }
}
```

### 字元設備的 file_operations

字元設備是最常見的驅動程式類型。Rust 版本的 file_operations 使用安全的回呼註冊：

```rust
static MY_FOPS: FileOperationsVtable<MyDriver> =
    FileOperationsVtable::new()
        .read(|dev, buf, count, offset| { ... })
        .write(|dev, buf, count, offset| { ... })
        .ioctl(|dev, cmd, arg| { ... });

struct MyDriver {
    #[device]
    device: Device,
}
```

### 鎖定與併發

核心環境中的併發處理是驅動程式開發的最大挑戰。Rust 的所有權模型顯著簡化了鎖定：

- `SpinLock<T>` — 取代 `spin_lock()` / `spin_unlock()`
- `Mutex<T>` — 取代 `mutex_lock()` / `mutex_unlock()`
- `Ref<T>` — 取代 `kref_get()` / `kref_put()`

編譯器保證：鎖必須在正確的作用域內釋放，資源永遠不會在未鎖定狀態下被存取。

### 從 C 遷移到 Rust 的策略

真實世界的驅動程式遷移通常採用漸進式策略：

1. **包裹式**：用 Rust 模組包裹現有 C 驅動，逐步取代內部實作
2. **純 Rust 重寫**：從零開始用 Rust 撰寫新的驅動程式
3. **混合驅動**：關鍵路徑用 Rust（中斷處理、DMA），其餘用 C

---

**下一步**：[程式實作](focus_code.md) → [核心模組基礎](focus1.md)

## 延伸閱讀

- [The Linux Kernel Module Programming Guide](https://www.google.com/search?q=Linux+kernel+module+programming+guide)
- [Rust for Linux Kernel](https://www.google.com/search?q=Rust+for+Linux+kernel)
- [Linux 核心 8.0 Rust 支援](https://www.google.com/search?q=Linux+8.0+Rust+kernel)
- [Writing a Linux Kernel Module in Rust](https://www.google.com/search?q=Writing+Linux+kernel+module+in+Rust)
