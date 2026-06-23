# 本期焦點

## 用 Rust 寫嵌入式系統程式 — 從暫存器到 RTOS

### 引言

嵌入式系統無所不在：從智慧手錶、感測器節點到工業控制器、汽車 ECU。過去二十年，C 語言是這個領域的霸主。但 Rust 的出現正在改變這一切。

Rust 的 `no_std` 能力讓它可以在沒有作業系統的裸機環境中運行，而所有權模型則從根本上解決了嵌入式開發中最頭痛的記憶體安全和資料競爭問題。更重要的是——Rust 在編譯期就能保證這些安全屬性，不需要垃圾回收或執行期開銷。

本期將帶領你從零開始探索 Rust 嵌入式開發。我們從最底層的暫存器操作開始，逐步建構出 GPIO、UART、中斷處理、RTOS 整合等完整的嵌入式開發知識體系。

---

## 大綱

* [程式：實作 mini-embedded — 從 GPIO 到 RTOS 模式](focus_code.md)
   - 記憶體映射暫存器抽象
   - GPIO 引腳控制
   - UART 輪詢與中斷模式
   - 軟體定時器與 RTOS 任務

1. [no_std 與嵌入式 Rust 基礎（2017-2026）](focus1.md)
   - 核心程式庫 vs 標準程式庫
   - panic_handler 與 allocator
   - 嵌入式目標 triple

2. [GPIO 與中斷控制（2018-2026）](focus2.md)
   - 暫存器層級 GPIO 操作
   - embedded-hal 抽象層
   - 外部中斷與 NVIC

3. [通訊協定：UART、SPI、I2C（2018-2026）](focus3.md)
   - 輪詢 vs 中斷 vs DMA
   - embedded-hal 的 blocking 與 async  trait
   - 常見感測器驅動模式

4. [定時器、PWM 與 ADC（2019-2026）](focus4.md)
   - SysTick 與通用定時器
   - PWM 輸出與舵機控制
   - ADC 取樣與 DMA

5. [RTOS 與 RTIC 框架（2020-2026）](focus5.md)
   - RTIC 的優先權模型
   - 資源管理與鎖定
   - 任務間通訊

6. [低功耗與記憶體最佳化（2019-2026）](focus6.md)
   - 睡眠模式與喚醒源
   - 堆疊使用分析
   - 編譯期最佳化技巧

7. [AI 輔助嵌入式開發（2024-2026）](focus7.md)
   - 用 LLM 生成暫存器定義
   - 自動化 HAL 綁定
   - 嵌入式測試與模擬

---

## 嵌入式軟體層次

```
應用層 (控制邏輯、感測器融合)
      │
驅動層 (embedded-hal 實作)
      │
HAL 抽象層 (embedded-hal traits)
      │
PAC 層 (外設存取 crate)
      │
硬體層 (MCU 暫存器、中斷)
```

## 濃縮回顧

### Rust 嵌入式生態的里程碑

- **2017**：embedded-hal 專案啟動，定義硬體抽象層 trait
- **2018**：cortex-m-rt 發布，提供 Cortex-M 啟動程式碼
- **2019**：embedded-hal v1.0 推出，生態開始成熟
- **2020**：RTIC v1.0 即時框架發布
- **2021**：Rust 編譯器正式支援 Cortex-M 後端
- **2023**：async embedded-hal 加入，支援非同步外設操作
- **2026**：Rust 已成為嵌入式領域的主流選擇之一

### 為什麼嵌入式開發者擁抱 Rust？

嵌入式開發有別於一般軟體開發的獨特挑戰：

| 挑戰 | C 的作法 | Rust 的優勢 |
|------|---------|-----------|
| 記憶體有限 | 人工追蹤分配 | 編譯期檢查 + 靜態配置 |
| 併發中斷 | 容易資料競爭 | Send/Sync 編譯期保證 |
| 暫存器操作 | 易讀錯 datasheet | 型別安全 PAC crate |
| 可攜性 | #ifdef 地獄 | trait 多型，零成本 |
| 部署安全 | 執行期崩潰 | 編譯期保證，無 panic |

### no_std：沒有標準庫的世界

嵌入式 Rust 的核心是 `#![no_std]`，它移除了標準庫的作業系統依賴：

```rust
#![no_std]
#![no_main]

use core::panic::PanicInfo;

#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
    loop {}
}
```

關鍵差異：
- 沒有 `Vec`、`String`、`HashMap`——改用固定大小陣列或 `heapless` crate
- 沒有堆積分配器——除非自行實作 `GlobalAlloc`
- 沒有 `std::io`、`std::thread`——直接操作硬體暫存器

### embedded-hal 抽象層

embedded-hal 是 Rust 嵌入式生態的核心抽象，定義了一組硬體周邊的 trait：

```rust
pub trait OutputPin {
    fn set_high(&mut self) -> Result<(), Self::Error>;
    fn set_low(&mut self) -> Result<(), Self::Error>;
}

pub trait SerialRead<Word> {
    fn read(&mut self) -> Result<Word, nb::Error<Self::Error>>;
}
```

這種設計讓應用程式碼可以跨 MCU 平台移植——更換 MCU 只需更換 HAL 實作，應用程式不用改。

### PAC、HAL 與 BSP 三層架構

Rust 嵌入式生態將驅動程式分為三個層級：

1. **PAC**（Peripheral Access Crate）：從 SVD 檔案自動生成的暫存器定義
2. **HAL**：基於 PAC 實作 embedded-hal trait，提供高階 API
3. **BSP**（Board Support Package）：針對特定開發板的整合層

```
範例：stm32f4xx-hal
PAC:  svd2rust 產生 stm32f4 crate
HAL:  實作 embedded-hal 的 SPI, I2C, GPIO
BSP:  stm32f4-discovery 預設 pin mapping
```

### RTIC 的優先權模型

RTIC（Real-Time Interrupt-driven Concurrency）是 Rust 嵌入式專用的 RTOS 框架：

```rust
#[rtic::app(device = pac)]
mod app {
    #[shared]
    struct Shared {
        counter: u32,
    }

    #[local]
    struct Local {
        led: gpio::PB0<Output>,
    }

    #[task(binds = TIM2, priority = 2, shared = [counter])]
    fn timer_handler(cx: timer_handler::Context) {
        cx.shared.counter.lock(|c| *c += 1);
    }

    #[idle]
    fn idle(_: idle::Context) -> ! {
        loop { continue; }
    }
}
```

RTIC 的關鍵設計：
- 編譯期優先權分析，無執行期排程開銷
- `lock()` 確保資源的互斥存取
- 零成本抽象——所有排程決策在編譯期完成

---

**下一步**：[程式實作](focus_code.md) → [no_std 與嵌入式 Rust 基礎](focus1.md)

## 延伸閱讀

- [The Embedded Rust Book](https://www.google.com/search?q=embedded+Rust+book)
- [embedded-hal 官方文件](https://www.google.com/search?q=embedded-hal+Rust)
- [RTIC 框架](https://www.google.com/search?q=RTIC+Rust+embedded)
- [Rust on ESP32](https://www.google.com/search?q=Rust+ESP32+embedded)
