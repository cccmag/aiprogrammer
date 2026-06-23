# AI 輔助遊戲開發（2024-2026）

## LLM 生成遊戲素材

2024 年以來，大型語言模型（LLM）和生成式 AI 深刻改變了遊戲開發流程。過去需要專業美術、音效設計師和程式設計師協作數週的工作，現在可以在數小時內由 AI 輔助完成。

### 程式碼生成

LLM 可以根據自然語言描述生成 Bevy 程式碼：

```
「生成一個 Bevy Plugin，包含 PhysicsPlugin，
整合 bevy_rapier3d，設定重力為 -9.81，
並在 Startup 中生成一個掉落中的方塊。」
```

```rust
use bevy::prelude::*;
use bevy_rapier3d::prelude::*;

pub struct PhysicsPlugin;

impl Plugin for PhysicsPlugin {
    fn build(&self, app: &mut App) {
        app.add_plugins(RapierPhysicsPlugin::<NoUserData>::default())
           .add_systems(Startup, spawn_test_cube);
    }
}

fn spawn_test_cube(mut commands: Commands) {
    commands.spawn((
        RigidBody::Dynamic,
        Collider::cuboid(0.5, 0.5, 0.5),
        TransformBundle::from(Transform::from_xyz(0.0, 10.0, 0.0)),
    ));
}
```

### 美術素材生成

結合 Stable Diffusion 與 LLM，開發者可以快速產出遊戲所需的美術資源：
- 角色立繪與精靈圖
- 場景背景圖
- UI 圖示和按鈕
- 紋理貼圖（法線貼圖、高度圖）

工作流程：LLM 生成提示詞 → 擴散模型生成圖像 → 後處理（去背、圖集打包）→ 匯入 Bevy。

### 音效生成

Meta 的 AudioCraft 和 Stable Audio 等模型可以根據文字描述生成音效和背景音樂：

```
「生成一首中世紀風格的冒險背景音樂，BPM 120，
使用風笛和魯特琴，持續 30 秒。」
```

AI 生成的音效可以直接匯出為 WAV 或 OGG，被 `bevy_audio` 使用。

## 程式化生成（Procedural Generation）

程式化生成是 AI 輔助遊戲開發的另一個重要面向。它使用演算法而非人工手動創建遊戲內容。

### 隨機地圖生成

使用 Perlin 雜訊（由 Ken Perlin 在 1983 年發明）生成地形高度圖：

```rust
fn generate_terrain(
    mut commands: Commands,
    meshes: ResMut<Assets<Mesh>>,
    materials: ResMut<Assets<StandardMaterial>>,
) {
    let noise = NoiseBuilder::fbm_2d(100, 100)
        .with_seed(42)
        .with_freq(0.05)
        .generate();

    for x in 0..100 {
        for y in 0..100 {
            let height = noise[(x * 100 + y) as usize];
            if height > 0.3 {
                // 生成樹木
                commands.spawn(PbrBundle {
                    mesh: meshes.add(Cylinder::new(0.1, 0.5)),
                    material: materials.add(Color::rgb(0.2, 0.8, 0.2)),
                    transform: Transform::from_xyz(x as f32, height, y as f32),
                    ..default()
                });
            }
        }
    }
}
```

常見的程式化生成演算法：
- **Perlin/Simplex 雜訊**：地形、雲層、紋理
- **Celluar Automata**：洞穴、地下城房間
- **Binary Space Partition（BSP）**：地牢佈局
- **Wave Function Collapse**：無限 tile 地圖
- **L-System**：樹木、植物、道路網絡

```rust
// Wave Function Collapse 概念
fn wfc_generate(grid: &mut Grid, rules: &TileRules) {
    // 1. 找到 entropy 最小的格子
    // 2. 對其進行崩塌（選擇一種可能性）
    // 3. 根據規則傳播約束
    // 4. 重複直到所有格子崩塌或失敗
}
```

