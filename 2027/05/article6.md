# 跨語言 WASM 開發 — Python/Go/Rust 協作實戰

## 1. 引言

WASM 最強大的特性之一就是「語言中立」。無論您的團隊使用 Rust、Go、Python 還是 TypeScript，每個人都可以用自己最熟悉的語言貢獻 WASM 元件，透過 WIT 介面無縫協作。本文將以一個完整的資料分析管線為例，展示多語言 WASM 元件的協作模式。

## 2. 多語言協作的架構設計

```
多語言 WASM 資料分析管線：
─────────────────────────

Python 元件：資料載入與前處理
    │  介面：source:read(path) → list<record>
    │  優勢：Pandas / NumPy 生態
    ▼
Rust 元件：核心數據處理
    │  介面：process:transform(records) → list<processed>
    │  優勢：高效能、安全、記憶體控制
    ▼
Go 元件：並發聚合與輸出
    │  介面：output:aggregate(results) → report
    │  優勢：goroutine 並發、簡單語法
    ▼
JavaScript 元件：結果視覺化
    介面：visualize:render(report) → html
    優勢：DOM 操作、Canvas/WebGL
```

## 3. 共用 WIT 介面

```wit
// data-pipeline.wit
package org:data-pipeline@0.1.0;

/// 共用型別定義
interface types {
    record data-record {
        id: u64,
        timestamp: u64,
        values: list<f64>,
        metadata: option<string>,
    }

    record processed-record {
        id: u64,
        mean: f64,
        std: f64,
        min: f64,
        max: f64,
        count: u32,
    }

    record report {
        title: string,
        summary: string,
        records: list<processed-record>,
        generated-at: u64,
    }

    variant pipeline-error {
        source-error(string),
        process-error(string),
        output-error(string),
    }
}

/// 資料來源介面（由 Python 實作）
interface source {
    use types.{data-record, pipeline-error};

    read-data: func(path: string, limit: u32)
        -> result<list<data-record>, pipeline-error>;
}

/// 資料處理介面（由 Rust 實作）
interface process {
    use types.{data-record, processed-record, pipeline-error};

    analyze: func(records: list<data-record>)
        -> result<list<processed-record>, pipeline-error>;

    filter: func(records: list<data-record>, min-value: f64)
        -> result<list<data-record>, pipeline-error>;
}

/// 輸出介面（由 Go 實作）
interface output {
    use types.{processed-record, report, pipeline-error};

    generate-report: func(records: list<processed-record>, title: string)
        -> result<report, pipeline-error>;
}

/// 管線主體（JavaScript 協調）
world pipeline-world {
    import source;
    import process;
    import output;

    export run-pipeline: func(data-path: string, report-title: string)
        -> result<report, string>;
}
```

## 4. Rust 元件實作：核心數據處理

```rust
// Rust 元件 — 編譯為 wasm32-wasip2
cargo_component::component!("pipeline-world");

use crate::bindings::org::data_pipeline::{
    types::{DataRecord, ProcessedRecord},
    process::{self, PipelineError},
};

struct DataProcessor;

impl Process for DataProcessor {
    fn analyze(records: Vec<DataRecord>) -> Result<Vec<ProcessedRecord>, PipelineError> {
        let mut results = Vec::with_capacity(records.len());

        for record in records {
            let values = &record.values;
            if values.is_empty() {
                continue;
            }

            let n = values.len() as f64;
            let sum: f64 = values.iter().sum();
            let mean = sum / n;

            let variance = values.iter()
                .map(|v| (v - mean).powi(2))
                .sum::<f64>() / n;
            let std = variance.sqrt();

            let min = values.iter().cloned().fold(f64::INFINITY, f64::min);
            let max = values.iter().cloned().fold(f64::NEG_INFINITY, f64::max);

            results.push(ProcessedRecord {
                id: record.id,
                mean,
                std,
                min,
                max,
                count: values.len() as u32,
            });
        }

        Ok(results)
    }

    fn filter(records: Vec<DataRecord>, min_value: f64) -> Result<Vec<DataRecord>, PipelineError> {
        Ok(records.into_iter()
            .filter(|r| r.values.iter().any(|&v| v >= min_value))
            .collect())
    }
}
```

## 5. Go 元件實作：並發聚合與報表

```go
// Go 元件 — 使用 wazero 或 wasmtime-go
package main

import (
	"fmt"
	"time"
)

// 由 wit-bindgen-go 生成的型別
type ProcessedRecord struct {
	ID    uint64
	Mean  float64
	Std   float64
	Min   float64
	Max   float64
	Count uint32
}

type Report struct {
	Title       string
	Summary     string
	Records     []ProcessedRecord
	GeneratedAt uint64
}

// 使用 goroutine 並發處理
func GenerateReport(records []ProcessedRecord, title string) (*Report, error) {
	// 並發計算統計數據
	type stats struct {
		totalRecords uint32
		totalValues  uint32
		globalMean   float64
	}

	ch := make(chan stats, 1)
	go func() {
		var s stats
		for _, r := range records {
			s.totalRecords++
			s.totalValues += r.Count
			s.globalMean += r.Mean * float64(r.Count)
		}
		if s.totalValues > 0 {
			s.globalMean /= float64(s.totalValues)
		}
		ch <- s
	}()

	// 主 goroutine 繼續準備報告
	result := <-ch
	summary := fmt.Sprintf(
		"Processed %d records with %d total values. Global mean: %.2f",
		result.totalRecords, result.totalValues, result.globalMean,
	)

	report := &Report{
		Title:       title,
		Summary:     summary,
		Records:     records,
		GeneratedAt: uint64(time.Now().Unix()),
	}

	return report, nil
}
```

