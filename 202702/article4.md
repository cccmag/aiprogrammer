# 遊戲 UI 設計：從 Egui 到 Unreal 風格的 HUD

## 即時模式 UI vs 保留模式 UI

遊戲 UI 有兩大流派：**即時模式（Immediate Mode）** 與 **保留模式（Retained Mode）**。

| 特性 | egui（即時模式） | bevy_ui（保留模式） |
|------|-----------------|--------------------|
| State 管理 | 自動（每幀重建） | 手動（元件 State 持久） |
| 開發週期 | 極快迭代 | 需較多設置 |
| 佈局靈活性 | 動態、程式化 | 宣告式、類似 HTML |
| 效能 | 每幀重建 UI | 僅更新變化的部分 |
| 學習曲線 | 低 | 中 |

## 使用 Egui 建立遊戲 HUD

### 基本設置

```rust
use bevy::prelude::*;
use bevy_egui::{egui, EguiContexts, EguiPlugin};

fn main() {
    App::new()
        .add_plugins((DefaultPlugins, EguiPlugin))
        .add_systems(Update, hud_system)
        .run();
}
```

### 血條（Health Bar）

血條是遊戲 UI 最基礎的元件：

```rust
fn hud_system(
    mut contexts: EguiContexts,
    player_query: Query<&Health, With<Player>>,
    score: Res<Score>,
) {
    let health = player_query.single();
    let ctx = contexts.ctx_mut();

    egui::Area::new("hud")
        .fixed_pos(egui::pos2(10.0, 10.0))
        .show(ctx, |ui| {
            // 血條背景
            let bar_width = 200.0;
            let bar_height = 20.0;
            let (_, rect) = ui.allocate_space(egui::vec2(bar_width, bar_height));

            let health_ratio = health.0 as f32 / health.max as f32;
            let color = if health_ratio > 0.5 {
                egui::Color32::GREEN
            } else if health_ratio > 0.25 {
                egui::Color32::YELLOW
            } else {
                egui::Color32::RED
            };

            // 繪製血條
            ui.painter().rect_filled(
                egui::Rect::from_min_size(rect.min, egui::vec2(bar_width * health_ratio, bar_height)),
                0.0,
                color,
            );
            ui.painter().rect_stroke(
                egui::Rect::from_min_size(rect.min, egui::vec2(bar_width, bar_height)),
                0.0,
                egui::Stroke::new(2.0, egui::Color32::WHITE),
            );

            // 文字
            ui.label(format!("HP: {}/{}", health.0, health.max));
        });
}
```

### 迷你地圖（Minimap）

```rust
fn minimap(
    ctx: &egui::Context,
    player_pos: &Transform,
    enemies: &Query<&Transform, With<Enemy>>,
) {
    egui::Area::new("minimap")
        .fixed_pos(egui::pos2(10.0, 100.0))
        .show(ctx, |ui| {
            let map_size = egui::vec2(150.0, 150.0);
            let (response, painter) =
                ui.allocate_painter(map_size, egui::Sense::hover());

            let center = response.rect.center();
            let scale = 2.0;

            // 繪製地圖背景
            painter.rect_filled(response.rect, 0.0, egui::Color32::from_rgba_premultiplied(0, 0, 0, 180));

            // 繪製敵人的位置
            for enemy_transform in enemies.iter() {
                let rel_x = (enemy_transform.translation.x - player_pos.translation.x) * scale;
                let rel_y = (enemy_transform.translation.z - player_pos.translation.z) * scale;
                painter.circle_filled(
                    egui::pos2(center.x + rel_x, center.y + rel_y),
                    3.0,
                    egui::Color32::RED,
                );
            }

            // 繪製玩家位置
            painter.circle_filled(center, 4.0, egui::Color32::GREEN);
        });
}
```

### 物品欄（Inventory Grid）

```rust
fn inventory_ui(ctx: &egui::Context, inventory: &Inventory) {
    egui::Window::new("物品欄")
        .fixed_pos(egui::pos2(600.0, 10.0))
        .show(ctx, |ui| {
            egui::Grid::new("inventory_grid")
                .min_col_width(60.0)
                .max_col_width(60.0)
                .show(ui, |ui| {
                    for (i, slot) in inventory.slots.iter().enumerate() {
                        if let Some(item) = slot {
                            ui.label(item.icon());
                            if ui.button("使用").clicked() {
                                // 使用物品
                            }
                        } else {
                            ui.label("─");
                        }
                        if (i + 1) % inventory.columns == 0 {
                            ui.end_row();
                        }
                    }
                });
        });
}
```

## Egui 風格與主題

```rust
fn setup_style(mut contexts: EguiContexts) {
    let ctx = contexts.ctx_mut();
    let mut style = (*ctx.style()).clone();

    // 遊戲風格的深色主題
    style.visuals.dark_mode = true;
    style.visuals.widgets.noninteractive.bg_fill = egui::Color32::from_rgb(20, 20, 30);
    style.visuals.widgets.inactive.bg_fill = egui::Color32::from_rgb(40, 40, 60);
    style.visuals.widgets.active.bg_fill = egui::Color32::from_rgb(60, 100, 200);

    // 自訂字型
    let mut fonts = egui::FontDefinitions::default();
    fonts.font_data.insert(
        "game_font".into(),
        egui::FontData::from_static(include_bytes!("../assets/fonts/pixel.ttf")),
    );
    fonts.families.get_mut(&egui::FontFamily::Proportional).unwrap()
        .insert(0, "game_font".into());

    ctx.set_fonts(fonts);
    ctx.set_style(style);
}
```

## bevy_ui：保留模式 UI

Bevy 內建的 `bevy_ui` 模組提供類似 CSS 的宣告式 UI：

```rust
fn setup_ui(mut commands: Commands, asset_server: Res<AssetServer>) {
    commands.spawn((
        NodeBundle {
            style: Style {
                width: Val::Percent(100.0),
                height: Val::Percent(100.0),
                align_items: AlignItems::Start,
                justify_content: JustifyContent::Start,
                ..default()
            },
            ..default()
        },
        // 血條
        Children::new(vec![
            commands.spawn(NodeBundle {
                style: Style {
                    width: Val::Px(200.0),
                    height: Val::Px(20.0),
                    position_type: PositionType::Absolute,
                    left: Val::Px(10.0),
                    top: Val::Px(10.0),
                    ..default()
                },
                background_color: BackgroundColor(Color::RED),
                ..default()
            }).id(),
        ]),
    ));
}
```

## 建議

- **原型階段**：使用 egui 快速迭代 UI 佈局
- **正式發布**：可考慮 bevy_ui 以求更穩定的渲染效能
- **混合使用**：egui 做除錯面板 + bevy_ui 做遊戲內 HUD

## 延伸閱讀

- [egui 文件與範例](https://www.google.com/search?q=egui+Rust+immediate+mode+GUI)
- [Bevy UI 官方文件](https://www.google.com/search?q=Bevy+UI+NodeBundle)
- [遊戲 UI 設計原則](https://www.google.com/search?q=game+HUD+design+best+practices)
