# ECS 架構基礎（2014-2026）

## 從物件導向到資料導向

傳統遊戲開發長期依賴物件導向繼承體系：`GameObject` → `Character` → `Player` / `Enemy`。這種設計在小型專案中可行，但當遊戲規模擴大時，繼承樹會變得僵硬——你想新增一個「會飛的敵人可以撿道具」，就必須在繼承鏈中四處修改。

ECS（Entity-Component-System）架構在 2007 年首次被《天網》（Operation Flashpoint）的開發商 Bohemia Interactive 的 Scott Bilas 在 GDC 上提出，但他的想法真正普及是在 Blizzard 的《守望先鋒》（2016）之後。Tim Ford 在 GDC 2017 的演講中詳細說明了《守望先鋒》的 ECS 實作如何讓遊戲在多人對戰中保持流暢。

```
傳統繼承：            ECS 組合：
GameObject             Entity = ID
 ├─ Character           Component = 純資料
 │   ├─ Player          System = 純行為
 │   ├─ Enemy
 │   └─ NPC
 └─ Item
```

## Entity — 只是一個 ID

ECS 的第一個洞察：實體不需要行為，不需要資料，只需要一個識別碼。

```rust
struct Entity(u64);

// 你有一個 Entity 實體
let player = world.spawn((
    Position { x: 0.0, y: 0.0 },
    Velocity { dx: 1.0, dy: 0.0 },
    Health(100),
    PlayerTag,
));
```

Entity 是輕量級的控制代碼（handle）。你可以刪除它、複製它、將它儲存在其他 Component 中作為參考——但它的「行為」完全由它所附加的 Component 決定。

## Component — 扁平、最小、可組合

Component 的設計是 ECS 能否成功的關鍵。三個原則：

**扁平化**：不要巢狀結構。`Position { x, y }` 比 `Transform { translation, rotation, scale }` 更容易查詢和快取。

**最小化**：每個 Component 只代表一個概念。`Health(100)` 是一個；`Velocity { dx, dy }` 是一個。不要把它們塞進 `CharacterStats` 大結構中。

**可組合**：Entity 透過組合 Component 來獲得能力：

```rust
// 一個靜態的牆
world.spawn((Position { x: 5.0, y: 3.0 }, Wall));

// 一個移動中的玩家
world.spawn((Position { x: 0.0, y: 0.0 }, Velocity { dx: 0.0, dy: 0.0 }, Player));

// 一個會移動的牆（Boss 戰）
world.spawn((Position { x: 5.0, y: 3.0 }, Velocity { dx: 0.5, dy: 0.0 }, Wall, Boss));
```

## System — 行為的容器

System 是 ECS 的「大腦」。它查詢特定組合的 Entity，然後對它們進行操作。關鍵在於 System 之間不直接交流——它們都透過 Component 資料間接交流。

```rust
fn movement(mut query: Query<(&mut Position, &Velocity)>) {
    for (mut pos, vel) in query.iter_mut() {
        pos.x += vel.dx;
        pos.y += vel.dy;
    }
}

fn collision(query: Query<(&Position, &Collider)>, mut events: EventWriter<CollisionEvent>) {
    // AABB 或圓形碰撞偵測
}
```

## System 排程策略

System 的執行順序可以透過多種方式控制：

1. **顯式排序**：A → B → C
2. **隱式排序**：透過資料存取模式自動推導（讀取 vs 寫入）
3. **並行排程**：讀取同一 Component 的多個 System 可並行執行；寫入同一 Component 的 System 必須序列化

Bevy 使用第二種方式。它在編譯期分析每個 System 查詢的 Component 存取權限（`&T` 唯讀 vs `&mut T` 可寫），然後建構一個無衝突的排程圖。

```rust
app.add_systems(Update, (
    movement,
    collision,
    render,
));
// Bevy 自動推導：movement 寫入 Position，collision 讀取 Position
// → movement 必須先於 collision
// render 只讀取 Transform → 可與兩者並行
```

## Rust 中 ECS 的優勢

Rust 的型別系統讓 ECS 實作達到了 C++ 無法比擬的安全層級。

| 特性 | Rust ECS (Bevy) | C++ ECS (EnTT) |
|------|----------------|----------------|
| 記憶體安全 | 編譯期檢查 | 執行期檢查 |
| 資料競爭 | 不可能發生 | 開發者自行負責 |
| 查詢過濾 | 型別層級，零成本 | 字串或位元標記 |
| 並行排程 | 自動推導 | 手動管理 |

最重要的是，ECS 的資料導向設計與 Rust 的所有權模型完美吻合。System 對 Component 的存取就是 Rust 借用檢查器的自然應用——唯讀查詢產生 `&T` 引用（共享借用），可變查詢產生 `&mut T` 引用（獨佔借用）。任何違反規則的程式碼在編譯期就會報錯，而不是在遊戲發佈後的某個半夜崩潰。

## ECS 在 2026 年的生態

到了 2026 年，ECS 已經成為遊戲引擎的主流架構選擇。Unity 的 DOTS（Data-Oriented Tech Stack）、Unreal Engine 的 Mass Entity、以及 Rust 生態中的 Bevy 和 hecs，都採用 ECS 為核心設計。ECS 不再只是一個「遊戲架構模式」——它代表了從物件導向到資料導向的典範轉移。

## 參考

- [ECS 架構史 — Scott Bilas GDC 2007](https://www.google.com/search?q=Scott+Bilas+GDC+2007+ECS)
- [守望先鋒 ECS 架構 GDC 2017](https://www.google.com/search?q=Overwatch+GDC+2017+ECS+Tim+Ford)
- [Component 設計原則](https://www.google.com/search?q=ECS+component+design+principles+game+development)
- [Bevy ECS 文件](https://www.google.com/search?q=Bevy+ECS+documentation)

---

*本篇文章為「AI 程式人雜誌 2027 年 2 月號」Rust 遊戲開發系列之一。*
