# 2D 遊戲開發實戰（2021-2026）

## Sprite 渲染與動畫

Bevy 的 2D 渲染基於 `Sprite` 元件和 `SpriteSheet` 圖集實現。最簡單的方式是使用 `SpriteBundle`：

```rust
fn setup(mut commands: Commands, asset_server: Res<AssetServer>) {
    commands.spawn(Camera2dBundle::default());

    commands.spawn(SpriteBundle {
        texture: asset_server.load("character.png"),
        transform: Transform::from_xyz(0.0, 0.0, 0.0),
        ..default()
    });
}
```

對於角色動畫，Bevy 使用 `TextureAtlas` 將多個影格打包成一個紋理圖集：

```rust
fn animate_sprite(
    time: Res<Time>,
    mut query: Query<(&mut TextureAtlasSprite, &mut Handle<TextureAtlas>)>,
) {
    for (mut sprite, _atlas) in query.iter_mut() {
        sprite.index = ((time.elapsed_seconds() * 10.0) as u32) % 4;
    }
}
```

這裡 `sprite.index` 根據時間循環切換圖集中的影格，實現行走或跳躍動畫。

## 碰撞偵測

2D 碰撞偵測有兩種主流方法：

**AABB（軸對齊包圍盒）**：最簡單的碰撞形式，適用於矩形物體。

```rust
fn aabb_collision(a: &Position, a_size: &Vec2, b: &Position, b_size: &Vec2) -> bool {
    let a_min = a.0 - *a_size / 2.0;
    let a_max = a.0 + *a_size / 2.0;
    let b_min = b.0 - *b_size / 2.0;
    let b_max = b.0 + *b_size / 2.0;

    a_min.x < b_max.x && a_max.x > b_min.x &&
    a_min.y < b_max.y && a_max.y > b_min.y
}
```

**圓形碰撞**：用於子彈、玩家等圓形物體，只需計算圓心距離。

```rust
fn circle_collision(a: &Position, a_radius: f32, b: &Position, b_radius: f32) -> bool {
    let dx = a.0.x - b.0.x;
    let dy = a.0.y - b.0.y;
    let dist_sq = dx * dx + dy * dy;
    let radius_sum = a_radius + b_radius;
    dist_sq <= radius_sum * radius_sum
}
```

實務中，遊戲會先使用空間分割（如四叉樹或網格）減少碰撞檢查次數，再對可能碰撞的物體對進行精確判斷。

## 2D 物理引擎 — Rapier2d

雖然你可以自己寫簡單的碰撞，但完整的 2D 物理模擬（重力、摩擦力、關節、感測器）需要專業引擎。Bevy 生態中最成熟的選擇是 `bevy_rapier2d`。

```rust
use bevy_rapier2d::prelude::*;

fn setup_physics(mut commands: Commands) {
    commands.spawn((
        RigidBody::Dynamic,
        Collider::cuboid(0.5, 0.5),
        Velocity { linvel: Vec2::new(5.0, 0.0), angvel: 0.0 },
        Position { x: 0.0, y: 10.0 }.into(),
    ));
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_plugin(RapierPhysicsPlugin::<NoUserData>::pixels_per_meter(100.0))
        .add_plugin(RapierDebugRenderPlugin::default())
        .add_systems(Startup, setup_physics)
        .run();
}
```

Rapier 由法國數學家 Sébastien Crozet 開發，使用純 Rust 撰寫（無 C 繫結），支援：
- 剛體動力學與運動學
- 多種碰撞體：矩形、圓形、凸多邊形、三角形網格
- 關節：固定、旋轉、稜柱、彈簧
- 感測器（觸發器）與碰撞事件
- 平行解算（利用 rayon）

## 攝影機控制

2D 遊戲的攝影機控制是玩家體驗的關鍵：

```rust
// 跟隨玩家
fn follow_player(
    mut query: Query<&mut Transform, With<Camera>>,
    player_query: Query<&Transform, (With<Player>, Without<Camera>)>,
) {
    let mut camera = query.single_mut();
    let player = player_query.single();
    camera.translation = camera.translation.lerp(
        Vec3::new(player.translation.x, player.translation.y, camera.translation.z),
        0.1, // 平滑跟隨
    );
}
```

**攝影機搖晃（Camera Shake）** 在攻擊或爆炸時增添回饋感：

```rust
fn camera_shake(
    time: Res<Time>,
    mut camera: Query<&mut Transform, With<Camera>>,
    mut shake_state: ResMut<ShakeState>,
) {
    if shake_state.intensity > 0.0 {
        let mut cam = camera.single_mut();
        let offset = Vec2::new(
            rand::random::<f32>() - 0.5,
            rand::random::<f32>() - 0.5,
        ) * shake_state.intensity;
        cam.translation.x += offset.x;
        cam.translation.y += offset.y;
        shake_state.intensity *= 0.9; // 衰減
        if shake_state.intensity < 0.01 {
            shake_state.intensity = 0.0;
        }
    }
}
```

## 2026 年的 2D Bevy 生態

到了 2026 年，Bevy 的 2D 生態已相當成熟。社群開發了各種專用插件：Tilemap 瓦片地圖編輯器、粒子系統、2D 光效（Lights2D）、 Spine 骨骼動畫匯入、Aseprite 精靈編輯器整合工具。Bevy 的 2D 渲染效能已經可以媲美專用 2D 引擎如 Godot。

## 參考

- [Bevy 2D 教學](https://www.google.com/search?q=Bevy+2D+game+tutorial+Rust)
- [bevy_rapier 文件](https://www.google.com/search?q=bevy_rapier2d+documentation)
- [AABB 碰撞偵測](https://www.google.com/search?q=AABB+collision+detection+2D+game)
- [Bevy 攝影機控制](https://www.google.com/search?q=Bevy+camera+follow+2D)

---

*本篇文章為「AI 程式人雜誌 2027 年 2 月號」Rust 遊戲開發系列之一。*
