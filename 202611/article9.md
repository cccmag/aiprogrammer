# 感測器資料處理與邊緣運算 — 資料融合、濾波、上雲

## 從原始資料到有用資訊

感測器的原始資料通常是噪聲的、不完整的。嵌入式系統的核心工作之一就是將這些原始資料轉換為有意義的資訊。

## 數位濾波

### 移動平均濾波

最簡單的濾波方法，適合平滑緩慢變化的訊號：

```rust
struct MovingAverage<const N: usize> {
    buffer: [f32; N],
    index: usize,
    sum: f32,
}

impl<const N: usize> MovingAverage<N> {
    fn update(&mut self, value: f32) -> f32 {
        self.sum -= self.buffer[self.index];
        self.buffer[self.index] = value;
        self.sum += value;
        self.index = (self.index + 1) % N;
        self.sum / N as f32
    }
}
```

### 互補濾波（Complementary Filter）

常用於 IMU 姿態估計：

```rust
fn complementary_filter(accel: &Vec3, gyro: &Vec3, dt: f32) -> Quaternion {
    // 加速度計提供長期穩定但短期噪聲的姿態
    // 陀螺儀提供短期精確但長期飄移的角速度
    const ALPHA: f32 = 0.98;

    let accel_quat = quaternion_from_accel(accel);
    let gyro_quat = integrate_gyro(gyro, dt);

    gyro_quat.slerp(accel_quat, 1.0 - ALPHA)
}
```

### 卡爾曼濾波

適合有準確系統模型的場景：

```rust
struct KalmanFilter1D {
    x: f32,  // 狀態估計
    p: f32,  // 誤差協方差
    q: f32,  // 過程噪聲
    r: f32,  // 測量噪聲
}

impl KalmanFilter1D {
    fn predict(&mut self, dt: f32) {
        self.p += self.q * dt;
    }

    fn update(&mut self, measurement: f32) {
        let k = self.p / (self.p + self.r);
        self.x += k * (measurement - self.x);
        self.p *= 1.0 - k;
    }
}
```

## 感測器融合

以 9 軸 IMU（加速度計 + 陀螺儀 + 磁力計）為例：

```rust
pub struct ImuFusion {
    madgwick: MadgwickFilter,
    kalman: AttitudeKalman,
}

impl ImuFusion {
    pub fn update(
        &mut self,
        accel: [f32; 3],
        gyro: [f32; 3],
        mag: [f32; 3],
        dt: f32,
    ) -> Attitude {
        // Madgwick 演算法運算量低，適合 MCU
        self.madgwick.update(accel, gyro, mag, dt)
    }
}
```

## 邊緣決策

在 MCU 上完成資料處理後，可以在本地做出決策，僅上傳必要資訊：

```rust
fn edge_decision(sensor_data: &SensorData) -> Action {
    // 異常檢測
    if sensor_data.temperature > 85.0 {
        return Action::Alert;
    }

    // 變化量檢測 — 只有變化超過閾值才上報
    if (sensor_data.vibration - baseline).abs() > THRESHOLD {
        return Action::Report;
    }

    // 定期上報
    if elapsed_time >= REPORT_INTERVAL {
        return Action::Report;
    }

    Action::Sleep
}
```

## 上雲端

### WiFi（ESP32）

```rust
use esp_wifi::wifi::WifiDevice;

async fn upload_data(wifi: &mut WifiDevice, data: &[u8]) {
    let mut socket = TcpSocket::new();
    socket.connect(IpAddr::from([192, 168, 1, 100]), 8080).await;
    socket.write(data).await;
}
```

### LoRa（長距離低功耗）

```rust
fn send_lora(lora: &mut LoraRadio, data: &[u8]) {
    lora.config(&LoraConfig {
        frequency: 868_000_000,
        spreading_factor: 12,
        bandwidth: 125_000,
        coding_rate: 5,
    });
    lora.send(data);
}
```

## 完整管線

```
感測器 → ADC/DMA 讀取 → 數位濾波 → 感測器融合
                                            ↓
雲端 ←─ WiFi/LoRa 傳輸 ←─ 邊緣決策 ←─ 特徵提取
```

## 延伸閱讀

- [卡爾曼濾波入門](https://www.google.com/search?q=Kalman+filter+tutorial+embedded)
- [Madgwick IMU 融合演算法](https://www.google.com/search?q=Madgwick+IMU+sensor+fusion+algorithm)
- [邊緣運算架構設計](https://www.google.com/search?q=edge+computing+architecture+MCU)
- [LoRa 通訊協定](https://www.google.com/search?q=LoRa+protocol+embedded+Rust)
