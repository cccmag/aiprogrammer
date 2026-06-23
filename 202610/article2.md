# 字元設備驅動程式實戰 — 完整的 Rust 字元設備範例

## 1. 引言

字元設備是 Linux 驅動程式的入門磚，也是最常見的驅動類型。從 UART、GPIO 到感測器，大部分簡單的硬體裝置都透過字元設備與使用者空間互動。本文將帶領你從零開始，建立一個完整的 Rust 字元設備驅動程式。

## 2. 什麼是字元設備？

字元設備以串流方式傳輸資料——你從裝置讀取一串位元組，或寫入一串位元組。與區塊設備（如硬碟）不同，字元設備不支援隨機存取。在 Linux 中，字元設備透過 `/dev` 下的裝置檔案暴露給使用者空間。

```
使用者空間: fopen("/dev/mydevice", "rw")
                 │
核心空間: file_operations 結構
           ├── .open  = my_open
           ├── .read  = my_read
           ├── .write = my_write
           ├── .ioctl = my_ioctl
           └── .release = my_close
```

## 3. 範例：Rust 字元設備驅動程式

### 3.1 模組結構

```rust
// SPDX-License-Identifier: GPL-2.0
use kernel::prelude::*;
use kernel::chrdev::{CDev, ChrdevRegion};
use kernel::file_operations::{FileOperations, FileOperationsVtable, File};
use kernel::io_buffer::{IoBufferReader, IoBufferWriter};
use kernel::sync::Mutex;

module! {
    name: "chardrv",
    author: "AI Programmer Magazine",
    description: "A simple character device driver in Rust",
    license: "GPL",
}

const BUF_SIZE: usize = 4096;

struct CharDrv {
    data: Mutex<Vec<u8>>,
    open_count: Mutex<u32>,
}
```

### 3.2 Module trait 實作

```rust
impl Module for CharDrv {
    fn init(module: &'static ModuleInfo) -> Result<Self> {
        pr_info!("chardrv: loading\n");

        // 註冊字元設備區域
        let region = ChrdevRegion::new(module.name(), 0, 1)?;
        let major = region.major();

        // 建立 cdev 並關聯 file_operations
        let cdev = CDev::new::<CharFops>(module)?;
        cdev.add(region, 0)?;

        pr_info!("chardrv: registered major {}\n", major);

        Ok(Self {
            data: Mutex::new(Vec::with_capacity(BUF_SIZE)),
            open_count: Mutex::new(0),
        })
    }
}

impl Drop for CharDrv {
    fn drop(&mut self) {
        pr_info!("chardrv: unloaded\n");
    }
}
```

### 3.3 FileOperations 實作

```rust
struct CharFops;

impl FileOperations for CharFops {
    kernel::declare_file_operations!(read, write, open, release, ioctl);

    fn open(
        this: &Self::TraitData,
        _file: &File,
    ) -> Result<()> {
        *this.open_count.lock() += 1;
        pr_info!("chardrv: opened (count: {})\n", *this.open_count.lock());
        Ok(())
    }

    fn read(
        this: &Self::TraitData,
        _file: &File,
        buf: &mut impl IoBufferWriter,
        offset: u64,
    ) -> Result<usize> {
        let data = this.data.lock();
        let len = data.len();
        let off = offset as usize;

        if off >= len {
            return Ok(0); // EOF
        }

        let avail = core::cmp::min(buf.len(), 4096);
        let actual = core::cmp::min(avail, len.saturating_sub(off));
        buf.write_slice(&data[off..off + actual])?;
        Ok(actual)
    }

    fn write(
        this: &Self::TraitData,
        _file: &File,
        buf: &impl IoBufferReader,
        _offset: u64,
    ) -> Result<usize> {
        let len = buf.len();
        let mut data = this.data.lock();
        data.clear();

        let actual = core::cmp::min(len, BUF_SIZE);
        let mut tmp = vec![0u8; actual];
        buf.read_slice(&mut tmp)?;
        data.extend_from_slice(&tmp);

        pr_info!("chardrv: wrote {} bytes\n", actual);
        Ok(actual)
    }

    fn release(
        this: &Self::TraitData,
        _file: &File,
    ) -> Result<()> {
        *this.open_count.lock() -= 1;
        pr_info!("chardrv: released\n");
        Ok(())
    }
}
```

