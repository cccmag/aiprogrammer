# Rust 中的遊戲 AI：行為樹與 GOAP

## 1. 引言

遊戲 AI 從早期遊戲的簡單狀態機演進到現代 AAA 遊戲中複雜的行為系統。Rust 的列舉型別（enum）和模式匹配讓實作狀態機變得自然，而其 trait 系統又為行為樹和 GOAP 提供了理想的抽象層。

## 2. 有限狀態機（FSM）

FSM 是最基礎的遊戲 AI 架構：

```rust
#[derive(Clone, Copy, PartialEq)]
enum NPCState {
    Idle,
    Patrol,
    Alert,
    Combat,
    Flee,
}

struct NPC {
    state: NPCState,
    health: f32,
    alert_level: f32,
}

impl NPC {
    fn update(&mut self, player_pos: Option<Vec2>) {
        self.state = match self.state {
            NPCState::Idle => {
                self.alert_level += 0.1;
                if self.alert_level > 5.0 { NPCState::Patrol } else { NPCState::Idle }
            }
            NPCState::Patrol => {
                if let Some(_) = player_pos { NPCState::Alert } else { NPCState::Patrol }
            }
            NPCState::Alert => {
                self.alert_level += 1.0;
                if self.alert_level > 10.0 { NPCState::Combat } else { NPCState::Alert }
            }
            NPCState::Combat => {
                if self.health < 20.0 { NPCState::Flee } else { NPCState::Combat }
            }
            NPCState::Flee => {
                if self.health > 80.0 { NPCState::Patrol } else { NPCState::Flee }
            }
        }
    }
}
```

FSM 的問題在於當狀態和轉換增多時，狀態爆炸讓維護變得困難。

## 3. 行為樹（Behavior Tree）

行為樹使用樹狀節點結構，每幀從根節點開始遍歷，決定 NPC 行為：

```rust
#[derive(Clone)]
enum BTStatus { Success, Failure, Running }

trait BTNode: Send + Sync {
    fn tick(&mut self, ctx: &mut AIContext) -> BTStatus;
}
```

### 3.1 基本節點

```rust
struct Sequence {
    children: Vec<Box<dyn BTNode>>,
    current: usize,
}

impl BTNode for Sequence {
    fn tick(&mut self, ctx: &mut AIContext) -> BTStatus {
        while self.current < self.children.len() {
            match self.children[self.current].tick(ctx) {
                BTStatus::Success => self.current += 1,
                BTStatus::Running => return BTStatus::Running,
                BTStatus::Failure => {
                    self.current = 0;
                    return BTStatus::Failure;
                }
            }
        }
        self.current = 0;
        BTStatus::Success
    }
}

struct Selector {
    children: Vec<Box<dyn BTNode>>,
    current: usize,
}

impl BTNode for Selector {
    fn tick(&mut self, ctx: &mut AIContext) -> BTStatus {
        while self.current < self.children.len() {
            match self.children[self.current].tick(ctx) {
                BTStatus::Failure => self.current += 1,
                BTStatus::Running => return BTStatus::Running,
                BTStatus::Success => {
                    self.current = 0;
                    return BTStatus::Success;
                }
            }
        }
        self.current = 0;
        BTStatus::Failure
    }
}
```

### 3.2 行為節點範例

```rust
struct PatrolNode {
    waypoints: Vec<Vec2>,
    index: usize,
}

impl BTNode for PatrolNode {
    fn tick(&mut self, ctx: &mut AIContext) -> BTStatus {
        let target = self.waypoints[self.index];
        let dist = ctx.position.distance(target);

        if dist < 5.0 {
            self.index = (self.index + 1) % self.waypoints.len();
        }

        // 向目標移動
        let direction = (target - ctx.position).normalize();
        ctx.position += direction * ctx.speed * ctx.dt;

        BTStatus::Running
    }
}

struct InRangeCondition {
    range: f32,
}

impl BTNode for InRangeCondition {
    fn tick(&mut self, ctx: &mut AIContext) -> BTStatus {
        if let Some(player) = ctx.player_pos {
            if ctx.position.distance(player) < self.range {
                BTStatus::Success
            } else {
                BTStatus::Failure
            }
        } else {
            BTStatus::Failure
        }
    }
}
```

