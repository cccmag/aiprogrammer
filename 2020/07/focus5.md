# GPT-3 的應用場景

## 文字生成

### 創意寫作

GPT-3 在創意寫作方面展現了令人驚艷的能力：

- 小說、詩歌創作
- 劇本對話生成
- 新聞文章撰寫

### 商業應用

- 自動生成產品描述
- 市場行銷文案
- 客戶服務回覆

### 限制

- 有時會產生重複內容
- 邏輯一致性不足
- 缺乏長期規劃能力

---

## 程式碼生成

### Codex 的誕生

OpenAI 開發了 Codex（一個基於 GPT-3 的程式碼生成模型），後來成為 GitHub Copilot 的基礎。

### 能力展示

```
Prompt: "Write a Python function to calculate fibonacci numbers"
Output: 
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### 支援語言

- Python
- JavaScript
- TypeScript
- Go
- Ruby
- 其他數十種語言

### 局限性

- 複雜架構理解不足
- 需要人類審查
- 可能產生安全漏洞

---

## 翻譯與摘要

### 多語言翻譯

GPT-3 展示了優秀的多語言能力：

| 語言對 | GPT-3 | SOTA |
|--------|-------|------|
| En-Fr | 41.6 | 45.6 |
| En-De | 40.2 | 41.2 |
| En-Ro | 38.2 | 39.9 |

### 文字摘要

可以使用 Few-shot 進行摘要：

```
Prompt:
"Article: [長文章內容]

Summary in 2 sentences: [模型輸出]"
```

---

## 問答系統

### 封閉域問答

GPT-3 能夠回答各種知識性問題：

```
Q: Who was the first person to walk on the moon?
A: Neil Armstrong
```

### 開放域問答

在 TriviaQA 等 benchmark 上達到 71.2% 準確率。

---

## 教育應用

### 智慧家教

GPT-3 可以作為個人導師：
- 解釋數學概念
- 輔助語言學習
- 提供個人化的學習建議

### 限制

- 可能產生錯誤資訊
- 需要事實核查
- 不適合高風險決策

---

## 遊戲與互動

### 文字冒險遊戲

GPT-3 可以創造互動式文字世界：

- 動態生成遊戲場景
- 智慧 NPC 對話
- 自動劇情生成

---

## 商業化挑戰

### API 訪問

2020 年 7 月，OpenAI 開放 GPT-3 API 申請，但アクセス受限。

### 定價模式

- 按 token 計費
- 不同模型的成本差異
- 大規模使用成本高昂

### 安全考量

- 有害內容生成
- 偏見放大
- 誤導資訊傳播

---

**下一步**：[Few-shot 的限制與挑戰](focus6.md)

## 延伸閱讀

- [GPT-3+applications+code+generation](https://www.google.com/search?q=OpenAI+GPT-3+code+generation+Copilot+2020)
- [GPT-3+translation+capabilities](https://www.google.com/search?q=OpenAI+GPT-3+translation+multilingual+2020)
- [AI+writing+GPT-3+creative+writing](https://www.google.com/search?q=AI+writing+GPT-3+creative+applications+2020)