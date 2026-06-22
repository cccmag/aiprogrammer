# RISC-V + Rust：開放硬體時代的程式設計

## 開放指令集的十年革命

2010 年，加州大學柏克萊分校的 Krste Asanović 教授帶領團隊啟動了一個看似簡單的計畫——設計一套完全開放、不受專利束縛的指令集架構（ISA）。誰也沒想到，這個名為 RISC-V 的計畫在十六年後會成為橫跨嵌入式系統、邊緣運算、資料中心乃至太空探索的處理器基礎。

2026 年的今天，RISC-V 不再是「明日之星」。根據 RISC-V International 的統計，2025 年全球 RISC-V 核心出貨量突破 200 億顆，預計 2027 年將達到 500 億顆。從 Alibaba 的 XuanTie 系列到 Ventana 的高效能伺服器晶片，從 Western Digital 的儲存控制器到 Google 的客製化 TPU 輔助處理器——RISC-V 已經滲透到運算的每一個角落。

這場開放硬體革命的獨特之處在於：它不僅僅是硬體工程師的遊戲。軟體開發者，尤其是 Rust 程式設計師，正站在這場變革的最前線。

## Rust 對 RISC-V 的支援

Rust 與 RISC-V 的緣分可以追溯到 2016 年。當時 Rust 編譯器（rustc）基於 LLVM 框架，而 LLVM 早在 2015 年就加入了 RISC-V 後端支援。這意味著 Rust 幾乎是「天生」就具備了交叉編譯到 RISC-V 目標的能力。

### 編譯器後端

目前 Rust 對 RISC-V 的支援分為三個層級：

| 目標三元組 | 說明 |
|---|---|
| `riscv64imac-unknown-none-elf` | 64 位元 RISC-V，IMA 架構 + 壓縮指令，無作業系統 |
| `riscv32imac-unknown-none-elf` | 32 位元 RISC-V，IMA 架構 + 壓縮指令，無作業系統 |
| `riscv64gc-unknown-none-elf` | 64 位元 RISC-V，G 通用架構，無作業系統 |
| `riscv64gc-unknown-linux-gnu` | 64 位元 RISC-V，執行 Linux |

這些目標在 rustc 中屬於 **Tier 2** 支援等級，這表示官方保證其通過測試套件，且會持續維護。對於嵌入式開發者而言，`riscv64imac-unknown-none-elf` 是最常見的目標——`bare-metal` 環境、沒有作業系統、直接操作硬體。

### 標準庫與 `no_std`

RISC-V 嵌入式環境的典型配置是 `no_std`——不使用 Rust 標準庫。這是因為標準庫依賴於作業系統的系統呼叫（檔案 I/O、網路、執行緒等），而在 bare-metal 環境中這些功能根本不存在。

但這不表示你什麼都沒有。`core` 庫提供了所有與作業系統無關的基礎功能：迭代器、閉包、Result/Option、基本資料結構等。`alloc` 庫則提供了堆疊分配（需要你自行實作分配器）。

換句話說：**你在 `no_std` 環境中失去的是 `std`，不是 Rust。**

### 嵌入式生態系統

RISC-V 的嵌入式 Rust 生態在 2026 年已經相當成熟：

- **riscv-rt**：RISC-V 的啟動程式碼與中斷向量表
- **riscv-peripherals**：通用 RISC-V 核心周邊（CLINT、PLIC、計時器等）的抽象層
- **embedded-hal**：硬體抽象層（HAL），讓同一份驅動程式碼可以在不同 MCU 之間移植
- **riscv-pac**：基於 SVD 檔案的周邊存取層（Peripheral Access Crate）

最重要的是，`embedded-hal` 和 `embedded-hal-async` 已經成為 Rust 嵌入式生態的核心標準。無論是 SiFive 的 FE310 系列、Espressif 的 ESP32-C3 還是 Bouffalo Lab 的 BL808，晶片廠商只需要實作 `embedded-hal` 的 traits，Rust 開發者就能直接使用數百個現成的驅動程式庫。

## 為什麼 Rust 是 RISC-V 開發的理想語言

這個問題的答案可以歸結為三個關鍵字：**安全、零成本、現代工具鏈**。

### 記憶體安全——在沒有 MMU 的環境中至關重要

許多 RISC-V 微控制器沒有記憶體管理單元（MMU）。在這種環境中，C/C++ 常見的緩衝區溢位、釋放後使用（use-after-free）、雙重釋放（double-free）等錯誤會直接導致系統崩潰——甚至更糟，造成安全漏洞。

Rust 的所有權模型在編譯期就消除了這些錯誤。在沒有 MMU 的 bare-metal 環境中，Rust 的記憶體安全保證從「錦上添花」變成了「不可或缺」。

### 零成本抽象

RISC-V 嵌入式系統的資源極其有限——可能只有 16 KB 的快閃記憶體和 8 KB 的 SRAM。Rust 的「零成本抽象」原則確保你使用高階語法（迭代器、trait、閉包）時，不會產生執行期開銷。

