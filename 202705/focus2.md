# WASI：伺服器端的 WASM（2019-2026）

## 從沙箱計算到系統級應用

WASI（WebAssembly System Interface）是 WASM 從瀏覽器走向伺服器的關鍵技術。沒有 WASI，WASM 只是一個被隔離的計算引擎；有了 WASI，WASM 模組可以存取檔案、建立網路連線、讀取時鐘——但一切都透過精細的權限控制。

### WASI 的設計哲學

WASI 核心設計理念是「能力為基礎的安全模型」（Capability-based Security）。與傳統作業系統的「使用者 vs 管理者」二元權限模型不同，WASI 採用更精細的授權方式：

```
傳統安全模型 vs WASI 能力模型：
─────────────────────────────────

傳統模型：
┌──────────────────────────────┐
│  行程（Process）               │
│  - UID: 1000                  │  ← 要嘛全部能讀，要嘛全部不能讀
│  - 可讀 /tmp、/home、/etc    │
│  - 可連線任意網路埠           │
└──────────────────────────────┘

WASI 能力模型：
┌──────────────────────────────┐
│  WASM 模組                     │
│  - 能力：["fd_write:stdout"]   │  ← 只有明確授予的能力
│  - 無法讀取任何檔案            │
│  - 無法建立任何網路連線        │
└──────────────────────────────┘

主機授權方式（以 wasmtime 為例）：
wasmtime run \
  --dir /tmp/data::/data \     # 授予 /tmp/data 目錄的讀寫權限
  --tcplisten 0.0.0.0:8080 \  # 授予聆聽 8080 埠的權限
  module.wasm
```

這種設計的安全性顯而易見：即使 WASM 模組包含惡意程式碼，它無法做任何未被授權的操作。攻擊面被嚴格限制在明確授予的能力集合中。

### wasip1 vs wasip2 的差異

WASI 經歷了兩個主要版本，差異巨大：

| 特性 | wasip1（預覽 1） | wasip2（預覽 2） |
|------|------------------|------------------|
| **發布年份** | 2019 | 2023（穩定於 2024） |
| **介面定義** | C 風格的函數簽名 | WIT（WebAssembly Interface Types） |
| **型別系統** | 只有整數與指標 | 高階型別（字串、列表、記錄、變體） |
| **非同步** | 無 | 原生非同步支援（stream 與 future） |
| **錯誤處理** | errno 整數錯誤碼 | 具型別的錯誤結果 |
| **模組化** | 單一命名空間 | 多層次介面（wasi:clock/monotonic-clock） |
| **與 Component Model** | 不相容 | 完全整合 |
| **Rust 目標** | wasm32-wasip1 | wasm32-wasip2 |

```
wasip1 的系統呼叫風格：
─────────────────────────

// C 風格的 errno 傳回
fn path_open(
    fd: Fd,           // 整數檔案描述子
    dirflags: u32,    // 位元旗標
    path: &[u8],      // 原始位元組路徑
    oflags: u32,      // 開啟選項的位元旗標
    fsrights: u64,    // 檔案系統權限的位元遮罩
) -> Result<Fd, Errno>;  // 錯誤是 i32 整數

wasip2 的 WIT 風格介面：
─────────────────────────

// wasi:filesystem/types.wit
interface types {
    record directory-entry {
        name: string,
        type: file-type,
    }

    variant error {
        access-denied,
        already-exists,
        not-found,
        not-permitted,
        io(u32),
    }

    open: func(
        fd: descriptor,
        path: string,
        mode: open-mode,
    ) -> result<descriptor, error>;
}
```

wasip2 的改進不僅是語法糖。WIT 型別系統讓工具可以自動生成型別安全的綁定——開發者不再需要手動處理位元遮罩和 errno 檢查。

### 主要的 WASI 系統介面

