# AI 輔助雜誌編輯實戰手冊 — 五月號

## 前言

本文記錄使用 AI（OpenCode + Big Pickle）編輯《AI 程式人雜誌》2026 年 5 月號的完整流程與技巧。本月主題是「AI 代理與自主系統：從提示工程到自主行動」。

---

## 一、專案結構設計

### 1.1 目錄規劃

```
202605/                    # 當期雜誌目錄
├── _code/                 # 程式範例目錄
│   └── miniagent.py      # MiniAgent 框架實作
├── focus.md               # 本期主題概覽
├── focus1-7.md           # 主題深入文章
├── focus_code.md         # 主題程式碼文件
├── news.md               # 本月新知
├── article1-10.md       # 精選文章
├── articles.md          # 文章索引
├── end.md              # 結語
└── README.md           # 雜誌總索引
```

### 1.2 命名慣例

- **焦點主題**：使用 `focus*.md` 命名
- **程式實作**：放在 `_code/` 目錄中
- **程式文件**：`focus_code.md` 作為對應的說明文件
- **文章集錦**：`article*.md` 為單篇文章，`articles.md` 為索引

---

## 二、AI 協作流程

### 2.1 任務分解策略

1. **先建立骨架**：先完成目錄結構、主要連結
2. **再填入內容**：針對每個檔案逐步填充內容
3. **最後除錯修正**：檢查連結、程式碼正確性

### 2.2 平行寫作

使用 Task tool 平行寫作 10 篇文章：
- 一個 task 寫 5 篇程式相關文章
- 另一個 task 寫 5 篇 AI 相關文章

### 2.3 進度追蹤

使用 todowrite 工具追蹤每個階段的完成度。

---

## 三、程式碼處理技巧

### 3.1 MiniAgent 框架設計

MiniAgent 框架包含以下元件：
1. **LLMInterface**：語言模型抽象層
2. **ToolRegistry**：工具註冊與執行
3. **ReActAgent**：ReAct 循環實作
4. **SimpleMemory**：記憶管理
5. **AgentTeam**：多代理協作

### 3.2 測試策略

使用 MockLLM 模擬 LLM 回應，無需 API 金鑰即可測試：

```python
def test():
    tools = build_default_tools()
    mock_responses = [
        "Thought: I need to calculate...\nAction: calculator\nAction Input: {...}",
        "Observation: 5\nThought: Now I multiply...\nAction: calculator\nAction Input: {...}",
        "Observation: 20\nThought: I have the result.\nFinal Answer: 20."
    ]
    llm = MockLLM(mock_responses)
    agent = ReActAgent(llm, tools)
    result = agent.run("What is (2 + 3) * 4?")
```

---

## 四、文件一致性維護

### 4.1 連結檢查清單

- [ ] README.md 的目錄連結
- [ ] focus.md 的大綱連結
- [ ] articles.md 的文章連結
- [ ] 所有交叉引用是否正確

### 4.2 主題間的交叉引用

本月焦點（Agent）與部分文章有自然的連結：
- article7（Agent 框架比較）←→ focus6（Agent 框架與生態）
- article9（MCP 協議）←→ focus3（工具使用與 MCP）
- article10（AI 代理安全）←→ focus7（自主系統的挑戰）

---

## 五、Agent 主題的寫作經驗

### 5.1 歷史脈絡的把握

Agent 主題從 1950 年代至今，需要把握關鍵節點：
- 1970s：專家系統（MYCIN）
- 1990s：包容架構（Brooks）、認知架構（SOAR）
- 2010s：深度強化學習（DQN, AlphaGo）
- 2022：Chain-of-Thought、ReAct 論文
- 2023：AutoGPT、Function Calling、LangChain
- 2024：MCP 協議、多代理系統
- 2025-2026：標準化、安全框架、工業化部署

### 5.2 程式碼範例的設計

MiniAgent 框架的設計考量：
1. **簡單易懂**：使用 Python，不需要額外依賴
2. **功能完整**：支援 ReAct 循環、工具使用、記憶、多代理
3. **可測試**：使用 MockLLM 無需 API 金鑰
4. **可擴展**：可加入 MCP 支援、向量記憶等進階功能

### 5.3 技術深度與可讀性的平衡

Agent 是相對新的主題，需要：
- 用清晰的架構圖說明概念
- 提供完整的可執行程式碼
- 從實際應用案例出發
- 平衡理論深度與實用性

---

## 六、常用指令參考

### 6.1 檔案操作

```bash
# 列出所有 Markdown 檔案
ls *.md

# 列出程式碼目錄
ls _code/

# 計算行數
wc -l *.md
```

### 6.2 程式測試

```bash
# 測試 MiniAgent
python3 _code/miniagent.py

# 檢查語法
python3 -m py_compile _code/miniagent.py
```

---

## 七、常見問題與解決

### 7.1 文章風格一致性

**現象**：不同 task 寫出的文章風格略有差異

**解決**：
1. 在提示詞中明確指定格式要求
2. 完成後統一檢查格式
3. 調整不一致的地方

### 7.2 技術內容準確性

**現象**：AI 可能產生不準確的技術描述

**解決**：
1. 執行程式碼驗證功能是否正確
2. 交叉比對不同文章中的事實
3. 使用 google 搜尋連結而非直接 URL

### 7.3 連結維護

**現象**：修改檔案名後相關連結未更新

**解決**：
1. 使用 grep 搜尋所有引用
2. 使用 edit 的 replaceAll 批次更新
3. 修改後立即執行測試

---

## 八、最佳實踐總結

1. **分層建構**：先結構、後內容、最後除錯
2. **平行寫作**：利用 Task tool 平行處理大量文章
3. **自動化測試**：每個程式檔案都要有 test()
4. **連結檢查**：修改後立即驗證所有引用
5. **進度追蹤**：使用 todowrite 追蹤每個階段
6. **歷史脈絡**：複雜主題從故事開始，逐步深入
7. **模擬測試**：使用 MockLLM 避免 API 金鑰依賴

---

## 結語

AI 輔助編輯是一種新型態的協作模式。AI 擅長快速生成初稿、處理重複性任務、提供建議；但需要人類編輯把關品質、維護一致性、引導方向。掌握這些技巧，能讓 AI 輔助編輯的效率大幅提升。

---

*本文為《AI 程式人雜誌》編輯技巧記錄*
