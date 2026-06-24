# 主題一：核心模組基礎

## Rust for Linux 與核心 API

### Rust for Linux 的誕生

2020 年 4 月，Miguel Ojeda 在 Linux 核心郵件列表上貼出了一封 RFC——提議將 Rust 作為 Linux 核心的第二語言。當時這一提議引發了廣泛的辯論：Linus Torvalds 本人表達了謹慎的樂觀態度，而核心維護者們則對 Rust 的整合方式、工具鏈要求和維護成本提出了許多疑慮。

### 核心 API 的 Rust 綁定

Rust for Linux 專案的核心是 `kernel` crate，它提供了對核心 API 的安全 Rust 綁定：

```rust
// 核心 API 綁定的基本模式
use kernel::prelude::*;
use kernel::sync::Mutex;

struct MyModule {
    data: Mutex<Vec<u8>>,
}

impl Module for MyModule {
    fn init(_module: &'static ModuleInfo) -> Result<Self> {
        pr_info!("MyModule loaded\n");
        Ok(Self { data: Mutex::new(Vec::new()) })
    }
}
```

### 模組初始化與卸載

Rust 核心模組的生命週期由 `Module` trait 管理：

- **`init()`** — 在模組載入時由核心呼叫，返回模組實例
- **`Drop::drop()`** — 在模組卸載時由核心呼叫，清理資源

```rust
#[module]
struct MyDriver {
    #[device]
    dev: Device,
    irq: u32,
}

impl Module for MyDriver {
    fn init(module: &'static ModuleInfo) -> Result<Self> {
        let dev = Device::from_dt(module, "mydevice")?;
        pr_info!("mydevice: found device\n");
        Ok(Self { dev, irq: 42 })
    }
}
```

### 可用的核心 API 抽象

截至 2026 年，Rust 綁定已涵蓋以下核心 API：

| API 類別 | Rust 抽象 | 核心對應 |
|---------|-----------|---------|
| 記憶體 | `Box<T>`、`KVirtBox<T>` | kmalloc/kfree |
| 鎖定 | `SpinLock<T>`、`Mutex<T>` | spin_lock/mutex_lock |
| 引用計數 | `ARef<T>`、`RefCount<T>` | kref_get/kref_put |
| 等待佇列 | `WaitQueue<T>` | wait_event_interruptible |
| 工作佇列 | `Work<T>` | schedule_work |
| 計時器 | `Timer<T>` | timer_setup |
| 核心通知鏈 | `Notifier<T>` | blocking_notifier_chain |
| 日誌 | `pr_info!()`、`dev_info!()` | printk |

### 編譯環境

Rust 核心模組使用專門的建構系統，不是標準的 `cargo build`：

```makefile
obj-m := mydriver.o
mydriver-y := mydriver.o

KERNELDIR ?= /lib/modules/$(shell uname -r)/build

all:
	$(MAKE) -C $(KERNELDIR) M=$(PWD) modules

clean:
	$(MAKE) -C $(KERNELDIR) M=$(PWD) clean
```

使用 `cargo-kmod` 可大幅簡化流程：

```bash
cargo kmod build --release
sudo cargo kmod load
```

---

**下一步**: [字元設備驅動程式](focus2.md)

## 延伸閱讀

- [Rust for Linux 核心抽象文檔](https://www.google.com/search?q=Rust+for+Linux+kernel+crate+documentation)
- [Linux 核心模組程式設計指南](https://www.google.com/search?q=Linux+kernel+module+programming+guide)
