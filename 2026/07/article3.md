# Candle 1.0：Rust 生態的機器學習框架

## Hugging Face 的 Rust 變革

2026 年 3 月，Hugging Face 正式發布了 **Candle 1.0**——一個以 Rust 撰寫的極簡機器學習框架。這個消息在 ML 社群引起了不小的震動：為什麼 Hugging Face——PyTorch 生態系的頭號推手——要投入 Rust ML 框架的開發？

答案很簡單：**生產環境的基礎設施需求**。

Hugging Face 每天要處理數百萬次的模型推論請求。每次請求都要載入模型、分配記憶體、執行計算、回傳結果。在這種規模下，Python/PyTorch 的啟動時間和記憶體開銷變成了顯著的成本。Candle 專案始於 2023 年，最初只是一個內部實驗——驗證 Rust 是否能成為 ML 推論的更高效替代方案。三年的打磨後，Candle 1.0 終於準備好迎接生產環境。

## Candle 1.0 的核心功能

### GPU 加速與多後端支援

Candle 的底層計算引擎設計極為精簡。它不重新發明輪子，而是直接對接現有的高效能計算函式庫：

- **CUDA 後端**：透過 `cuda_driver` 和 `cublas` 直接操作 NVIDIA GPU，無需依賴 cuDNN 或 TensorRT
- **Metal 後端**：原生支援 Apple Silicon 的 GPU 加速，在 MacBook 上即可進行本地推論
- **CPU 後端**：使用 **libcpu** 自行開發的 CPU 運算核心，支援 AVX2/AVX-512 等 SIMD 指令集

```rust
use candle_core::{Device, Tensor};
use candle_nn::{Linear, Module};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let device = Device::cuda_if_available()?;
    let tensor = Tensor::randn(0f32, 1.0, (3, 4), &device)?;
    println!("Created tensor on {:?}: {}", device, tensor);
    Ok(())
}
```

Device 的選擇是 Candle 的亮點之一：`Device::cuda_if_available()` 自動偵測 GPU 可用性，開發者不需要手動管理裝置切換。當 GPU 不可用時，優雅地降級到 CPU。

### 自動微分

Candle 的自動微分整合在 `candle_nn` 和 `candle_optimiser` 套件中。它採用**建置時計算圖**（build-time graph）而非 PyTorch 的動態計算圖（eager execution）：

```rust
use candle_nn::{Linear, Module, VarBuilder};
use candle_core::{Device, Tensor};

fn build_model() -> Linear {
    let device = Device::Cpu;
    let vb = VarBuilder::new(device);
    Linear::new(784, 256, vb.pp("layer1"))
}
```

這種設計讓 Candle 在訓練時也能保持極低的記憶體開銷。反向傳播的梯度計算在編譯期就已經確定，不需要在執行時期追蹤計算圖。

### 模型推論

Candle 1.0 的核心使用案例是模型推論。它支援直接從 Hugging Face Hub 載入 safetensors 格式的權重：

```rust
use candle_core::Device;
use candle_transformers::models::bert::BertModel;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let device = Device::cuda_if_available()?;
    // 從 Hugging Face Hub 載入 BERT 模型
    let model = BertModel::new(
        "sentence-transformers/all-MiniLM-L6-v2",
        "refs/pr/21",
        &device,
    )?;
    println!("BERT model loaded on {:?}", device);
    Ok(())
}
```

## 與 PyTorch 的對比

### 效能

在純推論場景下，Candle 的表現相當亮眼：

| 指標 | PyTorch 2.6 (CUDA) | Candle 1.0 (CUDA) |
|------|--------------------|--------------------|
| 模型載入時間 | 0.8-1.2s | 0.05-0.15s |
| 推論延遲 (BERT base) | 5-8ms | 4-6ms |
| 峰值記憶體 (BERT base) | ~420MB | ~180MB |
| 二進位大小 | ~800MB | ~15MB |

**啟動時間**是 Candle 最大的優勢。PyTorch 需要載入 Python 直譯器、初始化 CUDA 上下文、設定分散式通訊……這一切在 Candle 中都不存在。Candle 編譯後的二進位檔就是一切——直接執行、零等待。

### 記憶體使用

Candle 的記憶體使用量約為 PyTorch 的 40-50%。這來自幾個設計選擇：
- **沒有 Python 開銷**：每個 Python 物件都有額外的記憶體開銷，而 Rust 的 struct 就是純粹的資料
- **精確的記憶體控制**：Rust 的所有權模型讓記憶體在不再使用時立即被釋放，沒有 GC pause
- **safetensors 格式**：直接記憶體映射（mmap）權重檔，不需要解析和轉換

### 啟動時間

這可能是最令人驚豔的差距。一個部署在 AWS Lambda 的推論函數：

- **PyTorch**：冷啟動 8-12 秒（包含載入模型和初始化），熱啟動 200ms
- **Candle**：冷啟動 0.3-0.5 秒，熱啟動 20-30ms

這讓 Candle 成為 Serverless 推論的首選。AWS Lambda、Cloudflare Workers、Fly.io——這些環境對冷啟動時間極度敏感，Candle 提供了數十倍的改善。

