# NLP 任務的全面突破

## 前言

2019 年，幾乎所有 NLP 任務都經歷了效能的大幅提升。預訓練模型的崛起讓機器在許多任務上達到了或超越人類水準。

## GLUE 基準的突破

### GLUE 分數演進

| 時間 | 模型 | GLUE 分數 |
|------|------|-----------|
| 2018年前 | 人類基準 | 87.1 |
| 2018年6月 | GPT | 72.8 |
| 2018年10月 | BERT BASE | 80.2 |
| 2018年10月 | BERT LARGE | 86.2 |
| 2019年6月 | XLNet | 89.8 |
| 2019年7月 | RoBERTa | 90.2 |

### 各任務的突破

**問答（SQuAD）**

```
人類水準：91.2 EM
RoBERTa：94.6 EM（超越人類）
```

**情感分析（SST-2）**

```
人類水準：97.3%
RoBERTa：95.4%（接近人類）
```

## 各類任務的進展

### 文字分類

```python
from transformers import BertForSequenceClassification

model = BertForSequenceClassification.from_pretrained('bert-base-uncased')
# 在多種分類任務上超越傳統方法
```

### 命名實體識別

| 資料集 | 之前最佳 | BERT 系列 |
|--------|----------|-----------|
| CoNLL-2003 | 93.5% | 96.0% |

### 機器翻譯

Transformer 架構在機器翻譯上取得了巨大進步：

```python
# Transformer 翻譯示例
from transformers import MarianMTModel, MarianTokenizer

tokenizer = MarianTokenizer.from_pretrained('Helsinki-NLP/opus-mt-en-zh')
model = MarianMTModel.from_pretrained('Helsinki-NLP/opus-mt-en-zh')
```

## 預訓練+微調範式的勝利

### 遷移學習的流程

```
預訓練階段：
大型無標注文本 → 語言模型

微調階段：
預訓練模型 + 任務標注資料 → 任務模型
```

### 這種範式的優勢

```
優勢：
1. 可復用性高
2. 訓練效率高
3. 遷移能力強
```

## 新基準的建立

### SuperGLUE

隨著 GLUE 被超越，SuperGLUE 在 2019 年推出：

```
SuperGLUE 任務：
- BoolQ：布林問答
- CB：承諾銀行
- COPA：因果推理
- MultiRC：多選項閱讀理解
```

### 領域特定基準

2019 年湧現了多個領域特定的基準：

| 基準 | 領域 |
|------|------|
| BLUE | 生物醫學 |
| LEGAL-BERT | 法律 |
| SciBERT | 科學文獻 |

## 結論

2019 年是 NLP 領域的豐收年。預訓練模型幾乎在所有任務上都帶來了顯著提升。這種成功很大程度上歸功於預訓練+微調範式的勝利，以及 Transformer 架構的廣泛採用。

---

**延伸閱讀**

- [NLP+benchmark+2019](https://www.google.com/search?q=NLP+benchmark+2019)
- [GLUE+SuperGLUE+2019](https://www.google.com/search?q=GLUE+SuperGLUE+2019)
- [pretrained+models+NLP](https://www.google.com/search?q=pretrained+models+NLP+2019)