### 3.4 ioctl 實作

ioctl 提供裝置特定的控制介面。定義命令常量並匹配處理：

```rust
const IOCTL_GET_INFO: u32 = 0x1001;
const IOCTL_RESET: u32 = 0x1002;
const IOCTL_SET_SIZE: u32 = 0x1003;

impl CharFops {
    fn ioctl(
        this: &Self::TraitData,
        _file: &File,
        cmd: u32,
        arg: usize,
    ) -> Result<u32> {
        match cmd {
            IOCTL_GET_INFO => {
                // 回傳當前緩衝區大小和開啟次數
                let size = this.data.lock().len();
                let count = *this.open_count.lock();
                let info = (size as u32) | (count << 16);
                Ok(info)
            }
            IOCTL_RESET => {
                // 重置裝置狀態
                this.data.lock().clear();
                pr_info!("chardrv: device reset\n");
                Ok(0)
            }
            IOCTL_SET_SIZE => {
                // 設定緩衝區大小
                let new_size = arg as usize;
                let mut data = this.data.lock();
                data.resize(new_size, 0);
                Ok(0)
            }
            _ => {
                pr_warn!("chardrv: unknown ioctl 0x{:x}\n", cmd);
                Err(ENOTTY)
            }
        }
    }
}
```

## 4. 使用者空間測試程式

驅動程式載入後，可以用簡單的 C 程式測試：

```c
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>

int main() {
    int fd = open("/dev/chardrv", O_RDWR);
    if (fd < 0) { perror("open"); return 1; }

    write(fd, "Hello, kernel!", 14);

    char buf[64] = {0};
    read(fd, buf, 64);
    printf("read: %s\n", buf);  // 輸出 "Hello, kernel!"

    ioctl(fd, 0x1002, 0);       // 重置裝置
    close(fd);
    return 0;
}
```

編譯並測試：

```bash
cc -o test test.c && ./test
```

## 5. 編譯與載入

```bash
# 使用 cargo-kmod 建構
cargo kmod build --release

# 載入模組
sudo insmod chardrv.ko

# 確認裝置存在
ls -la /dev/chardrv*

# 卸載模組
sudo rmmod chardrv
```

## 6. 安全分析

Rust 版本與 C 版本的關鍵差異：

| 面向 | C 版本風險 | Rust 版本保護 |
|------|-----------|-------------|
| 緩衝區溢位 | 手動邊界檢查，易遺漏 | `IoBufferWriter` 自動邊界檢查 |
| 鎖定遺漏 | 忘記 unlock 導致死結 | `Mutex` 作用域自動釋放 |
| 釋放後使用 | 資源釋放後仍可存取 | 所有權系統杜絕懸浮指標 |
| open/close 計數 | 整數溢位或不同步 | `Mutex<u32>` 保護原子性 |
| 使用者空間指標 | TOCTOU 攻擊漏洞 | IoBuffer 抽象確保指標安全 |

## 7. 結語

本文展示了如何用 Rust 撰寫一個完整的字元設備驅動程式。從 Module trait、FileOperations 到 ioctl 處理，Rust 的型別系統和所有權模型在每一步都提供了比 C 語言更安全的開發體驗。關鍵在於，這些安全保證來自編譯器而不是開發者的紀律——你不需要記住每次都要檢查邊界或釋放鎖。

---

## 延伸閱讀

- [Linux 字元設備驅動程式教學](https://www.google.com/search?q=Linux+character+device+driver+tutorial)
- [Rust for Linux FileOperations 文件](https://www.google.com/search?q=Rust+for+Linux+FileOperations)
- [Linux 核心 ioctl 文件](https://www.google.com/search?q=Linux+kernel+ioctl+documentation)
