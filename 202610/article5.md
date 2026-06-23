# GPU/DRM 驅動程式入門 — Direct Rendering Manager、GEM 緩衝區

## 1. 引言

GPU 驅動程式是 Linux 核心中最複雜的驅動類型之一。一個現代 GPU 驅動需要管理數 GB 的 VRAM、排程數千個並行執行單元、處理複雜的顯示管線——同時滿足即時性和安全性的嚴格要求。Rust 在 GPU 驅動領域正在展現獨特的優勢，特別是在 Asahi Linux 和 Intel Xe 專案中。

## 2. DRM 子系統架構

Direct Rendering Manager（DRM）是 Linux 核心中負責圖形和顯示的框架：

```
使用者空間 (Mesa, X11/Wayland, Vulkan)
    │
DRM 核心層 (drm.ko)
    ├── DRM 檔案操作 (drm_open, drm_ioctl)
    ├── GEM 記憶體管理
    ├── KMS (Kernel Mode Setting)
    │   ├── CRTC（顯示計時控制器）
    │   ├── Encoder（視訊編碼器）
    │   ├── Connector（顯示介面）
    │   └── Plane（圖層合成）
    └── GPU 排程器 (DRM scheduler)
    │
GPU 驅動層 (mygpu.ko)
    ├── 硬體初始化/重置
    ├── 命令提交環
    ├── VRAM/快取管理
    ├── 中斷處理
    └── 電源管理
```

## 3. Rust DRM 驅動程式範例

### 3.1 基本裝置結構

```rust
use kernel::drm::{
    DrmDevice, DrmDriver, DrmFileOperations,
    gem::{GemManager, GemObject, GemDomain},
    kms::{Crtc, Encoder, Connector, Plane, Framebuffer},
};

struct MyGpuDrv {
    drm: DrmDevice,
    gem: GemManager,
    vram: IoMemory,
    regs: IoMemory,
    irq: u32,
    crtc: Crtc,
    connector: Connector,
}

impl DrmDriver for MyGpuDrv {
    fn load(pci_dev: &mut PciDevice, drm: DrmDevice) -> Result<Self> {
        pr_info!("mygpu: loading GPU driver\n");

        // 映射 VRAM 和暫存器
        let vram = pci_dev.get_iomem(0)?;
        let regs = pci_dev.get_iomem(2)?;
        let irq = pci_dev.get_irq()?;

        // 初始化 GEM 管理器（管理 256MB VRAM）
        let gem = GemManager::new(
            drm.clone(), 256 * 1024 * 1024,
        )?;

        // 設定顯示管線
        let crtc = Crtc::new(drm.clone(), "primary", 0)?;
        let encoder = Encoder::new(drm.clone(), EncoderType::Dpi)?;
        let connector = Connector::new(
            drm.clone(), ConnectorType::HdmiA,
        )?;

        // 硬體初始化
        regs.writel(GPU_RESET, 0x1);
        kernel::timer::udelay(100);
        regs.writel(GPU_RESET, 0x0);
        regs.writel(CLOCK_ENABLE, 0xFFFFFFFF);

        Ok(Self {
            drm,
            gem,
            vram,
            regs,
            irq,
            crtc,
            connector,
        })
    }
}
```

### 3.2 GEM 緩衝區管理

GEM（Graphics Execution Manager）是 DRM 的記憶體管理核心。它負責在 VRAM 和系統記憶體之間分配和遷移緩衝區：

```rust
impl MyGpuDrv {
    fn create_frame_buffer(&self, width: u32, height: u32) -> Result<Framebuffer> {
        let bpp = 32u32;
        let pitch = width * (bpp / 8);
        let size = pitch * height;

        // 在 VRAM 中分配 GEM 物件
        let gem_obj = self.gem.alloc(size, GemDomain::Vram)?;

        // 建立幀緩衝區
        let fb = Framebuffer::new(
            &gem_obj,
            width,
            height,
            bpp,
            pitch,
        )?;

        pr_info!("framebuffer: {}x{} ({} bytes)\n", width, height, size);
        Ok(fb)
    }

    fn handle_page_flip(&self, fb: &Framebuffer) -> Result<()> {
        // 將幀緩衝區的 DMA 位址寫入顯示控制器
        let gem_obj = fb.gem_object();
        let dma_addr = gem_obj.dma_address();

        // 設定顯示控制器掃描位址
        self.regs.writel(DISPLAY_ADDR_HI, (dma_addr >> 32) as u32);
        self.regs.writel(DISPLAY_ADDR_LO, dma_addr as u32);

        // 觸發下次 VBlank 時的頁面翻轉
        self.regs.writel(DISPLAY_TRIGGER, 0x1);
        Ok(())
    }
}
```

### 3.3 顯示模式設定（KMS）

KMS（Kernel Mode Setting）管理顯示器的解析度、更新率和連接狀態：