## 支援的模型架構

Candle 1.0 的模型支援透過 `candle-transformers` 套件提供，涵蓋了主流架構：

### Transformer 家族
- **BERT** / **RoBERTa** / **DistilBERT**：句子嵌入與分類任務
- **GPT-2** / **LLaMA** / **Mistral** / **Phi**：自迴歸語言模型
- **T5** / **BART**：編碼器-解碼器架構
- **Whisper**：語音辨識
- **Wav2Vec2**：語音特徵提取

### 視覺模型
- **ViT**（Vision Transformer）：影像分類
- **ResNet** / **MobileNet**：卷積網路
- **Stable Diffusion**：文字生成影像（實驗性支援）

### LLM 推論

Candle 1.0 對大型語言模型的支援尤為突出。它支援量化的 LLaMA/Mistral 模型，使用 4-bit 或 8-bit 量化後，7B 參數的模型僅需 4-6GB 記憶體：

```rust
use candle_transformers::models::llama::{Config, Llama};
use candle_core::Device;

fn load_llama() -> Result<(), Box<dyn std::error::Error>> {
    let device = Device::cuda_if_available()?;
    let config = Config::config_7b_v3();
    let model = Llama::new_quantized(
        "meta-llama/Llama-3.1-8B",
        "q4_0",
        &device,
    )?;
    println!("LLaMA 8B (4-bit) loaded on {:?}", device);
    Ok(())
}
```

## Rust 用於 ML 基礎設施的優勢

Candle 的出現不是偶然，它代表了 Rust 在 ML 領域的更深層趨勢。

### 零成本抽象

Rust 的核心承諾是「零成本抽象」——高階語言的表達力，低階語言的效能。對 ML 框架而言，這意味著：

1. **泛型張量運算**：型別安全的張量操作，所有型別檢查在編譯期完成
2. **迭代器與閉包**：資料預處理管線可以用高階的迭代器鏈撰寫，編譯後與手寫迴圈無異
3. **Enum 與 Pattern Matching**：處理不同的資料類型和裝置後端，無需執行時期的型別檢查

### 記憶體安全性

這可能是最被低估的優勢。C++ 的 ML 框架（TensorFlow 的 C++ 核心、llama.cpp）長期以來受記憶體錯誤困擾：

- 2017-2023 年間，TensorFlow 報告了超過 300 個記憶體相關的安全漏洞
- PyTorch 的 C++ 後端同樣存在 use-after-free 和 buffer overflow 的風險

Candle 在編譯期就排除了這些問題。Rust 的所有權模型確保了每次張量操作都是記憶體安全的——不是透過執行時期的檢查，而是透過編譯器的靜態證明。

### 安全的並行計算

GPU 運算本質上是高度並行的。Rust 的 `Send` 和 `Sync` trait 在編譯期檢查多執行緒的安全性：

```rust
fn parallel_inference() -> Result<(), Box<dyn std::error::Error>> {
    let device = Device::cuda_if_available()?;
    let model = Arc::new(MyModel::new(&device)?);
    
    // Rust 的型別系統保證了跨執行緒的安全性
    let handles: Vec<_> = (0..4).map(|i| {
        let model = model.clone();
        std::thread::spawn(move || {
            model.forward(Tensor::randn(0., 1., (1, 784), &device).unwrap())
        })
    }).collect();
    
    Ok(())
}
```

在 C++ 中，這樣的程式碼需要小心翼翼的 mutex 管理或 atomic 操作。在 Rust 中，編譯器會直接拒絕不安全的並行程式碼。

### 相依管理與建置

Cargo 對 ML 專案的影響經常被忽略。在 Python 生態中，管理 CUDA 版本、cuDNN 版本、PyTorch 版本的相容性是一場噩夢。Candle 透過 Cargo 的特徵標誌（feature flags）解決了這個問題：

```toml
[dependencies]
candle-core = { version = "1.0", features = ["cuda"] }
candle-nn = "1.0"
candle-transformers = "1.0"
```

不需要 conda 環境、不需要 pip 的 `--find-links`、不需要手動切換 CUDA 版本——只需切換 Cargo 的特徵標誌。

## 結語：Candle 的定位與未來

Candle 1.0 的目標不是取代 PyTorch。PyTorch 在研究和實驗方面的生態系仍然無可匹敵。Candle 的定位是**生產環境的高效能推論引擎**——當你需要低延遲、小體積、快速啟動的 ML 服務時，Candle 是最自然的選擇。

從更宏觀的角度看，Candle 代表了 Rust 在 ML 基礎設施中的崛起。它不是孤例：`ratchet`（邊緣裝置 ML）、`burn`（Rust 原生訓練框架）、`tract`（ONNX 推論）——越來越多的 Rust ML 專案正在成熟。

對於 ML 工程師而言，Candle 提供了一個獨特的工具選擇：不需要放棄 PyTorch 的研究生態系，但在生產部署時多了一個高效、安全、可靠的 Rust 原生選項。這正是 Hugging Face 團隊從 2023 年走到 1.0 的初心——讓 ML 從研究到生產的路徑，走得更快、更穩。
