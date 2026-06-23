# Bevy 引擎入門（2020-2026）

## Bevy 的誕生與哲學

Bevy 由 Carter Anderson 於 2020 年創立。Carter 曾是 Unity 的工程師，對 C# 遊戲引擎的設計限制感到沮喪。他在 2020 年 8 月發布了 Bevy 0.1，這是一個從頭開始就用 Rust 撰寫、完全基於 ECS 架構的遊戲引擎。

Bevy 的設計哲學可以用一句話概括：**資料導向、無 GC、模組化、開源友好**。它不依賴任何反射或執行期型別資訊——所有型別資訊都在編譯期透過 Rust 的 trait 系統解析。

## 版本演進

| 版本 | 日期 | 里程碑 |
|------|------|--------|
| 0.1 | 2020-08 | 首個公開版本，2D 渲染、ECS 核心 |
| 0.5 | 2021-04 | 3D 渲染支援、PBR 材質、GLTF 載入 |
| 0.9 | 2022-04 | 完整著色器管線、算圖（Compute Shader） |
| 1.0 | 2022-12 | API 穩定化、效能大幅提升 |
| 2.0 | 2024-06 | GPU 驅動排程、非同步任務系統、全新 UI 框架 |
| 2.5 | 2025-03 | 多執行緒渲染器、WebGPU 支援、行動平台最佳化 |
| 2.8 | 2026-01 | 完整編輯器（Bevy Editor）、資產管線強化 |

## AppBuilder 與 Plugin 系統

Bevy 的應用程式由 `App` 結構體建構。透過 Builder 模式，你可以逐步加入 Plugin、System、Resource 和 Event。

```rust
use bevy::prelude::*;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)  // 官方預設插件套件
        .add_plugins(MyGamePlugin)    // 自訂插件
        .run();
}
```

Plugin trait 是 Bevy 模組化的基石。它讓你可以將遊戲邏輯封裝成可獨立測試、可重複使用的套件：

```rust
pub struct MyGamePlugin;

impl Plugin for MyGamePlugin {
    fn build(&self, app: &mut App) {
        app
            .init_resource::<GameState>()
            .add_event::<ScoreEvent>()
            .add_systems(Startup, setup_camera)
            .add_systems(Update, (
                player_movement,
                enemy_ai,
                collision_detection,
            ));
    }
}
```

每個 Plugin 可以獨立：
- 註冊資源和事件
- 新增 System 到不同排程階段（Startup、Update、FixedUpdate）
- 引入子 Plugin

## 核心元件

Bevy 內建了遊戲開發所需的核心 Component：

```rust
// Transform — 位置、旋轉、縮放
struct Transform {
    translation: Vec3,
    rotation: Quat,
    scale: Vec3,
}

// Sprite — 2D 精靈渲染
struct Sprite {
    color: Color,
    custom_size: Option<Vec2>,
    flip_x: bool,
    flip_y: bool,
}

// Camera — 視角定義
struct Camera {
    // 投影矩陣由 Bevy 自動管理
}

// 將它們組合到一個 Entity：
commands.spawn((
    SpriteBundle {
        texture: asset_server.load("player.png"),
        transform: Transform::from_xyz(0.0, 0.0, 0.0),
        ..default()
    },
    Player,
));
```

## 資源（Resource）與事件（Event）

ECS 中的 Component 是附加到 Entity 的資料，但有些資料是全域性的——例如「遊戲分數」、「網路連線狀態」、「音效管理器」。這些就是 Resource。

```rust
#[derive(Resource)]
struct Score(u32);

// 在 System 中存取
fn show_score(score: Res<Score>) {
    println!("目前分數：{}", score.0);
}

fn add_score(mut score: ResMut<Score>) {
    score.0 += 100;
}
```

Event 是 Bevy 的訊息傳遞機制。用於「一次性」的溝通，例如「碰撞發生」、「敵人死亡」：

```rust
#[derive(Event)]
struct EnemyDied(Entity);

// 發送事件
fn detect_death(mut ev_death: EventWriter<EnemyDied>, health_query: Query<(Entity, &Health)>) {
    for (entity, health) in health_query.iter() {
        if health.0 <= 0 {
            ev_death.send(EnemyDied(entity));
        }
    }
}

// 接收事件
fn handle_death(mut ev_death: EventReader<EnemyDied>, mut commands: Commands) {
    for event in ev_death.read() {
        commands.entity(event.0).despawn();
        println!("敵人消滅！");
    }
}
```

Resource 與 Event 的區別：Resource 是持久狀態，Event 是瞬發訊息。兩者都在 ECS 架構中保持型別安全。

## Bevy 2.0 的關鍵創新

2024 年的 Bevy 2.0 引入了 GPU 驅動的 ECS 排程，允許部分 System 直接在 GPU 上執行，大幅減少了 CPU-GPU 間的資料傳輸。此外，它還引入了：

- **非同步資產載入**：不阻塞遊戲執行緒
- **動態連結**：Plugin 可在執行期載入/卸載
- **內建 UI 系統**：基於 flexbox 的宣告式 UI

到了 2026 年，Bevy 已經成為 Rust 遊戲開發的事實標準，被數百個商業專案採用。

## 參考

- [Bevy 官方網站](https://www.google.com/search?q=Bevy+game+engine)
- [Bevy Book 教學](https://www.google.com/search?q=Bevy+book+tutorial)
- [Bevy 2.0 更新日誌](https://www.google.com/search?q=Bevy+2.0+release+notes)
- [Carter Anderson 專訪](https://www.google.com/search?q=Carter+Anderson+Bevy+interview)

---

*本篇文章為「AI 程式人雜誌 2027 年 2 月號」Rust 遊戲開發系列之一。*
