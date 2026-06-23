# 合成資料生成技術（2021-2028）

## 資料稀缺的解決方案

合成資料（Synthetic Data）是人工生成的、模擬真實資料分布的數據。2021 年之後，合成資料的需求爆炸性成長，原因有三：

1. **隱私法規**：GDPR、CCPA 嚴格限制個人資料使用
2. **長尾分佈**：真實資料中稀有事件樣本不足
3. **成本考量**：真實資料標註成本極高，某些領域需要專家標註

## 合成資料生成方法

### 1. 基於規則的生成

最簡單的方法，適合結構化資料：

```python
import random, string

def generate_user_profile(n: int) -> list[dict]:
    cities = ["台北", "新竹", "台中", "高雄"]
    users = []
    for i in range(n):
        users.append({
            "user_id": i,
            "age": random.randint(18, 70),
            "city": random.choice(cities),
            "income": int(random.gauss(50000, 15000)),
            "signup_date": f"202{random.randint(4,8)}-{random.randint(1,12):02d}-01",
        })
    return users
```

### 2. 基於 GAN 的生成

生成對抗網路（GAN）在 2021-2023 年間成為合成影像的主流方法。StyleGAN、Diffusion Models 能生成逼真的人臉、醫學影像。

### 3. 基於 LLM 的生成

2023 年後，LLM 成為合成資料生成的主力工具。GPT-4 和後續模型可以生成：
- 對話資料（客服、助理）
- 文件摘要對（RAG 訓練用）
- 多輪問答對（微調資料）
- 程式碼與解釋對

```
LLM 合成資料的主要模式：

Context（主題、格式、數量）
  → Prompt Engineering
  → LLM 生成
  → 過濾 (品質、重複、偏差檢查)
  → 可用資料集
```

## SDV：合成資料工具

SDV（Synthetic Data Vault）是 2021 年崛起的最受歡迎開源合成資料工具：

```python
from sdv import SDV
from sdv.tabular import GaussianCopula

# 從真實資料學習分布
model = GaussianCopula()
model.fit(real_data)

# 生成合成資料
synthetic_data = model.sample(num_rows=1000)
```

## 資料增強

合成資料生成和資料增強（Data Augmentation）經常一起使用。2022 年後，NLP 領域的資料增強大幅依賴 LLM：

```python
def augment_text(text: str, llm_client) -> list[str]:
    prompt = f"Generate 3 paraphrases of: '{text}'"
    return llm_client.generate(prompt).split("\n")
```

## 品質與風險

合成資料不是萬能藥。需要注意：
- **隱私洩漏**：GAN 可能記憶訓練資料，導致隱私風險
- **分布偏差**：合成模型可能放大訓練資料中的偏差
- **評估困難**：合成資料的品質難以客觀衡量

2025 年後，差分隱私（Differential Privacy）訓練的生成模型成為業界標準。

## 延伸閱讀

- [Synthetic Data Vault](https://www.google.com/search?q=Synthetic+Data+Vault+SDV+open+source)
- [GAN for Synthetic Data](https://www.google.com/search?q=GAN+synthetic+data+generation)
- [LLM Data Augmentation](https://www.google.com/search?q=LLM+data+augmentation+NLP+2024)

---

*本篇文章為「AI 程式人雜誌 2028 年 4 月號」資料工程系列之六。*
