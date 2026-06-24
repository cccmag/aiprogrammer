# RTIC 框架即時系統開發 — 優先權模型、資源管理、任務排程

## 從中斷到 RTOS

傳統嵌入式開發的流程：
1. 在中斷服務常式中處理時間敏感任務
2. 在主循環中處理背景任務
3. 手動管理共享資料的同步

這種方式在簡單的專案中可行，但隨著系統複雜度增加，中斷巢狀、資源競爭、優先權反轉等問題會讓除錯變得極度困難。

RTIC 的設計目標：在 Rust 型別系統的基礎上，提供一個**編譯期安全**的即時框架。

## 建立 RTIC 專案

```toml
[dependencies]
cortex-m = "0.7"
cortex-m-rt = "0.7"
rtic = "2.1"
```

## 核心架構

```rust
#[rtic::app(device = pac)]
mod app {
    use super::*;

    #[shared]
    struct Shared {
        counter: u32,
        sensor_data: f32,
    }

    #[local]
    struct Local {
        led: gpio::PB0<Output>,
        uart: Uart<USART1>,
    }

    #[init]
    fn init(cx: init::Context) -> (Shared, Local) { ... }

    #[idle]
    fn idle(_: idle::Context) -> ! {
        loop { continue; }
    }

    #[task(binds = TIM2, priority = 2, shared = [counter])]
    fn timer_handler(cx: timer_handler::Context) { ... }
}
```

## 優先權模型與排程

RTIC 不使用執行期排程器。任務的執行順序完全由靜態優先權決定：

- 較高優先權的任務可以搶佔較低優先權的任務
- 同優先權的任務按 FIFO 順序執行
- 優先權在編譯期指定，不能動態改變

```rust
#[task(binds = TIM2, priority = 3)]
fn high_priority(_: high_priority::Context) {
    // 這個任務會搶佔 priority 1 和 2 的任務
}

#[task(binds = USART1, priority = 1)]
fn low_priority(_: low_priority::Context) {
    // 可能被 priority 2 和 3 搶佔
}
```

## 資源管理：lock()

共享資源必須透過 `lock()` 存取：

```rust
#[task(shared = [counter], priority = 2)]
fn increment(cx: increment::Context) {
    cx.shared.counter.lock(|c| *c += 1);
}

#[task(shared = [counter], priority = 1)]
fn reader(cx: reader::Context) {
    let val = cx.shared.counter.lock(|c| *c);
    log!("Counter: {}", val);
}
```

`lock()` 的關鍵行為：當高優先權任務持有 lock 時，試圖獲取同一資源的低優先權任務不會執行（也不會被排程）。這保證了不會有死結。

## 任務間通訊

RTIC 支援排程式任務（非中斷綁定）：

```rust
#[task(capacity = 4, priority = 1)]
fn process(cx: process::Context, value: u32) {
    // 佇列處理
}

#[task(priority = 2)]
fn producer(cx: producer::Context) {
    process::spawn(42).ok();
}
```

`spawn()` 是非阻塞的。如果佇列已滿，回傳 `Err(Full)`。

## 編譯期安全保證

RTIC 在編譯期驗證：

1. **無資料競爭**：所有共享資源都必須 `lock()`
2. **無死結**：lock 巢狀的順序在編譯期固定
3. **無優先權反轉**：lock 持有時間由編譯器分析
4. **堆疊使用量**：可靜態計算最大堆疊深度

## 與 embassy 的整合

RTIC 2.x 支援與 embassy 的 async 執行器整合：

```rust
#[task(priority = 2)]
async fn async_task(_: async_task::Context) {
    let val = read_sensor().await;
    shared_data.lock(|d| d.sensor = val).await;
}
```

## 延伸閱讀

- [RTIC 官方文件](https://www.google.com/search?q=RTIC+Rust+framework+tutorial)
- [RTIC 內部設計](https://www.google.com/search?q=RTIC+internals+architecture)
- [嵌入式即時排程演算法](https://www.google.com/search?q=embedded+real+time+scheduling+algorithms)
