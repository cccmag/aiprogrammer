# 主題四：PCI 與 USB 驅動程式

## PCI BAR、DMA 與 USB 驅動

### PCI 驅動程式模型

PCI 驅動程式是 Linux 中最常見的匯流排驅動類型，從網路卡到 GPU 都使用 PCI 介面。Rust for Linux 提供 `PciDriver` trait 簡化開發：

```rust
use kernel::pci::PciDriver;

struct MyPciDev {
    pci_dev: PciDevice,
    bar0: IoMemory,
    irq: u32,
}

impl PciDriver for MyPciDev {
    fn probe(dev: &mut PciDevice) -> Result<Self> {
        // 啟用 PCI 裝置
        dev.enable_device()?;
        dev.set_master()?;

        // 映射 BAR0 空間
        let bar0 = dev.get_iomem(0)?;

        // 獲取中斷
        let irq = dev.get_irq()?;

        Ok(Self { pci_dev: dev.clone(), bar0, irq })
    }

    fn remove(dev: &mut Self) -> Result<()> {
        dev.pci_dev.disable_device();
        Ok(())
    }
}
```

### PCI 裝置 ID 表

驅動程式需要宣告它支援哪些 PCI 裝置：

```rust
kernel::pci_device_table! {
    MyPciDev,
    { vendor: 0x10ec, device: 0x8168, subvendor: ANY, subdevice: ANY },
    { vendor: 0x8086, device: 0x153b, subvendor: ANY, subdevice: ANY },
}
```

### BAR 空間與 MMIO

PCI 裝置透過 Base Address Register（BAR）對外曝露暫存器空間：

```rust
fn read_config(pci_dev: &PciDevice) -> Result<()> {
    // 讀取 PCI 配置空間
    let vendor = pci_dev.config_read(0x00)?;          // Vendor ID
    let device = pci_dev.config_read(0x02)?;          // Device ID
    let bar0_raw = pci_dev.config_read(0x10)?;        // BAR0 位址

    // 透過 MMIO 操作裝置暫存器
    let reg_val = dev.bar0.readl(REG_STATUS);
    dev.bar0.writel(REG_COMMAND, CMD_START);
}
```

### DMA 操作

DMA（Direct Memory Access）讓裝置直接讀寫系統記憶體。Rust 為此提供了安全的 DMA 抽象：

```rust
use kernel::dma;

fn setup_dma(dev: &MyPciDev, size: usize) -> Result<DmaBuf> {
    // 分配 DMA 緩衝區
    let dma_buf = dma::alloc_coherent::<MyPciDev>(
        &dev.pci_dev, size, GFP_KERNEL
    )?;

    // 取得 DMA 位址（給硬體使用）
    let dma_addr = dma_buf.dma_address();

    // 取得 CPU 虛擬位址
    let cpu_addr = dma_buf.cpu_address();

    Ok(dma_buf)
}

fn start_dma_transfer(dev: &MyPciDev, buf: &DmaBuf, dir: dma::Direction) -> Result<()> {
    // 將 DMA 緩衝區映射到裝置
    let sg = dma::map_single(&dev.pci_dev, buf, dir)?;

    // 通知硬體開始傳輸
    dev.bar0.writel(DMA_ADDR_HI, (sg.dma_address() >> 32) as u32);
    dev.bar0.writel(DMA_ADDR_LO, sg.dma_address() as u32);
    dev.bar0.writel(DMA_SIZE, buf.size() as u32);
    dev.bar0.writel(DMA_START, 0x1);
}
```

### USB 驅動程式

USB 驅動使用類似的 `UsbDriver` trait：

```rust
use kernel::usb::UsbDriver;

impl UsbDriver for MyUsbDev {
    fn probe(dev: &mut UsbDevice) -> Result<Self> {
        let interface = dev.interface_number();
        let endpoints = dev.endpoints();

        // 註冊中斷端點
        let urb = UsbEndpoint::new_interrupt(
            endpoints[0], 64, handle_urb
        )?;

        Ok(Self { dev: dev.clone(), urb })
    }
}
```

USB 裝置 ID 表的宣告方式類似 PCI：

```rust
kernel::usb_device_table! {
    MyUsbDev,
    { vendor: 0x1234, product: 0x5678 },
}
```

### DMA 的安全保證

Rust 的 DMA 抽象解決了 C 語言中常見的問題：
- **生命週期管理**：`DmaBuf` 離開作用域時自動解除映射
- **方向檢查**：編譯器確保讀寫方向與 DMA 操作匹配
- **快取一致性**：coherent/streaming 映射在型別層面區分

---

**下一步**: [網路驅動程式](focus5.md)

## 延伸閱讀

- [Linux PCI 驅動程式 HOWTO](https://www.google.com/search?q=Linux+PCI+driver+howto)
- [Linux DMA API 文件](https://www.google.com/search?q=Linux+DMA+API+documentation)
- [Rust PCI Driver 範例](https://www.google.com/search?q=Rust+for+Linux+PCI+driver+example)
