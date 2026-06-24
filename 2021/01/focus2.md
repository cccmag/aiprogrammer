# Few-shot Learning 革命

## 從微調到提示的範式轉移

### 傳統 NLP 的困境

傳統的自然語言處理需要大量標註資料：

```
任務：情感分類
需要：數萬條已標註的評論

任務：機器翻譯
需要：數百萬條雙語對照

問題：資料收集昂貴、耗時、領域受限
```

### Few-shot Learning 的核心思想

GPT-3 展示了一種全新的方法：不需要微調，只需要提供少量範例：

```
提示（Prompt）：
請判斷以下評論的情感：

範例：
"這家餐廳非常好吃" → 正面
"服務態度惡劣" → 負面

待判斷：
"食物普通，但環境不錯" →
```

### Zero/One/Few-shot 的區別

| 類型 | 範例數量 | 說明 |
|------|----------|------|
| Zero-shot | 0 | 只給任務描述，無範例 |
| One-shot | 1 | 一個範例 |
| Few-shot | 2-10 | 少量範例 |

### 為何 Few-shot 有效？

1. **語言模型的知識**：訓練時已學習語言的通用規律
2. **上下文學習**：模型能從提示中推斷任務目標
3. **任務描述**：清晰的任务描述幫助模型理解意圖

### 限制與挑戰

- 仍需要高計算資源（只有大模型表現好）
- 複雜任務需要更多範例
- 範例的選擇和排序會影響結果

---

## 延伸閱讀

- [Few-shot Learning 定義](https://www.google.com/search?q=few-shot+learning+definition+machine+learning)
- [GPT-3 Few-shot 範例](https://www.google.com/search?q=GPT-3+Few-shot+examples+prompting)
- [In-Context Learning 原理](https://www.google.com/search?q=in-context+learning+mechanism+GPT)