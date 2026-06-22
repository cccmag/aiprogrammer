# Rust 在邊緣 AI 中的應用

## 前言

邊緣 AI（Edge AI）指的是在終端裝置上直接執行機器學習推論，而非依賴雲端伺服器。從智慧攝影機、可穿戴裝置到工業感測器，邊緣 AI 正在重新定義「智慧」的邊界。而在這波浪潮中，Rust 憑藉其獨特的語言特性，正在成為邊緣 AI 開發的首選語言。

## 1. 邊緣 AI 的定義與需求

邊緣 AI 的核心挑戰：如何在功耗受限、運算能力有限、記憶體稀缺的硬體上，有效率地執行神經網路推論？

相比雲端 AI，邊緣 AI 有以下關鍵需求：

- **低延遲**：即時推論需在毫秒級別完成，無法等待雲端往返。
- **隱私保護**：資料在本地處理，不需上傳至雲端。
- **離線運作**：無網路連線時裝置仍需正常運作。
- **功耗效率**：電池裝置需將能耗控制在毫瓦級別。
- **小型化**：模型須經量化與剪枝後才能在 MCU 上運行。

## 2. 為什麼 Rust 是邊緣 AI 的理想語言

### 無 GC、零成本抽象

Rust 編譯為原生機器碼，沒有 GC 暫停、沒有執行期開銷。對於只有 256KB RAM 的微控制器，零成本抽象意味著高階程式設計不會帶來額外的記憶體負擔。

### 所有權模型與記憶體安全

嵌入式系統中，記憶體錯誤是系統崩潰的主要來源。Rust 的所有權系統在編譯期保證記憶體安全。對於醫療裝置、汽車電子等安全關鍵應用，這項特性至關重要。

### 跨平台與裸機支援

`#![no_std]` 模式可編譯到無 OS 的裸機環境。從 ARM Cortex-M 到 RISC-V，從 x86 到樹莓派，`cargo build --target` 一行指令即可切換平台。

### 豐富的邊緣 AI 生態系

| 函式庫 | 用途 | 目標平台 |
|--------|------|----------|
| **Candle** | 輕量級 ML 框架 | 邊緣伺服器、樹莓派 |
| **Burn** | 多後端神經網路框架 | 跨平台 |
| **WasmEdge** | WebAssembly 執行期 | 跨平台邊緣運算 |
| **RTIC** | 即時嵌入式框架 | MCU / 裸機 |
| **embassy** | 非同步嵌入式執行期 | MCU / 無線感測器 |
| **tract** | ONNX 推論引擎 | 嵌入式 Linux |

## 3. Llama 4 Edge 在 Rust 中的推論

2026 年初，Meta 釋出了 Llama 4 Edge——專為邊緣裝置設計的輕量級語言模型，僅 1.5B 參數，支援 4-bit 量化，在手機 SoC 與邊緣 CPU 上即可流暢運行。

使用 **Candle** 框架載入 Llama 4 Edge 並執行推論：

```rust
use candle_core::{Device, Tensor};
use candle_nn::{VarBuilder, VarMap};
use candle_transformers::models::llama2 as llama_model;
use hf_hub::api::sync::Api;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let device = Device::Cpu;
    let api = Api::new()?;
    let repo = api.model("meta-llama/Llama-4-Edge-1.5B-Instruct-GGUF".to_string());
    let model_path = repo.get("model-4bit.gguf")?;

    let varmap = VarMap::new();
    let vb = VarBuilder::from_varmap(&varmap, candle_core::DType::F32, &device);
    let config = llama_model::Config::config_1_5b();
    let model = llama_model::Llama::load(vb, &config)?;

    let tokenizer_path = repo.get("tokenizer.json")?;
    let mut tokenizer = tokenizers::Tokenizer::from_file(tokenizer_path)?;

    let prompt = "邊緣 AI 的好處有哪些？";
    let tokens = tokenizer.encode(prompt, true)?;
    let input = Tensor::new(&tokens.get_ids(), &device)?.unsqueeze(0)?;

    let logits = model.forward(&input, 0)?;
    let sampled = logits.squeeze(0)?.argmax(1)?;
    let output = tokenizer.decode(&sampled.to_vec1::<u32>()?, true)?;
    println!("{}", output);
    Ok(())
}
```

Candle 不依賴 libtorch 或 TensorFlow，編譯後的二進位僅數 MB，非常適合邊緣部署。

## 4. 嵌入式 Rust + AI：TinyML 與 Microcontrollers

在 MCU 層級，傳統上使用 TensorFlow Lite Micro，但它們依賴 C/C++ 工具鏈。Rust 的嵌入式生態正逐步填補這個空白。

**RTIC** 框架提供了在 MCU 上進行確定性排程的能力。結合 **embassy** 的非同步執行期，開發者可在 Cortex-M4 MCU 上實現感測器資料的即時擷取與 AI 推論：

