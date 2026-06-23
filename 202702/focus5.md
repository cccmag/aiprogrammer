# 遊戲音效與輸入處理（2021-2026）

## bevy_audio 音效系統

Bevy 內建音效引擎，支援常見格式：

```rust
fn setup_audio(mut commands: Commands, asset_server: Res<AssetServer>) {
    commands.spawn(AudioBundle {
        source: asset_server.load("music/background.ogg"),
        settings: PlaybackSettings::LOOP,
    });
}

// 播放一次性音效（如射擊）
fn play_shoot_sound(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    mut shoot_events: EventReader<ShootEvent>,
) {
    for _ in shoot_events.read() {
        commands.spawn(AudioBundle {
            source: asset_server.load("sfx/shoot.wav"),
            settings: PlaybackSettings::ONCE,
        });
    }
}
```

支援的音效格式包括 OGG Vorbis、WAV、MP3 和 FLAC。Bevy 使用 `rodio` 作為後端音訊播放器，它支援：
- 音量的動態控制
- 3D 空間音效（透過 `SpatialAudioBundle`）
- 音效池管理（避免同一個音效重疊過多次）

對於更進階的需求，`bevy_kira_audio` 插件提供了更精細的控制：音效曲線、淡入淡出、即時混音。

## 鍵盤/滑鼠/遊戲手把輸入

Bevy 的輸入系統以 Resource 為基礎，提供統一的查詢 API：

```rust
fn keyboard_input(keyboard: Res<ButtonInput<KeyCode>>) {
    if keyboard.pressed(KeyCode::KeyW) {
        println!("W 鍵按住中");
    }
    if keyboard.just_pressed(KeyCode::Space) {
        println!("空白鍵按下");
    }
    if keyboard.just_released(KeyCode::ShiftLeft) {
        println!("左 Shift 放開");
    }
}
```

滑鼠輸入：

```rust
fn mouse_input(
    mouse: Res<ButtonInput<MouseButton>>,
    windows: Query<&Window>,
) {
    // 滑鼠按鍵
    if mouse.just_pressed(MouseButton::Left) {
        println!("左鍵點擊");
    }

    // 滑鼠位置（需要從 Window 獲取）
    if let Ok(window) = windows.get_single() {
        if let Some(cursor_pos) = window.cursor_position() {
            println!("滑鼠位置：{:?}", cursor_pos);
        }
    }
}
```

遊戲手把支援透過 `Gamepad` 類型實現：

```rust
fn gamepad_input(
    gamepads: Res<Gamepads>,
    buttons: Res<ButtonInput<GamepadButton>>,
    axis: Res<Axis<GamepadAxis>>,
) {
    for gamepad in gamepads.iter() {
        // 按鈕
        let jump = buttons.pressed(GamepadButton::new(gamepad, GamepadButtonType::South));

        // 類比搖桿
        if let Some(x) = axis.get(GamepadAxis::new(gamepad, GamepadAxisType::LeftStickX)) {
            println!("左搖桿 X 軸：{}", x);
        }
    }
}
```

Bevy 的 `ButtonInput<T>` 支援三種查詢：`pressed`（持續按住）、`just_pressed`（瞬間按下）、`just_released`（瞬間放開）。所有輸入類型都是泛型的，保持型別安全。

## 狀態管理（State）與場景切換

現實中的遊戲需要不同的「畫面」：選單、遊戲運行、暫停、遊戲結束。Bevy 使用 `State` 管理這些階段：

```rust
#[derive(States, Default, Clone, Eq, PartialEq, Hash, Debug)]
enum GameState {
    #[default]
    Menu,
    Playing,
    Paused,
    GameOver,
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .init_state::<GameState>()
        .add_systems(OnEnter(GameState::Menu), setup_menu)
        .add_systems(OnExit(GameState::Menu), cleanup_menu)
        .add_systems(Update, game_input.run_if(in_state(GameState::Playing)))
        .add_systems(Update, pause_input.run_if(in_state(GameState::Playing)))
        .run();
}
```

關鍵的狀態轉換函式：

```rust
fn pause_input(
    keyboard: Res<ButtonInput<KeyCode>>,
    mut next_state: ResMut<NextState<GameState>>,
    state: Res<State<GameState>>,
) {
    if keyboard.just_pressed(KeyCode::Escape) {
        match state.get() {
            GameState::Playing => next_state.set(GameState::Paused),
            GameState::Paused => next_state.set(GameState::Playing),
            _ => {}
        }
    }
}
```

搭配 `OnEnter`、`OnExit` 和 `OnTransition` 排程，你可以精確控制在進入/離開狀態時執行哪些 System。例如進入 Playing 時生成敵人、離開時清理子彈。

## 選單/遊戲/暫停狀態機

完整的狀態機設計如下：

```
          按 Enter
    Menu ────────► Playing
      ▲              │
      │  按 Esc      │ 按 Esc
      │    ┌─────────┘
      │    ▼
      │  Paused
      │    │
      └────┘ 按 Esc
            (返回 Playing)

    生命值歸零
    Playing ──────► GameOver
      ▲                │
      └────────────────┘ 按 R 重新開始
```

每個狀態都有自己的 System 集合，確保「選單狀態不會執行敵人 AI」、「遊戲結束時不會處理輸入」。這種設計模式讓代碼更容易維護，也更難出現邏輯錯誤。

## 參考

- [Bevy 輸入系統文件](https://www.google.com/search?q=Bevy+input+system+keyboard+mouse+gamepad)
- [Bevy 音效系統教學](https://www.google.com/search?q=Bevy+audio+tutorial)
- [Bevy State 管理](https://www.google.com/search?q=Bevy+state+machine+game)
- [bevy_kira_audio](https://www.google.com/search?q=bevy_kira_audio+plugin)

---

*本篇文章為「AI 程式人雜誌 2027 年 2 月號」Rust 遊戲開發系列之一。*
