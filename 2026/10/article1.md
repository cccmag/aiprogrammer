# Linux 核心 Rust 支援發展史 — 從 2020 年 RFC 到 2026 年正式穩定

## 1. 引言

2020 年 4 月，Miguel Ojeda 向 Linux 核心郵件列表發送了一封標題為「Rust as a Second Language for the Linux Kernel」的 RFC（Request for Comments）。當時很少有人預料到，這個提議將在六年後徹底改變 Linux 核心的開發景觀。本文記錄 Rust 進入 Linux 核心的完整歷程。

## 2. 萌芽期（2020）

### 初始 RFC（2020 年 4 月）

Miguel Ojeda 發布的 RFC 提出了用 Rust 撰寫核心模組的初步方案。RFC 的目標有兩個：

1. 減少核心驅動程式中記憶體安全相關的漏洞
2. 在不破壞現有 C 生態的前提下，引入更安全的系統程式設計語言

當時的反應是兩極化的——一些核心維護者熱情擁抱這個想法，另一些則對 Rust 的工具鏈複雜性、編譯時間和執行期開銷表示擔憂。

### Google 與 ISRG 的支援（2020 年 7 月）

Google 和 Internet Security Research Group（ISRG，Let's Encrypt 的母公司）宣布投入資源支援 Rust for Linux 的開發。Google 的工程師開始參與核心抽象的設計，ISRG 則提供了資金支援。這標誌著 Rust for Linux 從個人專案升級為有組織支援的計畫。

## 3. 發展期（2021-2022）

### 核心抽象層的設計

2021 年是設計階段。Rust for Linux 團隊設計了核心的抽象層次：

```
核心原始碼樹
├── include/linux/      # C 標頭
└── rust/
    ├── alloc.rs        # Rust 核心配置器綁定
    ├── bindings.rs     # C API 自動生成綁定
    ├── kernel/         # 高階 Rust 抽象
    │   ├── sync.rs     # 鎖定原語
    │   ├── printk.rs   # 核心日誌
    │   ├── device.rs   # 裝置模型
    │   └── file.rs     # file_operations
    └── module.rs       # 模組基礎設施
```

### 合入 Linux 6.1（2022 年 10 月）

2022 年 10 月，Linux 6.1 發布，正式包含 Rust 的初步支援。這是一個里程碑事件——雖然當時 Rust 支援被標記為「實驗性」，且只提供最基礎的 API，但這意味著 Rust 第一次成為 Linux 核心官方支援的語言。

## 4. 成長期（2023-2024）

### 驅動程式生態開始萌芽

2023 年開始，越來越多的驅動程式開始用 Rust 撰寫：

- **NVMe 驅動**：最初的示範專案，展示了 Rust 在儲存子系統的應用
- **GPU 驅動**：Asahi Linux 專案在 Apple Silicon GPU 驅動中大量使用 Rust
- **網路驅動**：Phy 和 MAC 層的 Rust 實作開始出現

### 核心 API 綁定的擴展

2024 年，Rust for Linux 專案達到了關鍵規模——核心抽象覆蓋了主要的驅動程式 API：

| 版本 | 新增 API |
|------|---------|
| 6.2 | 基礎同步原語、printk |
| 6.5 | file_operations、裝置模型 |
| 7.0 | PCI、DMA、中斷處理 |
| 7.5 | 網路（NAPI、net_device_ops） |
| 7.8 | DRM/GEM、USB、IIO |

## 5. 成熟期（2025-2026）

### 社群規模的爆發

到了 2025 年，Rust for Linux 的貢獻者超過 500 人，核心中的 Rust 程式碼突破 30 萬行。多家大公司（Google、Intel、Samsung、Red Hat、AWS）都投入了全職工程師。

### Linux 8.0：Rust 支援正式穩定（2026 年 3 月）

2026 年 3 月，Linux 8.0 發布，Linpus Torvalds 在發布公告中宣布 Rust 支援正式從「實驗性」升級為「穩定」。這意味著：

- Rust 核心模組的 ABI 不再頻繁變動
- 核心維護者開始要求新的驅動程式優先考慮 Rust
- Rust 被列入核心的官方語言支援清單

### Linux 8.1 的額外進展（2026 年 10 月）

本月發布的 Linux 8.1 進一步強化了 Rust 的整合：
- 統一的裝置模型抽象層（DMAL）
- 核心 Rust 驅動程式數量突破 200 個
- kernel-bindgen 工具正式發布

## 6. 關鍵里程碑回顧

```
2020-04  Miguel Ojeda 發布初始 RFC
2020-07  Google + ISRG 宣布支援
2021-06  首次核心抽象層提交
2022-10  Linux 6.1 合入實驗性 Rust 支援
2023-05  第一個 Rust 網路驅動
2024-03  Rust 核心程式碼突破 10 萬行
2025-01  Linux 7.0 大幅擴展 Rust API
2026-03  Linux 8.0 Rust 支援穩定
2026-10  Linux 8.1 DMAL + kernel-bindgen
```

## 7. 啟示與展望

Rust for Linux 的成功不僅是一個技術成就，更證明了大型開源專案的語言遷移是可行的。關鍵因素包括：

1. **漸進式策略**：不強制遷移，而是提供並行的 Rust 選項
2. **生態系支援**：Google、AWS 等企業的持續投入
3. **工具鏈成熟**：LLVM、rustc 對核心場景的支援逐步完善
4. **社群共識**：核心維護者對記憶體安全重要性的認知轉變

展望未來，Rust 在核心中的佔比將持續成長。預測到 2030 年，新撰寫的驅動程式中將有 50% 以上使用 Rust。

---

## 延伸閱讀

- [Rust for Linux RFC 原文](https://www.google.com/search?q= Miguel+Ojeda+Rust+for+Linux+RFC+2020)
- [Linux 6.1 Rust 支援公告](https://www.google.com/search?q=Linux+6.1+Rust+support)
- [Linux 8.0 發布說明](https://www.google.com/search?q=Linux+8.0+release+notes)
