# 作業系統核心

## Rust for Linux、核心模組、驅動程式（2020-2026）

### 前言

作業系統核心是系統程式設計的終極挑戰。Linux 核心包含超過 3000 萬行 C 程式碼，而記憶體安全漏洞是核心漏洞的主要來源。Rust for Linux 專案的目標是：**讓 Rust 成為 Linux 核心中 C 的安全替代方案**。

### Rust for Linux 專案

2020 年，Rust for Linux 專案正式啟動。2026 年，Linux 核心 8.0 將 Rust 作為第一級語言支援。

**核心中的 Rust 程式碼模式**：

```rust
// kernel crate：Rust for Linux 的核心支援
use kernel::prelude::*;
use kernel::sync::Arc;

// 定義一個核心模組
module! {
    type: MyDriver,
    name: "my_driver",
    author: "AI Programmer Magazine",
    description: "A sample Rust driver",
    license: "GPL",
}

// 驅動程式結構體
struct MyDriver {
    data: Arc<kernel::sync::Mutex<DriverData>>,
}

// 實作驅動程式 trait
impl kernel::Module for MyDriver {
    fn init(name: &'static CStr, module: &'static ThisModule) -> Result<Self> {
        pr_info!("MyDriver initialized\n");
        
        // 註冊字元裝置
        let data = Arc::try_new(DriverData::new())?;
        
        Ok(MyDriver { data })
    }
}

impl Drop for MyDriver {
    fn drop(&mut self) {
        pr_info!("MyDriver removed\n");
    }
}
```

### 核心中的安全抽象

Rust for Linux 的關鍵貢獻是將核心資源（檔案、連線、記憶體）包裝在型別安全的 Rust 抽象中：

```rust
// Rust for Linux：安全的記憶體分配
use kernel::alloc::flags;

// GFP 標誌在 Rust 中封裝為型別
let ptr = kernel::alloc::alloc(GFP_KERNEL, size)?;

// 核心中的 Vec（類似標準庫，但使用核心分配器）
let mut v = kernel::collections::Vec::new()?;
v.push(item, GFP_KERNEL)?;  // 每次操作都需要 GFP 標誌
```

**檔案系統抽象**：

```rust
// 核心中的 Rust 檔案系統實作
impl FileOperations for MyFileOps {
    fn open(shared: &Self::OpenData, _file: &File) -> Result<Self::Data> {
        Ok(MyFileData::new())
    }
    
    fn read(
        data: &Self::Data,
        _file: &File,
        writer: &mut impl IoVectorWriter,
        offset: u64,
    ) -> Result<usize> {
        let buf = data.read_data(offset)?;
        writer.write(&buf)?;
        Ok(buf.len())
    }
}
```

### 網路子系統

Rust 在 Linux 網路子系統中的應用：

```rust
// 核心中的 Rust 網路過濾器
use kernel::net::filter::{self, verdict, Context};

#[vtable]
pub trait NetfilterHook {
    fn hook(context: &Context, skb: &SkBuff) -> verdict::Verdict;
}

// TCP 封包過濾器實作
struct TcpFilter;

impl NetfilterHook for TcpFilter {
    fn hook(context: &Context, skb: &SkBuff) -> verdict::Verdict {
        // 使用型別安全的網路封包解析
        if let Some(tcp) = skb.transport_header().as_tcp() {
            if tcp.dest_port() == 8080 {
                pr_info!("Blocked TCP connection to port 8080\n");
                return verdict::NF_DROP;
            }
        }
        verdict::NF_ACCEPT
    }
}

// 註冊過濾器
kernel::net::filter::register!("tcp_filter", TcpFilter);
```

### 裝置驅動程式

Rust 裝置驅動程式的核心模式：

```rust
// I2C 裝置驅動程式
struct MyI2cDriver;

impl I2cDriver for MyI2cDriver {
    type Data = MyDeviceData;
    
    fn probe(client: &I2cClient, id: &I2cDeviceId) -> Result<Box<Self::Data>> {
        let data = MyDeviceData {
            // 初始化裝置狀態
        };
        
        pr_info!("Found device at address 0x{:x}\n", client.addr());
        Ok(Box::new(data))
    }
    
    fn remove(data: &mut Self::Data) {
        pr_info!("Device removed\n");
    }
}
```

### 為什麼核心需要 Rust？

核心漏洞的數據：

| 漏洞類型 | 比例 | Rust 能否預防？ |
|---------|------|---------------|
| Use-after-free | 30% | ✅ 編譯期 |
| 緩衝區溢位 | 20% | ✅ 邊界檢查 |
| 空指標解引用 | 15% | ✅ Option 型別 |
| 資料競爭 | 10% | ✅ Send/Sync |
| 其他 | 25% | 🟡 部分 |

**估算**：如果核心中的新程式碼用 Rust 撰寫，可減少約 70% 的記憶體安全漏洞。

### 核心開發的挑戰

Rust for Linux 面臨的核心挑戰：

**1. 分配器錯誤處理**：
```rust
// C：分配失敗回傳 NULL
// Rust：分配失敗回傳 Result
// 核心中所有分配必須小心處理 GFP 標誌
let buf = kernel::alloc::alloc(GFP_ATOMIC, 1024)?;
```

**2. 中斷上下文限制**：
```rust
// 在中斷上下文中不能睡眠
// Rust 型別系統可以強制這個規則！
fn interrupt_handler() {
    // GFP_ATOMIC：在中斷中只能使用原子分配
    let data = kernel::alloc::alloc(GFP_ATOMIC, size);
    // mutex_lock()：在中斷中不能使用！
}
```

**3. 核心特定的錯誤處理**：
```rust
// 核心使用 ERR_PTR 模式
// Rust 封裝為 Result
fn do_something() -> Result<(), kernel::Error> {
    let ptr = kernel::alloc::alloc(GFP_KERNEL, 1024)
        .map_err(|_| kernel::error::ENOMEM)?;
    Ok(())
}
```

### 獨立的核心模組

Rust 核心模組可以獨立於主線核心開發：

```bash
# 建立 Rust 核心模組
cargo kernel new my_rust_module
cd my_rust_module

# 編譯核心模組
cargo kernel build

# 載入模組
sudo insmod my_rust_module.ko

# 卸載模組
sudo rmmod my_rust_module
```

### Rust 核心生態的成長

| 年份 | 里程碑 |
|------|--------|
| 2020 | Rust for Linux 初始提案 |
| 2021 | 核心中的 Rust 基礎架構 |
| 2022 | Rust 驅動程式範例合併 |
| 2023 | 網路/檔案系統支援 |
| 2024 | 核心 Rust 程式碼超過 10 萬行 |
| 2025 | 設備驅動程式框架成熟 |
| 2026 | Linux 8.0：Rust 正式支援 |

### 小結

Rust for Linux 是系統程式設計領域最具影響力的專案之一。它代表了 Rust 的終極考驗——在最嚴格、最底層的環境中使用。

Rust 在核心中的成功不僅是技術的勝利，更證明了：**記憶體安全可以在不放棄效能和控制的情況下實現，即使在作業系統核心這種最嚴苛的環境中**。

---

**下一步**：[AI + 系統程式](focus7.md)

## 延伸閱讀

- [Rust for Linux Kernel](https://www.google.com/search?q=Rust+for+Linux+kernel)
- [Linux 核心 Rust 文件](https://www.google.com/search?q=Linux+kernel+Rust+documentation)
- [Writing Linux Kernel Modules in Rust](https://www.google.com/search?q=writing+Linux+kernel+modules+in+Rust)
