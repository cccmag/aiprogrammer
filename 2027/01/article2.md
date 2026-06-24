# Candle 框架實戰 — 輕量推論、Llama/Whisper 支援

## 1. 引言

Candle 是 Hugging Face 推出的輕量級 ML 框架，以「最小依賴」為設計目標。本文將透過實戰案例展示 Candle 的核心用法，包括張量運算、模型載入、以及主流模型（LLaMA、Whisper）的推論實作。

## 2. 張量運算核心

Candle 的張量 API 設計深受 PyTorch 影響：

```rust
use candle_core::{Device, Tensor, DType};

fn tensor_ops() -> Result<(), Box<dyn std::error::Error>> {
    let device = Device::Cpu;
    let a = Tensor::randn(0.0, 1.0, (3, 4), &device)?;
    let b = Tensor::randn(0.0, 1.0, (4, 5), &device)?;

    // 基本運算
    let c = a.matmul(&b)?;                 // 矩陣乘法
    let d = a.sum_all()?;                  // 所有元素和
    let e = a.mean_keepdim(0)?;             // 沿 dim 0 平均
    let f = a.broadcast_add(&Tensor::new(&[1.0, 2.0, 3.0], &device)?)?;  // 廣播加法

    // 形狀操作
    let g = a.reshape((2, 6))?;            // 重塑
    let h = a.transpose(0, 1)?;             // 轉置
    let i = a.unsqueeze(0)?;               // 增加維度

    Ok(())
}
```

## 3. 模型載入

Candle 原生支援 Hugging Face 的 safetensors 格式：

```rust
use candle_core::{Device, Tensor};
use candle_nn::{Linear, VarBuilder, Activation};

struct SimpleModel {
    fc1: Linear,
    fc2: Linear,
}

impl SimpleModel {
    fn new(vb: VarBuilder) -> Result<Self, candle_core::Error> {
        let fc1 = candle_nn::linear(784, 256, vb.pp("fc1"))?;
        let fc2 = candle_nn::linear(256, 10, vb.pp("fc2"))?;
        Ok(Self { fc1, fc2 })
    }

    fn forward(&self, input: &Tensor) -> Result<Tensor, candle_core::Error> {
        let x = input.apply(&self.fc1)?.relu()?;
        self.fc2.forward(&x)
    }
}

fn load_model() -> Result<(), Box<dyn std::error::Error>> {
    let device = Device::Cpu;
    let weights = std::fs::read("model.safetensors")?;
    let vb = VarBuilder::from_safetensors(
        std::collections::HashMap::from([("model.safetensors".to_string(), weights.into())]),
        DType::F32, &device
    )?;
    let model = SimpleModel::new(vb)?;
    Ok(())
}
```

## 4. LLaMA 推論

Candle 內建了 LLaMA 模型的支援：

```rust
use candle_transformers::models::llama as llama_model;
use candle_core::Device;
use tokenizers::Tokenizer;

fn llama_inference() -> Result<(), Box<dyn std::error::Error>> {
    let device = Device::Cpu;
    let tokenizer = Tokenizer::from_file("tokenizer.json")?;

    // 載入 LLaMA 配置與權重
    let config = llama_model::Config::from_file("config.json")?;
    let weights = std::fs::read("model.safetensors")?;
    let vb = VarBuilder::from_safetensors(/* ... */)?;
    let mut llama = llama_model::Llama::new(config, vb)?;

    // 編碼輸入
    let prompt = "Rust 是";
    let tokens = tokenizer.encode(prompt, true)?;
    let input = Tensor::new(&tokens.get_ids(), &device)?.unsqueeze(0)?;

    // 自回歸生成
    let output = llama.forward(&input, 0)?;
    let next_token = output.squeeze(0)?.argmax(1)?.to_scalar::<u32>()?;

    println!("下一個 token id: {}", next_token);
    Ok(())
}
```

## 5. Whisper 語音辨識

Candle 的 Whisper 實作讓語音辨識可以在本地端完成：

```rust
use candle_transformers::models::whisper as whisper_model;
use candle_core::Device;

fn whisper_transcribe(
    audio_path: &str
) -> Result<String, Box<dyn std::error::Error>> {
    let device = Device::Cpu;

    // 載入 Whisper 模型（tiny/base/small/medium/large）
    let model = whisper_model::Whisper::new(
        &whisper_model::Config::tiny_en(),
        VarBuilder::from_safetensors(/* ... */)?,
        &device
    )?;

    // 讀取並預處理音訊
    let audio = read_wav(audio_path)?;
    let mel = whisper_model::mel_filter(audio, &model.config)?;

    // 執行辨識
    let tokens = model.forward(&mel.unsqueeze(0)?)?;
    let text = decode_tokens(&tokens)?;

    Ok(text)
}
```

## 6. 在邊緣裝置上的部署

Candle 在 Raspberry Pi 上的部署非常直接：

```bash
# 交叉編譯
cargo build --target aarch64-unknown-linux-gnu --release

# 複製到裝置
scp target/aarch64-unknown-linux-gnu/release/myapp pi@raspberrypi:~
scp model.safetensors pi@raspberrypi:~

# 執行
ssh pi@raspberrypi './myapp'
```

Candle 二進位不依賴任何外部函式庫，只需要目標裝置的 Linux 核心支援。

## 7. 效能調校

| 技巧 | 說明 | 加速效果 |
|------|------|---------|
| 使用 Metal GPU | macOS 上的 GPU 加速 | 2-5x |
| FP16 推論 | 半精度減少頻寬 | 1.5-2x |
| 批次處理 | 同時推論多筆資料 | 2-4x |
| 模型量化 | INT8 權重 | 2-3x |

## 8. 結語

Candle 的生態已經相當完整。從 LLaMA 文字生成到 Whisper 語音辨識，Candle 提供了接近 Python 生態的模型支援，同時保持了 Rust 的效能和安全性。對於不需要 CUDA 的推論場景，Candle 是當前最佳選擇。

## 延伸閱讀

- [Candle LLaMA example](https://www.google.com/search?q=Candle+LLaMA+example+Rust)
- [Candle Whisper example](https://www.google.com/search?q=Candle+Whisper+Rust+example)
- [Candle safetensors](https://www.google.com/search?q=Candle+safetensors+load+model)
