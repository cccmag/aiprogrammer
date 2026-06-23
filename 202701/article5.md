# 邊緣裝置 ML 部署 — 嵌入式推論、感測器資料處理

## 1. 引言

邊緣 AI 是 Rust ML 部署最具優勢的領域。當 ML 模型需要被部署到沒有 GPU、沒有 Python、甚至沒有作業系統的裝置上時，Rust 的交叉編譯、精確記憶體控制和無執行期依賴特性顯得尤其珍貴。

## 2. 邊緣部署的挑戰

| 挑戰 | 說明 | Rust 解決方案 |
|------|------|-------------|
| 資源限制 | RAM < 1MB, Flash < 4MB | 精確記憶體控制, no_std |
| 無執行期 | 沒有 Python/Java VM | 靜態二進位 |
| 交叉編譯 | 不同 CPU 架構 | `rustup target add` |
| 即時要求 | 延遲 < 10ms | 無 GC, 可預測效能 |
| 低功耗 | 電池供電 | 非同步 + 休眠模式 |

## 3. 硬體層次與 Rust 選擇

### 邊緣伺服器（Raspberry Pi 5, Jetson Orin）

這些裝置執行完整的 Linux，適合標準 Rust + Candle/Burn/tract：

```rust
// Raspberry Pi 5 上的影像分類
use candle_core::{Device, Tensor};
use image::io::Reader as ImageReader;

fn classify_image(path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let device = Device::Cpu;

    // 載入並預處理影像
    let img = ImageReader::open(path)?
        .decode()?
        .resize_to_fill(224, 224, image::imageops::FilterType::Triangle);
    let input = preprocess_tensor(&img, &device)?;

    // 載入量化模型並推論
    let model = load_mobilenet_v2(&device)?;
    let output = model.forward(&input)?;

    // 取得 top-5 預測
    let top5 = output.argsort(1)?.slice(&[.., ..5])?;
    println!("Top-5 預測: {:?}", top5);
    Ok(())
}
```

### 嵌入式 Linux（BeagleBone, STM32MP）

這些裝置執行 Linux，但資源較少。Candle 是最佳選擇：

```bash
# 交叉編譯給 ARM Cortex-A
rustup target add armv7-unknown-linux-gnueabihf

# Cargo.toml 不需要特殊配置
cargo build --target armv7-unknown-linux-gnueabihf --release

# 二進位約 5MB，可直接 scp 到裝置
```

### 微控制器（ESP32, STM32F4, RP2040）

這些裝置執行裸機或 RTOS，需要 no_std 模式：

```rust
#![no_std]
#![no_main]

use panic_halt as _;
use cortex_m_rt::entry;

// 預先訓練的極小模型（INT8 權重）
static WEIGHTS: &[i8] = include_bytes!("../model/weights.bin");
const NUM_CLASSES: usize = 3;
const INPUT_SIZE: usize = 32;

#[entry]
fn main() -> ! {
    let sensor_data = read_sensor();

    // 極簡 ML 推論
    let result = tiny_inference(&sensor_data);

    // 根據結果控制執行器
    match result {
        0 => turn_led_off(),
        1 => turn_led_on(),
        2 => blink_led(),
    }

    loop { /* 休眠等待下一次中斷 */ }
}

fn tiny_inference(input: &[f32; INPUT_SIZE]) -> usize {
    // i8 量化矩陣乘法 + argmax
    let mut max_score = i32::MIN;
    let mut best_class = 0;

    for class in 0..NUM_CLASSES {
        let mut score = 0i32;
        for i in 0..INPUT_SIZE {
            let w = WEIGHTS[class * INPUT_SIZE + i] as i32;
            let x = (input[i] * 127.0) as i32;
            score += w * x;
        }
        if score > max_score {
            max_score = score;
            best_class = class;
        }
    }
    best_class
}
```

## 4. 感測器資料管線

完整的邊緣 ML 系統需要處理從感測器到決策的完整流程：

```rust
use embedded_hal::i2c::I2c;

pub struct MlsSensorPipeline<I2C> {
    i2c: I2C,
    model: TinyMlModel,
    buffer: [f32; 64],       // 環形緩衝區
    sample_index: usize,
}

impl<I2C: I2c> MlsSensorPipeline<I2C> {
    pub fn process_sample(&mut self) -> Result<Option<Action>, I2C::Error> {
        // 1. 從 I2C 感測器讀取資料
        let mut raw = [0u8; 6];
        self.i2c.read(0x76, &mut raw)?;

        // 2. 轉換為物理量
        let temperature = self.decode_temperature(&raw);
        let humidity = self.decode_humidity(&raw);

        // 3. 更新環形緩衝區
        self.buffer[self.sample_index % 64] = temperature;
        self.buffer[(self.sample_index + 32) % 64] = humidity;
        self.sample_index += 1;

        // 4. 每收集 64 個樣本執行一次推論
        if self.sample_index % 64 == 0 {
            let result = self.model.predict(&self.buffer);
            return Ok(Some(self.map_action(result)));
        }

        Ok(None)
    }
}
```

## 5. 模型壓縮策略

邊緣裝置上的模型需要極致壓縮：

| 技術 | 壓縮比 | 精度損失 | Rust 支援 |
|------|--------|---------|----------|
| INT8 量化 | 4x | 1-2% | Candle/tract |
| INT4 量化 | 8x | 3-5% | tract (實驗性) |
| 權重剪枝 | 2-5x | 0-1% | 自訂 Rust 程式 |
| 知識蒸餾 | 10x+ | 1-5% | Python 階段 |
| 結構化剪枝 | 2-3x | 0-2% | Python 階段 |

## 6. 實際案例：智慧農業感測器

一個完整的案例：在 ESP32 上運行土壤濕度分類模型。

```
感測器 (土壤濕度 + 溫度 + pH)
  → I2C 讀取 (每分鐘一次)
  → 特徵提取 (Rust, 無動態分配)
  → ML 推論 (INT8 量化 MLP, 4KB 權重)
  → 分類結果 (需澆水/正常/過濕)
  → BLE 通知手機 / MQTT 上傳
```

## 7. 結語

Rust 在邊緣 ML 部署中具有獨特的競爭優勢。從 Raspberry Pi 上的即時視覺推論到 STM32 上的感測器分類，Rust 提供了從雲端到終端的完整 ML 部署方案。隨著 RISC-V AI 晶片的普及，Rust ML 在嵌入式領域的影響力將持續增長。

## 延伸閱讀

- [Rust embedded ML](https://www.google.com/search?q=Rust+embedded+machine+learning+tutorial)
- [TFLite Micro alternatives](https://www.google.com/search?q=TFLite+Micro+vs+Rust+embedded+alternatives)
- [ESP32 ML inference](https://www.google.com/search?q=ESP32+Rust+machine+learning+inference)
