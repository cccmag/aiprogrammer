# 邊緣裝置 ML 推論

## 嵌入式推論, MCU, 感測器管線（2023-2026）

### 前言

邊緣 AI 是 Rust ML 推論最具優勢的場景之一。Python 需要完整的作業系統和執行期環境，而 Rust 可以編譯為靜態二進位直接在硬體上執行。

### 邊緣裝置的層次

```
雲端伺服器 → 邊緣伺服器 → 閘道器 → 終端裝置
  (x86/GPU)   (ARM/Linux)   (MCU/RTOS) (感測器節點)
```

Rust 可以在所有層次上運作：
- **邊緣伺服器**：Raspberry Pi、Jetson → 標準 Rust 二進位
- **閘道器**：ESP32、STM32MP → no_std + embedded-hal
- **終端感測器**：Cortex-M0/M4 → no_std + 最小配置

### 嵌入式 ML 推論管線

一個典型的邊緣 ML 系統架構：

```
感測器 (Camera/Mic/IMU)
    → 資料預處理 (Rust)
    → ML 推論 (Candle/tract)
    → 後處理 (Rust)
    → 決策/通訊 (MQTT/BLE)
```

### 在 Raspberry Pi 上部署

```rust
use candle_core::{Device, Tensor};
use candle_nn::VarBuilder;
use std::fs;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let device = Device::Cpu;

    // 載入量化模型
    let weights = fs::read("model_i8.safetensors")?;
    let vb = VarBuilder::from_buffers(
        vec![weights.into()], DType::I8, &device
    )?;

    // 從攝影機讀取影像（v4l2 或 OpenCV 綁定）
    let image = capture_frame()?;

    // 預處理：resize → normalize → CHW
    let input = preprocess(&image, &device)?;

    // 推論
    let output = model.forward(&input)?;

    // 後處理
    let result = postprocess(&output);
    println!("推論結果: {:?}", result);
    Ok(())
}
```

交叉編譯指令：
```bash
cargo build --target aarch64-unknown-linux-gnu --release
scp target/release/myapp pi@raspberrypi:~
```

### 在 ESP32 上部署

ESP32 這樣的微控制器需要 no_std 模式：

```rust
#![no_std]
#![no_main]

// 極簡的 ML 推論（預先量化權重）
struct TinyModel {
    weights: &'static [i8; 4096],  // 預先燒錄的 INT8 權重
    bias: &'static [i32; 64],
}

impl TinyModel {
    fn predict(&self, input: &[i8; 256]) -> [i8; 64] {
        let mut output = [0i8; 64];
        for i in 0..64 {
            let mut sum = self.bias[i];
            for j in 0..256 {
                sum += (input[j] as i32) * (self.weights[i * 256 + j] as i32);
            }
            output[i] = (sum >> 12) as i8;  // 量化縮放
        }
        output
    }
}
```

### 感測器資料管線

```rust
use embedded_hal::i2c::I2c;

struct SensorPipeline<B: I2c> {
    bus: B,
    model: TinyModel,
}

impl<B: I2c> SensorPipeline<B> {
    fn process(&mut self) -> Result<SensorReading, B::Error> {
        // 1. 讀取原始感測器資料
        let mut raw = [0u8; 32];
        self.bus.read(0x76, &mut raw)?;

        // 2. 轉換為模型輸入
        let input = self.normalize(&raw);

        // 3. ML 推論
        let output = self.model.predict(&input);

        // 4. 解析結果
        Ok(SensorReading::from(output))
    }
}
```

### 小結

Rust 在邊緣 ML 部署中的核心優勢是**無執行期依賴**和**精確資源控制**。無論是 Raspberry Pi 上的視覺推論還是 ESP32 上的感測器分類，Rust 都能以最少的資源完成工作。

---

**下一步**：[量化與模型最佳化](focus6.md)

## 延伸閱讀

- [Edge AI with Rust](https://www.google.com/search?q=edge+AI+Rust+embedded+machine+learning)
- [TFLite Micro vs Rust](https://www.google.com/search?q=TFLite+Micro+vs+Rust+embedded+ML)
- [ESP32 Rust ML](https://www.google.com/search?q=ESP32+Rust+machine+learning)
