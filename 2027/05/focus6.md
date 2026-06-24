# 跨語言互通：WASM 作為通用膠水（2020-2026）

## 語言藩籬的終結者

WASM Component Model 最引人注目的應用之一，是作為「跨語言通用膠水」——讓不同程式語言撰寫的模組可以在同一個程序內直接互相呼叫，無需序列化、無需網路通訊、無需共享記憶體的複雜約定。

### WASM 作為通用膠水的設計哲學

傳統的跨語言呼叫方案各有缺點：

```
跨語言方案的歷史演進：
─────────────────────────

JNI (Java Native Interface):
  Java ←→ C/C++
  └── 複雜、不安全、平台特定

FFI (Foreign Function Interface):
  Python ←→ C/Rust
  └── 依賴平台 ABI、編譯環境複雜

gRPC (微服務):
  Python → protobuf → JSON → Node.js
  └── 網路開銷、序列化成本

Shared Memory:
  Process A → mmap → Process B
  └── 同步複雜、無型別安全

──────── 分隔線以上 vs WASM Component Model ────────

WASM Component Model:
  Rust 元件 ──┐
               ├── WIT 定義 → 自動型別轉換 → 直接呼叫
  Python 元件 ─┘
  └── 統一格式、語言中立、無網路開銷、型別安全
```

WASM 的關鍵優勢在於：**所有語言都編譯到同一個中間表示**。不管原始語言是 Rust、Go、Python 還是 C，最終的 WASM 二進制都使用相同的指令集、記憶體模型、和呼叫約定。這意味著語言之間的介面不再是「語言 A 的 ABI 如何對應到語言 B」，而是「每個語言的 WASM 編譯器如何實作 WIT 定義的介面」。

### 從 Python 呼叫 Rust WASM 元件

Python 生態中，`wasmtime-py` 提供了在 Python 中載入和執行 WASM 元件的能力。

```wit
// math.wit — 介面定義
package example:math;

interface types {
    record matrix {
        data: list<f32>,
        rows: u32,
        cols: u32,
    }
}

world inference {
    export matmul: func(a: matrix, b: matrix) -> matrix;
    export relu: func(x: matrix) -> matrix;
}
```

```rust
// Rust 實作 — 編譯為 wasm32-wasip2
wit_bindgen::generate!({ path: "./math.wit" });

struct MathEngine;

impl Guest for MathEngine {
    fn matmul(a: Matrix, b: Matrix) -> Matrix {
        // 高效能矩陣乘法實作
        // ...
    }
    fn relu(x: Matrix) -> Matrix {
        Matrix {
            data: x.data.into_iter().map(|v| v.max(0.0)).collect(),
            rows: x.rows,
            cols: x.cols,
        }
    }
}

export!(MathEngine);
```

```python
# Python 主機端 — 載入 WASM 元件
import numpy as np
from wasmtime import Component, Store, Linker, Engine

# 載入 Rust 編譯的 WASM 元件
engine = Engine()
component = Component.from_file(engine, "math_engine.wasm")
store = Store(engine)
linker = Linker(engine)

# 實例化元件
instance = linker.instantiate(store, component)

# 取得元件匯出的函數
matmul = instance.exports(store)["matmul"]
relu = instance.exports(store)["relu"]

# 準備資料 — 自動轉換為 WASM 型別
a = Matrix(data=[1.0, 2.0, 3.0, 4.0], rows=2, cols=2)
b = Matrix(data=[5.0, 6.0, 7.0, 8.0], rows=2, cols=2)

# 呼叫 Rust 函數（零序列化開銷）
result = matmul(store, a, b)

# 轉回 numpy 陣列
output = np.array(result.data).reshape(result.rows, result.cols)
print(f"Result:\n{output}")

# 應用 ReLU
activated = relu(store, result)
print(f"After ReLU: {activated}")
```

```
執行流程：
─────────────────────────

Python 呼叫 Rust WASM 的資料流：

Python 側：
  numpy array (2x2) ──► WIT 自動轉換 ──► matrix {data: list<f32>, rows: u32, cols: u32}
                                             │
WASM 邊界（sandbox）                          │
                                             ▼
Rust 側：
  matrix {data: Vec<f32>, rows: u32, cols: u32} ──► 矩陣乘法 ──► matrix {data: Vec<f32>, ...}
                                             │
                                             ▼
Python 側：
  matrix {data: list<f32>, ...} ──► WIT 自動轉換 ──► numpy array (2x2)

整個過程：
- 無網路 I/O
- 無序列化（型別在編譯期決定）
- 無記憶體複製（所有資料在 WASM 線性記憶體中）
```

### 從 JavaScript 呼叫 Rust WASM

瀏覽器環境中的跨語言呼叫是 WASM 最初的應用場景。`wasm-bindgen` 讓 JS 與 Rust 之間的互動變得很自然：

