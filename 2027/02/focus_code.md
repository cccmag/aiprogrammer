# 程式實作：mini-ecs — 從零開始的 ECS 框架

## 簡介

本實作將從零開始建構一個迷你 ECS（Entity Component System）框架，幫助理解 Bevy 等遊戲引擎的核心架構原理。完整程式碼在 `_code/src/lib.rs`。

## 核心架構

### 1. Entity — 輕量識別碼

Entity 只是一個 `u64` 包裝：

```rust
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub struct Entity(u64);
```

Entity 本身不包含任何資料，僅作為 Component 的索引鍵。

### 2. Component Storage — 類型安全的儲存

使用 `HashMap<TypeId, Box<dyn Any>>` 實現類型安全的元件儲存。每個元件類型對應一個 `Vec<Option<T>>`，陣列索引對應 Entity ID：

```rust
pub struct World {
    next_id: u64,
    entities: Vec<Entity>,
    components: HashMap<TypeId, Box<dyn ComponentVec>>,
}
```

`ComponentVec` trait 透過 `as_any`/`as_any_mut` 實現向下轉型：

```rust
trait ComponentVec: Any {
    fn as_any(&self) -> &dyn Any;
    fn as_any_mut(&mut self) -> &mut dyn Any;
    fn push_none(&mut self);
}
```

### 3. 查詢系統

我們實作了簡單的唯讀與可變查詢：

```rust
pub struct Query<'w, 's, T> {
    storage: &'s Vec<Option<T>>,
    entities: &'w [Entity],
}
```

查詢迭代器過濾出有該元件的 Entity：

```rust
impl<'w, 's, T: 'static> Query<'w, 's, T> {
    pub fn iter(&self) -> impl Iterator<Item = (Entity, &T)> {
        self.entities.iter().enumerate().filter_map(move |(idx, entity)| {
            self.storage.get(idx)?.as_ref().map(|c| (*entity, c))
        })
    }
}
```

### 4. System Trait

所有系統實作 `System` trait：

```rust
pub trait System {
    fn run(&mut self, world: &mut World);
}
```

### 5. 範例元件與系統

```rust
// 元件
pub struct Position { pub x: f32, pub y: f32 }
pub struct Velocity { pub dx: f32, pub dy: f32 }
pub struct Health(pub i32);
pub struct Enemy;

// 系統：移動
pub struct MovementSystem;

impl System for MovementSystem {
    fn run(&mut self, world: &mut World) {
        let snapshots: Vec<(Entity, f32, f32)> = { /* 收集速度快照 */ };
        for (entity, dx, dy) in &snapshots {
            if let Some(pos) = world.get_component_mut::<Position>(*entity) {
                pos.x += dx;
                pos.y += dy;
            }
        }
    }
}
```

### 6. 遊戲迴圈

```rust
pub struct GameLoop {
    world: World,
    systems: Vec<Box<dyn System>>,
}

impl GameLoop {
    pub fn run(&mut self) {
        let mut frame = 0u64;
        while frame < 120 {
            for system in &mut self.systems {
                system.run(&mut self.world);
            }
            frame += 1;
        }
    }
}
```

## 完整範例

在 `main.rs` 中，我們建立了一個包含玩家、敵人和 NPC 的場景：

```rust
fn main() {
    let mut game = GameLoop::new();

    let player = game.world().spawn();
    game.world().add_component(player, Position { x: 0.0, y: 0.0 });
    game.world().add_component(player, Velocity { dx: 1.5, dy: 0.8 });
    game.world().add_component(player, Health(10));

    let enemy = game.world().spawn();
    game.world().add_component(enemy, Position { x: 50.0, y: 30.0 });
    game.world().add_component(enemy, Velocity { dx: -0.5, dy: -0.3 });
    game.world().add_component(enemy, Health(5));
    game.world().add_component(enemy, Enemy);

    game.add_system(MovementSystem);
    game.add_system(HealthSystem);
    game.add_system(StatusSystem);
    game.run();
}
```

## 與 Bevy 的對比

| 特性 | mini-ecs | Bevy |
|------|----------|------|
| Entity | `u64` 包裝 | 類似，支援世代 |
| Component | `Vec<Option<T>>` | `Table`/`SparseSet` 雙層儲存 |
| System | `System` trait | Function + `SystemParam` |
| 查詢 | 手動迭代 | `Query` 參數 + 編譯期過濾 |
| 排程 | 固定順序 | 平行排程 + 依賴圖 |

## 執行與測試

```bash
cd _code
cargo build
cargo test    # 10 個測試全部通過
cargo run     # 執行 120 幀的遊戲迴圈
```

## 下一步

嘗試擴展這個 mini-ecs：
1. 加入 Entity 的回收與世代管理
2. 加入 System 排程（Before/After）
3. 加入平行 System 執行 (rayon)
4. 加入 `With<T>` / `Without<T>` 查詢過濾器
