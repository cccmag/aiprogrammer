# AI 輔助雜誌編輯實戰手冊 — 九月號

## 前言

本文記錄使用 AI（OpenCode + Big Pickle）編輯《AI 程式人雜誌》2026 年 9 月號的完整流程與技巧。本月主題是「Rust 系統程式設計—嵌入式、unsafe、FFI 與低階抽象」。

---

## 一、專案結構設計

### 1.1 目錄規劃

```
202609/
├── _code/                 # Rust 系統程式專案
│   ├── Cargo.toml        # 依賴管理（libc）
│   ├── src/main.rs       # mini-rt 系統程式設計展示
│   └── test.sh          # 測試腳本
├── _doc/
│   ├── editor.md        # 編輯技巧記錄（本文件）
│   └── prompt.md        # 提示詞模板
├── focus.md              # 本期主題概覽
├── focus_*.md           # 深入教學文章
├── focus_code.md        # mini-rt 專案文件
├── news.md              # 本月新知
├── article1-10.md      # 精選文章
├── articles.md         # 文章索引
└── end.md              # 結語
```

### 1.2 技術棧

```
Rust 2024 Edition    語言版本
libc                  FFI 到 C 標準函式庫
GlobalAlloc trait     自訂配置器
Miri + Kani           程式碼驗證工具
```

---

## 二、系統程式專案的 AI 輔助開發

### 2.1 專案選擇

本月程式專案是 **mini-rt**——一個展示 Rust 系統程式設計核心概念的迷你專案：

1. **Bump Allocator**：實作 GlobalAlloc trait，展示自訂記憶體配置器
2. **FFI 封裝**：安全地呼叫 libc 函式（getpid、gethostname）
3. **MMIO 暫存器**：使用 volatile 存取模擬硬體暫存器
4. **Ring Buffer**：低階指標操作的環形緩衝區

### 2.2 AI 輔助開發流程

**Phase 1: Bump Allocator 設計**

第一次嘗試使用 `addr_of_mut!` 直接取得 HEAP_MEMORY 的指標，但 Rust 2024 Edition 禁止對 mutable static 建立 shared reference。修復為先計算位址再加法。

```rust
// 錯誤：在 2024 Edition 中不被允許
let ptr = unsafe { HEAP_MEMORY.as_ptr() };

// 正確：使用 addr_of_mut!
let ptr = unsafe { std::ptr::addr_of_mut!(HEAP_MEMORY) };
```

**Phase 2: 全域配置器與測試的衝突**

使用 `#[global_allocator]` 後，`cargo test` 崩潰（"memory allocation failed"）。原因是測試框架需要動態分配記憶體，但 bump allocator 無法回收記憶體。

**解決方案**：
- 在測試時不使用自訂全域配置器
- 使用 `#[cfg(not(test))]` 條件編譯

```rust
#[cfg(not(test))]
#[global_allocator]
static ALLOCATOR: BumpAllocator = BumpAllocator::new();
```

**Phase 3: unsafe 警告處理**

Rust 2024 Edition 對 unsafe-in-unsafe 的警告更嚴格。某些原本被認為需要 unsafe 的巨集（如 `addr_of!`、`addr_of_mut!`）在 2024 Edition 中不再需要 unsafe 區塊。

### 2.3 雜誌主題結構

本期採用「金字塔架構」：

```
層次 1：核心概念（focus_unsafe.md、focus_atomics.md）
  └─ 結構化教學文章

層次 2：生態系統（focus_tock.md、focus_linux_kernel.md）
  └─ 最新技術介紹

層次 3：專案實戰（_code/ + focus_code.md）
  └─ mini-rt 完整專案

層次 4：延伸閱讀（article1-10.md）
  └─ 10 篇主題文章
```

---

## 三、文章主題寫作經驗

### 3.1 主題規劃

```
unsafe Rust 規則    → 15% (focus_unsafe + article3)
FFI 與跨語言      → 15% (article4)
嵌入式 Linux      → 12% (article1)
Tock OS           → 12% (article2)
no_std            → 10% (article6)
Atomics           → 10% (article8 + focus_atomics)
Linux 核心模組     → 10% (article9)
驗證工具           → 8% (article7)
元程式設計         → 5% (article5)
未來展望           → 3% (article10)
```

### 3.2 與上期（Rust Web 生態）的區別

上期 focus：Rust 生態的 Web/後端應用（Tokio、Axum、SQLx）
本期 focus：Rust 系統程式設計（嵌入式、核心、FFI）

**寫作重點差異**：
- 上期：非同步、路由、資料庫
- 本期：unsafe、指標、記憶體配置、FFI

### 3.3 文章產出方式

所有文章使用平行任務（Task tool）一次生成，每個任務獨立產出一篇文章。10 篇文章分兩批平行生成（每批 5 篇），效率顯著。

---

## 四、常見問題與解決方案

### 4.1 Rust 2024 Edition 相容性

**問題**：Rust 2024 Edition 對 unsafe 的限制更嚴格

| 問題 | 解決方案 |
|------|---------|
| 對 static mut 建立 shared ref | 使用 `addr_of!` / `addr_of_mut!` |
| unsafe-in-unsafe 警告 | 移除不必要的 unsafe 區塊 |
| 測試與自訂配置器衝突 | 使用 `#[cfg(not(test))]` 條件編譯 |

### 4.2 全域配置器的測試策略

**問題**：自訂 `#[global_allocator]` 會影響測試框架本身

**解決**：
1. 使用條件編譯讓測試使用標準配置器
2. 在測試中用獨立的 bump allocator 實例測試配置邏輯

### 4.3 Bump Allocator 的限制

Bump allocator 是最簡單的配置器，但有以下限制：
- `dealloc` 是空操作，記憶體無法被單獨釋放
- 不適合長時間運行的程式
- 不支援執行緒安全（除非加鎖）
- 可能浪費大量記憶體

---

## 五、常用指令參考

```bash
# Rust 系統程式開發
cargo build                    # 編譯
cargo test                     # 執行測試
cargo run                      # 執行
cargo +nightly miri test       # 用 Miri 驗證
cargo kani                     # 用 Kani 驗證

# FFI
cargo install bindgen          # 安裝 bindgen

# 交叉編譯
rustup target add armv7-unknown-linux-gnueabihf
cargo build --target armv7-unknown-linux-gnueabihf
```

---

## 六、最佳實踐總結

1. **先 cargo build 再寫文章**：確保程式碼可編譯，文章中的範例才是正確的
2. **cfg 測試門檻**：自訂全域配置器要注意測試環境的適配
3. **平行生成文章**：使用 Task tool 平行生成文章，大幅提升效率
4. **版本相容性**：Rust 2024 Edition 有新限制，注意 `addr_of!` 等變化
5. **程式碼文件化**：用 focus_code.md 詳細解釋每個 unsafe 的使用理由

---

*本文為《AI 程式人雜誌》編輯技巧記錄*
