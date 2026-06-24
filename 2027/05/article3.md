# WASM 元件模型實戰 — WIT 與元件組合

## 1. 引言

WASM Component Model 是 WebAssembly 生態的典範轉移。它將 WASM 從「單一功能的編譯目標」提升為「可組合的元件生態系統」。本文將透過實戰範例，展示如何使用 WIT 定義介面、實作元件、以及組合多個元件。

## 2. WIT 介面定義進階技巧

### 2.1 多層次介面組織

在複雜專案中，WIT 介面通常按功能分層組織：

```wit
// wasi:http 風格的層次化介面
package myorg:data-pipeline@0.1.0;

/// 資料型別定義
interface types {
    record data-record {
        id: u64,
        timestamp: u64,
        payload: list<u8>,
        tags: list<string>,
    }

    variant data-error {
        parse-error(string),
        validation-error(string),
        io-error(string),
    }

    type data-stream = stream<data-record>;
}

/// 資料來源介面
interface source {
    use types.{data-record, data-stream, data-error};

    /// 從外部來源讀取資料
    read: func(limit: u32) -> result<data-stream, data-error>;

    /// 確認讀取完成
    ack: func(record-id: u64) -> result<(), data-error>;
}

/// 資料處理介面
interface processor {
    use types.{data-record, data-error};

    /// 過濾不符合條件的記錄
    filter: func(records: list<data-record>, predicate: string)
        -> result<list<data-record>, data-error>;

    /// 轉換記錄格式
    transform: func(records: list<data-record>)
        -> result<list<data-record>, data-error>;
}

/// 完整資料管線元件
world pipeline-world {
    import source;
    import processor;

    export run-pipeline: func() -> result<(), string>;
}
```

### 2.2 WIT 的版本管理

WIT 支援語義化版本管理，這對於大型專案的依賴管理至關重要：

```wit
// 依賴宣告範例
package myorg:app@1.0.0;

// 指定依賴的版本範圍
use myorg:data-pipeline@>=0.1.0 <1.0.0;

// 或者使用精確版本
use wasi:http@0.2.0;
use wasi:logging@0.1.0;
```

## 3. Rust 元件實作進階模式

### 3.1 使用 cargo-component

`cargo-component` 是建置 WASM 元件的首選工具：

```bash
# 安裝 cargo-component
cargo install cargo-component

# 建立新的元件專案
cargo component new --lib my-component
cargo component add --wit wit/data-pipeline.wit
```

產生的專案結構：

```
my-component/
├── Cargo.toml
├── wit/
│   ├── data-pipeline.wit
│   └── world.wit
└── src/
    └── lib.rs           # 自動生成的主檔案
```

### 3.2 實作多個介面的元件

```rust
// lib.rs — 由 cargo-component 引導
cargo_component::component!("pipeline-world");

use crate::bindings::exports::myorg::data_pipeline::{
    source::{self, DataRecord, DataStream},
    processor::{self, DataError},
};

struct PipelineComponent;

impl PipelineWorld for PipelineComponent {
    fn run_pipeline() -> Result<(), String> {
        // 從外部來源讀取資料
        let stream = source::read(1000)
            .map_err(|e| format!("read error: {:?}", e))?;

        // 收集所有記錄
        let records: Vec<DataRecord> = stream.collect();

        // 過濾
        let filtered = processor::filter(records, "age > 18 && active == true")
            .map_err(|e| format!("filter error: {:?}", e))?;

        // 轉換
        let transformed = processor::transform(filtered)
            .map_err(|e| format!("transform error: {:?}", e))?;

        println!("Processed {} records successfully", transformed.len());
        Ok(())
    }
}
```

### 3.3 撰寫主機端（Host）實作

```rust
// 主機端 — 提供 source 和 processor 的實作
use wasmtime::component::*;
use wasmtime_wasi::WasiCtxBuilder;

#[derive(Default)]
struct MySource {
    records: Vec<DataRecord>,
}

impl source::Host for MySource {
    fn read(&mut self, limit: u32) -> Result<DataStream, DataError> {
        let chunk: Vec<DataRecord> = self.records
            .drain(..limit as usize)
            .collect();
        Ok(DataStream::from_iter(chunk))
    }

    fn ack(&mut self, record_id: u64) -> Result<(), DataError> {
        println!("Acknowledged record {}", record_id);
        Ok(())
    }
}

#[derive(Default)]
struct MyProcessor;

impl processor::Host for MyProcessor {
    fn filter(
        &mut self,
        records: Vec<DataRecord>,
        predicate: String,
    ) -> Result<Vec<DataRecord>, DataError> {
        // 實作過濾邏輯
        Ok(records.into_iter()
            .filter(|r| r.tags.contains(&predicate))
            .collect())
    }

    fn transform(
        &mut self,
        records: Vec<DataRecord>,
    ) -> Result<Vec<DataRecord>, DataError> {
        // 實作轉換邏輯
        Ok(records)
    }
}
```

