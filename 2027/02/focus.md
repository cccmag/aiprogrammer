# 本期焦點

## Rust 遊戲開發 — Bevy 引擎與 ECS 架構

### 引言

遊戲開發一直是程式設計中最具挑戰性也最有回報的領域之一。過去，C++ 憑藉 Unreal Engine 主宰 AAA 遊戲開發，而 C# 則透過 Unity 成為獨立開發者和行動遊戲的首選。但 Rust 的出現正在悄悄地改變這個格局。

Rust 在遊戲開發中的優勢是獨特的：零成本抽象讓遊戲迴圈沒有 GC 停頓；所有權模型讓資源管理在編譯期就得到保證；而更重要的是——**ECS（Entity Component System）** 架構與 Rust 的型別系統天然契合，比 C++ 的 ECS 實作更安全、更優雅。

Bevy 是目前 Rust 生態中最成熟的遊戲引擎。它完全使用 ECS 架構，無需 GC，無需虛擬繼承——一切都是組合而非繼承。本期將帶領你從 ECS 的核心概念開始，逐步建構出完整的遊戲開發知識體系，最後探討 AI 如何輔助遊戲開發流程。

---

## 大綱

* [程式：實作 mini-ecs — 從零開始的 ECS 框架](focus_code.md)
   - Entity、Component、System 的核心實作
   - 查詢與迭代器
   - 遊戲迴圈與時間系統

1. [ECS 架構基礎（2014-2026）](focus1.md)
   - ECS 的起源與演進
   - Component 設計原則
   - System 的執行順序與排程

2. [Bevy 引擎入門（2020-2026）](focus2.md)
   - Bevy 的設計哲學
   - AppBuilder 與 Plugin
   - 核心元件與資源

3. [2D 遊戲開發實戰（2021-2026）](focus3.md)
   - Sprite 與動畫
   - 碰撞偵測與物理
   - 攝影機與視角控制

4. [3D 遊戲開發與著色器（2022-2026）](focus4.md)
   - Bevy 3D 渲染管線
   - WGSL 著色器程式設計
   - PBR 材質與光照

5. [遊戲音效與輸入處理（2021-2026）](focus5.md)
   - 音效引擎整合
   - 鍵盤/滑鼠/遊戲手把輸入
   - 狀態管理與場景切換

6. [網路多人遊戲（2022-2026）](focus6.md)
   - 客戶端-伺服器架構
   - 狀態同步與預測
   - Bevy Replicon 與 Matchbox

7. [AI 輔助遊戲開發（2024-2026）](focus7.md)
   - LLM 生成遊戲素材與程式碼
   - 程式化生成（Procedural Generation）
   - AI 驅動的 NPC 行為

---

## 遊戲開發架構層次

```
遊戲邏輯 (System: 移動、碰撞、AI)
      │  ECS 查詢
元件資料 (Component: Position, Health, Velocity)
      │  唯一 Entity ID
實體容器 (Entity: 輕量識別碼)
      │
Bevy 引擎核心 (AppBuilder、Plugin、Schedule)
      │
Rust 語言與工具鏈 ( cargo / wgpu / winit )
```

## 濃縮回顧

### Rust 遊戲開發的里程碑

- **2014**：Piston 專案啟動，最早的 Rust 遊戲引擎之一
- **2018**：Amethyst 引擎發布，引入 ECS 架構
- **2020**：Bevy 0.1 發布，純 ECS 設計
- **2021**：Bevy 0.5 加入 3D 渲染支援
- **2022**：Bevy 1.0 發布，正式穩定
- **2024**：Bevy 2.0 加入 GPU 驅動的 ECS 排程
- **2026**：Bevy 生態成熟，Steam 上出現多款 Rust 商業遊戲

### 為什麼 Rust 適合遊戲開發？

| 特性 | Rust | C++ (Unreal) | C# (Unity) |
|------|------|-------------|-----------|
| GC 停頓 | 無 | 無 | 有（頻繁） |
| ECS 安全 | 編譯期保證 | 執行期檢查 | 執行期檢查 |
| 記憶體控制 | 精確 | 精確 | 有限 |
| 編譯時間 | 中 | 長（AAA 專案） | 快 |
| 跨平台 | 原生支援 | 廣泛 | 廣泛 |

### ECS 的核心模式

ECS 將傳統物件導向的「遊戲物件」拆解為三個層次：

```rust
// Entity — 只是一個 ID
struct Entity(u64);

// Component — 純資料，無行為
struct Position { x: f32, y: f32 }
struct Velocity { dx: f32, dy: f32 }
struct Health(i32);

// System — 純行為，操作元件
fn movement_system(query: Query<(&mut Position, &Velocity)>) {
    for (mut pos, vel) in query.iter() {
        pos.x += vel.dx;
        pos.y += vel.dy;
    }
}
```

這種設計的關鍵優點：
- **資料導向**：相同類型的元件在記憶體中連續排列，CPU 快取友好
- **組合取代繼承**：Entity 的行為由它擁有的 Component 組合決定
- **系統解耦**：System 之間沒有直接依賴，易於測試和並行化

### Bevy Plugin 系統

Bevy 透過 Plugin 實現模組化：

```rust
struct HelloPlugin;

impl Plugin for HelloPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, setup)
           .add_systems(Update, (move_player, render));
    }
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_plugin(HelloPlugin)
        .run();
}
```

### ECS 查詢模式

Bevy 的查詢系統利用 Rust 的型別系統在編譯期建構存取模式：

```rust
// 唯讀查詢
fn read_positions(query: Query<&Position>) {}

// 可變查詢（一次只能有一個可變借用）
fn move_enemies(mut query: Query<&mut Position, With<Enemy>>) {}

// 排除特定元件
fn query_excluding(query: Query<&Transform, Without<Player>>) {}

// 多元件組合
fn complex_query(q: Query<(&Transform, &mut Velocity, Option<&Health>)>) {}
```

`With<T>`、`Without<T>`、`Option<T>` 等過濾器讓查詢表達力極強，且所有檢查都在編譯期完成。

---

**下一步**：[程式實作](focus_code.md) → [ECS 架構基礎](focus1.md)

## 延伸閱讀

- [Bevy 引擎官方網站](https://www.google.com/search?q=Bevy+game+engine+Rust)
- [ECS 架構深入介紹](https://www.google.com/search?q=Entity+Component+System+architecture)
- [Bevy Book](https://www.google.com/search?q=Bevy+book+tutorial)
- [Rust 遊戲開發入門](https://www.google.com/search?q=Rust+game+development+tutorial)
