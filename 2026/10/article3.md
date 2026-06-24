# PCI 驅動程式開發指南 — PCI 列舉、BAR 空間、DMA

## 1. 引言

PCI（Peripheral Component Interconnect）是現代電腦中最通用的匯流排標準。從 NVMe SSD、GPU、網路卡到音效卡，幾乎所有高效能週邊裝置都使用 PCI Express 介面。撰寫 PCI 驅動程式是核心開發者的核心技能之一。本文帶你了解如何用 Rust 開發 PCI 驅動程式。

## 2. PCI 子系統架構

PCI 裝置的發現是由核心在開機時自動完成的——核心掃描 PCI 匯流排，列舉所有裝置，並收集其配置空間資訊。驅動程式的工作是找到它支援的裝置並初始化。

```
PCI 列舉流程：
1. 核心掃描 PCI 匯流排
2. 讀取每個裝置的 Vendor ID / Device ID
3. 與註冊的 pci_device_id 表匹配
4. 呼叫匹配驅動的 probe 函式
```

## 3. Rust PCI 驅動程式範例

### 3.1 驅動程式結構

```rust
use kernel::pci::{PciDriver, PciDevice, PciDeviceId};
use kernel::sync::Mutex;
use kernel::io_memory::IoMemory;

const VENDOR_MYDEV: u16 = 0x1234;
const DEVICE_MYDEV: u16 = 0x5678;

struct MyPciDev {
    dev: PciDevice,
    bar0: IoMemory,
    bar2: Option<IoMemory>,
    irq: u32,
    dma_buf: Mutex<Option<DmaRegion>>,
    regs: IoMemory,
}

impl PciDriver for MyPciDev {
    fn probe(dev: &mut PciDevice) -> Result<Self> {
        // 步驟 1：啟用 PCI 裝置
        dev.enable_device()?;
        dev.set_bus_master()?;

        // 步驟 2：讀取 BAR 空間
        let bar0_base = dev.config_read(0x10)?; // BAR0
        let bar0 = dev.get_iomem(0)?;

        let bar2 = if dev.config_read(0x18)? != 0 {
            Some(dev.get_iomem(2)?)
        } else {
            None
        };

        // 步驟 3：請求中斷
        let irq = dev.get_irq()?;

        // 步驟 4：讀取裝置特定暫存器
        let regs = dev.get_iomem(0)?;
        let rev_id = regs.readl(0x00);
        pr_info!("PCI device rev {:#x}, irq {}\n", rev_id, irq);

        Ok(Self {
            dev: dev.clone(),
            bar0,
            bar2,
            irq,
            dma_buf: Mutex::new(None),
            regs,
        })
    }

    fn remove(&mut self) -> Result<()> {
        // 清理 DMA 緩衝區
        if let Some(buf) = self.dma_buf.lock().take() {
            buf.free();
        }
        self.dev.disable_device();
        pr_info!("PCI device removed\n");
        Ok(())
    }
}

// 註冊 PCI 裝置 ID 表
kernel::pci_device_table! {
    MyPciDev,
    { vendor: VENDOR_MYDEV, device: DEVICE_MYDEV, subvendor: ANY, subdevice: ANY },
}
```

### 3.2 BAR 空間操作

PCI 裝置透過 Base Address Register（BAR）對外暴露暫存器或記憶體空間。BAR 可以是兩種型別：

```rust
impl MyPciDev {
    fn read_bar_info(&self, bar_num: u32) -> Result<BarInfo> {
        let raw = self.dev.config_read(0x10 + bar_num * 4)?;

        let is_memory = (raw & 0x1) == 0;
        let is_64bit = if is_memory {
            (raw & 0x6) == 0x4  // 64-bit memory space
        } else {
            false
        };

        Ok(BarInfo {
            bar_num,
            is_memory,
            is_64bit,
            base: self.dev.get_iomem(bar_num as usize)?.start() as u64,
            size: self.dev.get_iomem(bar_num as usize)?.len(),
        })
    }

    fn write_device_register(&self, offset: u32, value: u32) {
        self.regs.writel(offset, value);
    }

    fn read_device_register(&self, offset: u32) -> u32 {
        self.regs.readl(offset)
    }
}
```

### 3.3 DMA 操作實戰

