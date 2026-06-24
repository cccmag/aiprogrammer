# WASM 工具鏈 — wasm-pack, wit-bindgen, cargo-component

## 1. 引言

Rust 在 WASM 生態中的主導地位，很大程度上歸功於其完備的工具鏈。從編譯、綁定生成、最佳化到部署，一套成熟的工具鏈讓開發者可以專注於業務邏輯，而非底層的 WASM 細節。本文將詳細介紹三組核心工具：wasm-pack（瀏覽器 WASM）、wit-bindgen（介面綁定）、cargo-component（元件建置）。

## 2. wasm-pack：瀏覽器 WASM 的瑞士軍刀

### 2.1 工作流程

```
wasm-pack 的內部流程：
─────────────────────────

開發者寫 Rust 程式碼
    │
    ▼
wasm-pack build
    │
    ├── 1. 呼叫 cargo build --target wasm32-unknown-unknown
    │      輸出：.wasm 二進制
    │
    ├── 2. 呼叫 wasm-bindgen
    │      輸入：.wasm + Rust 元資料
    │      輸出：JS 膠水程式碼 + TypeScript 定義
    │
    ├── 3. 呼叫 wasm-opt（可選）
    │      輸出：最佳化後的 .wasm
    │
    └── 4. 生成 package.json + .d.ts
        輸出：pkg/ 目錄（可直接發布到 npm）
```

### 2.2 進階建置策略

```bash
# 1. 多目標同時建置
wasm-pack build --target web --out-dir pkg/web
wasm-pack build --target nodejs --out-dir pkg/node
wasm-pack build --target bundler --out-dir pkg/bundler

# 2. 啟用除錯符號
wasm-pack build --debug --out-dir pkg/debug

# 3. 自訂 wasm-opt 選項
wasm-pack build \
    --target web \
    --out-dir pkg/optimized \
    -- \
    -Z wasm-opt=Oz \
    --features "optimize-size"

# 4. 使用自訂設定檔案
# wasm-pack.toml
[package]
name = "my-wasm-lib"
description = "高性能 WASM 庫"

[build]
target = "web"
out-dir = "pkg"
profiling = false

[wasm-opt]
optimization = "Oz"
debug = false
```

### 2.3 開發環境整合

```json
// package.json — 開發腳本範例
{
  "scripts": {
    "build:wasm": "wasm-pack build --target web",
    "dev": "npm run build:wasm && webpack serve",
    "profile": "wasm-pack build --profiling && wasm-profiler pkg/my_lib_bg.wasm",
    "size": "wasm-pack build --release && wasm-opt -Oz pkg/my_lib_bg.wasm -o pkg/optimized.wasm && gzip -k pkg/optimized.wasm && ls -lh pkg/"
  }
}
```

## 3. wit-bindgen：語言中立的綁定生成器

### 3.1 支援的語言

wit-bindgen 在 2026 年支援以下語言：

| 語言 | 工具 | 狀態 |
|------|------|------|
| Rust | `wit-bindgen` crate | ✅ 生產就緒 |
| Go | `wit-bindgen-go` | ✅ 生產就緒 |
| C/C++ | `wit-bindgen-c` | ✅ 生產就緒 |
| Python | `wit-bindgen-py` | ⚠️ Beta |
| TypeScript | `jco` | ✅ 生產就緒 |
| Kotlin | `wit-bindgen-kt` | ⚠️ Beta |

### 3.2 進階 WIT 模式

```wit
// wasm-ai.wit — AI 推理元件的 WIT 定義
package ai:inference@1.0.0;

/// 張量型別
interface tensor {
    record tensor {
        data: list<u8>,
        shape: list<u32>,
        dtype: data-type,
    }

    enum data-type {
        f32,
        f16,
        i8,
        u8,
        i32,
    }
}

/// 模型管理
interface model {
    use tensor.{tensor};

    record model-metadata {
        name: string,
        version: string,
        input-shape: list<u32>,
        output-shape: list<u32>,
        quantization: option<string>,
    }

    load: func(path: string) -> result<model-metadata, string>;
    unload: func() -> result<(), string>;
}

/// 推理引擎
interface engine {
    use tensor.{tensor, data-type};
    use model.{model-metadata};

    /// 執行推理（支援批次處理）
    infer: func(input: list<tensor>) -> result<list<tensor>, string>;

    /// 取得引擎的後端資訊
    get-backend: func() -> string;
}

/// 完整的推理元件
world inference-world {
    import model;
    import engine;

    export build-pipeline: func(model-path: string) -> result<(), string>;
    export run: func(input: list<tensor>) -> result<list<tensor>, string>;
}
```

### 3.3 實戰：Rust 整合 wit-bindgen

