# 為什麼需要版本控制？

## 版本控制的核心價值

在軟體開發過程中，變更管理是至關重要的環節。版本控制系統 (VCS) 記錄了檔案的每一次變更，讓開發者可以回溯到任何歷史狀態。

### 沒有版本控制的困境

想像您正在開發一個專案，不斷新增功能、修復錯誤，隨著時間推移：

- 忘記了某段程式碼為什麼這樣寫
- 不小心刪除了重要的功能
- 多人修改同一個檔案時互相覆蓋
- 找不到穩定的版本可以發布

這些問題在沒有版本控制的團隊中每天都在發生。

### 版本控制的優勢

1. **歷史記錄**：每一次修改都有完整紀錄，包含誰、何時、為什麼修改
2. **協作能力**：多人可以同時開發，系統會自動合併變更
3. **分支實驗**：可以在隔離的環境中嘗試新功能，不影響主線
4. **備份還原**：任何時候都可以回復到過去的穩定版本

### 分散式 vs 集中式

Git 屬於分散式版本控制系統 (DVCS)，與傳統的集中式系統 (如 SVN) 最大的差異在於：

- 每個開發者都有完整的儲存庫副本
- 不需要網路就能提交變更
- 沒有單點故障的風險

### 實際案例

一個典型的 Git 工作流程：

```python
# 用 Python 模擬版本控制的概念
class VersionControl:
    def __init__(self):
        self.history = []
        self.current = 0
    
    def save_version(self, content, message):
        self.history.append({
            "content": content,
            "message": message,
            "version": len(self.history) + 1
        })
        self.current = len(self.history)
    
    def rollback(self, version):
        return self.history[version - 1]["content"]

vc = VersionControl()
vc.save_version("print('hello')", "初始版本")
vc.save_version("print('hello world')", "新增 world")
print(vc.rollback(1))  # 回到最初版本
```

更多關於版本控制的概念請參考 https://www.google.com/search?q=版本控制+為什麼+重要。
