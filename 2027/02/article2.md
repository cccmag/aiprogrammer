# 從物件導向到 ECS：思維轉換與實戰模式

## OOP 遊戲的經典困境

傳統物件導向的遊戲程式碼會寫出這樣的繼承結構：

```rust
// OOP 方式 — 類別繼承、虛擬分派
trait GameObject {
    fn update(&mut self, dt: f32);
    fn draw(&self);
}

struct Player {
    x: f32, y: f32,
    hp: i32,
    inventory: Vec<Item>,
}

impl GameObject for Player {
    fn update(&mut self, dt: f32) { /* 玩家邏輯 */ }
    fn draw(&self) { /* 繪製玩家 */ }
}

struct Enemy {
    x: f32, y: f32,
    hp: i32,
    ai_type: AiKind,
}

impl GameObject for Enemy {
    fn update(&mut self, dt: f32) { /* AI 邏輯 */ }
    fn draw(&self) { /* 繪製敵人 */ }
}
```

這種設計有幾個問題：
- **虛擬分派開銷**：每幀呼叫 `Box<dyn GameObject>` 方法需要兩次指標間接
- **破碎的資料佈局**：不同型別的 `GameObject` 分散在堆積各處，快取效率差
- **跨領域功能難以共享**：如果 `Player` 和 `Enemy` 都需要碰撞檢測，無法簡單複用

## ECS 的基本概念

ECS（Entity-Component-System）將上述結構拆解為三個層次：

1. **Entity**：只是一個 ID（`u32` 或 `u64`）
2. **Component**：純資料結構，沒有方法
3. **System**：純邏輯，操作一組具有特定 Component 的 Entity

```rust
// ECS 方式 — 資料與行為分離
struct Position(f32, f32);
struct Health(i32);
struct Velocity(f32, f32);
struct PlayerTag;   // 標記元件（marker component）
struct EnemyTag;

// Entity 只是 ID
// component 資料儲存在連續的 Vec 中
```

## Bevy ECS 實作

使用 Bevy 的 ECS 框架實作：

```rust
use bevy::prelude::*;

// 元件定義
#[derive(Component)]
struct Position { x: f32, y: f32 }

#[derive(Component)]
struct Health(i32);

#[derive(Component)]
struct Velocity { x: f32, y: f32 }

// System — 移動邏輯
fn movement_system(
    time: Res<Time>,
    mut query: Query<(&mut Position, &Velocity)>,
) {
    for (mut pos, vel) in query.iter_mut() {
        pos.x += vel.x * time.delta_seconds();
        pos.y += vel.y * time.delta_seconds();
    }
}

// System — 碰撞傷害
fn collision_system(
    mut enemies: Query<(&Position, &mut Health), With<EnemyTag>>,
    player: Query<&Position, With<PlayerTag>>,
) {
    let player_pos = player.single();
    for (pos, mut hp) in enemies.iter_mut() {
        let dist = ((pos.x - player_pos.x).powi(2)
                  + (pos.y - player_pos.y).powi(2)).sqrt();
        if dist < 10.0 {
            hp.0 -= 1;
        }
    }
}
```

## 重構案例：OOP 轉 ECS

### OOP 版本（反模式）

```rust
trait Bullet {
    fn update(&mut self, dt: f32);
    fn on_hit(&mut self, target: &mut dyn GameObject);
}

struct PlayerBullet { x: f32, y: f32, speed: f32, damage: i32 }

impl Bullet for PlayerBullet {
    fn update(&mut self, dt: f32) { self.y += self.speed * dt; }
    fn on_hit(&mut self, target: &mut dyn GameObject) { /* 複雜分派 */ }
}
```

### ECS 版本

```rust
#[derive(Component)]
struct Bullet { speed: f32, damage: i32 }

fn bullet_system(
    time: Res<Time>,
    mut bullets: Query<(&mut Transform, &Bullet)>,
) {
    for (mut transform, bullet) in bullets.iter_mut() {
        transform.translation.y += bullet.speed * time.delta_seconds();
    }
}

fn bullet_hit_system(
    mut commands: Commands,
    bullets: Query<(Entity, &Transform, &Bullet)>,
    enemies: Query<(&Transform, &mut Health)>,
) {
    // 遞迴查詢的寫法，編譯器完全靜態展開
}
```

## ECS 設計模式

| 模式 | 說明 | 適用場景 |
|------|------|----------|
| **Marker Component** | 無資料的標記元件 | 標記玩家、敵人、道具 |
| **Singleton Resource** | 全域共享資料 | 時間、輸入、音效管理器 |
| **Event System** | 跨 System 通訊 | 碰撞事件、得分事件 |
| **System Chaining** | System 執行順序控制 | 物理→動畫→渲染 |
| **Command Buffer** | 延遲生成/銷毀實體 | 子彈生成、敵人死亡 |

## System 執行順序

```rust
fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_systems(Update, (
            input_system,
            movement_system.after(input_system),
            collision_system.after(movement_system),
            death_system.after(collision_system),
        ))
        .run();
}
```

## 何時不該用 ECS？

- 簡單的回合制遊戲：傳統 OOP 更直接
- 實體數量極少（< 100）：ECS 優勢不明顯
- 深度巢狀的狀態機：考慮行為樹（behavior tree）

## 延伸閱讀

- [Bevy ECS 官方指南](https://www.google.com/search?q=Bevy+ECS+guide)
- [Game Programming Patterns — ECS](https://www.google.com/search?q=game+programming+patterns+ECS)
- [資料導向設計簡介](https://www.google.com/search?q=data-oriented+design+introduction)