```rust
// 使用 wit-bindgen 生成 Rust 綁定
wit_bindgen::generate!({
    path: "./wit",
    world: "inference-world",
    // 自訂選項
    generate_all,
    std_feature,
    // 跳過預設的 Guest trait 定義
    skip: [],
});

use crate::bindings::ai::inference::{
    tensor::{Tensor, DataType},
    model::ModelMetadata,
    engine,
};

/// 自訂推理元件
struct InferencePipeline {
    model_path: String,
    metadata: Option<ModelMetadata>,
}

impl InferenceWorld for InferencePipeline {
    fn build_pipeline(model_path: String) -> Result<(), String> {
        // 載入模型中繼資料
        let metadata = model::load(&model_path)?;
        println!("Loaded model: {}", metadata.name);
        Ok(())
    }

    fn run(input: Vec<Tensor>) -> Result<Vec<Tensor>, String> {
        // 執行引擎推理
        let outputs = engine::infer(input)?;
        Ok(outputs)
    }
}

export!(InferencePipeline);
```

## 4. cargo-component：元件的專用建置工具

### 4.1 專案管理

```bash
# 建立新的元件專案
cargo component new --lib my-component
cargo component new --lib --target wasm32-wasip2 my-component

# 新增 WIT 依賴
cargo component add --wit wasi:http@0.2.0
cargo component add --wit myorg:data-pipeline@0.1.0

# 建置（自動解析 WIT 依賴）
cargo component build --release

# 測試元件
cargo component test
```

### 4.2 Cargo.toml 設定

```toml
[package]
name = "my-component"
version = "0.1.0"
edition = "2024"

[lib]
crate-type = ["cdylib"]

[dependencies]
wit-bindgen = "0.30"
anyhow = "1"

# WASI 依賴（透過 cargo-component 管理）
[package.metadata.component]
package = "myorg:my-component"
world = "my-world"

[package.metadata.component.dependencies]
"wasi:http" = "0.2.0"
"wasi:logging" = "0.1.0"

[profile.release]
opt-level = "z"
lto = true
strip = true
codegen-units = 1

[lints.rust]
unsafe_code = "forbid"
```

### 4.3 多工作空間管理

```toml
# workspace Cargo.toml
[workspace]
members = [
    "components/data-source",
    "components/data-processor",
    "components/data-output",
    "components/pipeline-orchestrator",
]

[workspace.package]
edition = "2024"

[workspace.dependencies]
wit-bindgen = "0.30"
anyhow = "1"

# 共享 WIT 套件
[workspace.metadata.component.packages]
"org:data-pipeline" = { path = "./wit/data-pipeline" }
"wasi:http" = "0.2.0"
```

## 5. 工具鏈整合實戰

### 5.1 完整的開發工作流程

```bash
#!/bin/bash
# build-and-deploy.sh — 完整的 WASM 元件 CI/CD 流程

set -euo pipefail

echo "=== 1. 安裝工具鏈 ==="
rustup target add wasm32-wasip2
cargo install cargo-component wasm-tools wit-bindgen-cli

echo "=== 2. 建置 WASM 元件 ==="
cargo component build --release

echo "=== 3. 分析二進制大小 ==="
wasm-tools size target/wasm32-wasip2/release/my_component.wasm

echo "=== 4. 驗證元件結構 ==="
wasm-tools validate target/wasm32-wasip2/release/my_component.wasm
wasm-tools component wit target/wasm32-wasip2/release/my_component.wasm

echo "=== 5. 最佳化 ==="
wasm-tools optimize \
    -Oz \
    --enable-multi-memory \
    --strip-debug \
    -o dist/optimized.wasm \
    target/wasm32-wasip2/release/my_component.wasm

echo "=== 6. 執行測試 ==="
wasmtime run --component dist/optimized.wasm --invoke test

echo "=== 完成 ==="
ls -lh dist/
```

### 5.2 工具鏈的未來發展

2026 年的 WASM 工具鏈仍然在快速演進：

| 發展方向 | 說明 | 預計時程 |
|----------|------|----------|
| **統一工具鏈** | cargo-component 整合 wasm-pack 的功能 | 2027 Q1 |
| **WASM Registry** | 統一的 WASM 元件倉儲（類似 npm/crates.io） | 2027 Q2 |
| **IDE 整合** | rust-analyzer 原生支援 WIT 檔案編輯 | 2027 Q1 |
| **除錯體驗** | DWARF→WASM 除錯資訊格式標準化 | 2026 Q4 |
| **AI 輔助工具** | LLM 輔助 WIT 介面設計和綁定生成 | 2027 Q2 |

## 6. 結語

WASM 工具鏈在 2026 年已經足夠成熟，支援從瀏覽器到伺服器的完整開發流程。wasm-pack 專注於瀏覽器環境，cargo-component 專注於元件生態，wit-bindgen 則是語言互通的核心。選擇正確的工具並理解它們的設計哲學，是高效開發 WASM 應用的關鍵。

---

## 延伸閱讀

- [wasm-pack 完整文件](https://www.google.com/search?q=wasm-pack+documentation)
- [cargo-component 使用指南](https://www.google.com/search?q=cargo-component+guide)
- [wit-bindgen 生成器選項](https://www.google.com/search?q=wit-bindgen+code+generation)
- [wasm-tools 命令參考](https://www.google.com/search?q=wasm+tools+cli+reference)
- [WASM 開發工作流程](https://www.google.com/search?q=WASM+development+workflow+Rust)
