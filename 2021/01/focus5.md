# Prompt Engineering

## 提示詞設計技巧

### 基本原則

1. **明確任務**：清楚說明要完成的任務
2. **提供範例**：Few-shot 學習的關鍵
3. **格式設定**：指定輸出的格式和結構
4. **角色扮演**：賦予模型特定的角色

### 常用模式

#### 1. Zero-shot Prompting
```
任務：解釋量子糾纏
```

#### 2. Few-shot Prompting
```
範例：
"今天很累" → 需要休息
"壓力很大" → 需要放鬆

任務：
"考試很難" →
```

#### 3. Chain of Thought
```
問題：小明有 5 個蘋果，給了 小華 2 個，又買了 3 個，請問有多少個？

思考過程：
1. 開始有 5 個蘋果
2. 給了小華 2 個 → 5 - 2 = 3
3. 又買了 3 個 → 3 + 3 = 6
答案：6 個蘋果
```

#### 4. 角色扮演
```
你是一位專業的 Python 程式設計師，請解釋什麼是裝飾器。
```

### 溫度與 Top-p

- **Temperature（溫度）**：
  - 低（0.1-0.3）：確定性輸出
  - 中（0.5-0.7）：平衡
  - 高（0.8-1.0）：創造性/多樣性

- **Top-p**（核採樣）：
  - 控制考慮的詞彙範圍
  - 較低的 top_p 更確定

### 避免幻覺的技巧

1. 要求提供引用來源
2. 要求模型在不确定時表示「不知道」
3. 將大問題分解為小步驟

### 複雜任務的提示設計

```
任務：撰寫技術部落格文章

提示結構：
1. 主題明確
2. 目標讀者定義
3. 文章結構要求
4. 字數限制
5. 風格指南
```

---

## 延伸閱讀

- [Prompt Engineering Guide](https://www.google.com/search?q=prompt+engineering+guide+GPT-3)
- [Chain+of+Thought+Prompting](https://www.google.com/search?q=chain+of+thought+prompting+paper)
- [Few-shot+Prompting+Examples](https://www.google.com/search?q=few-shot+prompting+examples)