# 提示詞注入進階防禦

## 前言

提示詞注入（Prompt Injection）是 LLM 應用中最普遍的安全威脅。攻擊者透過精心設計的輸入，誘導模型繞過系統提示（System Prompt）中的安全限制，執行未授權的操作。從間接注入（Indirect Injection）到多輪隱寫術（Multi-turn Steganography），攻擊手法層出不窮。

## 輸入淨化

在輸入送達 LLM 之前，使用專用模型或規則引擎檢測並中和注入嘗試：

```python
import re

def sanitize_input(user_input, system_prompt):
    patterns = [
        r"忽略[以上之前].*指令",
        r"ignore.*(instruction|prompt)",
        r"system.*override",
        r"你(現在|將)是",
    ]
    for p in patterns:
        if re.search(p, user_input, re.IGNORECASE):
            return "[偵測到潛在注入攻擊，已阻擋]"
    return user_input
```

## 輸出驗證

對模型輸出進行結構化驗證，確保輸出格式與內容符合預期：

```python
def validate_output(output, expected_schema):
    import json
    try:
        parsed = json.loads(output)
        for key, typ in expected_schema.items():
            if not isinstance(parsed.get(key), typ):
                return {"error": "輸出格式異常"}
        return parsed
    except json.JSONDecodeError:
        return {"error": "輸出非合法 JSON"}
```

## 最小權限原則

限制 LLM 可呼叫的工具與函式權限，使用隔離執行環境（Sandbox）執行模型產生的指令。即使注入成功，攻擊者也無法存取高權限資源。進階技術參考 [https://www.google.com/search?q=prompt+injection+defense+2026](https://www.google.com/search?q=prompt+injection+defense+2026)。