## 4. GOAP（Goal-Oriented Action Planning）

GOAP 是一種基於規劃的 AI 架構——NPC 有一組目標和一組可用的行動，執行時搜尋最低成本的行動序列：

```rust
#[derive(Clone)]
struct WorldState {
    has_weapon: bool,
    has_ammo: bool,
    enemy_alive: bool,
    health: f32,
    distance_to_enemy: f32,
}

trait Action {
    fn cost(&self, state: &WorldState) -> f32;
    fn preconditions(&self) -> WorldState;
    fn effects(&self) -> WorldState;
    fn execute(&self, ctx: &mut AIContext);
}

struct GoapPlanner {
    actions: Vec<Box<dyn Action>>,
}

impl GoapPlanner {
    fn plan(&self, start: &WorldState, goal: &WorldState)
        -> Option<Vec<usize>>
    {
        // A* 搜尋：從 start 到 goal 的行動序列
        // 使用 preconditions/effects 做狀態轉換
        // 用 action.cost() 作為啟發式成本
        let mut open_set = Vec::new();
        let mut came_from = Vec::new();
        // ... A* 實作細節
        None // 簡化示範
    }
}
```

### 4.1 GOAP vs 行為樹

| 面向 | 行為樹 | GOAP |
|------|--------|------|
| 設計目標 | 可預測的行為流水線 | 動態規劃最佳解 |
| 除錯 | 容易（樹結構可視化） | 困難（規劃路徑不直觀） |
| 靈活性 | 需手動設計所有分支 | 自動組合行動序列 |
| 效能 | O(tree depth) | O(actions × states) |
| 適用場景 | 日常行為、巡邏、動畫 | 策略選擇、資源管理 |

## 5. Bevy ECS 整合

將行為樹整合到 Bevy 的 system 中：

```rust
#[derive(Component)]
struct BehaviorTreeComponent {
    tree: Box<dyn BTNode>,
}

#[derive(Resource)]
struct AIContextResource {
    player_pos: Option<Vec2>,
}

fn ai_system(
    mut query: Query<(&mut BehaviorTreeComponent, &mut Transform)>,
    context: Res<AIContextResource>,
    time: Res<Time>,
) {
    for (mut bt, mut transform) in query.iter_mut() {
        let mut ctx = AIContext {
            position: transform.translation.truncate(),
            player_pos: context.player_pos,
            dt: time.delta_seconds(),
            speed: 100.0,
        };
        bt.tree.tick(&mut ctx);
        transform.translation.x = ctx.position.x;
        transform.translation.y = ctx.position.y;
    }
}
```

## 6. 混合架構實務

大型專案通常結合兩者——行為樹處理 NPC 的日常行為，GOAP 在關鍵時刻（如 combat）接管。Rust 的列舉讓這種混合架構乾淨明確：

```rust
enum AIArchitecture {
    BehaviorTree(BehaviorTreeComponent),
    GoapPlanner(GoapPlanner),
    FSM(NPCState),
}
```

## 7. 結語

行為樹和 GOAP 各有適用場景。對獨立遊戲開發者，從行為樹開始是最務實的選擇；當 NPC 行為需要動態應對複雜環境時，再引入 GOAP。Rust 的型別系統為這兩種架構提供了堅實的基礎。

## 延伸閱讀

- [Behavior trees for game AI](https://www.google.com/search?q=behavior+trees+game+AI+implementation)
- [GOAP in game development](https://www.google.com/search?q=Goal-Oriented+Action+Planning+game+AI)
- [Game AI programming patterns](https://www.google.com/search?q=game+AI+programming+FSM+behavior+tree+GOAP)
