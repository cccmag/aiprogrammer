# LLM 生成神經網路架構：從描述到程式碼

## 前言

大型語言模型（LLM）不僅可以撰寫文章和程式碼，還能設計神經網路架構。給定自然語言描述，LLM 可以生成對應的 Rust 深度學習程式碼——包括張量運算、層的定義、前向傳播邏輯等。這大幅降低了深度學習框架的入門門檻。

本文探討如何使用 LLM 從描述生成神經網路架構程式碼，以及如何驗證生成結果的正確性。

## 從描述到架構

### 提示詞工程（Prompt Engineering）

生成可編譯的 Rust 深度學習程式碼，需要精心設計提示詞：

```
你是一個 Rust 深度學習框架的專家。請根據以下描述生成程式碼。

描述：一個兩層的多層感知器（MLP），輸入維度 784，
隱藏層維度 256 使用 ReLU 激活函數，輸出維度 10 使用 softmax。
使用 Candle 框架。

要求：
1. 完整的 struct 定義和 impl 區塊
2. forward 方法
3. 型別安全，使用 candle_core::Result
4. 加上 #[derive] 和必要的 use 陳述
```

LLM 回傳的程式碼：

```rust
use candle_core::{Device, Result, Tensor};
use candle_nn::{linear, Activation, Linear, VarBuilder};

pub struct MLP {
    fc1: Linear,
    fc2: Linear,
}

impl MLP {
    pub fn new(vb: VarBuilder) -> Result<Self> {
        let fc1 = linear(784, 256, vb.pp("fc1"))?;
        let fc2 = linear(256, 10, vb.pp("fc2"))?;
        Ok(MLP { fc1, fc2 })
    }

    pub fn forward(&self, x: &Tensor) -> Result<Tensor> {
        let x = self.fc1.forward(x)?.relu()?;
        let x = self.fc2.forward(&x)?;
        candle_nn::ops::log_softmax(&x, 1)
    }
}
```

### 程式碼生成策略

| 策略 | 描述 | 適用場景 |
|------|------|---------|
| Zero-shot | 直接給出描述 | 簡單架構（MLP、CNN） |
| Few-shot | 提供數個範例 | 複雜或自訂架構 |
| Chain-of-Thought | 逐步推理架構設計 | 新穎/研究性架構 |
| 迭代改善 | 編譯錯誤回饋 LLM | 除錯與修正 |

## 案例：生成 ResNet 區塊

給予 Candle 框架的 ResNet 區塊描述：

```rust
// LLM 生成的 BasicBlock
use candle_core::{Result, Tensor};
use candle_nn::{conv2d, Conv2d, BatchNorm, batch_norm, Activation};

pub struct BasicBlock {
    conv1: Conv2d,
    bn1: BatchNorm,
    conv2: Conv2d,
    bn2: BatchNorm,
    shortcut: Option<Conv2d>,
    stride: usize,
}

impl BasicBlock {
    pub fn new(
        in_planes: usize,
        planes: usize,
        stride: usize,
        vb: candle_nn::VarBuilder,
    ) -> Result<Self> {
        let conv1 = conv2d(in_planes, planes, 3, stride, 1, vb.pp("conv1"))?;
        let bn1 = batch_norm(planes, 1e-5, vb.pp("bn1"))?;
        let conv2 = conv2d(planes, planes, 3, 1, 1, vb.pp("conv2"))?;
        let bn2 = batch_norm(planes, 1e-5, vb.pp("bn2"))?;

        let shortcut = if stride != 1 || in_planes != planes {
            Some(conv2d(in_planes, planes, 1, stride, 0, vb.pp("shortcut"))?)
        } else {
            None
        };

        Ok(BasicBlock { conv1, bn1, conv2, bn2, shortcut, stride })
    }

    pub fn forward(&self, x: &Tensor) -> Result<Tensor> {
        let residual = x.clone();
        let x = self.conv1.forward(x)?;
        let x = self.bn1.forward(&x)?;
        let x = x.relu()?;
        let x = self.conv2.forward(&x)?;
        let x = self.bn2.forward(&x)?;

        let residual = match &self.shortcut {
            Some(conv) => conv.forward(&residual)?,
            None => residual,
        };

        (x + residual)?.relu()
    }
}
```

## 驗證生成的架構

生成程式碼後，必須驗證其正確性。驗證分為三個層次：

### 層次一：編譯檢查

```rust
// 在專案中編譯生成的程式碼
// 使用 cargo check 驗證型別正確
fn test_mlp_compiles() {
    let dev = Device::Cpu;
    let vb = candle_nn::VarBuilder::new(
        &[], candle_core::DType::F32, &dev
    );
    let mlp = MLP::new(vb).unwrap();
    let x = Tensor::randn(0f32, 1.0, (1, 784), &dev).unwrap();
    let y = mlp.forward(&x).unwrap();
    assert_eq!(y.dims(), &[1, 10]);
}
```

