# tract ONNX 推論引擎

## ONNX 格式, 載入執行, 最佳化量化（2021-2026）

### 前言

tract 是由 Sonos 開發的純 Rust ONNX 推論引擎，2021 年首次發布。tract 不追求通用 ML 框架的定位，而是專注於 ONNX 格式的載入、最佳化與執行。

### ONNX 格式

ONNX（Open Neural Network Exchange）是微軟和 Facebook 於 2017 年發起的開放模型交換格式：

```
model.onnx
├── IR 版本號
├── 模型元資料（名稱、作者、描述）
├── 計算圖（Graph）
│   ├── 輸入定義（名稱、形狀、型別）
│   ├── 輸出定義
│   ├── 節點列表（Node）
│   │   ├── 算子類型（Conv, MatMul, Relu...）
│   │   ├── 輸入張量名稱
│   │   └── 輸出張量名稱
│   └── 初始值（Initializer = 權重）
```

ONNX 的設計目標是**跨框架互操作**——任何支援 ONNX 匯出的框架都可以互通。

### tract 的載入與執行

tract 提供了一個流暢的 API 來載入和執行 ONNX 模型：

```rust
use tract_onnx::prelude::*;

fn main() -> TractResult<()> {
    // 1. 載入模型
    let model = onnx()
        .model_for_path("mobilenet_v2.onnx")?;

    // 2. 設定輸入規格
    let model = model
        .with_input_fact(0, InferenceFact::dt_shape(
            f32::datum_type(), tvec!(1, 3, 224, 224)
        ))?;

    // 3. 最佳化
    let model = model.into_optimized()?;

    // 4. 轉換為可執行實體
    let engine = model.into_runnable()?;

    // 5. 執行推論
    let input = Tensor::from_shape(&[1, 3, 224, 224])?
        .into_tensor();
    let result = engine.run(tvec!(input))?;

    // 6. 取得輸出
    let output = result[0].to_array_view::<f32>()?;
    println!("預測結果: {:?}", output);
    Ok(())
}
```

### 最佳化管道

tract 內建了多層最佳化：

| 最佳化 | 說明 | 加速效果 |
|--------|------|---------|
| 常數摺疊（Const Fold） | 編譯期計算靜態子圖 | 減少執行期計算 |
| 節點融合（Fusion） | 合併相鄰算子 | 減少記憶體頻寬 |
| 形狀推導（Shape Inference） | 靜態化動態形狀 | 減少執行期分支 |
| 算子簡化（Simplification） | 替換為高效算子 | 提升計算效率 |
| 記憶體規劃（Memory Planning） | 預先分配緩衝區 | 減少配置開銷 |

### 量化支援

tract 支援 ONNX 標準的量化格式：

```rust
// 載入量化模型
let model = onnx()
    .model_for_path("model.quant.onnx")?
    .with_input_fact(0, InferenceFact::dt_shape(
        u8::datum_type(), tvec!(1, 3, 224, 224)
    ))?
    .into_optimized()?
    .into_runnable()?;
```

tract 支援 INT8/INT16/FP16 量化，以及動態/靜態量化模式。

### 生產部署

tract 在生產環境中廣泛使用。Sonos 在其音響產品中使用 tract 執行音訊處理模型。tract 的二進位大小約 2MB（靜態編譯，不含模型權重），非常適合嵌入式設備。

### 小結

tract 是 ONNX 推論的首選 Rust 引擎。如果您的 ML 工作流程已經使用 ONNX 作為交換格式，tract 提供了最直接、最高效的 Rust 部署路徑。

---

**下一步**：[邊緣裝置 ML 推論](focus5.md)

## 延伸閱讀

- [tract documentation](https://www.google.com/search?q=tract+ONNX+Rust+documentation)
- [ONNX format](https://www.google.com/search?q=ONNX+format+specification)
- [tract performance](https://www.google.com/search?q=tract+ONNX+Rust+performance+benchmark)