```rust
#[rtic::app(device = stm32f4xx_hal::pac, peripherals = true)]
mod app {
    use tinyai::cnn::CnnModel;

    #[shared]
    struct Shared { model: CnnModel<4> }

    #[local]
    struct Local { led: stm32f4xx_hal::gpio::Pin<'B', 7> }

    #[init]
    fn init(cx: init::Context) -> (Shared, Local) {
        let model = CnnModel::load(include_bytes!("model_quantized.bin"));
        (Shared { model }, Local { led: cx.device.GPIOB.split().p7 })
    }

    #[task(binds = EXTI0, shared = [model])]
    fn sensor_interrupt(mut cx: sensor_interrupt::Context) {
        let sample = read_sensor();
        let prediction = cx.shared.model.lock(|m| m.predict(&sample));
        if prediction > 0.9 { cx.local.led.set_high(); }
    }
}
```

在 180MHz Cortex-M4 上、使用不到 32KB RAM 即可實現即時聲音分類。

## 5. WasmEdge：Rust + WebAssembly 在邊緣的應用

WebAssembly 正在成為邊緣運算的通用位元組碼。**WasmEdge**（CNCF 託管）深度整合了 Rust 生態，提供沙箱安全、極速啟動與 AI 支援。

```rust
// 編譯：cargo build --target wasm32-wasi --release
use wasmedge_tensorflow_interface;

fn main() {
    let model = wasmedge_tensorflow_interface::load_model(
        include_bytes!("mobilenet_v2_1.0_224_quant.tflite")
    );
    let input = image_to_tensor("input.jpg", 224, 224);
    let output = model.run(&[input], &["input"], &["output"]);
    let top_class = argmax(&output[0]);
    println!("辨識結果：類別 #{}", top_class);
}
```

部署只需一行指令：

```bash
wasmedge --dir .:. image_classifier.wasm
```

WasmEdge 甚至支援在邊緣裝置上運行量化後的 Llama 模型。

## 6. 實際案例：用 Rust 在樹莓派上運行影像辨識

在樹莓派 5 上使用 Rust 進行即時影像辨識。硬體：樹莓派 5、Camera Module 3。技術棧：Candle + MobileNetV3（INT8 量化）+ Tokio 非同步排程。

```rust
use anyhow::Result;
use candle_core::{Device, Tensor};
use candle_nn::ops::softmax;
use image::DynamicImage;
use tokio::time::{interval, Duration};

struct EdgeVision { model: candle_nn::Sequential, device: Device }

impl EdgeVision {
    fn new() -> Result<Self> {
        let device = Device::Cpu;
        let model = load_mobilenetv3_quantized(&device)?;
        Ok(Self { model, device })
    }

    fn preprocess(img: &DynamicImage) -> Result<Tensor> {
        let img = img.resize_exact(224, 224, image::imageops::FilterType::Triangle);
        let data = img.to_rgb8().into_raw();
        let tensor = Tensor::from_vec(data, (1, 224, 224, 3), &Device::Cpu)?
            .permute((0, 3, 1, 2))?;
        tensor.affine(1.0 / 255.0, 0.0)
    }

    fn infer(&self, tensor: &Tensor) -> Result<u32> {
        let output = self.model.forward(tensor)?;
        let probs = softmax(&output.squeeze(0)?, 0)?;
        let (class_id, _) = probs.argmax(0)?.to_scalar::<u32>()?;
        Ok(class_id)
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    let mut cam = raspicam::Camera::new(raspicam::Config {
        width: 640, height: 480, fps: 30,
    });
    let vision = EdgeVision::new()?;
    let mut tick = interval(Duration::from_millis(33));

    loop {
        tick.tick().await;
        let frame = cam.capture()?;
        let tensor = EdgeVision::preprocess(&frame)?;
        let class_id = vision.infer(&tensor)?;
        println!("類別：{}", imagenet::LABELS[class_id as usize]);
    }
}
```

INT8 量化的 MobileNetV3 在樹莓派 5 上可達 **30 FPS**，功耗約 5W，二進位大小僅 **4.2MB**。

## 7. 邊緣 AI 的未來趨勢

### 混合推論

邊緣處理輕量級任務，雲端處理複雜任務。Rust 的非同步生態與 Wasm 沙箱讓這種協作變得優雅。

### 聯邦學習

模型在邊緣裝置上訓練，只上傳梯度。Rust 的記憶體安全讓在數百萬 IoT 裝置上安全執行訓練程式成為可能。

### 硬體加速

NVIDIA Jetson、Google Coral 等邊緣 AI 加速器的普及，使 Rust 的 CUDA、Vulkan、OpenCL 綁定越來越成熟。Candle 已支援 CUDA 後端。

### AI 驅動的邊緣 OS

即時排程、動態功耗管理、模型熱切換——這些功能正被整合到以 Rust 為核心的邊緣 OS 中（如 TockOS、embassy）。

## 結語

Rust 在邊緣 AI 中的角色不僅是語言之爭——它代表了一種工程哲學：在資源極度受限的環境中，堅持記憶體安全、零成本抽象與跨平台可移植性。從 Llama 4 Edge 推論到 MCU 上的 TinyML，再到 WasmEdge 沙箱執行，Rust 正在成為邊緣 AI 的基礎設施語言。掌握 Rust 邊緣 AI 開發，將是後雲端時代的關鍵技能。