## AI 驅動的 NPC 行為

傳統的 NPC AI 使用有限狀態機（FSM）和行為樹。2024 年後，LLM 開始被用於驅動更自然的 NPC 對話和行為。

### GOAP（Goal-Oriented Action Planning）

Jeff Orkin 在《F.E.A.R.》（2005）中推廣的 GOAP 將 NPC 行為視為目標導向的規劃問題：

```rust
#[derive(Component)]
struct NPCGoal {
    goal: GoalType,
    priority: f32,
}

#[derive(Component)]
struct NPCAction {
    name: String,
    preconditions: WorldState,
    effects: WorldState,
    cost: f32,
}

fn goap_planner(
    npc: Entity,
    goals: &[NPCGoal],
    actions: &[NPCAction],
    world: &WorldState,
) -> Vec<Action> {
    // A* 搜尋從當前狀態到滿足最高優先級目標的路徑
    // 回傳一系列 action
}
```

### 行為樹（Behavior Tree）

行為樹是現代遊戲中最流行的 AI 架構，Bevy 社群有 `bevy_behavior_tree` 插件：

```rust
// Sequence 節點依序執行子節點
// Selector 節點選擇第一個成功的子節點
// Condition 節點檢查條件
// Action 節點執行操作

fn patrol_behavior() -> BehaviorTree {
    Sequence(vec![
        Condition(Box::new(IsPatrolTime)),
        Action(Box::new(MoveToPatrolPoint)),
        Action(Box::new(Wait { duration: 3.0 })),
    ])
}
```

### LLM 驅動的 NPC

2025-2026 年的最新進展是在本地運行小型 LLM（如 Llama 3、Gemma、Phi）來驅動 NPC 對話。NPC 擁有「記憶」和「個性」，對話不再基於固定腳本：

```rust
fn npc_llm_dialog(
    player_message: &str,
    npc_profile: &NPCProfile,
    conversation_history: &[Message],
) -> String {
    let prompt = format!(
        "你是 {}，一個 {} 個性的 NPC。\n背景：{}\n\n{}",
        npc_profile.name,
        npc_profile.personality,
        npc_profile.backstory,
        conversation_history.iter()
            .map(|m| format!("{}: {}", m.role, m.text))
            .collect::<Vec<_>>()
            .join("\n")
    );
    // 調用本地 LLM 推理
    llm_infer(&prompt)
}
```

## Rust + AI 的遊戲測試自動化

AI 的另一個應用是自動化遊戲測試。利用 LLM 生成測試腳本，並結合 Rust 的型別系統驗證遊戲邏輯：

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_movement_system() {
        let mut app = App::new();
        app.add_systems(Update, movement);

        let player = app.world.spawn((
            Position { x: 0.0, y: 0.0 },
            Velocity { dx: 1.0, dy: 0.0 },
        )).id();

        app.update(); // 執行一個 tick

        let pos = app.world.get::<Position>(player).unwrap();
        assert_eq!(pos.x, 1.0); // 速度 * delta = 移動
    }
}
```

AI 可以：
- 分析程式碼結構，生成邊界測試案例
- 模擬玩家操作，檢測崩潰和異常
- 生成效能基準測試，檢查迴歸

## 參考

- [LLM 遊戲素材生成](https://www.google.com/search?q=LLM+game+asset+generation+AI)
- [程式化生成演算法](https://www.google.com/search?q=procedural+generation+algorithms+game)
- [GOAP 遊戲 AI 規劃](https://www.google.com/search?q=GOAP+goal+oriented+action+planning+game+AI)
- [行為樹遊戲 AI](https://www.google.com/search?q=behavior+tree+game+AI+tutorial)
- [Rust 遊戲測試自動化](https://www.google.com/search?q=Rust+game+testing+automation+framework)

---

*本篇文章為「AI 程式人雜誌 2027 年 2 月號」Rust 遊戲開發系列之一。*
