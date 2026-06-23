# RTOS 與 RTIC 框架（2020–2026）

## RTIC 優先權模型

RTIC（Real-Time Interrupt-driven Concurrency）是 Rust 專屬的即時框架。其核心模型基於中斷優先權：

```rust
#[rtic::app(device = pac)]
mod app {
    #[task(binds = TIM2, priority = 2)]
    fn task_a(_: task_a::Context) { ... }

    #[task(binds = USART1, priority = 1)]
    fn task_b(_: task_b::Context) { ... }
}
```

優先權數字越大，優先級越高。RTIC 在編譯期分析任務間的優先權關係，確保沒有死結。

## 資源管理

RTIC 區分兩類資源：

```rust
#[shared]
struct Shared {
    counter: u32,       // 多個任務共享，需 lock()
}

#[local]
struct Local {
    led: GPIOPin,       // 專屬資源，不需鎖
}

#[task(shared = [counter], priority = 2)]
fn incrementer(cx: incrementer::Context) {
    cx.shared.counter.lock(|c| *c += 1);
}
```

`lock()` 保證在高優先權任務執行期間，低優先權任務無法存取共享資源。

## 任務間通訊

RTIC 支援訊息傳遞機制：

```rust
#[task(capacity = 8)]
fn receiver(cx: receiver::Context, msg: u32) {
    // 每個訊息處理一次
}

fn sender() {
    receiver::spawn(42).ok();
}
```

`spawn()` 將訊息放入接收任務的訊息佇列，接收任務在適當的優先權排程中被喚醒。

## 編譯期排程分析

RTIC 最獨特的功能：所有排程決策在編譯期完成。它分析：

- 任務間的優先權關係
- 資源的使用衝突
- 中斷巢狀可能性

這意味著**零執行期排程開銷**——沒有 RTOS 的核心排程迴圈。

## 與傳統 RTOS 對比

| 特性 | FreeRTOS（C） | RTIC（Rust） |
|------|-------------|-------------|
| 排程開銷 | 每次任務切換 | 零（編譯期） |
| 記憶體安全 | 人工保證 | 編譯器保證 |
| 資源鎖 | Mutex/Semaphore | lock() 巨集 |
| 任務數量 | 執行期動態 | 編譯期靜態 |

## 延伸閱讀

- [RTIC 官方文件](https://www.google.com/search?q=RTIC+Rust+framework+documentation)
- [FreeRTOS vs RTIC](https://www.google.com/search?q=FreeRTOS+vs+RTIC+comparison)
- [嵌入式即時系統設計](https://www.google.com/search?q=embedded+real+time+system+design)
