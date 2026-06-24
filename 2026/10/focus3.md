# 主題三：平台驅動程式與裝置樹

## platform_driver 與 Device Tree

### 平台裝置模型

平台驅動程式（Platform Driver）是 Linux 核心中用於處理非列舉型匯流排（如 SoC 內部週邊）的驅動模型。過去這些裝置由 BSP（Board Support Package）程式碼手動註冊，現在主要由 Device Tree 描述。

### Rust 的 platform_driver 抽象

Rust for Linux 的 `PlatformDriver` trait 封裝了核心的 `platform_driver`：

```rust
use kernel::platform::PlatformDriver;

struct MyPlatformDev {
    mmio: IoMemory,
    irq: u32,
}

impl PlatformDriver for MyPlatformDev {
    fn probe(dev: &mut platform::Device) -> Result<Self> {
        // 從 Device Tree 獲取資源
        let mmio = dev.get_iomem(0, "reg")?;    // 暫存器空間
        let irq = dev.get_irq(0)?;               // 中斷號

        pr_info!("platform device: irq={}, mmio={:#x}\n", irq, mmio.start());
        Ok(Self { mmio, irq })
    }

    fn remove(dev: &mut Self) -> Result<()> {
        pr_info!("platform device removed\n");
        Ok(())
    }
}
```

### Device Tree 匹配

裝置驅動需要宣告它支援哪些 Device Tree 兼容字串：

```rust
kernel::platform_device_table! {
    MyPlatformDev,
    compatible: "vendor,mydevice-v1", "vendor,mydevice-v2",
}
```

相對應的 Device Tree 節點：

```dts
mydevice@f0000000 {
    compatible = "vendor,mydevice-v1";
    reg = <0x0 0xf0000000 0x0 0x1000>;
    interrupts = <0 42 4>;
};
```

### 電源管理整合

平台驅動程式通常需要處理電源管理。Rust 為此提供了 `SystemSleep` trait：

```rust
impl SystemSleep for MyPlatformDev {
    fn suspend(&mut self) -> Result<()> {
        pr_info!("suspending device\n");
        self.mmio.write(0x00, 0x1);  // 設定睡眠模式
        Ok(())
    }

    fn resume(&mut self) -> Result<()> {
        pr_info!("resuming device\n");
        self.mmio.write(0x00, 0x0);  // 恢復正常模式
        Ok(())
    }
}
```

### SoC 內建週邊範例

一個典型的 SoC 內建 GPIO 控制器平台驅動程式：

```rust
impl PlatformDriver for GpioController {
    fn probe(dev: &mut platform::Device) -> Result<Self> {
        let mmio = dev.get_iomem(0, "gpio")?;
        let irq = dev.get_irq(0)?;

        // 初始化硬體
        mmio.write(GPIO_OE, 0x0000_0000);  // 所有腳位設為輸入
        mmio.write(GPIO_IRQ_EN, 0x0000_0000);

        Ok(Self { mmio, irq, /* ... */ })
    }
}
```

### 中斷處理

平台驅動的中斷處理使用 `irq::Handler`：

```rust
fn handle_irq(dev: &MyPlatformDev) -> Result<irq::IRQReturn> {
    let status = dev.mmio.read(IRQ_STATUS);
    if status != 0 {
        dev.mmio.write(IRQ_CLEAR, status);
        // 處理中斷事件
        Ok(irq::IRQReturn::Handled)
    } else {
        Ok(irq::IRQReturn::None)
    }
}
```

---

**下一步**: [PCI 與 USB 驅動程式](focus4.md)

## 延伸閱讀

- [Linux Device Tree 文件](https://www.google.com/search?q=Linux+Device+Tree+documentation)
- [Platform Driver Rust API](https://www.google.com/search?q=Rust+for+Linux+platform+driver)
