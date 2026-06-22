# 編譯器與工具鏈

## rustc、Cargo、LLVM 後端（2015-2020）

### rustc：Rust 的編譯器

Rust 編譯器 `rustc` 是整個 Rust 生態的核心。從 Rust 1.0 到 2026 年，rustc 經歷了多次重大重構和最佳化。

**編譯流程**：

```
原始碼 → 詞法分析 → 語法分析 → HIR → THIR → MIR → LLVM IR → 機器碼
```

- **HIR**（High-level IR）：保留高階語法資訊，用於型別檢查和借用檢查
- **THIR**（Typed HIR）：帶型別資訊的 HIR
- **MIR**（Mid-level IR）：控制流程和借用檢查的核心表示。所有權和生命週期檢查在這裡進行
- **LLVM IR**：交給 LLVM 進行低階最佳化，生成機器碼

這個多層次的中間表示設計讓 Rust 能夠：
1. 在 HIR 層面進行語法檢查和型別推斷
2. 在 MIR 層面進行借用檢查和所有權驗證
3. 利用 LLVM 後端進行高效的最佳化

### 借用檢查器（Borrow Checker）

借用檢查器是 rustc 中最複雜的元件。它在 MIR 層面上工作，分析程式中所有引用的生命週期。

從 Rust 1.0 到 NLL（Non-Lexical Lifetimes, 2018），再到 Ownership 2.0（2026），借用檢查器的能力持續提升：

```rust
// Rust 1.0：借用檢查器較為保守
fn example() {
    let mut data = vec![1, 2, 3];
    let slice = &data;  // 借用
    // data.push(4);    // 在 Rust 1.0 中，即使在 slice 未使用時也不允許
    println!("{:?}", slice);
    data.push(4);       // OK，slice 已不再使用
}
```

NLL（2018 年穩定）讓借用檢查器能夠理解**引用何時最後被使用**，從而允許更多合理的程式碼。Ownership 2.0（2026）則引入了精確的借用追蹤，進一步減少了與借用檢查器的「戰鬥」。

### Cargo：不僅僅是套件管理器

`Cargo` 是 Rust 的套件管理器、建置工具和測試執行器。從 2015 年 1.0 到 2026 年，Cargo 一直是 Rust 體驗的核心部分。

Cargo 的關鍵功能：

```toml
# Cargo.toml — 專案設定檔
[package]
name = "my-project"
version = "0.1.0"
edition = "2024"

[dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1", features = ["full"] }
```

```bash
# 基本命令
cargo new hello_world     # 建立新專案
cargo build              # 編譯
cargo run                # 編譯並執行
cargo test               # 執行測試
cargo check              # 快速檢查類型（不生成機器碼）
cargo doc                # 產生文件
cargo publish            # 發布到 crates.io
```

Cargo 的設計理念是「**慣例優於設定**」（convention over configuration）：
- 標準的目錄結構（`src/main.rs`、`src/lib.rs`、`tests/`）
- 自動依賴解析和版本管理（SemVer）
- 內建測試、基準測試、文件和格式化工具

### LLVM 後端

Rust 選擇 LLVM 作為編譯器後端，這是一項戰略性的決定：

- **成熟的最佳化**：LLVM 提供了世界級的最佳化框架（內聯、向量化、全域值編號等）
- **跨平台支援**：LLVM 支援數十種硬體架構，Rust 繼承了這些支援
- **工具整合**：LLVM 生態提供了 AddressSanitizer、ThreadSanitizer、CFI 等除錯工具

```bash
# 交叉編譯到 ARM
cargo build --target aarch64-unknown-linux-gnu
```

Rust 的 LLVM 整合也讓**即時編譯（JIT）**成為可能——透過 `cranelift` 後端，Rust 可以實現快速編譯和增量編譯。

### 編譯時間的挑戰與改進

Rust 編譯時間一直是開發者最常抱怨的問題。Rust 團隊從 1.0 開始就不斷改進：

**2015-2018**：增量編譯（incremental compilation）——只重新編譯變更的部分
**2019-2021**：平行前端（parallel frontend）——平行化語法分析和型別檢查
**2022-2024**：LLVM 最佳化——引入 ThinLTO、PGO、BOLT
**2025-2026**：ML 驅動的編譯最佳化——使用機器學習預測最佳化策略

```bash
# 2015 年的編譯時間（典型專案）
cargo build    # 10-30 秒
cargo check    # 5-15 秒

# 2026 年的編譯時間
cargo build    # 2-5 秒（modular codegen）
cargo check    # 0.5-2 秒（parallel typeck）
```

### Cargo 生態：crates.io

截至 2026 年 7 月，crates.io 上已超過 20 萬個 crate，下載次數超過 500 億次。Cargo 的依賴解析器使用 SAT solver（基於 MiniSAT）來解決複雜的依賴衝突問題。

### 工具鏈生態

Rust 的工具鏈不僅僅是編譯器：

| 工具 | 功能 | 開始年份 |
|------|------|----------|
| rustfmt | 自動格式化 | 2017 |
| clippy | 靜態分析/提示 | 2017 |
| rust-analyzer | IDE 支援/LSP | 2019 |
| cargo-edit | 依賴管理 | 2017 |
| cargo-audit | 安全審計 | 2018 |
| cargo-deny | 授權檢查 | 2020 |

### 小結

Rust 的編譯器和工具鏈是 Rust 成功的重要支柱。多層次的中間表示（HIR → MIR → LLVM IR）讓 Rust 能夠在提供強大安全保證的同時，生成高效的機器碼。Cargo 提供了無縫的開發體驗，而 LLVM 後端則保證了跨平台和高效的最佳化。

**編譯器不是限制，而是保障**——這是 Rust 的設計哲學。花在編譯上的每一秒鐘，都在防止執行時期的崩潰和安全漏洞。

---

**下一步**：[非同步與並行](focus4.md)

## 延伸閱讀

- [Rust Compiler Architecture](https://www.google.com/search?q=Rust+compiler+architecture)
- [Cargo: The Rust Package Manager](https://www.google.com/search?q=Cargo+Rust+package+manager)
- [Rust Compile Time Improvements](https://www.google.com/search?q=Rust+compile+time+improvements)
