# 主題六：GPU 與 DRM 驅動程式

## Direct Rendering Manager 與 GEM 緩衝區

### DRM 子系統架構

Linux 核心的 Direct Rendering Manager（DRM）是 GPU 驅動程式的核心子系統，負責：
- 顯示控制器管理（CRTC、Encoder、Connector）
- 幀緩衝區分配與管理（GEM/CMA）
- 命令提交與 GPU 排程（Command Submission）
- 記憶體管理（VRAM、GTT）

Rust for Linux 的 DRM 抽象讓這些複雜任務更安全：

```rust
use kernel::drm::{DrmDevice, DrmDriver};

struct MyGpuDev {
    drm: DrmDevice,
    gem: GemManager,
    vram: IoMemory,
}

impl DrmDriver for MyGpuDev {
    fn load(dev: &mut pci::PciDevice) -> Result<Self> {
        let vram = dev.get_iomem(0)?;
        let drm = DrmDevice::new(dev, "mygpu")?;
        let gem = GemManager::new(drm.clone(), 64 * 1024 * 1024)?;

        Ok(Self { drm, gem, vram })
    }
}
```

### GEM 緩衝區管理

Graphics Execution Manager（GEM）是 DRM 的記憶體管理層：

```rust
use kernel::drm::gem::{GemObject, GemCreate};

impl GemCreate for MyGpuDev {
    fn create_object(size: usize) -> Result<Box<GemObject>> {
        // 在 VRAM 中分配緩衝區
        let gem_obj = GemObject::new(size, GemDomain::Vram)?;
        Ok(gem_obj)
    }

    fn free_object(obj: Box<GemObject>) -> Result<()> {
        obj.free();
        Ok(())
    }
}
```

### 顯示管線

DRM 的顯示管線由 CRTC、Encoder、Connector 和 Plane 組成：

```rust
fn setup_display_pipeline(gpu: &MyGpuDev) -> Result<()> {
    // CRTC：顯示計時控制器
    let crtc = Crtc::new(gpu.drm.clone(), "primary-crtc")?;
    crtc.set_vblank_handler(handle_vblank)?;

    // Encoder：視訊訊號編碼器
    let encoder = Encoder::new(gpu.drm.clone(), EncoderType::Hdmi)?;

    // Connector：實際的顯示介面
    let connector = Connector::new(gpu.drm.clone(), ConnectorType::HdmiA)?;
    connector.set_display_info(DisplayInfo {
        width: 1920,
        height: 1080,
        refresh_rate: 60,
    })?;

    // Plane：圖層合成
    let primary_plane = Plane::new(gpu.drm.clone(), PlaneType::Primary)?;
    primary_plane.set_fb(Framebuffer::new(&gpu.gem.create_object(4 * 1920 * 1080)?)?)?;

    Ok(())
}
```

### Framebuffer 與顯示更新

```rust
fn handle_vblank(crtc: &Crtc) -> Result<()> {
    // VBlank 中斷——準備顯示下一幀
    let fb = crtc.next_framebuffer()?;

    // DMA 將幀資料傳送到顯示控制器
    crtc.set_fb(fb)?;
    Ok(())
}
```

### GPU 命令提交

現代 GPU 需要透過命令緩衝區（Command Buffer）提交渲染工作：

```rust
fn submit_command(gpu: &MyGpuDev, cmd_buf: &[u32]) -> Result<()> {
    let gpu_cmd = gpu.vram.alloc(cmd_buf.len() * 4)?;

    // 將命令複製到 GPU 可存取的記憶體
    gpu_cmd.write(cmd_buf)?;

    // 通知 GPU 開始處理
    gpu.vram.writel(GPU_RING_DOORBELL, gpu_cmd.gpu_addr() as u32);
    Ok(())
}
```

### Rust 對 GPU 驅動的獨特優勢

GPU 驅動程式的複雜性使其成為 Rust 安全保證的最大受益者之一：

| 問題域 | C 語言常見 bug | Rust 解決方案 |
|--------|--------------|-------------|
| 命令緩衝區生命週期 | 提交後釋放 | 所有權系統確保緩衝區在使用期間存活 |
| GEM 物件引用計數 | 計數錯誤導致過早釋放 | `ARef<T>` 自動管理引用 |
| 記憶體類型轉換 | VRAM/系統記憶體混淆 | 型別系統區分 `VramMem` vs `SysMem` |
| GPU 虛擬位址管理 | 位址空間洩漏 | `Drop` trait 自動回收 |
| 併發命令提交 | 競態條件 | `Mutex`/`SpinLock` 強制鎖定 |

---

**下一步**: [AI 輔助驅動程式開發](focus7.md)

## 延伸閱讀

- [Linux DRM/KMS 文件](https://www.google.com/search?q=Linux+DRM+KMS+documentation)
- [Rust for Linux GPU 驅動](https://www.google.com/search?q=Rust+GPU+driver+Linux)
- [Intel Xe Rust GPU Driver](https://www.google.com/search?q=Intel+Xe+Rust+GPU+driver)
