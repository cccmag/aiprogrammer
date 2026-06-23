# 低功耗與記憶體最佳化（2019–2026）

## MCU 睡眠模式

ARM Cortex-M 提供多種睡眠模式，功耗遞減但喚醒延遲遞增：

| 模式 | 功耗 | 喚醒源 | 喚醒時間 |
|------|------|--------|---------|
| Sleep | ~mA | 任何中斷 | 數 ns |
| Deep Sleep | ~µA | 特定周邊 | µs 級 |
| Standby | ~nA | RTC、外部中斷 | ms 級 |
| Shutdown | ~nA | Reset、特定引腳 | ms 級 |

## 從 Rust 控制睡眠模式

```rust
use cortex_m::asm;

// 淺睡眠（Sleep-On-Exit 模式）
asm::wfi();  // Wait For Interrupt

// 深睡眠（需配置 SCB）
SCB::sysreset_req();  // 軟體重啟
```

## 喚醒源配置

典型的電池供電感測器節點工作流程：

```rust
loop {
    asm::wfi();                    // 睡眠等待中斷
    if rtc::is_alarm() {           // RTC 喚醒
        sensor.measure();          // 測量
        radio.send();              // 傳送
        rtc.set_alarm(60_sec);     // 設定下次喚醒
    } else if exti::is_pending() { // 外部中斷喚醒
        process_event();
    }
}
```

## 堆疊使用量分析

嵌入式環境中堆疊溢位是災難性的。Rust 提供分析工具：

```bash
# 在 Cargo.toml 中設定堆疊大小
cargo rustc -- -C link-arg=-Tmemory.x

# 使用 stack-sizes 工具分析
cargo install cargo-call-stack
cargo call-stack
```

`cargo-call-stack` 會靜態分析所有可能的呼叫路徑，計算最大堆疊使用量。

## 編譯期最佳化

```toml
[profile.release]
opt-level = "s"        # 最佳化體積
lto = "fat"            # 連結時最佳化
codegen-units = 1      # 禁用並行 codegen（更多最佳化機會）
debug-assertions = false
```

設定 `opt-level = "z"` 可進一步縮小二進位體積，適合 Flash 有限的 MCU。

## 延伸閱讀

- [ARM Cortex-M 低功耗模式](https://www.google.com/search?q=ARM+Cortex-M+low+power+modes)
- [Rust cargo-call-stack](https://www.google.com/search?q=cargo-call-stack+Rust)
- [嵌入式 Rust 最佳化指南](https://www.google.com/search?q=embedded+Rust+optimization+guide)
