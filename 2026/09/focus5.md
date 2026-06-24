# 即時作業系統

## RTIC、Tock OS、FreeRTOS 整合（2019-2026）

### 前言

即時系統（Real-Time Systems）是嵌入式系統中最嚴格的分類——任務必須在指定的時間限制內完成。延遲可能導致災難性後果：安全氣囊應在碰撞後 10ms 內點火，煞車控制器必須在 1ms 內回應。

Rust 的型別系統和所有權模型為即時系統帶來了獨特的優勢：**在編譯期檢查任務的資源競爭和優先級反轉**。

### RTIC：即時中斷驅動並行

RTIC（Real-Time Interrupt-driven Concurrency）是 Rust 生態中最成熟的即時框架：

```rust
use rtic::app;

#[app(device = stm32f4xx_hal::pac)]
const APP: () = {
    // 共用資源
    struct Resources {
        #[lock_free]
        led: Led,
        #[lock_free]
        counter: u32,
    }
    
    // 初始化
    #[init]
    fn init(cx: init::Context) -> init::LateResources {
        // ... 初始化硬體
        init::LateResources {
            led: Led::new(),
            counter: 0,
        }
    }
    
    // 高優先級任務（由定時器觸發）
    #[task(binds = TIM2, priority = 2, resources = [counter])]
    fn timer_tick(cx: timer_tick::Context) {
        *cx.resources.counter += 1;  // 無鎖存取！
    }
    
    // 低優先級任務
    #[task(binds = USART1, priority = 1, resources = [led, counter])]
    fn uart_handler(cx: uart_handler::Context) {
        if *cx.resources.counter > 100 {
            cx.resources.led.toggle();
        }
    }
    
    // 空閒任務
    #[idle]
    fn idle(_cx: idle::Context) -> ! {
        loop {
            cortex_m::asm::wfi();  // 等待中斷
        }
    }
};
```

**RTIC 的關鍵特性**：

1. **靜態優先級**：任務的優先級在編譯時確定，執行時期無法更改
2. **無鎖資源共享**：RTIC 利用中斷優先級來保證資源訪問的安全性——不需要 Mutex
3. **編譯時排程分析**：RTIC v3 可以在編譯時檢測優先級反轉和死鎖
4. **零成本抽象**：RTIC 的開銷接近手寫中斷處理程式

**優先級系統**：

```
高優先級
  ┊
TIM2（priority=2）── 可以搶佔 USART1
  ┊
USART1（priority=1）── 可以被 TIM2 搶佔
  ┊
idle（priority=0）── 最低優先級
```

### Tock OS：安全嵌入式作業系統

Tock OS 是一個用 Rust 寫的安全嵌入式 OS，專為資源受限的 MCU 設計：

```
┌──────────────────────────────────┐
│           應用程式層              │
│  (用 Rust 或 C 撰寫，彼此隔離)    │
├──────────────────────────────────┤
│           核心層                  │
│   ┌────────┐ ┌─────────────────┐│
│   │ 排程器  │ │  驅動程式框架    ││
│   └────────┘ └─────────────────┘│
├──────────────────────────────────┤
│           晶片支援層              │
│   ┌────────────────────────────┐ │
│   │   Cortex-M / RISC-V HAL    │ │
│   └────────────────────────────┘ │
└──────────────────────────────────┘
```

**Tock OS 的創新**：

1. **基於 Rust 型別系統的權限模型**：
```rust
// 應用程式必須明確請求權限
impl SyscallDriver for TemperatureSensor {
    fn command(&self, cmd_num: u32, arg1: u32, _: u32, process: &Process) -> CommandResult {
        match cmd_num {
            0 => {
                // 檢查應用程式是否有溫度感測器權限
                if !process.has_permission(KernelPermission::Temperature) {
                    return CommandResult::failure(ErrorCode::NoPermission);
                }
                // ...讀取溫度
            }
            // ...
        }
    }
}
```

2. **應用程式的記憶體隔離**：
```rust
// 每個應用程式在自己的位址空間中運行
// 核心使用 MPU（Memory Protection Unit）隔離應用程式
pub struct Process {
    memory: MemoryRegion,      // 應用程式的記憶體區域
    permissions: PermissionSet, // 允許的核心呼叫
    state: ProcessState,       // 執行狀態
}
```

