# 本期焦點

## Rust 系統程式設計：從嵌入式到作業系統核心

### 引言

Rust 最初是為了解決系統程式設計的問題而誕生的。在前兩期（語言的歷史與生態、Web 服務實戰）之後，本期回歸 Rust 的本源——系統程式設計。

系統程式設計是 Rust 的「舒適區」：沒有 GC、零成本抽象、精確的記憶體控制、與 C 的無縫互操作。這些正是嵌入式系統、作業系統核心、裝置驅動程式和即時系統所需要的。

本期將探索 Rust 在系統程式設計領域的完整面貌：

- **no_std 與裸機**：沒有標準庫，直接與硬體對話
- **unsafe Rust**：何時跨越安全邊界，如何負責任地使用
- **FFI**：與 C 程式碼的無縫整合
- **即時系統**：在時限內完成任務的保證
- **作業系統核心**：從驅動程式到核心模組

---

## 大綱

* [程式：實作 mini-rt — 自訂記憶體配置器與 FFI](focus_code.md)
   - 從零實作 GlobalAlloc
   - 安全地包裹 unsafe 介面
   - 透過 FFI 呼叫 C 標準庫

1. [嵌入式 Rust（2017-2026）](focus1.md)
   - no_std 與標準庫的關係
   - embedded-hal 抽象層
   - Cortex-M 與 RISC-V

2. [裸機程式設計（2018-2026）](focus2.md)
   - 啟動流程與中斷向量表
   - 記憶體映射暫存器
   - panic 處理與異常

3. [unsafe Rust（2015-2026）](focus3.md)
   - unsafe 的超能力
   - 安全抽象的模式
   - 常見陷阱與最佳實踐

4. [FFI 與 C 互動（2016-2026）](focus4.md)
   - bindgen / cbindgen
   - ABI 相容性
   - 從 C 呼叫 Rust

5. [即時作業系統（2019-2026）](focus5.md)
   - RTIC 框架
   - Tock OS
   - FreeRTOS 整合

6. [作業系統核心（2020-2026）](focus6.md)
   - Rust for Linux
   - 核心模組開發
   - 裝置驅動程式

7. [AI + 系統程式（2024-2026）](focus7.md)
   - AI 輔助 unsafe 審查
   - 自動 FFI 生成
   - 形式化驗證整合

---

## 系統程式設計層次

```
應用層
  ┊  unsafe 隔離
嵌入式框架層 (embedded-hal, RTIC)
  ┊ 硬體抽象
硬體抽象層 (HAL crate)
  ┊  unsafe 暫存器存取
硬體層 (MCU 暫存器、中斷)
```

## 濃縮回顧

### 從 Web 到裸機

Rust 的設計目標是系統程式設計。所有權模型——所有權、借用、生命週期——本質上是為了解決 C/C++ 中的記憶體安全問題而設計的。但有趣的是，Rust 在 Web 服務領域反而最先獲得大規模採用。

直到 2020 年以後，Rust 在系統程式設計領域才真正起飛：

- **2017**：embedded-hal 發布，標準化嵌入式抽象
- **2019**：Rust for Linux 專案啟動
- **2020**：RTIC v1 發布，即時系統框架
- **2021**：Tock OS 2.0，安全嵌入式 OS
- **2023**：Cortex-M 生態成熟
- **2026**：Linux 核心 8.0 Rust 支援穩定

### no_std：沒有標準庫的世界

Rust 的標準庫假設有作業系統（檔案系統、網路、執行緒）。但在嵌入式系統中，這些可能不存在。no_std 環境下：

- 沒有 Vec、String、HashMap（但有 `core::` 中的替代品）
- 沒有堆分配（除非自訂 allocator）
- 沒有檔案 I/O 或網路
- 有精確的控制：中斷、暫存器、記憶體佈局

### unsafe 的責任

unsafe 是 Rust 系統程式設計的核心。它賦予了五種「超能力」：
1. 解引用裸指標
2. 呼叫 unsafe 函式（如 FFI）
3. 存取或修改可變靜態變數
4. 實作 unsafe trait（如 Send、Sync）
5. 存取 union 欄位

unsafe 的關鍵不是「禁用安全檢查」，而是「由開發者保證安全檢查」。

### Rust 在系統程式設計中的獨特優勢

| 需求 | Rust | C | C++ |
|------|------|---|-----|
| 記憶體安全 | ✅ 編譯期保證 | ❌ 人工管理 | 🟡 智慧指標 |
| 零成本抽象 | ✅ | ✅ | 🟡 部分 |
| 與 C FFI | ✅ 原生支援 | — | ✅ |
| 泛型/模板 | ✅ trait | ❌ | ✅ 模板 |
| 中斷安全 | ✅ Send/Sync | ❌ | ❌ |
| 裸機支援 | ✅ no_std | ✅ | 🟡 部分 |

---

**下一步**：[程式實作](focus_code.md) → [嵌入式 Rust](focus1.md)

## 延伸閱讀

- [The Embedded Rust Book](https://www.google.com/search?q=embedded+Rust+book)
- [Rustonomicon: The Unsafe Book](https://www.google.com/search?q=Rustonomicon+unsafe+book)
- [Rust for Linux](https://www.google.com/search?q=Rust+for+Linux+kernel)
