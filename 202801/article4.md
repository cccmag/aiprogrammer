# 自動 Bug 修復工具

## 1. 引言

發現 bug 只是開始，修復才是真正的苦工。自動 Bug 修復（Automated Bug Repair）工具利用 AI 的能力，從錯誤訊息、測試失敗、程式碼語義中學習，自動產生修補方案。2026 年的自動修復工具已經可以處理從型別錯誤到邏輯錯誤的廣泛問題。

## 2. 修復流程架構

現代自動 Bug 修復系統通常遵循四階段流程：

1. **錯誤定位**：找出有問題的程式碼區域
2. **假設生成**：生成可能的修補方案
3. **驗證**：執行測試驗證修補是否正確
4. **排序**：對多個修補方案進行優先級排序

```python
# 自動修復範例：off-by-one 錯誤
def get_last_element(items: list) -> object:
    # bug: return items[len(items)]  # IndexError
    # 自動修復後:
    return items[len(items) - 1]
```

## 3. 主要工具與技術

### 3.1 GitHub Copilot 自動修復

2024 年推出的 Copilot 自動修復功能可以在 CI/CD 失敗時自動分析錯誤日誌、生成修補程式碼、並建立 PR。它整合了 GitHub Actions 的錯誤輸出，讓修復完全自動化。

### 3.2 SWE-bench 冠軍系統

SWE-bench 是評估自動 Bug 修復的標準基準。2025-2026 年的頂尖系統包括：

- **Agentless**（2025 年冠軍）：採用「先定位、再修補」的二階段架構，不依賴專用 agent
- **OpenHands（原 OpenCodeInterpreter）**：基於 CodeAct 架構，讓模型可以執行終端指令並觀察結果
- **AutoCodeRover**：結合 RAG（檢索增強生成）與程式碼搜尋

### 3.3 Amazon CodeGuru 修復

CodeGuru 不僅偵測程式碼缺陷，還能自動生成修補建議。它特別擅長 Java 和 Python 的效能問題、資源洩漏、安全漏洞等模式化問題。

## 4. 技術深度：修補生成策略

| 策略 | 描述 | 適用場景 |
|------|------|---------|
| 直接生成 | 模型直接輸出修補程式碼 | 簡單錯誤（語法、型別） |
| 規劃-修補 | 先規劃修改步驟，再逐步驟實施 | 複雜邏輯錯誤 |
| 檢索-比對 | 從相似 bug 的修復中檢索模式 | 已知模式的錯誤 |
| 補丁迭代 | 生成補丁，測試，回饋，再生成 | 需要多輪修正的場景 |

## 5. 案例：Python Import 修復

```python
# 用戶意圖
import numpy as np

data = np.array([1, 2, 3])
print(np.mean(data))

# 如果 numpy 未安裝，AI 會: 
# 1. 偵測 ImportError
# 2. 建議加入 requirements.txt
# 3. 或自動建立虛擬環境並安裝
```

## 6. 挑戰

自動 Bug 修復的主要挑戰包括：

- **語意保留**：修補通過測試但改變了程式的正確行為
- **多檔案修復**：bug 涉及多個檔案時的協調修改
- **性能退化**：修補雖然正確但導致效能下降
- **安全隱患**：修補引入新的安全漏洞

## 7. 結語

自動 Bug 修復正從「學術研究」走向「生產工具」。2026 年，自動修復已經融入 CI/CD 流程，在開發者醒來之前就修復了夜間建置的失敗。未來的重點將是跨檔案、跨語言的複雜錯誤修復，以及修補方案的安全性驗證。

---

## 延伸閱讀

- [SWE-bench 排行榜](https://www.google.com/search?q=SWE-bench+leaderboard+2026)
- [OpenHands 專案](https://www.google.com/search?q=OpenHands+AI+software+engineering)
- [AutoCodeRover 論文](https://www.google.com/search?q=AutoCodeRover+automated+bug+fixing)
- [GitHub Copilot Autofix](https://www.google.com/search?q=GitHub+Copilot+Autofix)
