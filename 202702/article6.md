# 大型語言模型在遊戲開發中的應用

## 1. 引言

2025–2026 年間，大型語言模型（LLM）在程式碼生成能力上達到了一個轉折點——對於 Rust / Bevy 遊戲開發者而言，LLM 已經從「有趣的玩具」變成「日常生產力工具」。本文探討如何在遊戲開發流程中有效地使用 LLM。

## 2. LLM 輔助 Rust / Bevy 程式碼生成

### 2.1 元件與系統

Bevy ECS 的樣板程式碼很適合由 LLM 生成：

```
使用者輸入：
「為 Bevy 建立一個生命值（Health）元件和一個傷害 system，
元件值範圍 0–100，system 減少指定實體的生命值。」

LLM 輸出：

```rust
#[derive(Component)]
struct Health {
    current: f32,
    max: f32,
}

fn damage_system(
    mut query: Query<&mut Health>,
    mut events: EventReader<DamageEvent>,
) {
    for ev in events.read() {
        if let Ok(mut health) = query.get_mut(ev.entity) {
            health.current = (health.current - ev.amount).max(0.0);
        }
    }
}
```

### 2.2 自訂工具（Tool Use）

針對複雜的遊戲邏輯，將問題分解後逐步引導 LLM：

1. **定義資料結構**：先讓 LLM 產生元件定義
2. **實作 system**：基於已定義的元件實作 system
3. **加入測試**：要求 LLM 同時產生測試案例

這種鏈式提示（chain-of-thought prompting）在處理 Bevy 的查詢繫結和系統排序時特別有效。

## 3. NPC 對話與任務設計

### 3.1 對話樹生成

LLM 可以根據角色設定自動生成分支對話樹：

```
系統提示：
「你是一個奇幻 RPG 的 NPC 對話生成器。角色是一位性格孤僻但知識淵博的圖書館管理員。
生成 5 個對話選項，每個選項有 2 層子對話。」

LLM 輸出 JSON 格式的對話樹：

```json
{
  "npc": "艾爾德雷克",
  "greeting": "哼，又來了個打擾我讀書的傢伙……",
  "options": [
    {
      "text": "我想查閱古代龍族的資料",
      "response": "龍族？左轉第三排書架，編號 7–12 區。小心別弄亂我的分類。",
      "sub_options": [
        { "text": "謝謝。", "response": "快去吧，我還要看書。" },
        { "text": "我聽說龍族已經滅絕了？", "response": "哼，書上寫的不一定對……" }
      ]
    }
  ]
}
```

### 3.2 任務編織（Quest Weaving）

LLM 擅長將多個任務串聯成有意義的敘事弧。開發者提供世界觀設定和任務節點，LLM 自動產生過渡對話和邏輯條件。

## 4. 提示工程最佳實踐

### 4.1 Bevy 專用提示模式

| 提示元素 | 說明 | 範例 |
|---------|------|------|
| 版本指定 | 明確指定 Bevy 版本 | `Bevy 0.15, Rust edition 2024` |
| 架構提示 | 指明 ECS 模式 | `使用 Component + System + Resource` |
| 範例注入 | 提供相似的程式碼片段 | `類似於 Query<&Transform, With<Player>>` |
| 限制說明 | 避免 LLM 使用不存在的 API | `不要使用 RemovedComponents，改用 Removed` |

### 4.2 常見失敗模式

LLM 在遊戲程式碼生成中有幾個常見問題：

- **API 幻覺**：編造不存在的 Bevy API（如 `bevy::ecs::system::ParallelSystem`）
- **版本錯亂**：混淆 Bevy 0.13 和 0.15 的 API 差異
- **遺漏標記**：忘記 `#[derive(Component)]` 或 `#[derive(Resource)]`
- **System 順序**：忽略 `add_systems` 中的順序依賴

解決方式是在提示中**注入當前專案的真實依賴版本和已存在的程式碼片段**，讓 LLM 有準確的上下文。

## 5. 具體工具比較

| 工具 | 擅長領域 | 弱點 |
|------|---------|------|
| ChatGPT 4o | 對話設計、任務架構 | Rust 語法深度不夠 |
| Claude 3.5+ | Rust/Bevy 程式碼、unsafe 分析 | 對新版本 API 有延遲 |
| Cursor/GitHub Copilot | 即時補全、重構 | 大型重組容易出錯 |
| Qwen Coder 專用模型 | 程式碼除錯、最佳化 | 遊戲領域知識有限 |

## 6. 結語

LLM 不會取代遊戲開發者，但它能顯著減少樣板程式碼和重複性工作。2027 年的高效遊戲開發者，是那些懂得如何與 AI 協作的人——關鍵不在於讓 AI 寫多少程式碼，而在於寫對哪些程式碼。

## 延伸閱讀

- [LLM for game development](https://www.google.com/search?q=LLM+game+development+code+generation)
- [Prompt engineering for game code](https://www.google.com/search?q=prompt+engineering+game+development+Rust+Bevy)
- [AI assisted game design](https://www.google.com/search?q=AI+assisted+NPC+dialogue+generation+game)