## 4. 元件組合策略

### 4.1 靜態組合（編譯時期）

靜態組合在編譯時將多個元件合併為一個二進制：

```bash
# 使用 wasm-tools 組合元件
wasm-tools compose \
    --output combined.wasm \
    source-component.wasm \
    process-component.wasm \
    output-component.wasm

# 檢視組合後的元件的介面
wasm-tools component wit combined.wasm
```

### 4.2 動態組合（執行時期）

動態組合在執行時期根據需求決定載入哪些元件：

```rust
use wasmtime::component::*;

fn dynamic_composition(engine: &Engine) -> Result<(), anyhow::Error> {
    let mut linker = ComponentLinker::new(engine);

    // 根據配置載入不同的處理元件
    let processor = if use_gpu {
        load_component("gpu-processor.wasm")?
    } else {
        load_component("cpu-processor.wasm")?
    };

    // 載入資料來源元件
    let source = load_component("source-plugin.wasm")?;

    // 動態鏈接
    linker.instance("source")?.component(&source)?;
    linker.instance("processor")?.component(&processor)?;

    // 實例化主應用元件
    let app = load_component("app.wasm")?;
    let mut store = Store::new(engine, AppState::new());
    let instance = linker.instantiate(&mut store, &app)?;

    // 執行
    let run = instance.get_export(&mut store, "run").unwrap();
    // ...
    Ok(())
}

fn load_component(path: &str) -> Result<Component, anyhow::Error> {
    let engine = Engine::new(&Config::new())?;
    Ok(Component::from_file(&engine, path)?)
}
```

## 5. 元件組合的企業級應用

### 5.1 外掛系統架構

```
產品主程式
    │
    ├── 核心介面（WIT）：plugin.wit
    │   ├── interface plugin-lifecycle {
    │   │     init(config: string) -> result<(), string>;
    │   │     execute(input: string) -> result<string, string>;
    │   │     shutdown() -> result<(), string>;
    │   │ }
    │
    ├── 第三方外掛 A（Rust WASM 元件）
    ├── 第三方外掛 B（Go WASM 元件）
    └── 第三方外掛 C（C WASM 元件）
```

### 5.2 版本相容性檢查

```bash
# 檢查兩個元件的介面是否相容
wasm-tools component compatible \
    --old plugin-v1.wasm \
    --new plugin-v2.wasm

# 輸出範例：
# Compatible: YES
# Removed exports: []
# Added exports: [normalize]
# Changed exports: [process] (backward compatible)
```

## 6. 效能量測與最佳化

元件組合的開銷主要來自介面轉換：

```rust
// 效能測試：跨元件呼叫開銷
fn benchmark_cross_component(engine: &Engine) {
    let iterations = 100_000;
    let start = std::time::Instant::now();

    for i in 0..iterations {
        // 每次呼叫都跨越 WASM 元件邊界
        let result = call_component_function(engine, i);
        std::hint::black_box(result);
    }

    let elapsed = start.elapsed();
    println!(
        "Cross-component call overhead: {:.2} ns/call",
        elapsed.as_nanos() as f64 / iterations as f64
    );
}
```

在 wasmtime 上，跨元件呼叫的開約為 **50-100 ns**——比 gRPC 微服務的毫秒級延遲快 10,000 倍以上。

## 7. 結語

WASM Component Model 不僅是技術規範，更是軟體架構的重新思考。它讓我們能夠以元件為單位思考軟體設計，而不是以服務或函式庫為單位。結合 WIT 的型別安全性、版本管理、和多語言支援，元件模型正在成為現代軟體工程的核心基礎設施。

---

## 延伸閱讀

- [cargo-component 官方指南](https://www.google.com/search?q=cargo-component+guide)
- [wasm-tools 元件組合文件](https://www.google.com/search?q=wasm+tools+component+composition)
- [WIT 介面設計最佳實務](https://www.google.com/search?q=WIT+interface+design+best+practices)
- [WASM 元件註冊表](https://www.google.com/search?q=WASM+component+registry)
