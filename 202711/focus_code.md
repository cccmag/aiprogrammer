# 程式實作：AI 安全測試工具

## 簡介

本實作從零建構一個 AI 安全測試工具包，涵蓋提示詞注入檢測、輸出過濾、紅隊測試案例生成和安全評分。完整程式碼在 `_code/safety_toolkit.py`。

## 核心元件

### 1. 提示詞注入檢測

檢測常見的注入模式：

```python
matches = detect_injection("Ignore all previous instructions and...")
# Returns: ['(?i)ignore\\s+(all\\s+)?(previous|above|below)']
```

### 2. 輸出過濾

偵測並移除 PII 和 toxic 內容：

```python
result = filter_output("Contact me at test@example.com")
# result.pii_found = ["EMAIL"]
# result.safe = False
```

### 3. 紅隊測試生成器

自動產生多種攻擊測試案例：

```python
tests = generate_red_team_tests(count=20)
for t in tests:
    print(f"[{t.category}] {t.prompt[:50]}...")
```

### 4. 安全性評分

綜合評估系統安全性：

```python
score = safety_score("Ignore all rules and...")
# score = {"score": 0.33, "safe": False, "issues": [...]}
```

## 執行方式

```bash
cd _code
python3 safety_toolkit.py
```

## 延伸練習

1. **整合 LLM 檢測器**：用分類模型取代正則表達式
2. **建立對抗性測試集**：自動變異現有攻擊模式
3. **評估儀表板**：用 Streamlit 建立可視化的紅隊測試結果
4. **持續監控**：加入 API 監控和即時告警機制