## 6. Python 主機端協調

```python
# Python 主機 — 使用 wasmtime-py 載入並協調多語言元件
import asyncio
from wasmtime import Component, Store, Linker, Engine
from typing import List

class PipelineRunner:
    """多語言 WASM 管線協調器"""

    def __init__(self):
        self.engine = Engine()
        self.linker = Linker(self.engine)
        self.store = Store(self.engine)

    def load_components(self, components: dict):
        """載入多個 WASM 元件"""
        for name, path in components.items():
            component = Component.from_file(self.engine, path)
            self.linker.define_component(self.store, name, component)

    def run_pipeline(self, data_path: str) -> dict:
        """執行完整資料管線"""
        # 步驟 1：Python 讀取資料
        raw_data = self.load_data_with_pandas(data_path)

        # 步驟 2：將資料傳遞給 Rust 元件進行分析
        rust_component = Component.from_file(
            self.engine, "rust-processor.wasm"
        )
        rust_instance = self.linker.instantiate(self.store, rust_component)
        processed = rust_instance.exports(self.store)["analyze"](
            self.store, raw_data
        )

        # 步驟 3：將結果傳遞給 Go 元件生成報告
        go_component = Component.from_file(
            self.engine, "go-reporter.wasm"
        )
        go_instance = self.linker.instantiate(self.store, go_component)
        report = go_instance.exports(self.store)["generate-report"](
            self.store, processed, "Data Analysis Report"
        )

        return report

    def load_data_with_pandas(self, path: str) -> List[dict]:
        """使用 Pandas 讀取資料"""
        import pandas as pd
        df = pd.read_csv(path)
        records = []
        for _, row in df.iterrows():
            records.append({
                "id": row["id"],
                "timestamp": row["timestamp"],
                "values": [float(v) for v in row["values"].split(",")],
                "metadata": row.get("metadata", None),
            })
        return records


async def main():
    runner = PipelineRunner()
    runner.load_components({
        "rust-processor": "rust-processor.wasm",
        "go-reporter": "go-reporter.wasm",
    })
    report = runner.run_pipeline("data/sample.csv")
    print(f"Report: {report['title']}")
    print(f"Summary: {report['summary']}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 7. GitLab CI 多語言建置管線

```yaml
# .gitlab-ci.yml — 多語言 WASM 元件建置
stages:
  - build-rust
  - build-go
  - compose
  - test

build-rust:
  stage: build-rust
  image: rust:latest
  script:
    - rustup target add wasm32-wasip2
    - cargo component build --release
    - cp target/wasm32-wasip2/release/rust_processor.wasm dist/
  artifacts:
    paths:
      - dist/rust_processor.wasm

build-go:
  stage: build-go
  image: golang:latest
  script:
    - go install github.com/bytecodealliance/wit-bindgen-go/cli/wit-bindgen-go@latest
    - tinygo build -o dist/go_reporter.wasm -target=wasi ./cmd/reporter
  artifacts:
    paths:
      - dist/go_reporter.wasm

compose:
  stage: compose
  script:
    - wasm-tools compose -o dist/pipeline.wasm \
        dist/rust_processor.wasm \
        dist/go_reporter.wasm

test:
  stage: test
  script:
    - python3 -m pytest tests/
    - wasmtime run --component dist/pipeline.wasm --invoke run-pipeline
```

## 8. 跨語言協作的挑戰與解決方案

| 挑戰 | 說明 | 解決方案 |
|------|------|----------|
| **型別系統差異** | 不同語言的型別系統差異（如 Rust 的 Option vs Go 的 nil） | WIT 定義明確的 optional 和 variant 型別，wit-bindgen 自動處理轉換 |
| **記憶體管理** | WASM 共享線性記憶體，GC vs 手動管理 | Component Model 的 Canonical ABI 定義了統一的記憶體配置協議 |
| **錯誤處理** | Rust 的 Result vs Go 的 error vs Python 的 Exception | WIT 的 `result<T, E>` 型別統一了錯誤處理模式 |
| **非同步模型** | Rust 的 async/await vs Go 的 goroutine vs Python 的 asyncio | WASI Preview 2 的 stream 和 future 提供了統一的非同步抽象 |
| **套件管理** | 各語言有不同的套件生態 | WIT 的語義化版本管理和 WASM Registry 提供統一的套件管理 |

## 9. 結語

跨語言 WASM 開發不僅是技術可能性，更是現實需求。在大型專案中，不同團隊可能使用不同的語言，WASM 提供了讓這些語言在單一程序內協作的標準化層。2026 年，隨著 wit-bindgen 對更多語言的支援成熟和 WASM Registry 的普及，多語言 WASM 元件協作將成為企業級應用的標準架構。

---

## 延伸閱讀

- [wit-bindgen 多語言支援](https://www.google.com/search?q=wit-bindgen+multi+language)
- [wasmtime-py 文件](https://www.google.com/search?q=wasmtime+Python+API)
- [TinyGo WASM 支援](https://www.google.com/search?q=TinyGo+WASM+support)
- [多語言 WASM 元件組合案例](https://www.google.com/search?q=multi+language+WASM+component+composition)
