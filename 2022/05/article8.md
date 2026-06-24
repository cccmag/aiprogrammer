# GPT 提示工程

## 提示工程的核心

提示工程（Prompt Engineering）是設計輸入提示以引導大型語言模型產生預期輸出的技術。在 GPT-3 之後，這已經成為一個重要的技能領域。

## 基本技巧

### 1. 角色設定

```python
# 沒有角色設定
prompt = "解釋量子糾纏"

# 有角色設定
prompt = """你是一位量子物理學教授。
請用高中生能理解的方式解釋量子糾纏。
使用日常生活中的比喻。
"""
```

角色設定提供上下文，幫助模型選擇合適的知識領域和表達風格。

### 2. 少量範例（Few-shot）

```python
# Zero-shot
prompt = "將以下英文翻譯成中文：Hello, world!"

# Few-shot
prompt = """
English: I love programming
Chinese: 我熱愛程式設計

English: Machine learning is fascinating
Chinese: 機器學習令人著迷

English: Hello, world!
Chinese:"""
```

Few-shot 讓模型從範例中理解任務格式和期望。

### 3. 拆解步驟

```python
# 直接問
"解決這個數學問題：..."

# 拆解步驟
"""
逐步解決這個數學問題：
1. 首先，理解問題的已知條件
2. 然後，確定需要使用的公式
3. 接著，代入數值進行計算
4. 最後，驗證答案的合理性

問題：[你的問題]
"""
```

## 思維鏈提示

思維鏈（Chain-of-Thought, CoT）提示是讓模型在給出最終答案前展示推理過程：

```python
prompt = """
問題：一顆蘋果 3 元，一個柳丁 5 元。
小明買了 4 顆蘋果和 2 個柳丁，總共多少錢？

推理：
蘋果總價 = 4 × 3 = 12 元
柳丁總價 = 2 × 5 = 10 元
總價 = 12 + 10 = 22 元

答案：22 元

問題：一個書包 250 元，打 8 折後再打 9 折，
最後是多少錢？

推理："""
```

CoT 顯著提升了模型在推理任務上的表現（如數學問題、邏輯推理）。

## 提示設計原則

### 具體明確

```
❌ "寫點關於 AI 的東西"
✅ "寫一篇 300 字的部落格文章，介紹大語言模型在醫療領域的應用，
    目標讀者是沒有技術背景的醫療從業人員"
```

### 提供限制條件

```
❌ "翻譯這段文字"
✅ "將以下英文翻譯成繁體中文，保持原文的正式語氣，
    專業術語保留英文不翻譯：[文字]"
```

### 使用分隔符

```python
prompt = """
分析以下評論的情感（正面/負面/中性）：

---
這家餐廳的服務很好，但食物普通。
---

情感分析結果：
"""
```

## 進階技巧

### 溫度參數調整

- **低溫度（0.0-0.3）**：事實性任務（問答、翻譯）
- **中溫度（0.4-0.7）**：創意寫作、對話
- **高溫度（0.8-1.0）**：頭腦風暴、詩歌

### 系統提示

GPT API 支援系統級別的提示設定：

```python
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "你是一位友善的程式設計教練，用台灣繁體中文回答"},
        {"role": "user", "content": "解釋什麼是遞迴"}
    ]
)
```

## 常見陷阱

1. **過度引導**：提示中包含了太多範例答案，限制創造力
2. **矛盾指令**：同時要求簡潔和詳細
3. **遺漏格式**：沒指定輸出格式（JSON、列表、表格等）

## 延伸閱讀

- [Prompt Engineering Guide](https://www.google.com/search?q=prompt+engineering+guide)
- [GPT Best Practices](https://www.google.com/search?q=GPT+best+practices+prompt+engineering)
- [Chain-of-Thought Prompting](https://www.google.com/search?q=chain+of+thought+prompting)
