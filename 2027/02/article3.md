# Bevy Plugin 生態導覽：從音效到物理

## 什麼是 Bevy Plugin？

Bevy 採用模組化架構，每項功能都以 Plugin 的形式存在。Plugin 可以註冊 system、component、resource、event，並設定執行順序。官方提供 `DefaultPlugins`（核心功能），社群則提供數百個第三方 plugin。

## 物理引擎：bevy_rapier

`bevy_rapier` 是 Bevy 生態中最成熟的物理引擎，基於 Rapier 物理庫：

```toml
[dependencies]
bevy = "0.14"
bevy_rapier2d = "0.28"
# 或 bevy_rapier3d = "0.28"
```

```rust
use bevy::prelude::*;
use bevy_rapier2d::prelude::*;

fn main() {
    App::new()
        .add_plugins((DefaultPlugins, RapierPhysicsPlugin::<NoUserData>::default()))
        .add_plugins(RapierDebugRenderPlugin::default())
        .add_systems(Startup, spawn_ball)
        .run();
}

fn spawn_ball(mut commands: Commands) {
    commands.spawn((
        RigidBody::Dynamic,
        Collider::ball(0.5),
        Restitution::coefficient(0.7),
        Velocity { linvel: Vec2::new(2.0, 0.0), angvel: 0.0 },
        TransformBundle::from(Transform::from_xyz(0.0, 4.0, 0.0)),
    ));
}
```

支援剛體、關節、感測器、碰撞事件、連續碰撞檢測（CCD）。

## 音效引擎：bevy_kira_audio

`bevy_kira_audio` 包裝 Kira 音訊庫，提供高品質音訊播放：

```rust
use bevy::prelude::*;
use bevy_kira_audio::prelude::*;

fn main() {
    App::new()
        .add_plugins((DefaultPlugins, AudioPlugin))
        .add_systems(Startup, play_music)
        .run();
}

fn play_music(asset_server: Res<AssetServer>, audio: Res<Audio>) {
    audio.play(asset_server.load("music/background.ogg"))
         .with_volume(0.6)
         .looped();
}
```

支援 WAV、OGG、MP3、FLAC。可控制音量、聲像、淡入淡出、音效實例管理。

## UI 框架：bevy_egui

將 egui 嵌入 Bevy，適合除錯 UI 和工具視窗：

```rust
use bevy::prelude::*;
use bevy_egui::{egui, EguiContexts, EguiPlugin};

fn main() {
    App::new()
        .add_plugins((DefaultPlugins, EguiPlugin))
        .add_systems(Update, ui_example)
        .run();
}

fn ui_example(mut contexts: EguiContexts) {
    egui::Window::new("除錯面板").show(contexts.ctx_mut(), |ui| {
        ui.label("FPS: 60");
        if ui.button("重置場景").clicked() {
            // 觸發重置事件
        }
    });
}
```

## 除錯工具：bevy_inspector_egui

視覺化編輯 scene 中的元件值：

```rust
use bevy::prelude::*;
use bevy_inspector_egui::quick::WorldInspectorPlugin;

fn main() {
    App::new()
        .add_plugins((
            DefaultPlugins,
            WorldInspectorPlugin::new(),
        ))
        .run();
}
```

## 動畫系統：bevy_tweening

宣告式補間動畫：

```rust
use bevy::prelude::*;
use bevy_tweening::*;

fn spawn_animated_ui(mut commands: Commands) {
    let tween = Tween::new(
        EaseFunction::QuadraticInOut,
        Duration::from_secs(2),
        TransformPositionLens {
            start: Vec3::ZERO,
            end: Vec3::new(100.0, 0.0, 0.0),
        },
    ).with_repeat_count(RepeatCount::Infinite);

    commands.spawn((
        SpriteBundle { ..default() },
        Animator::new(tween),
    ));
}
```

## 粒子系統：bevy_hanabi

GPU 驅動的粒子系統，支援大量粒子效果：

```rust
use bevy::prelude::*;
use bevy_hanabi::prelude::*;

fn spawn_fire(mut commands: Commands, mut effects: ResMut<Assets<EffectAsset>>) {
    let mut fire = ParticleEffect::default();
    fire.max_particle_count = 1024;
    fire.initializer = Box::new(InitPositionCircleModifier { ..default() });
    fire.update = vec![
        Box::new(UpdateSizeModifier { ..default() }),
        Box::new(UpdateAgeModifier { ..default() }),
    ];
    commands.spawn(ParticleEffectBundle {
        effect: ParticleEffect::new(effects.add(fire)),
        ..default()
    });
}
```

## 生態對比

| 功能 | Plugin | 替代方案 | 特點 |
|------|--------|----------|------|
| 物理 2D | bevy_rapier2d | bevy_xpbd_2d | Rapier 功能更全面 |
| 物理 3D | bevy_rapier3d | bevy_xpbd_3d | Rapier 支援 CCD |
| 音效 | bevy_kira_audio | bevy_oddio | Kira 功能較多 |
| UI | bevy_egui | bevy_ui / bevy_simple_text | egui 即時模式靈活 |
| 除錯 | bevy_inspector_egui | bevy_debug_text | Inspector 圖形化 |
| 動畫 | bevy_tweening | bevy_tween | Tweening 生態較大 |
| 粒子 | bevy_hanabi | bevy_wasm_particles | Hanabi GPU 加速 |

## 安裝策略

選擇 plugin 時考慮：
- **維護狀態**：檢查 GitHub 最近更新時間
- **Bevy 版本相容性**：確認 plugin 支援的 Bevy 版本
- **文件完整性**：範例程式碼是否可直接使用
- **效能需求**：行動裝置需輕量化方案

## 延伸閱讀

- [Bevy Assets — Plugin 列表](https://www.google.com/search?q=Bevy+Assets+Plugin+list)
- [Rapier 物理引擎文件](https://www.google.com/search?q=Rapier+physics+engine+Rust)
- [Bevy 官方 plugin 開發指南](https://www.google.com/search?q=Bevy+plugin+development+guide)
