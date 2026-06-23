# Rust for Linux 專案深度解析 — 專案架構、維護模式、社群治理

## 1. 引言

Rust for Linux 不僅僅是一組程式碼綁定——它是一個在數十年歷史的 C 語言專案中引入全新語言和工具鏈的大型基礎設施專案。它的成功不僅依賴於技術設計，還得益於深思熟慮的專案治理和社群策略。本文深入分析 Rust for Linux 的內部運作機制。

## 2. 專案架構

### 2.1 核心元件

Rust for Linux 的程式碼分布在 Linux 核心原始碼樹的幾個部分：

```
linux/
├── rust/
│   ├── alloc.rs          # 核心記憶體分配器 (Rust Global allocator)
│   ├── bindings.rs       # C API 自動生成的 FFI 綁定
│   ├── kernel/            # 核心 Rust 抽象
│   │   ├── prelude.rs     # 常用匯入和巨集
│   │   ├── sync.rs        # 同步原語 (SpinLock, Mutex, Ref)
│   │   ├── device.rs      # 裝置模型抽象
│   │   ├── file.rs        # file_operations 抽象
│   │   ├── platform.rs    # 平台驅動程式抽象
│   │   ├── pci.rs         # PCI 驅動程式抽象
│   │   ├── net.rs         # 網路裝置抽象
│   │   ├── drm/           # DRM/GPU 抽象
│   │   ├── i2c.rs         # I2C 抽象
│   │   ├── gpio.rs        # GPIO 抽象
│   │   └── firmware.rs    # 韌體載入抽象
│   ├── macros.rs          # proc-macro（如 #[module]）
│   └── helpers.c          # 輔助 C 函式（橋接 Rust-C）
│
├── include/linux/rust/    # Rust 相關的 C 標頭
│
└── samples/rust/          # Rust 驅動程式範例
```

### 2.2 抽象層次設計

Rust for Linux 的抽象分為三個層次：

**L0 — 原始 FFI 綁定（bindings.rs）**

自動從 C 標頭生成的原始嵌入（`extern "C"`）：

```rust
// 自動生成的 FFI 綁定
extern "C" {
    pub fn printk(fmt: *const u8, ...);
    pub fn kmalloc(size: usize, flags: u32) -> *mut u8;
    pub fn kfree(ptr: *mut u8);
}
```

**L1 — 安全包裹（kernel::sync, kernel::alloc 等）**

為原始 FFI 提供安全抽象：

```rust
// 安全的 kmalloc/kfree 包裹
pub struct KVirtBox<T: ?Sized> {
    ptr: NonNull<T>,
    layout: Layout,
}

impl<T> KVirtBox<T> {
    pub fn new(val: T, flags: GFPFlags) -> Result<Self> {
        let layout = Layout::new::<T>();
        let ptr = unsafe { kmalloc(layout.size(), flags.0) };
        // ...
    }
}

impl<T: ?Sized> Drop for KVirtBox<T> {
    fn drop(&mut self) {
        unsafe { kfree(self.ptr.as_ptr() as *mut u8); }
    }
}
```

**L2 — 高階驅動抽象（kernel::platform, kernel::pci 等）**

提供驅動程式開發者使用的完整 API：

```rust
// 開發者直接使用的高階 API
impl PlatformDriver for MyDriver {
    fn probe(dev: &mut platform::Device) -> Result<Self> {
        let mmio = dev.get_iomem(0, "reg")?;
        let irq = dev.get_irq(0)?;
        Ok(Self { mmio, irq })
    }
}
```

## 3. 架構決策：為什麼是 `kernel` crate 而不是獨立 cgroup？

### 設計考量

Rust for Linux 選擇將 `kernel` crate 放在核心原始碼樹內，而不是作為外部 cgroup，基於以下原因：

1. **版本鎖定**：`kernel` crate 與核心版本嚴格綁定，API 的演進與核心同步
2. **編譯整合**：使用核心的 Kbuild 系統編譯，避免外部工具鏈問題
3. **API 穩定性**：核心不提供穩定的內部 API（不承諾向後相容），外部 crate 無法維持
4. **性能優化**：編譯器可以進行跨語言的最佳化（LTO）

## 4. 維護模式

### 4.1 貢獻流程

Rust for Linux 的貢獻流程與核心其他子系統一致：

```
1. 開發者在 rust-for-linux/linux fork 上開發
2. 提交 Pull Request
3. 自動 CI (KernelCI) 測試：
   ├── x86_64, aarch64, riscv 編譯測試
   ├── 連結檢查 (rustc LTO)
   ├── clippy lint
   ├── Rust 測試 (cargo test)
   └── 核心模組載入測試
4. Rust for Linux 維護者審查
5. 子系統維護者審查（如 PCI 變更需要 PCI 維護者 ACK）
6. Linus Torvalds 合入
```

### 4.2 維護者層級

| 層級 | 職責 | 代表人物 |
|------|------|---------|
| Rust 子系統維護者 | 管理 rust/ 目錄、抽象層設計 | Miguel Ojeda, Wedson Almeida Filho |
| Rust 抽象維護者 | 維護特定抽象（PCI、網路等） | 子系統專家 |
| Rust 驅動程式維護者 | 維護特定 Rust 驅動程式 | 驅動開發者 |
| C 子系統協作者 | 審查影響 C 核心的 Rust 變化 | 各子系統維護者 |

## 5. 社群治理

### 5.1 協調模型

Rust for Linux 與上游 Linux 核心的整合採用「漸進式協調」模型：

1. **初期（2021-2023）**：單獨的 rust-for-linux/linux 分支，獨立演進
2. **中期（2024-2025）**：核心元件分批合入主線，部分保留在外部
3. **成熟期（2026+）**：完全整合，Rust 支援是核心不可分割的一部分

### 5.2 關鍵討論與決策

**工具鏈版本策略**

Rust for Linux 需要特定的 Rust 編譯器版本。核心的決定是：
- 追蹤最新的 stable Rust（每年 6 個版本）
- 最低支援 N-2 個 stable 版本
- 允許用 nightly 的功能（但需有 stable 的替代方案路線圖）

**安全性 vs 性能權衡**

部分核心開發者擔憂 Rust 的安全檢查會帶來執行期開銷。實際測量顯示：
- Rust 核心模組的平均開銷在 1-3% 之間
- 在大多數場景中，Rust 的編譯器最佳化可以彌補開銷
- 關鍵路徑（如中斷處理）允許使用 `unsafe` 來消除邊界檢查

## 6. 貢獻者生態

截至 2026 年 10 月，Rust for Linux 的貢獻者生態：

```
每月活躍貢獻者: ~120 人
企業支援: Google, Intel, Red Hat, Samsung, AWS, Canonical
驅動程式數量: 200+（核心中）+ 300+（外部樹）
文件: 完整的中英文 API 文件
```

## 7. 結語

Rust for Linux 的專案架構和社群治理模型值得其他大型開源專案借鏡。它的核心洞察是：語言遷移不是技術挑戰，而是社會挑戰——成功的關鍵在於設計一個讓 C 開發者和 Rust 開發者能夠和諧共存的合作模式，而不是強制所有人都轉向 Rust。

---

## 延伸閱讀

- [Rust for Linux 專案官網](https://www.google.com/search?q=Rust+for+Linux+project)
- [Rust for Linux 維護者指南](https://www.google.com/search?q=Rust+for+Linux+maintainer+guide)
- [Linux 核心 Rust 編碼規範](https://www.google.com/search?q=Linux+kernel+Rust+coding+guidelines)