編譯器會將這些抽象內聯展開，最終產生的機械碼與手寫組合語言幾乎無法區分。

### Cargo 與工具鏈

在嵌入式開發中，專案管理往往是噩夢——Makefile、連結腳本、交叉編譯器路徑……每一個環節都可能出錯。

Rust 的 `cargo` 配合 `.cargo/config.toml` 可以輕鬆管理交叉編譯設定：

```toml
[target.riscv32imac-unknown-none-elf]
runner = "probe-rs run --chip=CH32V307"
rustflags = ["-C", "link-arg=-Tmemory.x"]
```

加上 `probe-rs` 或 `openocd` 等除錯工具，Rust 開發者可以用 `cargo run` 一條指令完成編譯、燒錄、除錯的完整流程。

## 嵌入式 Rust 搭配 RISC-V 的實戰範例

讓我們來看一個最簡單的 RISC-V 嵌入式專案——在 FE310-G002（SiFive HiFive1 Rev B 開發板）上點亮 LED。

首先，建立一個 `no_std` 專案：

```console
$ cargo new blink --edition 2024
$ cd blink
```

在 `Cargo.toml` 中加入相依庫：

```toml
[dependencies]
riscv-rt = "0.12"
panic-halt = "0.2"
riscv = "0.12"
embedded-hal = "1.0"
```

最重要的檔案是 `src/main.rs`——RISC-V 嵌入式 Rust 的標準入口：

```rust
#![no_std]
#![no_main]

use panic_halt as _;
use riscv_rt::entry;

#[entry]
fn main() -> ! {
    let peripherals = unsafe { /* memory-mapped I/O */ };
    loop {
        // blink LED
    }
}
```

等等——上面的程式碼還沒有真正的硬體操作。讓我們改用 SiFive 的 PAC（周邊存取層）來實作實際的 LED 閃爍：

```rust
#![no_std]
#![no_main]

use panic_halt as _;
use riscv_rt::entry;
use sifive_fe310_g002::GPIO0;

#[entry]
fn main() -> ! {
    let gpio = unsafe { &*GPIO0::ptr() };

    // 設定 pin 13（LED）為輸出
    gpio.output_en.modify(|_, w| w.pin13().set_bit());
    gpio.port.modify(|_, w| w.pin13().clear_bit());

    loop {
        gpio.port.modify(|_, w| w.pin13().set_bit());
        delay(10000);
        gpio.port.modify(|_, w| w.pin13().clear_bit());
        delay(10000);
    }
}

fn delay(cycles: u32) {
    for _ in 0..cycles {
        unsafe { core::ptr::read_volatile(&0x1000_0000 as *const u32) }
    }
}
```

這個範例展示了 RISC-V 嵌入式 Rust 的幾個關鍵特性：

1. **PAC 層級操作**：透過 `sifive_fe310_g002` crate 直接操作記憶體映射暫存器
2. **型別安全**：`modify`、`set_bit`、`clear_bit` 等方法在編譯期檢查位元操作的正確性
3. **`#[entry]` 巨集**：由 `riscv-rt` 提供，自動設置堆疊指標、初始化 .bss/.data 段

在 C 語言中，相同的功能需要手動撰寫啟動程式碼（startup.s）、連結腳本（linker.ld），並仔細處理 volatile 關鍵字的位置。Rust 將這些繁瑣的細節封裝在經過社群驗證的 crate 中，開發者可以專注於實際的應用邏輯。

## SiFive 與 Intel：RISC-V 晶片的最新發展

2026 年的 RISC-V 處理器市場出現了兩個重量級玩家：SiFive 和 Intel。

### SiFive 的 RISC-V 產品線

SiFive 作為 RISC-V 的商業化先驅，在 2026 年推出了三條主要產品線：

- **Essential 系列**：針對嵌入式與 IoT 的 32/64 位元核心，P 系列主打高效能、E 系列主打低功耗
- **Performance 系列（P670/P870）**：支援亂序執行（out-of-order）、向量擴展（RVV 1.0），效能直逼 ARM Cortex-A7x 系列
- **Intelligence 系列（X280/X390）**：內建矩陣運算加速器，專門針對 AI 推論與邊緣 ML 工作負載

其中 X390 值得特別關注——它整合了 SiFive 與 Esperanto Technologies 共同開發的張量處理單元（TPU），能在 1W 以下的功耗範圍內提供 4 TOPS 的 INT8 推論效能。對於 Rust 開發者來說，這意味著可以在邊緣裝置上執行 Rust 撰寫的 ML 推論管線，完全在本地處理資料，不需要雲端連線。

### Intel 的 RISC-V 佈局

Intel 對 RISC-V 的態度在過去幾年中經歷了 180 度大轉彎——從最初的不屑一顧，到 2023 年加入 RISC-V International 並投入 10 億美元成立 RISC-V 研發基金。

2026 年，Intel 的 RISC-V 策略更加明確：