```rust
impl MyGpuDrv {
    fn setup_display(&self) -> Result<DisplayConfig> {
        // 讀取顯示器 EDID 資訊
        let edid = self.read_edid()?;

        // 建立顯示模式
        let mode = self.crtc.find_mode(&edid)?;
        pr_info!("best mode: {}x{} @ {}Hz\n",
            mode.width(), mode.height(), mode.refresh_rate());

        // 設定 CRTC
        self.crtc.set_mode(&mode)?;

        // 建立主圖層
        let primary = Plane::new(self.drm.clone(), PlaneType::Primary)?;
        let fb = self.create_frame_buffer(mode.width(), mode.height())?;
        primary.set_fb(fb)?;

        // 設定連接器
        self.connector.set_display_info(DisplayInfo {
            width: mode.width(),
            height: mode.height(),
            refresh_rate: mode.refresh_rate(),
            bpc: 10,
        })?;

        Ok(DisplayConfig {
            width: mode.width(),
            height: mode.height(),
            refresh_rate: mode.refresh_rate(),
        })
    }

    fn read_edid(&self) -> Result<Edid> {
        // 透過 I2C 讀取顯示器的 EDID 資料
        let mut edid_raw = [0u8; 128];

        // 初始化 DDC/I2C 匯流排
        self.regs.writel(DDC_ADDR, 0x50);
        self.regs.writel(DDC_OFFSET, 0x00);

        for i in 0..128 {
            self.regs.writel(DDC_READ, 0x1);
            kernel::timer::udelay(40);
            edid_raw[i] = self.regs.readl(DDC_DATA) as u8;
        }

        let edid = Edid::from_raw(&edid_raw)?;
        Ok(edid)
    }
}
```

### 3.4 GPU 命令提交

現代 GPU 透過命令緩衝區（Ring Buffer / Command Queue）來提交渲染工作：

```rust
impl MyGpuDrv {
    fn submit_commands(&self, cmds: &[u32]) -> Result<GpuFence> {
        let size = cmds.len() * 4;

        // 從 VRAM 分配命令緩衝區
        let cmd_buf = self.gem.alloc(size, GemDomain::Vram)?;

        // 將命令複製到 VRAM（透過 WC mapping 或 DMA）
        cmd_buf.write(cmds)?;

        // 取得 GPU 可存取的位址
        let gpu_addr = cmd_buf.dma_address();

        // 寫入 GPU 的命令提交環
        let ring_head = self.regs.readl(RING_HEAD);
        let ring_tail = self.regs.readl(RING_TAIL);
        let ring_size = 1024 * 4; // 4KB

        // 將命令放入環緩衝區
        let ring_mem = self.vram.ioffset(RING_BASE);
        let offset = ring_tail as usize % ring_size;
        ring_mem.write_cmds(offset, &[gpu_addr as u32, size as u32])?;

        // 更新環尾指標，通知 GPU 有新的命令
        let new_tail = (ring_tail + 8) % ring_size as u32;
        self.regs.writel(RING_TAIL, new_tail);

        // 回傳 fence，用於等待 GPU 完成
        let seqno = self.regs.readl(LAST_SEQNO);
        Ok(GpuFence::new(self.drm.clone(), seqno))
    }
}
```

## 4. 中斷處理與 VBlank

```rust
fn irq_handler(gpu: &MyGpuDrv) -> irq::Return {
    let status = gpu.regs.readl(GPU_IRQ_STATUS);

    if status & VBLANK_IRQ != 0 {
        // VBlank 中斷發生——通知 DRM 核心
        gpu.crtc.handle_vblank();
        gpu.regs.writel(GPU_IRQ_CLEAR, VBLANK_IRQ);
    }

    if status & DMA_DONE_IRQ != 0 {
        // DMA 完成——喚醒等待的處理器
        gpu.drm.scheduler().wake_up();
        gpu.regs.writel(GPU_IRQ_CLEAR, DMA_DONE_IRQ);
    }

    irq::Return::Handled
}
```

## 5. Rust 在 GPU 驅動中的特殊優勢

| 面向 | C 語言常見問題 | Rust 解決方案 |
|------|--------------|-------------|
| VRAM 指標 | 無型別的 void* 指標 | `IoMemory` 型別區分 VRAM/暫存器 |
| GEM 物件引用 | 手動 kref_get/put | `ARef<T>` 自動引用計數 |
| 命令緩衝區 | 提交後 GPU 使用中釋放 | 所有權確保緩衝區存活 |
| GPU 虛擬位址 | 手動管理頁表 | `GpuVma` 型別安全位址空間 |
| 多執行緒命令提交 | spinlock 容易忘記 | `Mutex<CommandQueue>` 強制鎖定 |

## 6. 結語

GPU 驅動程式是核心中複雜度最高的驅動類型，數十萬行程式碼、複雜的硬體狀態機、嚴格即時要求的顯示管線——這些特性使 GPU 驅動成為 Rust 安全保證的終極考驗。2026 年，隨著 Intel Xe Rust GPU 驅動和 Asahi Linux 專案的持續進展，Rust 在 GPU 驅動領域的可行性已無庸置疑。

---

## 延伸閱讀

- [Linux DRM KMS 文件](https://www.google.com/search?q=Linux+DRM+KMS+documentation)
- [Intel Xe Rust GPU Driver](https://www.google.com/search?q=Intel+Xe+Rust+GPU+driver)
- [Asahi Linux GPU 驅動](https://www.google.com/search?q=Asahi+Linux+GPU+driver+Rust)
- [DRM GEM 文件](https://www.google.com/search?q=DRM+GEM+graphics+execution+manager)
