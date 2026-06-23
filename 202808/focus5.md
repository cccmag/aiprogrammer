# 警報策略與自動回復

## 從吵鬧到安靜可靠（2023-2028）

### 前言

警報系統最常見的問題不是太少而是太多。當每個指標漂移都觸發警報時，團隊會開始忽略所有通知——這就是「警報疲勞」。好的警報策略不僅要減少雜訊，還要能在真正危急時自動採取行動。

### 警報層級設計

```
┌──────────┐
│ Critical │ → 立即通知、自動回復、開 P0 事故
├──────────┤
│ Warning  │ → 上班時間通知、創建 Jira ticket
├──────────┤
│ Info     │ → 儀表板顯示、週報匯總
└──────────┘
```

### 觸發條件設計原則

1. **基於趨勢而非單點**：單一請求失敗不應觸發警報，但連續 5 分鐘錯誤率 > 5% 應該觸發。
2. **窗口化計算**：使用滑動視窗（如過去 10 分鐘）而非累積統計。
3. **避免對抗性閾值**：不要把閾值設在業務邊界上，否則系統會剛好卡在邊緣反覆觸發。

### 去重與抑制

`_code/observability.py` 中的 `AlertManager` 實作了基本的抑制機制：

```python
alert_mgr = AlertManager()
alert_mgr.add_rule("latency_p99", condition=lambda: ...)

# 抑制已知問題的警報
alert_mgr.suppress("latency_p99")
```

去重策略包括：
- **時間去重**：同一規則在 T 分鐘內只觸發一次
- **內容去重**：完全相同訊息不重複通知
- **因果分組**：將相關警報歸納為單一事故

### 警報升級（Escalation）

當警報持續未被確認時，自動升級：

1. 0 分鐘：發送 Slack 通知
2. 5 分鐘：呼叫值班人員手機
3. 15 分鐘：通知團隊主管
4. 30 分鐘：自動執行回復腳本

### 自動回復策略

**Rollback**：新模型版本監控到準確率下降時，自動回退到上一個穩定版本。

**Scale Up**：推論延遲 P99 超過 1s 時，自動擴展推理節點。

**Fallback**：主要模型不可用時，切換到輕量備用模型。

**Circuit Breaker**：錯誤率超過 50% 時，停止發送新請求並回傳快取結果。

```python
class CircuitBreaker:
    def __init__(self, threshold=5, window=60):
        self.failures = []
        self.threshold = threshold
        self.window = window

    def record_failure(self):
        now = time.time()
        self.failures = [f for f in self.failures if now - f < self.window]
        self.failures.append(now)
        return len(self.failures) >= self.threshold
```

### 事故事後分析

每次事故後撰寫事後分析報告（Postmortem），重點在於：
- 如何更快發現？→ 改進監控指標
- 如何更快恢復？→ 增加自動回復路徑
- 如何防止再發生？→ 系統架構改進

### 小結

好的警報系統是「安靜的」。它只在真正需要人類介入時才發出通知。其他時候，自動回復機制應該默默處理問題。

---

**下一步**：[AI 系統健康檢查框架](focus6.md)

## 延伸閱讀

- [Alert Fatigue Prevention](https://www.google.com/search?q=alert+fatigue+prevention+ML+monitoring)
- [Circuit Breaker Pattern](https://www.google.com/search?q=circuit+breaker+pattern+machine+learning)
- [Incident Response for ML](https://www.google.com/search?q=incident+response+for+machine+learning+systems)