1. **Horse Creek 平台**：採用 SiFive P550 核心的開發平台，代號「Horse Creek」，內建 Intel 4 製程（7nm），目標是讓 RISC-V 在資料中心領域具備競爭力
2. **Agilex FPGA 整合**：Intel 的 Agilex 7/9 FPGA 系列現在支援 RISC-V 軟核心，可以在 FPGA 內部靈活配置 RISC-V 處理器
3. **IFS（Intel Foundry Services）**：Intel 代工服務現在接受 RISC-V 晶片的委託設計，並提供經過驗證的 RISC-V 核心 IP

值得注意的是，Intel 的 IFS 部門已經與多家 RISC-V 新創公司（包含 Ventana Micro Systems、Esperanto Technologies）簽訂了代工合約，這些晶片預計在 2027-2028 年量產。

### Rust 在這些晶片上的部署

對於 Rust 開發者而言，SiFive 和 Intel 的 RISC-V 晶片部署提供了完整的軟體支援：

- **SiFive 提供官方的 Rust PAC crate**：`sifive-fe310-g002`、`sifive-s71` 等
- **Intel 的 IFS 客戶可以透過 Tock OS 支援 Rust**：Tock 是一個專門為 RISC-V 設計的嵌入式作業系統，核心和驅動程式完全用 Rust 撰寫
- **Linux 核心中的 Rust 支援**：RISC-V 版本的 Linux 核心現在可以使用 Rust 撰寫核心模組，這在 2024 年 Linux 6.8 中正式啟用

## 開放硬體 + 開放軟體的未來

RISC-V 與 Rust 的結合不僅僅是技術上的巧合——它代表了一個更深層次的運動：**從封閉到開放**的全面轉變。

### 硬體開源化的三個層次

開放硬體運動可以分為三個層次：

1. **ISA 開放**：RISC-V 指令集規範採用 BSD 授權，任何人都可以實作而不需要付授權費
2. **核心開放**：SiFive、OpenHW Group、Ibex 等提供開源的 RTL（暫存器傳輸層級）實作
3. **工具鏈開放**：LLVM、GCC、QEMU、OpenOCD 等工具鏈全部開源

Rust 在這個生態中扮演的角色是「安全膠水」——它不僅填補了高階語言到硬體的鴻溝，還確保了這個橋樑的安全性。當你的程式碼最終被轉換為 RISC-V 機械碼並燒錄到晶片中時，Rust 的編譯期保證是你對程式正確性的最後一道防線。

### RISC-V + Rust 的殺手級應用場景

在 2026 年，以下幾個領域正在成為 RISC-V + Rust 的殺手級應用：

**物聯網安全**：Tock OS（用 Rust 撰寫）在 RISC-V 平台上提供基於核心的安全隔離。每個驅動程式在獨立的「膠囊」（capsule）中執行，即使某個驅動程式被攻陷，也不會影響整個系統。

**量子運算控制器**：澳洲的量子新創公司 Diraq 正在使用 Rust 搭配 RISC-V 微控制器來控制量子位元的讀寫時序——在奈秒級別的精確度下，任何記憶體錯誤都會導致量子態崩潰。

**太空電子系統**：歐洲太空總署（ESA）的 OBC 專案採用了 RISC-V（NG-ULTRA 計畫），並使用 Rust 撰寫關鍵的容錯飛行軟體。Rust 的安全性保證讓工程師能夠更有信心地處理太空輻射導致的單位元翻轉（Single Event Upset）。

**AI 邊緣推論**：如上所述，SiFive X390 與 Esperanto 的 TPU 搭配 Rust 的 ML 推論框架（如 `candle`、`burn`），讓邊緣裝置能夠在功耗預算內執行大型語言模型的推論。

### 展望 2030

如果從今天的趨勢推算，2030 年的運算世界可能是這樣的：

- **桌上型電腦**：ARM 與 x86 各據一方，RISC-V 開始出現在低功耗筆電中
- **伺服器**：AMD 和 Intel 主導，但 RISC-V 開始在特定工作負載（網路處理、儲存控制器）中佔有一席之地
- **嵌入式系統**：RISC-V 已經成為主流，與 ARM Cortex-M 系列分庭抗禮
- **AI 加速器**：RISC-V 向量擴展與矩陣擴展成為 AI 晶片的標準介面

而在這一切的底層，Rust 將編譯成這些 RISC-V 核心上運行的機械碼——安全、高效、可靠。

### 結語

「開放硬體時代的程式設計」聽起來像是一個遙遠的未來願景。但對於今天的 Rust 開發者而言，這個未來已經來臨。

你可以從一塊售價 20 美元的 RISC-V 開發板開始，用 `cargo` 建立一個專案，寫幾行程式碼，然後看著 LED 閃爍——這與 Arduino 入門體驗類似，但不同的是，你使用的是語言史上第一個在編譯期保證記憶體安全的系統程式語言。

RISC-V 給了我們開放硬體的承諾，Rust 給了我們安全軟體的工具。這兩者的結合，正在重新定義程式設計的邊界。

---

*本文作者為嵌入式系統工程師，專注於 RISC-V 架構與 Rust 嵌入式開發。*