### 層次二：形狀一致性

生成程式必須確保所有張量形狀在傳播時一致：

```rust
fn verify_shapes(model: &MLP, input_shape: &[usize]) -> Result<()> {
    let dev = Device::Cpu;
    let x = Tensor::randn(0.0, 1.0, input_shape, &dev)?;
    let output = model.forward(&x)?;

    // 檢查輸出形狀是否符合預期
    let expected_output = &[input_shape[0], 10];
    assert_eq!(output.dims(), expected_output,
        "Output shape mismatch: expected {:?}, got {:?}",
        expected_output, output.dims());
    Ok(())
}
```

### 層次三：語意正確性

最嚴格的驗證：與參考實作（如 PyTorch）的輸出一致：

```rust
fn verify_semantics() -> Result<()> {
    // 1. 在 PyTorch 中定義相同架構並匯出權重
    // 2. 在 Rust/Candle 中載入相同權重
    // 3. 對相同輸入進行推論
    // 4. 比較輸出（允許少量浮點誤差）

    let dev = Device::Cpu;
    let vb = candle_nn::VarBuilder::from_safetensors(
        &["pytorch_weights.safetensors"],
        candle_core::DType::F32,
        &dev,
    )?;

    let model = MLP::new(vb)?;

    // 使用固定種子確保可重現
    let input = Tensor::arange(0f32, 784.0, &dev)?.reshape((1, 784))?;
    let output = model.forward(&input)?;

    // 從 PyTorch 匯出的參考輸出
    let expected = Tensor::read_file("expected_output.npy", &dev)?;
    let diff = (output - expected)?.abs()?.sum_all()?;

    assert!(diff.to_scalar::<f32>()? < 0.01,
        "Semantic mismatch: diff={}", diff.to_scalar::<f32>()?);
    Ok(())
}
```

## 進階：LLM 生成客製化運算

不僅是標準層，LLM 也可以生成全新的自訂運算：

```rust
// 提示詞：實現一個客製化的 GELU 激活函數
// 使用 x * 0.5 * (1 + tanh(sqrt(2/pi) * (x + 0.044715 * x^3)))

fn custom_gelu(x: &Tensor) -> Result<Tensor> {
    const SQRT_2_OVER_PI: f64 = 0.7978845608028654;
    let x3 = (x * x)? * x?;
    let inner = x + (x3 * 0.044715)?;
    let tanh = (inner * SQRT_2_OVER_PI)?.tanh()?;
    x * (tanh + 1.0)? * 0.5
}
```

LLM 生成的程式碼可以直接整合進 Candle 或 Burn 的運算圖中。

## 工具：Candle x LLM 整合

```rust
// 一個範例工具：從 YAML 描述生成 Candle 模型
use serde::Deserialize;

#[derive(Deserialize)]
struct ArchSpec {
    name: String,
    layers: Vec<LayerSpec>,
}

#[derive(Deserialize)]
#[serde(tag = "type")]
enum LayerSpec {
    Linear { in_features: usize, out_features: usize },
    Conv2d { in_channels: usize, out_channels: usize,
             kernel_size: usize, stride: usize },
    Relu,
    Flatten,
}

fn generate_model(spec: &ArchSpec) -> String {
    // 將 spec 轉為 LLM 提示詞
    let prompt = format!(
        "Generate a Candle model struct named {} with:\n{:?}",
        spec.name, spec.layers
    );
    // 呼叫 LLM API 取得生成的程式碼
    // llm_call(&prompt)
    todo!()
}
```

## 限制與挑戰

| 挑戰 | 說明 | 緩解方案 |
|------|------|---------|
| 幻覺（Hallucination） | LLM 可能產生不存在的 API | 編譯驗證、few-shot |
| 不一致的維度 | 層之間維度不匹配 | 自動形狀推斷檢查 |
| 效能陷阱 | 生成的程式碼可能效能不佳 | 程式碼審查、benchmark |
| 安全性 | 生成包含惡意程式碼 | 沙箱執行、權限限制 |

## 總結

LLM 生成神經網路架構程式碼的能力正在快速進步。對 Candle/Burn 等 Rust 框架而言，LLM 可以：
1. 從自然語言描述生成完整的模型定義
2. 幫助初學者跨越 API 學習曲線
3. 自動化架構搜尋（NAS）過程
4. 生成測試用例驗證正確性

--- 

**參考資料**

- https://www.google.com/search?q=LLM+generate+neural+network+architecture+code
- https://www.google.com/search?q=Candle+LLM+code+generation
- https://www.google.com/search?q=LLM+for+model+architecture+search
- https://www.google.com/search?q=prompt+engineering+deep+learning+Rust
- https://www.google.com/search?q=verifying+LLM+generated+ML+code
