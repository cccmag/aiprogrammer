# 大型語言模型的限制

## 當前技術的瓶頸

### 幻覺問題（Hallucination）

大型語言模型有時會生成看似合理但實際錯誤的內容：

```
問題：生成的事實可能不正確

示例：
"比特幣在 2020 年達到 10 萬美元"
（實際：2020 年比特幣從未達到 10 萬美元）
```

解決方向：
- 接入外部知識庫
- 要求模型引用來源
- 強化學習人類反饋（RLHF）

### 推理能力限制

#### 1. 數學推理
```
問題：7 * 8 = ?
大型語言模型可能回答錯誤（67）
```

#### 2. 邏輯推理
```
問題：所有 A 都是 B
     所有 B 都是 C
     請問所有 A 都是 C 嗎？
部分模型會混淆
```

#### 3. 常識推理
模型可能缺乏人類認為理所當然的常識

### 知識截止日期

GPT-3 的訓練資料有時間限制：
- 訓練資料截止：2021 年 6 月
- 無法知道之後發生的事件
- 解決方案：結合瀏覽能力

### 計算資源需求

```
訓練 GPT-3：
- GPU：數千張 A100
- 電力：數百萬美元
- 時間：數週

這限制了只有大公司能訓練此類模型
```

### 安全與倫理問題

1. **偏見**：訓練資料中的社會偏見
2. **誤用**：生成假新聞、惡意程式碼
3. **隱私**：可能記憶訓練資料中的敏感資訊
4. **能耗**：巨大的碳足跡

### 當前的緩解策略

- **RLHF**：透過人類反饋進行微調
- **Constitutional AI**：基於原則的約束
- **輸出過濾**：防止有害內容生成

---

## 延伸閱讀

- [Hallucination+Problem+LLM](https://www.google.com/search?q=hallucination+large+language+models)
- [GPT-3+limitations+analysis](https://www.google.com/search?q=GPT-3+limitations+reasoning)
- [AI+safety+alignment+research](https://www.google.com/search?q=AI+safety+alignment+research)