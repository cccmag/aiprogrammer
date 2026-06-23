# 網路多人遊戲（2022-2026）

## 多人遊戲的挑戰

網路遊戲開發的核心挑戰在於：如何讓多台電腦共享同一個遊戲世界，同時應對延遲、封包遺失和頻寬限制？傳統的鎖步同步（Lockstep）已不敷使用，現代遊戲需要更複雜的技術。

Bevy 生態中有兩個主要的多人遊戲函式庫：**bevy_replicon**（基於可靠 UDP 的狀態同步框架）和 **Matchbox**（配對與 WebRTC 連線）。

## 客戶端-伺服器架構

在 Bevy 中，客戶端和伺服器可以共用同一個程式碼庫，透過 Plugin 的條件啟用來區分：

```rust
struct NetworkPlugin;

impl Plugin for NetworkPlugin {
    fn build(&self, app: &mut App) {
        #[cfg(feature = "server")]
        app.add_plugins(ServerPlugin);

        #[cfg(feature = "client")]
        app.add_plugins(ClientPlugin);
    }
}

// 伺服端
struct ServerPlugin;
impl Plugin for ServerPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, start_server)
           .add_systems(Update, (receive_inputs, game_tick, broadcast_state));
    }
}
```

伺服器是權威（Authority），負責所有遊戲邏輯的驗證和世界狀態的維護。客戶端只是顯示伺服器的世界投影，並將玩家的輸入發送給伺服器。

## 狀態同步（Replication）

`bevy_replicon` 提供了 ECS 原生的狀態同步機制。你只需標記要同步的 Component，框架會自動處理序列化和網路傳輸：

```rust
use bevy_replicon::prelude::*;

// 只有標記 Replication 的 Component 才會被同步
#[derive(Component, Serialize, Deserialize)]
struct Health(i32);

#[derive(Component, Serialize, Deserialize)]
struct Position {
    x: f32,
    y: f32,
}

// 將要同步的 Component 註冊到 ServerPlugin
app.replicate::<Position>()
   .replicate::<Health>();
```

伺服器只需修改 Entity 上的 Component 值，replicon 會自動計算差異（delta compression）並廣播給所有客戶端。

```rust
fn server_tick(mut query: Query<(&mut Position, &Velocity)>, time: Res<Time>) {
    for (mut pos, vel) in query.iter_mut() {
        pos.x += vel.dx * time.delta_seconds();
        pos.y += vel.dy * time.delta_seconds();
    }
    // replicon 會自動偵測 Position 的變化並發送給客戶端
}
```

## 客戶端預測與伺服器回朔

網路延遲是不可避免的。如果客戶端必須等待伺服器回傳結果才能更新畫面，玩家會感到明顯的延遲。解決方案是**客戶端預測**：

```rust
// 客戶端：立即應用玩家的操作
fn client_prediction(
    mut query: Query<(&mut Position, &Velocity), With<LocalPlayer>>,
    input: Res<PlayerInput>,
    time: Res<Time>,
) {
    for (mut pos, vel) in query.iter_mut() {
        pos.x += input.horizontal * 200.0 * time.delta_seconds();
        pos.y += input.vertical * 200.0 * time.delta_seconds();
    }
}
```

客戶端先「假設」自己的操作會被伺服器接受，立即更新畫面。當伺服器的權威狀態到達時，客戶端需要將自己的預測狀態與伺服器狀態對齊——這就是**伺服器回朔**（Server Reconciliation）。

```
時間線：
客戶端：輸入 A ──► 預測狀態 A'  ──► 輸入 B ──► 預測狀態 B'
                    │                              │
                    │ 網路延遲                       │
伺服器：            ├── 收到 A ──► 計算 A' ──► 廣播 A'
                                                  │
客戶端：(回朔)      ◄────────────────────────── 收到伺服器 A'
          └── 如果預測和權威不一致，修正位置
```

實作中，客戶端會保存最近 N 幀的輸入歷史。當伺服器狀態到達時，客戶端找到對應的時間點，修正狀態，然後重新套用尚未被伺服器確認的輸入。

## GGPO 回朔（Rollback）

GGPO（Good Game Peace Out）是由 Tony Cannon（FightCade 創辦人）開發的網路代碼技術，專為格鬥遊戲設計。它是伺服器回朔的極端版本——不僅預測自己的操作，還預測對手的操作。

當伺服器的權威狀態與客戶端的預測不一致時，GGPO 會「回朔」到衝突的時間點，重新模擬所有玩家的操作，然後快速「快轉」回當前幀。這個過程必須在單幀時間內完成。

```rust
// GGPO 風格的回朔架構（概念性）
fn rollback_simulation(
    mut world: ResMut<RollbackWorld>,
    inputs: Res<SavedInputs>,
    frame: Res<CurrentFrame>,
) {
    // 1. 儲存當前世界狀態
    let snapshot = world.save_snapshot();

    // 2. 回朔到衝突幀
    world.load_snapshot(&snapshot_at(frame.conflict_frame));

    // 3. 使用校正後的輸入重新模擬
    for f in frame.conflict_frame..frame.current {
        world.apply_inputs(&inputs.for_frame(f));
        world.tick();
    }

    // 4. 完成——世界已修正到當前幀
}
```

## Bevy Replicon 與 Matchbox

**bevy_replicon**（2022 年發布）是 Bevy 社群最成熟的網路同步庫，支援：
- 基於 Component 的自動同步
- 權限管理（伺服器權威、客戶端權威、混合）
- 優先級佇列與頻寬控制
- 房間管理

**Matchbox** 負責連線建立與 NAT 穿透，基於 WebRTC 或原始 UDP Socket。兩者搭配使用：

```rust
fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_plugins(MatchboxClient::new(WebRtcSocket::new("wss://matchbox.example.com")))
        .add_plugins(RepliconServerPlugin)
        .add_systems(Update, server_tick);
}
```

到了 2026 年，已有 Steam 上架的 Rust 遊戲（如《Veloren》開源 RPG）使用 Bevy + Replicon 實現多人連線，驗證了這個架構的成熟度。

## 參考

- [Bevy Replicon 文件](https://www.google.com/search?q=bevy_replicon+documentation)
- [GGPO Rollback 網路代碼](https://www.google.com/search?q=GGPO+rollback+networking+code)
- [客戶端預測與伺服器回朔](https://www.google.com/search?q=client+prediction+server+reconciliation+game)
- [Matchbox Bevy 配對](https://www.google.com/search?q=Matchbox+Bevy+networking)

---

*本篇文章為「AI 程式人雜誌 2027 年 2 月號」Rust 遊戲開發系列之一。*
