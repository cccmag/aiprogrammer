# 工具使用與 MCP 協議：Agent 的雙手與感官（2024-2025）

## 為什麼 Agent 需要工具？

大語言模型本質上是一個「靜態知識庫」——它的知識停留在訓練資料的最後截止日期，無法存取即時資訊，也無法直接影響外部世界。要讓 LLM 從「會說話的書」變成「能幹活的助手」，工具使用能力是關鍵。

```
┌───────────────────────────────────────────────────┐
│          LLM 有工具 vs 無工具的對比                 │
├───────────────────────────────────────────────────┤
│                                                     │
│  無工具的 LLM：                                     │
│  使用者：今天台積電股價多少？                       │
│  LLM：抱歉，我的知識截止於 2025 年底，              │
│        無法提供即時股價資訊。                       │
│                                                     │
│  有工具的 LLM：                                     │
│  使用者：今天台積電股價多少？                       │
│  LLM：（呼叫 stock_price("2330.TW")）               │
│       台積電 (2330) 今日收盤價 1,080 元，           │
│       較昨日上漲 2.5%。                             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 函式呼叫：Agent 工具使用的第一步

### OpenAI Function Calling

2023 年 6 月，OpenAI 發布了 GPT-4 的函式呼叫（Function Calling）功能。這是 LLM Agent 工具使用的里程碑——LLM 不再只是輸出文字，而是可以結構化地輸出「我想呼叫某個工具並傳入這些參數」。

```python
# 定義工具
tools = [
    {
        "name": "get_weather",
        "description": "獲取指定地點的天氣",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "城市名稱"
                }
            }
        }
    }
]

# LLM 輸出結構化工具呼叫
response = openai.chat.completions.create(
    model="gpt-4",
    tools=tools,
    messages=[{"role": "user", "content": "台北天氣如何？"}]
)
# response 包含:
# {
#   "tool_calls": [{
#     "function": "get_weather",
#     "arguments": {"location": "台北"}
#   }]
# }
```

### Function Calling 的局限

Function Calling 雖然是重大突破，但存在幾個問題：

1. **供應商鎖定**：每家 LLM 的函式呼叫格式不同
2. **靜態定義**：工具需要在對話開始前註冊，無法動態發現
3. **無安全隔離**：沒有標準方式控制工具行為邊界
4. **無標準協定**：每個應用需要自行實作工具呼叫邏輯

## MCP 協議：標準化的工具介面

### MCP 的誕生

2024 年 11 月，Anthropic 提出了 Model Context Protocol（MCP）——一個開放標準，旨在統一 AI 模型與外部工具和資料來源之間的互動方式。

MCP 的設計類似於 USB 協議：

```
┌───────────────────────────────────────────────────┐
│            MCP 協議架構（類比 USB）                 │
├───────────────────────────────────────────────────┤
│                                                     │
│  USB 設備     USB 主機                              │
│  ┌────────┐   ┌────────┐                           │
│  │ 鍵盤    │   │ 電腦   │                           │
│  │ 滑鼠    │──►│ 作業   │  即插即用                 │
│  │ 印表機  │   │ 系統   │                           │
│  └────────┘   └────────┘                           │
│                                                     │
│  MCP 工具     MCP 主機                              │
│  ┌────────┐   ┌────────┐                           │
│  │資料庫   │   │ AI     │                           │
│  │API      │──►│ Agent  │  即插即用                 │
│  │檔案系統 │   │ 框架   │                           │
│  └────────┘   └────────┘                           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### MCP 的核心元件

```
┌───────────────────────────────────────────────┐
│              MCP 架構                          │
├───────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────────┐                           │
│  │   MCP Client    │  ─── 每個 Agent 一個      │
│  │  (LLM Agent)    │                           │
│  └────────┬────────┘                           │
│           │ MCP 協議                            │
│  ┌────────┴────────┐                           │
│  │   MCP Host      │  ─── 管理工具清單         │
│  │  (應用程式)      │                           │
│  └────────┬────────┘                           │
│           │                                      │
│  ┌────────┴────────┐  ┌──────────────────┐     │
│  │  MCP Server 1   │  │  MCP Server 2    │     │
│  │  (資料庫)        │  │  (檔案系統)       │     │
│  └─────────────────┘  └──────────────────┘     │
│                                                 │
└─────────────────────────────────────────────────┘
```

MCP 定義了三種核心能力：

1. **工具發現（Tool Discovery）**：Agent 可以查詢 MCP Server 提供的所有工具
2. **資源存取（Resource Access）**：Agent 可以讀取 Server 提供的資源（檔案、資料庫等）
3. **提示模板（Prompt Templates）**：Server 可以提供結構化的提示模板

### MCP 2.0：企業級功能

