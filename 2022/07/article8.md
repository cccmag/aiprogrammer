# 資料擴增：回譯、EDA

## 資料擴增技術在 NLP 中的應用

### 為什麼需要資料擴增

在 NLP 任務中，標註資料的獲取成本很高。資料擴增（Data Augmentation）透過對現有資料進行有控制的變換，生成新的訓練樣本，提升模型泛化能力。主要好處包括增加資料量、提升魯棒性、減少過擬合。

### EDA（Easy Data Augmentation）

EDA 包含四種操作：

```python
import random

def synonym_replacement(text, n=1):
    words = list(text.split())
    for _ in range(n):
        idx = random.randint(0, len(words)-1)
        words[idx] = random.choice(get_synonyms(words[idx]) or [words[idx]])
    return ' '.join(words)

def random_insertion(text, n=1):
    words = list(text.split())
    for _ in range(n):
        words.insert(random.randint(0, len(words)), random.choice(words))
    return ' '.join(words)

def random_swap(text, n=1):
    words = list(text.split())
    for _ in range(n):
        i, j = random.sample(range(len(words)), 2)
        words[i], words[j] = words[j], words[i]
    return ' '.join(words)

def random_deletion(text, p=0.1):
    words = list(text.split())
    if len(words) == 1:
        return text
    result = [w for w in words if random.random() > p]
    return ' '.join(result) if result else random.choice(words)
```

### 回譯

回譯是最有效的擴增方法。將原始文本翻譯到另一種語言再翻譯回來，產生語義相似但表述不同的句子。

```python
def back_translate(text, source='zh', bridge='en'):
    intermediate = translate(text, source, bridge)
    return translate(intermediate, bridge, source)
```

回譯的優點：保持語義不變、產生自然的多樣化表達、覆蓋多種語言風格。

### 雜訊注入

在文字中加入輕微拼寫錯誤或鍵盤錯誤：

```python
def add_typo(text, p=0.05):
    chars = list(text)
    for i in range(len(chars)):
        if random.random() < p and chars[i].isalpha():
            chars[i] = random.choice('abcdefghijklmnopqrstuvwxyz')
    return ''.join(chars)
```

### 擴增策略選擇

文字分類推薦 EDA 和回譯；機器翻譯推薦回譯和反向翻譯；命名實體識別需使用同義詞替換並保持實體邊界；情感分析可使用 EDA 和回譯。

### 注意事項

確保擴增樣本不改變原始標籤，對結果進行抽樣檢查，控制擴增比例避免引入過多雜訊。

---

## 延伸閱讀

- [EDA: Easy Data Augmentation 論文](https://www.google.com/search?q=EDA+easy+data+augmentation+Wei+Zou)
- [回譯資料擴增技術](https://www.google.com/search?q=back+translation+data+augmentation+NLP)
- [NLP 資料擴增綜述](https://www.google.com/search?q=NLP+data+augmentation+survey)
