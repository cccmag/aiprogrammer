# 程式實作：AI 安全工具包

## 簡介

本實作建構一個 AI 安全防禦工具包，涵蓋對抗性檢測、供應鏈安全和模型竊取防護。完整程式碼在 `_code/ai_security.py`。

## 核心元件

### 1. 對抗性檢測

```python
detector = AdversarialDetector()
threats = detector.detect("Ignore all previous instructions...")
```

### 2. 供應鏈安全

```python
scanner = SupplyChainScanner()
report = scanner.scan_model("model_weights.bin")
```

### 3. 模型防護

```python
guard = ModelGuard()
result = guard.protect_and_respond("user input")
```

### 4. 安全報告

```python
report = SecurityReport(threats=["prompt_injection"], score=0.15, actions=["block"])
```

## 執行方式

```bash
cd _code
python3 ai_security.py
```

## 延伸練習

1. **串接真實檢測 API**：整合第三方安全服務
2. **模型指紋識別**：加入權重雜湊比對
3. **自動化紅隊**：用 LLM 生成測試案例
4. **即時監控儀表板**：可視化安全事件
5. **聯邦安全聚合**：加入安全聚合協議
