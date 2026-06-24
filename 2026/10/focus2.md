# 主題二：字元設備驅動程式

## file_operations 與 ioctl

### 字元設備的角色

字元設備是 Linux 中最簡單也最常見的驅動程式類型。從 `/dev/tty` 到 `/dev/nvme0`，所有以串流方式讀寫的硬體裝置背後都是字元設備驅動程式。

### Rust 的 FileOperations

Rust for Linux 的 `FileOperations` trait 封裝了核心的 `file_operations` 結構：

```rust
use kernel::file_operations::{FileOperations, FileOperationsVtable};

struct MyCharDevice;

impl FileOperations for MyCharDevice {
    kernel::declare_file_operations!(read, write, ioctl);

    fn read(
        _this: &Self,
        _file: &File,
        buf: &mut impl IoBufferWriter,
        _offset: u64,
    ) -> Result<usize> {
        let data = b"Hello from kernel!\n";
        buf.write_slice(data)?;
        Ok(data.len())
    }

    fn write(
        _this: &Self,
        _file: &File,
        buf: &impl IoBufferReader,
        _offset: u64,
    ) -> Result<usize> {
        let len = buf.len();
        pr_info!("wrote {} bytes to device\n", len);
        Ok(len)
    }
}
```

### ioctl 實作

ioctl 是裝置特定的控制介面。在 Rust 中，ioctl 命令透過 `IoctlCommand` 類型安全地分派：

```rust
fn ioctl(
    this: &Self,
    _file: &File,
    cmd: &IoctlCommand,
    arg: usize,
) -> Result<u32> {
    match cmd {
        cmd if cmd == GET_INFO => {
            let info = DeviceInfo { irq: 42, mmio: 0xf000_0000 };
            // 將資訊複製到使用者空間
            let buf = unsafe { UserSlice::new(arg as *mut u8, size_of::<DeviceInfo>()) };
            buf.write(&info)?;
            Ok(0)
        }
        cmd if cmd == RESET => {
            this.reset_device()?;
            Ok(0)
        }
        _ => Err(ENOTTY),
    }
}
```

### 完整模組組合

字元設備驅動需要將 `Module`、`FileOperations` 和 `device` 註冊結合：

```rust
#[module]
struct CharDriver {
    #[device]
    device: Device,
    data: Mutex<Vec<u8>>,
}

impl Module for CharDriver {
    fn init(module: &'static ModuleInfo) -> Result<Self> {
        // 註冊字元設備區域
        let region = module.create_chrdev_region("chardrv", 0, 1)?;
        // 建立 cdev 並註冊 file_operations
        let cdev = CDev::new::<MyFOps>(module)?;
        cdev.add(region, 0)?;
        Ok(Self { device: cdev, data: Mutex::new(Vec::new()) })
    }
}
```

### 與使用者空間溝通

字元設備的核心價值是核心/使用者空間的資料交換：

- **read/write** — 序列化串流資料傳輸
- **ioctl** — 控制命令與參數配置
- **mmap** — 將核心記憶體直接映射到使用者空間（適用於幀緩衝區等場景）

Rust 的 `IoBufferWriter`/`IoBufferReader` 抽象確保了使用者空間緩衝區的存取安全性——不會發生因競態條件導致的使用者空間指標重複取值（TOCTOU）攻擊。

---

**下一步**: [平台驅動程式與裝置樹](focus3.md)

## 延伸閱讀

- [Linux 字元設備驅動程式](https://www.google.com/search?q=Linux+character+device+driver+Rust)
- [FileOperations Trait 文件](https://www.google.com/search?q=Rust+for+Linux+FileOperations+trait)
