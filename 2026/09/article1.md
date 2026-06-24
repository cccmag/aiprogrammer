# Rust 在嵌入式 Linux 中的應用

## 1. 引言

嵌入式系統是現代科技的重要基石，從智慧家電到工業控制器，無處不在。過去，C 語言一直是嵌入式開發的主流選擇，但其記憶體安全問題始終是開發者的痛點。Rust 的出現，為嵌入式世界帶來了新的可能性——兼具 C 語言的效能與現代語言的記憶體安全保障。本文將探討 Rust 在嵌入式 Linux 領域的實際應用與技術細節。

## 2. 嵌入式 Linux 與裸機嵌入式系統

在深入了解 Rust 的應用之前，必須先釐清兩個容易混淆的概念：**嵌入式 Linux** 與 **裸機嵌入式系統**。

**裸機嵌入式系統**（Bare-metal）沒有作業系統，程式直接運行在硬體上，開發者需要自行管理中斷、記憶體和週邊設備。典型的例子是使用 STM32 或 ESP32 微控制器，執行即時性要求極高的任務。Rust 在裸機領域透過 `cortex-m-rt`、`embedded-hal` 等 crate 提供了完善的支援。

**嵌入式 Linux** 則是在配備 MMU（記憶體管理單元）的處理器上運行完整的 Linux 核心，例如 Raspberry Pi、BeagleBone 或 NXP i.MX 系列。這裡的開發更接近一般的 Linux 程式設計，但需要面對資源限制、交叉編譯和直接硬體存取等挑戰。

兩者的關鍵區別如下：

| 特性 | 裸機嵌入式 | 嵌入式 Linux |
|------|-----------|-------------|
| OS | 無 | Linux 核心 |
| MMU | 通常無 | 必有 |
| 記憶體管理 | 手動 | 虛擬記憶體 |
| 即時性 | 極高 | 視核心配置而定 |
| 開發複雜度 | 高（需處理底層細節） | 中（OS 抽象化） |
| Rust 適用場景 | 驅動、RTOS 任務 | 應用程式、核心模組 |

## 3. Rust 在嵌入式 Linux 中的定位

在嵌入式 Linux 中，Rust 可以在兩個層面發揮作用：

### 3.1 應用層（User Space）

這是最直接的切入點。Rust 編譯成標準的二進位執行檔，透過 Linux 系統呼叫與核心互動，存取 `/dev/gpiochip`、`/dev/i2c-X` 等裝置檔案。開發者可以使用標準的 Rust 工具鏈，搭配 `libgpiod`、`i2cdev`、`spidev` 等 crate 來操作硬體。

### 3.2 核心層（Kernel Space）

Linux 核心從 6.1 版開始正式支援 Rust 作為第二語言。開發者可以用 Rust 編寫核心驅動程式，利用 Rust 的所有權模型在編譯期防止許多常見的核心錯誤（如釋放後使用、雙重釋放）。目前這部分仍在快速發展中，但已可用於生產環境。

對於大多數專案，**建議從應用層切入**，門檻較低且生態系更成熟。

## 4. 使用 Rust 編寫嵌入式 Linux 應用程式

### 4.1 GPIO 控制實例

以下範例展示如何使用 Rust 透過 GPIO chardev 介面（`/dev/gpiochip`）控制 GPIO 腳位。這是最新的核心 GPIO 使用者空間 API，取代了舊式的 sysfs 介面。

```rust
use gpiod::{Chip, LineRequest, Options};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 開啟 GPIO 控制器
    let mut chip = Chip::new("/dev/gpiochip0")?;

    // 設定 GPIO 17 為輸出，初始值為低電位
    let options = Options::output([17]).with_values([false]);
    let mut line = chip.request_lines(options)?;

    // 輸出高電位
    line.set_values([true])?;
    println!("GPIO 17 設為高電位");

    std::thread::sleep(std::time::Duration::from_secs(2));

    // 輸出低電位
    line.set_values([false])?;
    println!("GPIO 17 設為低電位");

    Ok(())
}
```

在 `Cargo.toml` 中加入相依套件：

```toml
[dependencies]
gpiod = "0.3"
```

編譯時需指定目標平臺，並確保目標裝置的 Linux 核心版本 ≥ 4.8（引入 GPIO chardev API）。

### 4.2 I2C 與 SPI 存取

Rust 生態系提供了多個 crate 來操作常見的匯流排協定：

```rust
use linux_embedded_hal::I2cdev;
use embedded_hal::blocking::i2c::WriteRead;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut dev = I2cdev::new("/dev/i2c-1")?;
    let addr = 0x76; // BMP280 感測器位址
    let mut buf = [0u8; 6];

    // 寫入暫存器位址，然後讀取 6 個位元組
    dev.write_read(addr, &[0xF7], &mut buf)?;

    let temp_raw = ((buf[0] as u32) << 12) | ((buf[1] as u32) << 4) | ((buf[2] as u32) >> 4);
    let temp = temp_raw as f32 * 0.025 + 40.0;
    println!("溫度: {:.2}°C", temp);

    Ok(())
}
```

這裡使用了 `linux-embedded-hal` 這個橋接 crate，它實作了 `embedded-hal` trait，讓開發者可以在 Linux 上編寫與裸機平臺共用的硬體抽象程式碼。

