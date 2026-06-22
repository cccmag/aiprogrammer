# 文章集錦

## Rust 系統程式設計專輯

### 程式相關（10 篇）

#### 1. [Rust 在嵌入式 Linux 中的應用](article1.md)

嵌入式 Linux 與裸機嵌入式系統的區別、Rust 在嵌入式 Linux 中的定位、GPIO/I2C/SPI 存取、交叉編譯工具鏈、Yocto/Buildroot 整合。包含 GPIO sysfs 與 /dev/gpiochip 的 Rust 程式碼範例。

#### 2. [Tock OS：Rust 寫的安全嵌入式作業系統](article2.md)

Tock OS 的架構與設計理念、基於型別系統的 Capability 權限模型、MPU 記憶體保護、Tock OS 3.0 新特性、與 FreeRTOS 的比較。適合物聯網和感測器網路場景。

#### 3. [unSAFE Rust 實戰：正確使用 unsafe 的 10 條規則](article3.md)

最小化作用域、Safety 文件規範、安全封裝模式、Miri/Kani 驗證工具、Send/Sync 審查等 10 條 unsafe 使用規則，每條附有說明和程式碼範例。

#### 4. [Rust 與 C 的互相操作實戰](article4.md)

extern "C" 與 ABI 相容性、bindgen 自動生成 FFI 綁定、cbindgen 生成 C 頭檔、回呼函式、動態載入、所有權跨語言傳遞。包含 libzstd 整合案例。

#### 5. [Rust 編譯時元程式設計：從 proc-macro 到 const generics](article5.md)

proc-macro 的原理與應用、const generics 泛型參數、const fn 編譯時計算。包含 #[derive(MMIO)] 的 proc-macro 實戰案例。

#### 6. [no_std Rust：沒有標準庫的 Rust 程式設計](article6.md)

#![no_std] 與核心 crate（core、alloc）、panic_handler、alloc_error_handler、embedded-hal 驅動開發。包含 LED 驅動的完整案例。

#### 7. [用 Miri 與 Kani 驗證 Rust 系統程式碼](article7.md)

Miri 借用檢查器模擬器、Kani 形式化驗證工具、UB 偵測、正確性證明、CI 整合。包含自訂配置器的驗證案例。

#### 8. [Rust Atomics 與記憶體順序深入探討](article8.md)

六種記憶體順序（Relaxed、Acquire、Release、AcqRel、SeqCst）的深入分析、自旋鎖實作、x86 與 ARM 架構差異、與 C++20 記憶體模型的比較。

#### 9. [在 Linux 核心中寫 Rust：核心模組實戰](article9.md)

Linux 核心 Rust 支援歷史、Rust for Linux 專案現狀、核心記憶體配置與錯誤處理、Rust 與 C 核心程式碼的共存。包含 /proc 條目的核心模組範例。

#### 10. [Rust 系統程式設計的未來展望](article10.md)

Rust 2027/2030 發展路徑、嵌入式生態系（embassy、rtic）、Linux/Redox/sel4 核心採用、太空安全領域應用（NASA、ESA）、WebAssembly 邊緣運算、學習路徑建議。
