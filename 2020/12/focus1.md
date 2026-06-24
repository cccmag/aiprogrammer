# 大型語言模型的爆發：GPT-3 與預訓練模型

## 前言

2020 年 6 月，OpenAI 發布了 GPT-3，這是大型語言模型發展的里程碑。1750 億參數的規模展示了 Scale Law 的威力。

## GPT-3 的規格

```
GPT-3 規格：
────────────────────────────────

參數數量：  1750 億
訓練資料：  CommonCrawl, WebText, Books, Wikipedia
模型大小：  ~350GB
訓練成本：  估計 ~1200 萬美元
訓練 tokens：約 3000 億

對比：
GPT-1:    1.17 億   參數
GPT-2:    15 億     參數
GPT-3:   1750 億    參數  ◄─ 100x 增長
```

## GPT-3 的核心能力

### Few-Shot 學習

```python
# GPT-3 的 few-shot 能力示例

# 翻譯任務 - 只需給出範例
prompt = """Translate English to French:

English: "hello"
French: "bonjour"

English: "goodbye"
French: "au revoir"

English: "thank you"
French:"""

# GPT-3 可以從上下文學習模式，生成正確翻譯
# 輸出: "merci"
```

### 程式碼生成

```python
# Codex - GPT-3 的程式碼專家

prompt = """# Python function to find the longest palindrome in a string

def longest_palindrome(s):
"""

# Codex 可以生成完整的回文查找函數
```

## 預訓練模型生態系

```
2020 年重要模型：
────────────────────────────────

1. T5 (Google, 3月)
   - 110 億參數
   - 統一的文字到文字 transformer

2. GPT-3 (OpenAI, 5-6月)
   - 1750 億參數
   - 最強大的語言模型之一

3. GPT-Neo (EleutherAI, 7月)
   - 開放的 GPT-3 替代
   - 2.7B 和 1.3B 版本

4. CLIP (OpenAI, 1月)
   - 文字-影像對比學習
   - 零樣本影像分類
```

## 大型語言模型的影響

```
GPT-3 的影響：
────────────────────────────────

1. 商業模式創新
   └── AI 即服務 (AI-as-a-Service)
   └── API 經濟

2. 應用創新
   └── 文案生成
   └── 程式碼輔助
   └── 對話系統

3. 研究方向
   └── Scale Law 研究
   └── Prompt Engineering
   └── 知識蒸餾
```

## 挑戰與批評

```
爭議論點：
────────────────────────────────

1. 能源消耗
   └── 訓練成本昂貴
   └── 環境影響

2. 偏見問題
   └── 訓練資料中的偏見
   └── 有害內容生成

3. 存取不平等
   └── 只有大公司能訓練
   └── 數位落差加劇
```

## 延伸閱讀

- [GPT-3 論文](https://www.google.com/search?q=GPT-3+paper+language+models+few-shot)
- [大型語言模型倫理](https://www.google.com/search?q=large+language+model+ethics+bias)
- [Scale Law 研究](https://www.google.com/search?q=neural+scaling+laws+GPT-3)

---

*本篇文章為「AI 程式人雜誌 2020 年 12 月號」年度回顧系列之一。*