## 5. 交叉編譯工具鏈與目標設定

嵌入式裝置通常無法直接執行開發機器上的編譯產物，因此需要交叉編譯。

### 5.1 安裝目標

以 ARM 架構為例（例如 Raspberry Pi）：

```bash
rustup target add armv7-unknown-linux-gnueabihf
```

### 5.2 指定連結器

在專案根目錄建立 `.cargo/config.toml`：

```toml
[target.armv7-unknown-linux-gnueabihf]
linker = "arm-linux-gnueabihf-gcc"
```

### 5.3 編譯與部署

```bash
cargo build --target armv7-unknown-linux-gnueabihf --release
scp target/armv7-unknown-linux-gnueabihf/release/myapp user@device:/home/user/
```

對於 aarch64（ARM 64 位元）或 RISC-V 架構，只需將 target 替換為 `aarch64-unknown-linux-gnu` 或 `riscv64gc-unknown-linux-gnu` 即可。

## 6. Yocto/Buildroot 與 Rust 的整合

在量產環境中，使用 Yocto 或 Buildroot 建立客製化嵌入式 Linux 發行版是常見做法。Rust 的整合方式如下：

### 6.1 Yocto

Yocto 的 `meta-rust` 層提供了 Rust 工具的支援。將該層加入 `bblayers.conf` 後，即可在配方中使用 `inherit rust`：

```bitbake
SUMMARY = "My Rust application"
LICENSE = "MIT"
inherit rust

SRC_URI = "git://github.com/example/myapp.git;branch=main"
S = "${WORKDIR}/git"

do_compile() {
    oe_compile_rust
}

do_install() {
    oe_install_rust_bin
}
```

### 6.2 Buildroot

Buildroot 從 2022.02 版開始支援 Rust。在主選單中啟用 `BR2_PACKAGE_RUST` 和 `BR2_PACKAGE_CARGO` 後，即可在 `package/` 目錄下建立 Rust 套件：

```makefile
MYAPP_VERSION = 1.0.0
MYAPP_SITE = https://github.com/example/myapp.git
MYAPP_SITE_METHOD = git

define MYAPP_BUILD_CMDS
    cargo build --target $(RUSTC_TARGET_NAME) --release
endef

define MYAPP_INSTALL_TARGET_CMDS
    $(INSTALL) -D -m 0755 $(@D)/target/$(RUSTC_TARGET_NAME)/release/myapp \
        $(TARGET_DIR)/usr/bin/myapp
endef

$(eval $(generic-package))
```

## 7. 實際案例：用 Rust 控制感測器

讓我們用一個完整的案例來總結：在 Raspberry Pi 上使用 Rust 讀取 DHT22 溫濕度感測器資料，並透過 MQTT 上傳至雲端。

### 7.1 專案結構

```
sensor-mqtt/
├── Cargo.toml
├── .cargo/config.toml
└── src/
    └── main.rs
```

### 7.2 主要程式碼

```rust
use rumqttc::{MqttOptions, AsyncClient, QoS};
use rppal::gpio::{Gpio, InputPin};
use anyhow::Result;
use tokio::time;

const DHT_PIN: u8 = 4;
const MQTT_BROKER: &str = "mqtt://test.mosquitto.org";
const TOPIC: &str = "sensors/dht22";

#[tokio::main]
async fn main() -> Result<()> {
    let gpio = Gpio::new()?;
    let mut pin = gpio.get(DHT_PIN)?.into_input();
    let mut mqttopts = MqttOptions::new("sensor-01", MQTT_BROKER, 1883);
    let (client, mut eventloop) = AsyncClient::new(mqttopts, 10);
    client.connect().await?;

    loop {
        match read_dht22(&mut pin) {
            Ok((temp, humidity)) => {
                let payload = serde_json::json!({
                    "temperature": temp,
                    "humidity": humidity,
                    "timestamp": chrono::Utc::now().to_rfc3339()
                });
                client.publish(TOPIC, QoS::AtLeastOnce, false, payload.to_string())
                    .await?;
            }
            Err(e) => eprintln!("讀取失敗: {}", e),
        }
        time::sleep(time::Duration::from_secs(30)).await;
    }
}
```

### 7.3 編譯執行

```bash
cargo build --target armv7-unknown-linux-gnueabihf --release
scp target/armv7-unknown-linux-gnueabihf/release/sensor-mqtt pi@raspberrypi:~
ssh pi@raspberrypi ./sensor-mqtt
```

這個案例展示了 Rust 在嵌入式 Linux 中的完整開發流程：硬體控制、非同步網路通訊、序列化與 MQTT 協定整合，全部在記憶體安全的環境下完成。

## 8. 結語

Rust 在嵌入式 Linux 領域的潛力正在被快速兌現。從應用層的 GPIO 控制到核心層的驅動程式開發，Rust 提供了比 C 語言更安全的開發體驗，同時不犧牲效能。對於正在規劃新嵌入式專案的團隊，採用 Rust 不僅能減少運行時錯誤，還能透過豐富的類型系統和生態系工具提升開發效率。

在下一期文章中，我們將深入探討 Rust 的 unsafe 程式設計與 FFI 實戰，敬請期待。