2026 年 5 月，MCP 2.0 被 ISO/IEC 正式採納，新增了以下企業級功能：

```
MCP 2.0 新增功能
─────────────────────────────────
1. 安全沙箱（Sandbox）
   - 工具執行在隔離環境中
   - 限制資源使用（CPU、記憶體、網路）
   - 自動逾時和中斷

2. 交易隔離（Transaction Isolation）
   - Agent 的操作可以分組為交易
   - 失敗時可完整回滾
   - 支援補償操作（Compensating Actions）

3. 審計追蹤（Audit Trail）
   - 記錄所有工具呼叫
   - 誰、何時、呼叫了什麼、參數是什麼
   - 滿足法規合規要求

4. 權限委派（Delegated Authorization）
   - OAuth 2.0 整合
   - 細粒度的工具權限控制
   - 使用者可隨時撤銷權限
```

## 工具使用的最佳實踐

### 工具設計原則

**1. 單一職責**

每個工具應該只做一件事，並把它做好：

```
❌ 不好的設計：
   全能工具(query, operation, data)  // 模糊的參數

✅ 好的設計：
   search_web(query, max_results)
   read_file(path)
   calculate(expression)
```

**2. 明確的 Schema**

工具的參數應該有清晰的型別和描述：

```python
{
    "name": "send_email",
    "description": "發送電子郵件",
    "parameters": {
        "to": {"type": "string", "description": "收件人地址"},
        "subject": {"type": "string", "description": "郵件主旨"},
        "body": {"type": "string", "description": "郵件內容"}
    },
    "required": ["to", "subject", "body"]
}
```

**3. 安全的第一道防線**

```
工具安全檢查清單：
□ 輸入驗證：檢查參數型別和範圍
□ 權限檢查：使用者是否有權限執行此工具
□ 速率限制：防止濫用
□ 內容過濾：避免注入攻擊
□ 結果清理：不洩露敏感資訊
```

### 常見的 Agent 工具類別

```python
# 資訊檢索類
tools = {
    "search_web":    "搜尋網路",
    "read_news":     "讀取新聞",
    "get_weather":   "查天氣",
    "get_stock":     "查股價",
}

# 檔案操作類
tools = {
    "read_file":     "讀取檔案",
    "write_file":    "寫入檔案",
    "list_dir":      "列出目錄",
    "run_code":      "執行程式碼",
}

# 通訊類
tools = {
    "send_email":    "發送郵件",
    "send_message":  "發送訊息",
    "create_event":  "建立行事曆",
}

# 資料庫類
tools = {
    "query_sql":     "SQL 查詢",
    "get_record":    "取得記錄",
    "update_record": "更新記錄",
}
```

## 從 Function Calling 到 MCP

### 演進時間線

```
2023.06  OpenAI Function Calling 發布
          └── 每個 LLM 各有各的格式
          
2024.03  Google Gemini Function Calling
2024.06  Anthropic Claude Tool Use
          └── 格式不統一，開發者痛苦
          
2024.11  Anthropic 提出 MCP 協議
          └── 統一的標準化方案
          
2025.01  OpenAI 加入 MCP 陣營
2025.03  Google 加入 MCP 陣營
2025.06  Microsoft 在 Azure AI 中內建 MCP
          └── MCP 成為事實標準
          
2026.05  ISO/IEC 正式採納 MCP 2.0
          └── 成為國際標準
```

### MCP 的影響

MCP 標準化對 AI Agent 生態的影響是深遠的：

1. **工具開發者**：一次開發，到處使用（寫一個 MCP Server，所有 AI Agent 都能用）
2. **Agent 開發者**：不再需要為每個工具編寫客製化整合
3. **使用者**：可以在不同 Agent 之間無縫切換同一組工具

## 結語

工具使用是 AI Agent 從「被動對話」到「主動行動」的關鍵能力。從 OpenAI 的 Function Calling 到 MCP 國際標準，工具介面的標準化正在推動 Agent 生態系統的快速發展。

正如 USB 標準讓所有外接設備即插即用，MCP 正在讓所有 AI Agent 即插即用任何工具。這為下一階段的發展——多代理協作——鋪平了道路。

下一篇文章將介紹多代理系統：如何讓多個 Agent 協作解決複雜問題。

---

## 延伸閱讀

- [OpenAI Function Calling](https://www.google.com/search?q=OpenAI+function+calling+documentation)
- [MCP 協議規範](https://www.google.com/search?q=Model+Context+Protocol+MCP)
- [Anthropic Tool Use](https://www.google.com/search?q=Anthropic+tool+use+documentation)
- [MCP vs Function Calling 比較](https://www.google.com/search?q=MCP+vs+function+calling+comparison)

---

*本篇文章為「AI 程式人雜誌 2026 年 5 月號」歷史回顧系列之一。*