```
WASI 介面層次 ─ 以 wasip2 為例：
────────────────────────────────────

wasi:clocks/
├── monotonic-clock  獲取高精度時間戳
└── wall-clock       獲取牆上時間（日曆時間）

wasi:filesystem/
├── types            檔案類型、錯誤、開啟模式
└── preopens         預先開啟的目錄

wasi:sockets/
├── network          網路位址與名稱解析
├── tcp              串流連線
├── tcp-create-socket 建立連線（非同步）
└── udp              資料封包

wasi:random/
└── random           亂數產生器

wasi:io/
├── streams         非同步位元組串流
└── poll            事件輪詢機制
```

### Rust 對 WASI 的支援現狀

Rust 對 WASI 的支援是生態中最成熟的。截至 2026 年，Rust 工具鏈提供了完整的 WASI 支援：

**編譯目標：**

```bash
# Rust 的 WASI 目標（均已穩定）
rustup target add wasm32-wasip1   # WASI 預覽 1
rustup target add wasm32-wasip2   # WASI 預覽 2 + Component Model
```

**標準程式庫支援：**

```rust
// wasm32-wasip1 目標下，Rust 標準程式庫經過適配
// 以下程式碼在 WASM 中可直接使用

use std::fs::File;
use std::io::Read;
use std::net::TcpStream;
use std::time::SystemTime;

// 讀取檔案（需要主機授予目錄權限）
fn read_config(path: &str) -> String {
    let mut file = File::open(path).unwrap();
    let mut contents = String::new();
    file.read_to_string(&mut contents).unwrap();
    contents
}

// 建立 TCP 連線（需要主機授予網路權限）
fn fetch_url() -> String {
    let mut stream = TcpStream::connect("example.com:80").unwrap();
    // ...
}
```

**在 wasip2 中需要手動實作 WIT 介面：**

```rust
// 使用 wit-bindgen 生成 wasip2 介面的 Rust 綁定
wit_bindgen::generate!({
    path: "wasi-imports.wit",
    world: "my-component",
});

// 標準程式庫中的 std::fs 在 wasip2 目標中改用 WASI 介面
// 開發者通常不需直接操作 WASI 系統呼叫
```

### WASI 的實際應用場景

截至 2026 年，WASI 已被廣泛用於以下場景：

1. **Serverless 函數**：每個函數執行在獨立的 WASM 沙箱中，透過 WASI 存取必要的系統資源
2. **資料處理管線**：WASM 元件在資料流中執行 ETL 操作，安全地讀寫檔案系統
3. **外掛系統**：第三方外掛程式碼在 WASM 沙箱中執行，透過 WASI 獲得有限的系統存取權限
4. **開發工具**：`wasmtime` CLI 工具讓開發者可以直接執行 WASM 程式，如同執行原生二進制

```
WASI 的安全模型在實戰中的優勢：
─────────────────────────────────

傳統外掛系統（Native .so/.dll）：
- 外掛可存取所有系統資源
- 惡意外掛可讀取 /etc/passwd 或 ~/.ssh/id_rsa
- 修補方式：手寫沙箱程式碼（如 seccomp）

WASI 外掛系統：
- 外掛預設無權存取任何系統資源
- 主機明確授予所需的最小權限集
- 即使外掛有惡意，攻擊面為零（若授予權限正確）
```

WASI 將 WASM 從一個瀏覽器技術轉變為通用伺服器執行期。它的能力模型不僅提升了安全性，還改變了我們對軟體元件的信任假設——不必信任程式碼，只需信任授予的能力。

---

## 延伸閱讀

- [WASI 官方規範](https://www.google.com/search?q=WASI+specification)
- [wasip1 vs wasip2 差異](https://www.google.com/search?q=wasip1+vs+wasip2+differences)
- [Rust WASI 支援](https://www.google.com/search?q=Rust+WASI+support)
- [wasmtime WASI 文件](https://www.google.com/search?q=wasmtime+WASI+documentation)

---

*本篇文章為「AI 程式人雜誌 2026 年 7 月號」WASM 系列之二。*
