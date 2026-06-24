# 具身 AI 與機器人

## 從聊天到行動：AI 獲得身體的這一年

### 通用機器人基座模型

2029 年是「具身 AI」（Embodied AI）爆發之年。RT-3、PaLM-E 2、以及 Tesla Optimus Gen-3 證明了通用機器人基座模型的有效性——單一模型可以控制不同形態的機器人。

核心技術棧：

```
感知層 → 世界模型 → 任務規劃 → 動作控制
  │          │           │          │
  └── 多模態編碼器    │          └── 阻抗控制
               └── 物理模擬器     └── 即時重規劃
```

```python
class EmbodiedAgent:
    def __init__(self, robot_type: str):
        self.world_model = WorldModel()
        self.motor_controller = MotorController(robot_type)
        self.task_queue = []

    def act(self, instruction: str, sensor_input: dict) -> list[float]:
        state = self.world_model.update(sensor_input)
        plan = self.plan(instruction, state)
        return self.motor_controller.execute(plan)

    def plan(self, instruction: str, state: dict) -> list[str]:
        # 使用世界模型進行物理推理
        prompt = f"Task: {instruction}. State: {state}. Output: sequence of actions."
        return llm_generate(prompt).split("\n")
```

### 家庭機器人的 iPhone 時刻

Figure AI 和 Tesla 在 2029 年先後推出消費級通用機器人，售價 $19,999。上市首季銷量突破 200 萬台。主要場景：

- 家務整理（摺衣、洗碗、整理櫥櫃）
- 老人陪護（用藥提醒、跌倒偵測、緊急呼叫）
- 教育輔助（陪伴學習、作業輔導）

### 工業機器人全面升級

製造業機器人從「重複固定動作」升級為「自主適應」：

| 功能 | 2026 | 2029 |
|------|------|------|
| 任務切換 | 需工程師重新編程 | 自然語言指令切換 |
| 異常處理 | 停機等待人工 | 自主診斷並修復 |
| 協作 | 固定安全圍欄 | 動態人機協作 |
| 學習 | 離線訓練 | 線上持續學習 |

### 倫理挑戰

具身 AI 帶來了新的安全問題：機器人誤用、隱私侵犯、責任歸屬。各國緊急立法要求機器人配備「kill switch」和「倫理晶片」。

### 小結

2029 年，AI 不再只是螢幕後的智慧——它走進了家庭、工廠和街頭。具身 AI 是最終的「介面革命」，讓機器不再需要鍵盤和螢幕。

---

**下一步**：[AI 治理與社會影響](focus5.md)

## 延伸閱讀

- [Embodied AI 2029 進展](https://www.google.com/search?q=Embodied+AI+2029+robotics)
- [通用機器人基座模型](https://www.google.com/search?q=robotics+foundation+model+2029)
- [消費級機器人市場報告](https://www.google.com/search?q=consumer+robot+2029+market)