3. **核心完全用 Rust 撰寫**：保證核心本身沒有記憶體安全漏洞

### FreeRTOS 與 Rust

FreeRTOS 是嵌入式世界最流行的 RTOS。Rust 社群提供了 FreeRTOS 的 Rust 綁定：

```rust
use freertos_rust::*;

fn main() {
    // 建立任務
    let task1 = Task::new()
        .name("task1")
        .stack_size(256)
        .priority(1)
        .start(|| {
            loop {
                println!("Task 1 running");
                FreeRtosUtils::delay_ms(1000);
            }
        })
        .unwrap();
    
    // 建立佇列
    let queue = Queue::new(10).unwrap();
    
    // 建立第二個任務
    let task2 = Task::new()
        .name("task2")
        .stack_size(256)
        .priority(1)
        .start(move || {
            loop {
                queue.send(42, 100).unwrap();
                FreeRtosUtils::delay_ms(500);
            }
        })
        .unwrap();
    
    // 啟動排程器
    FreeRtosUtils::start_scheduler();
}
```

### 三種即時方案的比較

| 特性 | RTIC | Tock OS | FreeRTOS+Rust |
|------|------|---------|---------------|
| 架構 | 框架 | 完整 OS | RTOS + 綁定 |
| 語言 | 純 Rust | 純 Rust | C + Rust 綁定 |
| 排程器 | 中斷驅動 | 協同式 + 搶佔 | 搶佔式 |
| 記憶體保護 | ❌ | ✅ (MPU) | ❌ |
| 編譯時分析 | ✅ 優先級/資源 | 🟡 權限 | ❌ |
| 硬體需求 | 低 (1KB RAM) | 中 (16KB RAM) | 低 (1KB RAM) |
| 最佳場景 | 簡單即時控制 | 安全多應用 | 複雜多任務 |

### Rust 在即時系統中的優勢

**1. 無 GC 暫停**：
```
C 語言：無暫停（但需要人工保證記憶體安全）
Java：GC 暫停（無法用於硬即時系統）
Rust：無暫停 + 編譯器保證記憶體安全 ✅
```

**2. 靜態分配**：
```rust
// Rust 鼓勵靜態分配（在即時系統中至關重要）
// 靜態陣列：分配在棧上或 .bss 段
static mut BUFFER: [u8; 1024] = [0; 1024];

// 而非堆分配（可能導致不可預測的延遲）
let buf = vec![0u8; 1024];  // 避免在即時任務中使用
```

**3. 零成本中斷處理**：
```rust
// RTIC：中斷處理直接對應硬體中斷向量
// 沒有額外的函式呼叫開銷
#[task(binds = TIM2, priority = 2)]
fn timer_handler(_: timer_handler::Context) {
    // 這段程式碼直接在中斷上下文中執行
    // 效能 = 手寫 C 中斷處理程式碼
}
```

### 即時系統的未來

1. **RTIC 主導市場**：RTIC 的靜態分析能力使其成為安全關鍵系統的首選
2. **Tock OS 的權限模型影響其他 OS**：基於型別的權限檢查正在被其他嵌入式 OS 借鑑
3. **Rust 標準化即時抽象**：embedded-hal 正在擴展即時支援
4. **AI 輔助排程分析**：AI 可以幫助分析任務的 WCET（最差情況執行時間）

### 小結

即時系統是 Rust 系統程式設計的「殺手級應用」。C 在即時領域統治了 40 年，直到 Rust 出現——Rust 在提供等同 C 的效能和控制的同時，新增了編譯器保證的記憶體安全和型別安全的資源管理。

**Rust 讓即時程式設計不再需要在「效能」和「安全性」之間做選擇**。

---

**下一步**：[作業系統核心](focus6.md)

## 延伸閱讀

- [RTIC 官方文件](https://www.google.com/search?q=RTIC+Rust+documentation)
- [Tock OS 書籍](https://www.google.com/search?q=Tock+OS+Rust+book)
- [FreeRTOS Rust 綁定](https://www.google.com/search?q=FreeRTOS+Rust+bindings)