DMA 是 PCI 驅動程式的核心功能。Rust 的 DMA 抽象確保了記憶體映射的安全性：

```rust
use kernel::dma::{DmaDirection, DmaRegion, dma_alloc_coherent};

impl MyPciDev {
    fn setup_dma(&self, size: usize) -> Result<()> {
        // 分配一致的 DMA 緩衝區（同時可被 CPU 和裝置存取）
        let region = dma_alloc_coherent::<MyPciDev>(
            &self.dev, size, GFP_KERNEL
        )?;

        let dma_addr = region.dma_address();
        let cpu_addr = region.cpu_address();

        pr_info!("DMA buffer: cpu={:#x}, dma={:#x}, size={}\n",
            cpu_addr as usize, dma_addr, size);

        // 將 DMA 位址寫入裝置暫存器
        self.regs.writel(DMA_ADDR_LOW, dma_addr as u32);
        self.regs.writel(DMA_ADDR_HIGH, (dma_addr >> 32) as u32);
        self.regs.writel(DMA_SIZE, size as u32);

        *self.dma_buf.lock() = Some(region);
        Ok(())
    }

    fn start_dma_read(&self) -> Result<()> {
        // 啟動裝置到記憶體的 DMA 傳輸
        self.regs.writel(DMA_CONTROL, DMA_DIR_DEVICE_TO_MEM);
        self.regs.writel(DMA_START, 0x1);
        Ok(())
    }

    fn dma_done(&self) -> bool {
        self.regs.readl(DMA_STATUS) & DMA_DONE_FLAG != 0
    }
}
```

## 4. 中斷處理

PCI 裝置通常使用 MSI-X 或傳統 INTx 中斷：

```rust
use kernel::irq;

impl MyPciDev {
    fn request_irq(&self) -> Result<irq::HandlerRegistration> {
        // 嘗試 MSI-X 優先
        let irq_num = if self.dev.msi_enabled() || self.dev.msix_enabled() {
            self.dev.get_irq()?
        } else {
            self.dev.get_irq()?  // 回退到傳統 INTx
        };

        // 註冊中斷處理器
        let handler = irq::Registration::new(
            irq_num,
            |dev: &MyPciDev| {
                let status = dev.regs.readl(IRQ_STATUS);
                if status != 0 {
                    dev.regs.writel(IRQ_CLEAR, status);
                    // 處理中斷事件（如 DMA 完成）
                    if status & DMA_DONE_FLAG != 0 {
                        dev.process_dma_completion();
                    }
                    irq::Return::Handled
                } else {
                    irq::Return::None
                }
            },
            irq::Flags::SHARED,
            "mypci",
        )?;

        Ok(handler)
    }
}
```

## 5. PCI Express 擴展功能

PCIe 提供了比傳統 PCI 更多的功能：

```rust
impl MyPciDev {
    fn configure_pcie(&self) -> Result<()> {
        // 讀取 PCIe 能力結構
        if let Some(cap) = self.dev.find_cap(PCI_CAP_ID_EXP) {
            let devctl = self.dev.config_read(cap + 0x08)?;

            // 啟用 Relaxed Ordering
            self.dev.config_write(cap + 0x08, devctl | 0x10)?;

            // 設定 Max Payload Size
            let max_payload = /* 來自裝置樹或自動協商 */ 128;
            self.dev.config_write(cap + 0x08,
                (devctl & !0xE0) | (max_payload.trailing_zeros() as u16) << 5)?;
        }
        Ok(())
    }
}
```

## 6. 結語

PCI 驅動程式的開發涉及裝置列舉、BAR 空間映射、DMA 和中斷處理等多個複雜面向。Rust 在 PCI 驅動開發中的最大貢獻，是讓 DMA 緩衝區的生命週期管理和中斷處理的同步變得安全且可預測——這些正是 C 語言 PCI 驅動程式中錯誤率最高的部分。

---

## 延伸閱讀

- [Linux PCI 驅動程式 HOWTO](https://www.google.com/search?q=Linux+PCI+driver+HOWTO)
- [PCI 基本概念](https://www.google.com/search?q=PCI+Base+Address+Register+tutorial)
- [Linux DMA-API 文件](https://www.google.com/search?q=Linux+DMA+API)
- [MSI-X 中斷](https://www.google.com/search?q=MSI+X+interrupt+Linux)
