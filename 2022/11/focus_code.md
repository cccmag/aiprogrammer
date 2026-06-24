# 對話系統完整實作

## 前言

本篇文章將展示四種核心對話系統技術的 Python 實作，涵蓋從規則驅動到機器學習模擬的各個層面。完整的程式碼請參考 `_code/dialog_system.py`。

## 原始碼

完整的 Python 實作請參考：[_code/dialog_system.py](_code/dialog_system.py)

### 1. Eliza 風格模式匹配

```python
ELIZA_PATTERNS = [
    (r'.*我感到(.+)',        '你感到{m1}，能多說說嗎？'),
    (r'.*我(覺得|認為)(.+)',  '你{op}{topic}，是什麼讓你有這種想法？'),
    (r'.*我需要(.+)',         '如果你可以得到{m1}，你認為會怎樣？'),
]
```

Eliza 使用正則表達式比對使用者輸入，並根據匹配的群組生成回覆。這是對話系統最原始的形態。

### 2. 檢索式回覆引擎

```python
RETRIEVAL_KB = {
    '天氣': '今天天氣晴朗，高溫 28°C，午後有局部雷陣雨。',
    '股價': '台積電今日收盤價 580 元，漲幅 1.2%。',
}
```

基於關鍵詞的檢索系統從預先定義的知識庫中選取最相關的回覆。

### 3. Seq2Seq 對話模擬

```python
SEQ2SEQ_KB = {
    '你叫什麼名字': '我是 chatbot，由序列到序列模型生成。',
}
```

簡化的 Seq2Seq 模擬展示了生成式對話的概念。

### 4. 對話狀態追蹤

```python
class DialogState:
    def __init__(self):
        self.slots = {}
    def update(self, user_input, system_response):
        # Slot filling via regex
```

狀態追蹤記錄每個槽位的填充狀態，是任務型對話的核心。

## 執行結果

```
=== AI 對話系統綜合展示 ===
1. Eliza 風格對話
   使用者: 我感到難過
   Eliza : 你感到難過，能多說說嗎？
2. 檢索式回覆
   使用者: 今天天氣如何？
   系統  : 今天天氣晴朗，高溫 28°C...
3. Seq2Seq 模擬
   使用者: 你叫什麼名字
   系統  : 我是 chatbot，由序列到序列模型生成。
4. 對話狀態追蹤
   摘要  : 狀態：{'intent': 'booking', 'name': '小明'}，已進行 2 輪
```

## 技術分析

### 四種方法的比較

| 方法 | 優點 | 缺點 | 適用場景 |
|------|------|------|---------|
| 模式匹配 | 簡單、可控 | 缺乏彈性 | 簡單問答 |
| 檢索式 | 回覆品質高 | 知識有限 | 客服FAQ |
| 生成式 | 靈活多變 | 不夠穩定 | 開放聊天 |
| 狀態追蹤 | 結構化 | 設計複雜 | 任務完成 |

## 延伸閱讀

- [ELIZA 原始論文](https://www.google.com/search?q=ELIZA+Weizenbaum+1966)
- [AIML 規範](https://www.google.com/search?q=AIML+Alice+bot)
- [Seq2Seq 對話生成](https://www.google.com/search?q=Seq2Seq+dialogue+generation)
- [對話狀態追蹤](https://www.google.com/search?q=Dialog+State+Tracking+DST)

*本篇文章為「AI 程式人雜誌 2022 年 11 月號」對話系統專題的程式實作解析。*