```rust
// Rust 端 — 影像處理函數
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub struct ImageProcessor {
    width: u32,
    height: u32,
    pixels: Vec<u8>,
}

#[wasm_bindgen]
impl ImageProcessor {
    #[wasm_bindgen(constructor)]
    pub fn new(width: u32, height: u32) -> ImageProcessor {
        ImageProcessor {
            width,
            height,
            pixels: vec![0u8; (width * height * 4) as usize],
        }
    }

    /// 應用高斯模糊
    pub fn gaussian_blur(&mut self, radius: u32) {
        // 高效能模糊實作
    }

    /// 轉為灰階
    pub fn to_grayscale(&mut self) {
        for chunk in self.pixels.chunks_exact_mut(4) {
            let gray = (0.299 * chunk[0] as f32
                + 0.587 * chunk[1] as f32
                + 0.114 * chunk[2] as f32) as u8;
            chunk[0] = gray;
            chunk[1] = gray;
            chunk[2] = gray;
        }
    }

    pub fn get_pixels(&self) -> Vec<u8> {
        self.pixels.clone()
    }
}
```

```javascript
// JavaScript 端 — 載入 WASM 模組
import init, { ImageProcessor } from "./wasm_image_processor.js";

async function processImage() {
    await init();  // 初始化 WASM

    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");
    const imageData = ctx.getImageData(0, 0, 800, 600);

    // 建立 Rust 處理器
    const processor = new ImageProcessor(800, 600);
    processor.gaussian_blur(3);
    processor.to_grayscale();

    // 取回處理後的像素
    const processed = processor.get_pixels();
    imageData.data.set(processed);
    ctx.putImageData(imageData, 0, 0);
}
```

```
JS ↔ Rust WASM 的型別轉換成本：
─────────────────────────────────

數值操作（i32 / f64）:
  零成本 — 直接對應到 WebAssembly 值

字串傳遞:
  JS (UTF-16) ──► WASM (UTF-8) ──► Rust (String)
  成本：編碼轉換 + 記憶體配置

Buffers (Uint8Array ↔ Vec<u8>):
  成本：一次記憶體複製（如果使用共享陣列緩衝則為零複製）

JavaScript 閉包:
  JS Closure ──► wasm-bindgen ──► Rust
  成本：動態調度 + V8 與 WASM 之間的轉換
```

### 實戰案例：多語言資料管線

以下是一個真實的資料管線案例，結合了 Python（資料載入與視覺化）、Rust（高效能計算）、JavaScript（網頁前端）：

```
每日資料處理管線：
─────────────────────────

                      資料來源（CSV / Parquet）
                              │
                              ▼
              ┌─────────────────────────────┐
              │ 步驟 1：資料載入與清理         │
              │ 語言：Python                  │
              │ 工具：Pandas（`wasmtime-py`） │
              │ 輸出：WASM 相容格式            │
              └──────────────┬──────────────┘
                              │
                              ▼
              ┌─────────────────────────────┐
              │ 步驟 2：資料轉換             │
              │ 語言：Rust（編譯為 WASM）    │
              │ 工作：資料正規化、過濾、聚合   │
              │ 輸出：WASM 元件              │
              └──────────────┬──────────────┘
                              │
                    （WASM 元件組合）
                              │
                              ▼
              ┌─────────────────────────────┐
              │ 步驟 3：統計分析             │
              │ 語言：Rust（編譯為 WASM）    │
              │ 工作：迴歸分析、聚類          │
              │ 輸出：分析結果                │
              └──────────────┬──────────────┘
                              │
                              ▼
              ┌─────────────────────────────┐
              │ 步驟 4：結果視覺化           │
              │ 語言：Python + JavaScript    │
              │ 工具：Plotly / D3.js         │
              │ 輸出：網頁儀表板              │
              └─────────────────────────────┘
```

```bash
# 管線執行腳本
python step1_load.py && \
  wasmtime run --component step2_transform.wasm && \
  wasmtime run --component step3_analyze.wasm && \
  python step4_visualize.py
```

這種架構的關鍵收益：

| 面向 | 傳統微服務架構 | WASM 元件架構 |
|------|---------------|---------------|
| **通訊方式** | HTTP/gRPC（序列化開銷） | 程序內直接呼叫（無序列化） |
| **部署單元** | Docker 容器（~100MB） | WASM 模組（~100KB） |
| **語言選擇** | 整個服務一種語言 | 每個元件獨立選擇語言 |
| **啟動時間** | 數秒到數分鐘 | 微秒到毫秒 |
| **隔離模型** | 行程級（OS 調度） | 語言級（WASM 沙箱） |

WASM 作為通用膠水的願景正在實現。它不只是一個編譯目標——而是一個讓不同語言生態系統能夠無縫協作的標準化層。這對於現代軟體開發中的多語言協作有著深遠的影響。

---

## 延伸閱讀

- [wasmtime-py](https://www.google.com/search?q=wasmtime+Python)
- [wasm-bindgen + JavaScript](https://www.google.com/search?q=wasm-bindgen+JavaScript)
- [WASM 跨語言互通](https://www.google.com/search?q=WASM+cross+language+interoperability)
- [WIT 語言綁定](https://www.google.com/search?q=WIT+bindings+generation)
- [WASM 資料管線](https://www.google.com/search?q=WASM+data+pipeline+pattern)

---

*本篇文章為「AI 程式人雜誌 2026 年 7 月號」WASM 系列之六。*
