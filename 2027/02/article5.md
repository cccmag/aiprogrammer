# 跨平台部署：從 Windows 到 WebAssembly 的遊戲發布

## Bevy 的跨平台支援

Bevy 基於 wgpu 圖形 API 抽象層，天生支援多種後端（Vulkan、Metal、DX12、OpenGL、WebGPU）。這意味著同一份程式碼可以編譯到六大平台：

| 平台 | 圖形後端 | 發行方式 |
|------|---------|----------|
| Windows | Vulkan / DX12 | 原生 exe |
| macOS | Metal / Vulkan | 原生 app bundle |
| Linux | Vulkan | 原生 binary |
| Web (WASM) | WebGPU / WebGL | wasm + HTML |
| iOS | Metal | App Store |
| Android | Vulkan | APK / Play Store |

## 桌面平台發布

### 跨編譯環境配置

```bash
# Windows 目標（在 macOS 上）
rustup target add x86_64-pc-windows-gnu
brew install mingw-w64

# Linux 目標（在 macOS 上）
rustup target add x86_64-unknown-linux-gnu

# macOS 目標（原生）
cargo build --release
```

### Cargo 配置最佳化

```toml
[profile.release]
opt-level = 3          # 最大化最佳化
lto = true             # 連結時最佳化，減少 binary 大小
codegen-units = 1      # 單一編譯單元，允許更多 inline
strip = "symbols"      # 移除除錯符號
```

## WebAssembly 發布

### 安裝工具鏈

```bash
rustup target add wasm32-unknown-unknown
cargo install wasm-bindgen-cli
cargo install trunk

# Trunk 是 Bevy WASM 部署的標準工具
```

### 設定 wasm 相容性

Bevy 需要針對 WASM 進行一些調整：

```rust
// 在 Cargo.toml 中設定預設特性排除音效
[dependencies]
bevy = { version = "0.14", default-features = false, features = [
    "bevy_winit",
    "bevy_pbr",
    "bevy_render",
] }

// 無法在 WASM 使用的 plugin 需要條件編譯
#[cfg(not(target_arch = "wasm32"))]
.add_plugins(WinAudioPlugin)

#[cfg(target_arch = "wasm32")]
.add_plugins(WebAudioPlugin)
```

### 建立 index.html

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { margin: 0; overflow: hidden; background: #000; }
        canvas { display: block; width: 100vw; height: 100vh; }
    </style>
</head>
<body>
    <script src="https://cdn.jsdelivr.net/npm/bevy_wasm_profiler/profiler.js"></script>
</body>
</html>
```

### 建置與部署

```bash
trunk build --release

# trunk 會自動處理 wasm-bindgen 和資源打包
# 輸出在 dist/ 目錄
ls dist/
# index.html   my_game_bg.wasm   my_game.js

# 部署到任何靜態伺服器即可
# 或使用 wasm-server -p 8080 dist/
```

## 行動平台發布

### iOS

```bash
rustup target add aarch64-apple-ios
cargo build --release --target aarch64-apple-ios
```

使用 Xcode 專案包裝。注意 iOS 的 Metal 要求以及 Touch 輸入處理：

```rust
fn touch_input_system(
    touches: Res<Touches>,
    mut player: Query<&mut Transform, With<Player>>,
) {
    for touch in touches.iter() {
        // 處理觸控輸入
        let position = touch.position();
    }
}
```

### Android

需要 NDK 和 cargo-ndk：

```bash
rustup target add aarch64-linux-android
cargo install cargo-ndk

cargo ndk -t arm64-v8a -o ../android/app/src/main/jniLibs build --release
```

Android 需要注意螢幕方向、硬體返回鍵、生命週期管理。

## 平台特定注意事項

### 檔案系統路徑

遊戲開發中處理資源路徑最常見的坑：

```rust
use bevy::asset::AssetServer;

fn asset_path() -> &'static str {
    #[cfg(target_arch = "wasm32")]
    { "assets/" }
    #[cfg(not(target_arch = "wasm32"))]
    { "assets/" }
}
```

### 輸入裝置差異

```rust
fn universal_input(
    keyboard: Res<Input<KeyCode>>,
    gamepad: Res<GamepadSettings>,
    touches: Res<Touches>,
) {
    #[cfg(not(target_arch = "wasm32"))]
    if keyboard.pressed(KeyCode::Space) {
        jump();
    }

    #[cfg(target_arch = "wasm32")]
    if touches.any_just_pressed() {
        jump();
    }
}
```

### 螢幕解析度適應

```rust
fn setup_resolution(mut windows: Query<&mut Window>) {
    let mut window = windows.single_mut();

    #[cfg(target_arch = "wasm32")]
    {
        // WASM 模式填滿視窗
        if let Some(web_sys_window) = web_sys::window() {
            let width = web_sys_window.inner_width().unwrap().as_f64().unwrap() as f32;
            let height = web_sys_window.inner_height().unwrap().as_f64().unwrap() as f32;
            window.resolution.set(width, height);
        }
    }

    #[cfg(not(target_arch = "wasm32"))]
    {
        // 桌面模式設定固定解析度
        window.resolution.set(1920.0, 1080.0);
    }
}
```

## CI/CD 自動化

使用 GitHub Actions 同時建置所有平台：

```yaml
jobs:
  build:
    strategy:
      matrix:
        target:
          - x86_64-pc-windows-gnu
          - x86_64-apple-darwin
          - x86_64-unknown-linux-gnu
          - wasm32-unknown-unknown
    steps:
      - uses: actions/checkout@v4
      - run: rustup target add ${{ matrix.target }}
      - run: cargo build --release --target ${{ matrix.target }}
```

## 延伸閱讀

- [Bevy 跨平台部署指南](https://www.google.com/search?q=Bevy+cross+platform+deployment+guide)
- [Rust WASM 遊戲開發](https://www.google.com/search?q=Rust+WebAssembly+game+development)
- [Trunk WASM 建置工具](https://www.google.com/search?q=Trunk+Rust+WASM+bundler)
