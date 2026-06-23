# no_std 與嵌入式 Rust 基礎（2017–2026）

## core vs std

嵌入式 Rust 的核心差異在於 `#![no_std]`。移除標準庫後，可用 API 僅限於 `core` crate：

| 可用於 no_std | 不可用於 no_std |
|--------------|----------------|
| 基本型別、迭代器、closure | `Vec`、`String`、`HashMap` |
| 模式匹配、trait 系統 | `std::thread`、`std::sync` |
| `core::cell`（RefCell、Cell） | `Box`、`Rc`、`Arc`（無 alloc） |
| panic/assert 巨集 | 檔案系統、網路 socket |

## panic_handler

沒有標準庫就沒有預設的 panic 行為。必須自訂：

```rust
#![no_std]
#![no_main]

#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
    // 可以點亮 LED 或輸出錯誤訊息
    loop {}
}
```

實務上常使用 `panic-halt` 或 `panic-semihosting` 等 crate。

## 嵌入式目標 triple

Rust 支援數十種嵌入式目標：

| 目標 triple | 說明 |
|------------|------|
| `thumbv7em-none-eabihf` | Cortex-M4F/M7（含 FPU） |
| `thumbv6m-none-eabi` | Cortex-M0/M0+（無 FPU） |
| `riscv32imac-unknown-none-elf` | RISC-V 32-bit |
| `aarch64-unknown-none` | Cortex-A 系列裸機 |

## allocator 與 heapless

若需要動態分配，可引入 `alloc` crate 並實作 `GlobalAlloc`。但在嵌入式環境中更常使用固定大小的替代方案：

- **heapless**：提供 `Vec`、`String`、`LinearMap` 的固定容量版本
- **fixed**：編譯期大小決定的佇列和緩衝區

## 關鍵里程碑

- **2017**：embedded 工作小組成立，定義 no_std 生態基礎
- **2019**：cortex-m crate 成熟，提供安全暫存器存取
- **2021**：Rust 編譯器正式支援 Cortex-M 後端
- **2024**：RISC-V 嵌入目標達到 Tier 2 支援

## 延伸閱讀

- [The Embedded Rust Book](https://www.google.com/search?q=embedded+Rust+book+no_std)
- [Rust 嵌入式目標列表](https://www.google.com/search?q=Rust+embedded+target+triple)
- [heapless crate](https://www.google.com/search?q=heapless+Rust+crate)
