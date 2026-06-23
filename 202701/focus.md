# 本期焦點

## Rust 與機器學習推論 — 從框架到邊緣部署

### 引言

機器學習模型的訓練由 Python 主宰——PyTorch、TensorFlow、JAX 提供了無可匹敵的靈活性。但**部署推論**是另一個故事。當模型訓練完成，需要被整合到生產環境、嵌入式系統或瀏覽器中時，Rust 展現了獨特的優勢。

Rust 的 ML 推論生態在 2024-2026 年間快速成熟。Candle、Burn、tract 等框架讓 Rust 開發者可以在沒有 Python 執行期的環境中執行 ML 模型，同時享受 Rust 的記憶體安全、零成本抽象和跨平台能力。這對於邊緣運算、嵌入式 AI 和延遲敏感的應用至關重要。

本期將帶領你探索 Rust 的 ML 推論生態，從最底層的張量運算開始，逐步構建出完整的推論管線，最後探討如何在邊緣裝置上部署量化模型。

---

## 大綱

* [程式：實作 mini-ml — 從零開始的推論引擎](focus_code.md)
   - 張量（Tensor）實作
   - 線性層與激勵函式
   - 前向傳播
   - 模型序列化

1. [Rust ML 生態總覽（2022-2026）](focus1.md)
   - Candle、Burn、tract 的定位
   - 何時用 Rust 做 ML，何時用 Python
   - Rust 在 ML 推論中的優勢

2. [Candle 框架（2023-2026）](focus2.md)
   - 輕量級 ML 框架設計哲學
   - 支援的模型架構
   - 從 PyTorch 移植到 Candle

3. [Burn — 可組合的深度學習（2023-2026）](focus3.md)
   - Burn 的後端抽象設計
   - 自訂模型與訓練
   - WGPU 後端與 GPU 推論

4. [tract — ONNX 推論引擎（2021-2026）](focus4.md)
   - ONNX 格式與跨框架互通
   - tract 的載入與執行
   - 優化與量化

5. [邊緣裝置 ML 推論（2023-2026）](focus5.md)
   - 嵌入式裝置上的模型執行
   - 微控制器 ML（TFLite Micro vs Rust）
   - 感測器資料處理管線

6. [量化與模型最佳化（2022-2026）](focus6.md)
   - FP32 → FP16 → INT8 量化
   - 模型剪枝與蒸餾
   - Rust 在模型最佳化工具中的角色

7. [AI 輔助 Rust 開發（2024-2026）](focus7.md)
   - 用 LLM 生成 Rust ML 程式碼
   - 自動化模型綁定生成
   - Rust 作為 AI 基礎設施語言

---

## ML 推論部署層次

```
Python 訓練 (PyTorch / TensorFlow)
      │  ONNX 匯出 / 權重轉換
Rust 推論引擎 (Candle / Burn / tract)
      │
邊緣裝置 (Raspberry Pi / 手機)
      │
嵌入式 MCU (Cortex-M / RISC-V)
```

## 濃縮回顧

### Rust ML 生態的里程碑

- **2021**：tract 發布，成為第一個純 Rust ONNX 推論引擎
- **2022**：Burn 框架誕生，主打可組合的深度學習
- **2023**：Candle 由 Hugging Face 發布，輕量無依賴設計
- **2024**：Candle 支援 LLaMA、Whisper 等主流模型
- **2025**：Burn 的 WGPU 後端成熟，GPU 推論無縫支援
- **2026**：Rust ML 生態已能覆蓋大部分推論場景

### 為什麼用 Rust 做 ML 推論？

| 需求 | Python | Rust |
|------|--------|------|
| 冷啟動時間 | 數百毫秒（含直譯器啟動） | 微秒級 |
| 二進位大小 | 需 Python 執行期（數十 MB） | 單一靜態二進位（數 MB） |
| 記憶體使用 | 高（GC + 動態型別） | 精確控制 |
| 跨平台部署 | 需 Python 環境 | 交叉編譯任意目標 |
| 併發推論 | GIL 限制 | 無開銷併發 |
| 嵌入式支援 | 有限 | no_std 裸機 |

### 張量：ML 的核心資料結構

張量（Tensor）是多維陣列，是所有 ML 運算的基礎：

```rust
struct Tensor {
    data: Vec<f32>,
    shape: Vec<usize>,
}

impl Tensor {
    fn new(data: Vec<f32>, shape: Vec<usize>) -> Self {
        assert_eq!(data.len(), shape.iter().product());
        Tensor { data, shape }
    }

    fn matmul(&self, other: &Tensor) -> Tensor {
        // 矩陣乘法實作
    }

    fn relu(&self) -> Tensor {
        Tensor::new(
            self.data.iter().map(|&x| x.max(0.0)).collect(),
            self.shape.clone(),
        )
    }
}
```

### 線性層與前向傳播

一個簡單的神經網路由線性層（權重矩陣 + 偏置）和激勵函式組成：

```rust
struct Linear {
    weight: Tensor,  // [out_features, in_features]
    bias: Tensor,    // [out_features]
}

impl Linear {
    fn forward(&self, input: &Tensor) -> Tensor {
        // output = input @ weight.T + bias
        let mut output = input.matmul(&self.weight.transpose());
        output.add_bias(&self.bias);
        output.relu()
    }
}
```

### Candle 的設計哲學

Candle 的核心理念是「最小依賴」：

```rust
// Candle 風格的模型定義
struct Linear {
    weight: Tensor,
    bias: Tensor,
}

impl Linear {
    fn forward(&self, x: &Tensor) -> Tensor {
        x.matmul(&self.weight.t())? + &self.bias
    }
}
```

Candle 不需要 CUDA、cuDNN 或任何 C++ 函式庫，只需要 Rust 編譯器。這使得它在邊緣部署場景中極具吸引力。

### 量化：讓模型在邊緣運行

量化是將 FP32 權重轉換為 INT8 以減少模型大小和加速推論的技術：

```rust
// INT8 量化示意
struct QuantizedLinear {
    weight_i8: Vec<i8>,      // 量化後的權重
    scale: f32,              // 縮放因子
    bias: Vec<f32>,          // 偏置（保持 FP32）
}

impl QuantizedLinear {
    fn forward(&self, input: &[f32]) -> Vec<f32> {
        // input @ weight_i8 使用 INT8 矩陣乘法
        // 結果乘以 scale
        // 加上 bias
    }
}
```

量化可以將模型大小減少 4 倍，在支援 INT8 指令的硬體上推論速度提升 2-3 倍。

---

**下一步**：[程式實作](focus_code.md) → [Rust ML 生態總覽](focus1.md)

## 延伸閱讀

- [Candle 框架](https://www.google.com/search?q=Candle+ML+framework+Rust)
- [Burn 深度學習框架](https://www.google.com/search?q=Burn+deep+learning+Rust)
- [tract ONNX 推論](https://www.google.com/search?q=tract+ONNX+Rust)
- [HuggingFace Candle 範例](https://www.google.com/search?q=HuggingFace+Candle+examples)
