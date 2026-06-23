# mini-kmod：Linux 驅動程式模式模擬

## 概述

mini-kmod 是一個使用者空間的驅動程式模式展示專案。由於真正的 Linux 核心模組需要核心原始碼與專用工具鏈，我們用 Rust 的使用者空間程式模擬了核心驅動程式的核心模式：

1. **模組生命週期** — `init_module()` / `cleanup_module()`
2. **字元設備操作** — open / close / read / write / ioctl
3. **MMIO 暫存器模型** — 記憶體映射 I/O 的讀寫模擬
4. **中斷處理** — 硬體中斷觸發的暫存器更新
5. **平台裝置模型** — 裝置名稱、IRQ、MMIO 位址

## 核心概念

### 1. 模組初始化和卸載

核心模組的兩個關鍵函式用 Rust 的普通函式模擬：

```rust
fn init_module() -> MiniDriver {
    let driver = MiniDriver::new("mini-kmod", 42, 0xf000_0000, 64);
    MODULE_LOADED.store(true, Ordering::SeqCst);
    driver
}

fn cleanup_module(_driver: &MiniDriver) {
    MODULE_LOADED.store(false, Ordering::SeqCst);
}
```

在真正的 Linux 核心中，這是透過 `module_init()` / `module_exit()` 巨集註冊的。

### 2. MMIO 暫存器模型

核心驅動程式透過 MMIO（Memory-Mapped I/O）與硬體溝通。模擬中使用 `Mutex<Vec<u8>>` 作為暫存器陣列：

```rust
fn read_reg(&self, offset: usize) -> u8 {
    assert!(offset < self.mmio_size, "MMIO offset out of bounds");
    let data = self.device_data.lock().unwrap();
    data[offset]
}

fn write_reg(&self, offset: usize, value: u8) {
    let mut data = self.device_data.lock().unwrap();
    data[offset] = value;
}
```

在真實驅動程式中，這對應到 `ioremap()` 後的 `readl()` / `writel()`。

### 3. file_operations 字元設備

字元設備是 Linux 中最簡單的驅動程式類型。模擬中透過 `open_count` 追蹤設備開啟次數：

| 操作 | 模擬方式 | 真實核心對應 |
|------|---------|------------|
| open | 增加計數 | `struct file_operations.open` |
| close | 減少計數 | `struct file_operations.release` |
| read | 複製內部資料 | `struct file_operations.read` |
| write | 寫入內部資料 | `struct file_operations.write` |
| ioctl | 命令分派 | `struct file_operations.unlocked_ioctl` |

### 4. ioctl 命令分派

核心驅動程式透過 ioctl 提供自訂控制介面：

```rust
fn ioctl(&self, cmd: u32, arg: usize) -> io::Result<usize> {
    match cmd {
        0 => { /* GET_INFO */ Ok(self.irq as usize) }
        1 => { /* RESET */ self.device_data.lock().unwrap().fill(0); Ok(0) }
        _ => Err(...)
    }
}
```

### 5. 中斷處理模擬

硬體中斷觸發驅動程式讀取暫存器來得知發生了什麼事：

```rust
fn simulate_hardware_interrupt(driver: &MiniDriver) {
    for i in 0..4 {
        let val = (i as u8) << 4 | i as u8;
        driver.write_reg(i, val);
    }
}
```

在真實核心中，中斷處理程式在 IRQ 發生時被核心呼叫，不能在任意上下文執行任意操作。

### 6. 確保模組只載入一次

`AtomicBool` 模擬核心模組的載入狀態：

```rust
static MODULE_LOADED: AtomicBool = AtomicBool::new(false);
```

## 測試

專案包含 8 個測試，覆蓋所有核心功能：

```
running 8 tests
test tests::test_register_out_of_bounds ... ok
test tests::test_module_init_exit ... ok
test tests::test_ioctl ... ok
test tests::test_file_operations ... ok
test tests::test_hardware_interrupt ... ok
test tests::test_mmio_register ... ok
test tests::test_read_write ... ok
test tests::test_register_out_of_bounds_panics ... ok
test result: ok. 8 passed; 0 failed
```

## 執行結果

```
=== mini-kmod: Linux Driver Patterns Demo ===

[init] mini-kmod: loading
[init] registered device: mini-kmod (irq=42, mmio=0xf0000000)

--- IRQ 42: hardware interrupt ---
  [MMIO]  write 0x00 -> reg[0xf0000000]
  [MMIO]  write 0x11 -> reg[0xf0000001]
  [MMIO]  write 0x22 -> reg[0xf0000002]
  [MMIO]  write 0x33 -> reg[0xf0000003]
--- interrupt handler done ---

--- file operations ---
  [open]  mini-kmod (count: 1)
  [read]  8 bytes from mini-kmod
  read buf: [11, 22, 33, 00, 00, 00, 00, 00]
  [write] 8 bytes to mini-kmod
  [read]  8 bytes from mini-kmod
  read buf: [68, 65, 6c, 6c, 6f, 00, 00, 00] ('hello')
  [ioctl] GET_INFO: irq=42, mmio=0xf0000000
  [ioctl] RESET: device reset
  [close] mini-kmod (count: 0)

--- platform device model ---
  device:    mini-kmod
  irq:       42
  mmio_base: 0xf0000000
  mmio_size: 64
  reg[0]:    0x00
[exit] mini-kmod: unloading
[exit] device unregistered

=== demo completed ===
```

## mini-kmod 教會我們的事

### 1. 驅動程式的本質是抽象

無論是 MMIO、中斷還是 DMA，驅動程式的工作是將硬體的複雜性抽象成整齊的檔案操作介面。

### 2. Rust 的所有權在驅動程式中發光

核心環境中，併發存取是規則而不是例外。`Mutex<T>` 和 `AtomicBool` 在編譯期保證了資料競爭不會發生。

### 3. iremap 與 MMIO

核心驅動程式無法直接存取實體位址。需要先透過 `ioremap()` 將實體位址映射到核心虛擬位址空間，然後才能安全地讀寫暫存器。

### 4. 模擬 vs 真實

mini-kmod 展示了驅動程式的**模式**而不是其實作。真實核心模組需要：
- Linux 核心原始碼樹的 headers
- 使用 `kernel` crate 中的核心 API 綁定
- 透過 `cargo-xbuild` 或核心專用 Makefile 編譯

---

## 延伸閱讀

- [完整程式碼](_code/src/main.rs)
- [Linux 核心模組程式設計指南](https://www.google.com/search?q=Linux+kernel+module+programming+guide)
- [Rust for Linux 專案官方文件](https://www.google.com/search?q=Rust+for+Linux+kernel+documentation)
- [Linux 裝置驅動程式（第三版）](https://www.google.com/search?q=Linux+device+drivers+third+edition)
