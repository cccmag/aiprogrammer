# 從自動補全到自主開發（2016-2028）

## 2016：Copilot 的前夜

2016 年，Microsoft 推出的 IntelliSense 和 Eclipse 的 JDT 仍然是程式碼補全的主流。這些工具依賴靜態分析——根據型別系統和語法樹提供建議。它們可靠但有限，就像一個只能看到下一塊拼圖的助手。

```
使用者輸入: list.
靜態補全: list.add(), list.get(), list.size()
            (只依據型別推論，不含語義)
```

## 2018：程式碼補全的 AI 化

TabNine 在 2018 年登場，使用 GPT-2 風格的語言模型來預測程式碼。這是第一次，程式碼補全從「語法驅動」轉向「語義驅動」。

```python
# 使用者寫到一半，模型自動補全
def send_email(recipient, subject, body):
    # 這裡開始打字
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        # TabNine 在此處建議
        server.starttls()
        server.login("user@gmail.com", "password")
        server.sendmail(recipient, subject, body)
```

模型不是理解 SMTP 協議，而是從數百萬個 GitHub 倉庫學到了這個模式。

## 2021：GitHub Copilot 的誕生

2021 年 6 月，GitHub Copilot 正式發布。基於 OpenAI Codex（GPT-3 的程式碼微調版本），它首次實現了「描述即生成」：

```python
# 用自然語言描述 → 生成完整函式
def calculate_moving_average(prices, window):
    # 模型生成的程式碼
    if len(prices) < window:
        return []
    moving_averages = []
    for i in range(len(prices) - window + 1):
        window_avg = sum(prices[i:i+window]) / window
        moving_averages.append(window_avg)
    return moving_averages
```

Copilot 的關鍵創新在於：**將自然語言理解與程式碼生成無縫結合**。開發者不再需要記住 API 細節。

## 2024：Cursor 與 Agent 模式

2024 年，Cursor 編輯器重新定義了程式碼生成的互動模式。它的 Agent 模式允許 AI 自主規劃、搜索、編輯多個檔案：

```
開發者: "建立一個 REST API 伺服器"
Agent:
  1. 分析需求 → 建立目錄結構
  2. 生成 main.py → Flask 路由
  3. 生成 models.py → SQLAlchemy 模型
  4. 生成 config.py → 設定檔案
  5. 生成 tests/ → 單元測試
```

這是從「補全一行」到「補全一個專案」的躍進。

## 2028：自主開發的願景

2028 年，AI 已經可以接管大部分日常開發工作。開發者的角色從「編寫者」轉變為「審閱者和設計者」。以下是一個典型的場景：

```python
# 開發者只寫規格，AI 完成實現
spec = """
建立一個批次處理系統：
1. 從 S3 讀取 CSV 檔案
2. 驗證資料格式
3. 轉換為 Parquet 格式
4. 寫入資料庫
5. 發送通知郵件
"""

# AI 自主完成整個 pipeline
result = ai_agent.develop(spec)
print(result.summary)
# 輸出: 5 個檔案生成，43 個測試通過，部署完成
```

## 關鍵技術演進

| 年份 | 里程碑 | 核心技術 | 準確率（HumanEval） |
|------|--------|----------|-------------------|
| 2016 | 靜態補全 | AST 分析 | 0% |
| 2018 | TabNine | GPT-2 | ~10% |
| 2021 | Copilot | Codex | ~47% |
| 2023 | GPT-4 | RLHF | ~87% |
| 2025 | Claude 3.5 | Agentic | ~93% |
| 2028 | ? | 全自主 | ~98% |

## 延伸閱讀

- [GitHub Copilot 2021 發布](https://www.google.com/search?q=GitHub+Copilot+2021+launch)
- [TabNine 程式碼補全](https://www.google.com/search?q=TabNine+code+completion+2018)
- [Cursor Agent 模式](https://www.google.com/search?q=Cursor+AI+agent+mode+2024)
- [HumanEval 基準測試](https://www.google.com/search?q=HumanEval+code+generation+benchmark)

---

*本篇文章為「AI 程式人雜誌 2028 年 1 月號」主題系列之一。*
