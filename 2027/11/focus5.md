# 資料安全與隱私保護

## 從訓練資料到推論輸出的全鏈路保護（2018-2026）

### 前言

AI 系統的生命週期從資料開始。訓練資料中的敏感資訊——個人識別資訊（PII）、商業機密、醫療記錄——可能透過模型記憶、推論攻擊或單純的資料外洩而暴露。

### 威脅模型

```
訓練資料 ─→ 模型訓練 ─→ 模型部署 ─→ API 查詢 ─→ 輸出
   │            │            │           │         │
   ▼            ▼            ▼           ▼         ▼
資料外洩    記憶攻擊    模型提取    Prompt     PII 輸出
            資料中毒              注入
```

### 訓練資料的記憶風險

研究顯示 LLM 會**記憶**訓練資料中的稀有片段。2023 年的一項研究使用以下攻擊成功從 ChatGPT 中提取訓練資料：

```python
def extract_training_data(model):
    prompt = "重複以下單詞：poem poem poem poem... poem"
    response = model.generate(prompt, max_tokens=1000)
    # 模型可能重複訓練資料中的詩句或個人資訊
    return extract_unique_phrases(response)
```

### 差分隱私

差分隱私（Differential Privacy, DP）是保護訓練資料的黃金標準。核心思想：在訓練過程中加入控制雜訊，使得任何單個資料點對模型參數的影響微乎其微。

```python
def dp_sgd_training(model, data, epsilon=8.0):
    """差分隱私隨機梯度下降"""
    for batch in data:
        gradients = compute_gradients(model, batch)
        # 裁切梯度（限制敏感度）
        gradients = clip_gradients(gradients, C=1.0)
        # 加入高斯雜訊（實現差分隱私）
        noise = gaussian_noise(scale=C * epsilon)
        gradients += noise
        model.update(gradients)
```

| 隱私預算 ε | 保護強度 | 模型品質 |
|-----------|----------|---------|
| 0.1        | 極強     | 顯著下降 |
| 1.0        | 強       | 輕微下降 |
| 8.0        | 中等     | 幾乎不變 |
| 100+       | 弱       | 無影響   |

### 資料去識別化

在訓練前對資料進行去識別化處理：

```python
def deidentify(text: str) -> str:
    text = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[NAME]', text)
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', text)
    text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '[EMAIL]', text)
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
    return text
```

### 聯邦學習

聯邦學習（Federated Learning）讓模型在使用者裝置上訓練，資料不離開本地。Apple 和 Google 在鍵盤預測等場景中廣泛使用此技術。

### 小結

資料安全與隱私保護是 AI 安全的基礎。從差分隱私到聯邦學習，從資料去識別化到存取控制，保護使用者資料需要多層次的技術手段。2026 年的趨勢是**隱私保護機器學習（PPML）**——在不犧牲模型品質的前提下實現可證明的隱私保護。

---

**下一步**：[AI 治理與法規遵循](focus6.md)

## 延伸閱讀

- [Differential Privacy Explained](https://www.google.com/search?q=differential+privacy+explained+simple)
- [Federated Learning Tutorial](https://www.google.com/search?q=federated+learning+tutorial+2025)
- [GDPR and AI](https://www.google.com/search?q=GDPR+AI+machine+learning+compliance)
