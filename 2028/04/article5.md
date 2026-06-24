# 合成資料生成方法

## 前言

真實資料往往涉及隱私、稀缺或不平衡等問題。合成資料生成技術可以產生與真實資料統計特性相似的人工資料，用於模型訓練、測試和隱私保護。本文介紹三種主流的合成資料方法。

## SDV：生成式表格資料

SDV（Synthetic Data Vault）是最流行的開源合成資料庫，支援 CTGAN、Copula 等多種生成模型：

```python
from sdv.single_table import CTGANSynthesizer
from sdv.metadata import SingleTableMetadata
import pandas as pd

# 載入真實資料
real_data = pd.read_csv("customers.csv")
print(f"原始資料: {real_data.shape}")

# 自動推斷中繼資料
metadata = SingleTableMetadata()
metadata.detect_from_dataframe(real_data)

# 建立 CTGAN 合成器
synthesizer = CTGANSynthesizer(
    metadata,
    epochs=300,
    batch_size=500,
    discriminator_dim=(256, 128),
    generator_dim=(256, 128),
)

# 訓練模型
synthesizer.fit(real_data)

# 生成合成資料
synthetic_data = synthesizer.sample(num_rows=10000)
print(f"合成資料: {synthetic_data.shape}")

# 評估品質
from sdv.evaluation import evaluate
quality_report = evaluate(synthetic_data, real_data)
print(f"整體品質分數: {quality_report.get_score():.2f}")
```

## Faker：基於規則的資料生成

當需要特定格式的測試資料時，Faker 提供了最簡單的解決方案：

```python
from faker import Faker
import pandas as pd

fake = Faker("zh_TW")  # 台灣繁體中文

def generate_user_data(n: int) -> pd.DataFrame:
    data = []
    for _ in range(n):
        data.append({
            "name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "address": fake.address(),
            "company": fake.company(),
            "credit_card": fake.credit_card_number(),
            "created_at": fake.date_time_this_year(),
        })
    return pd.DataFrame(data)

users = generate_user_data(1000)
print(users.head())
```

## 擴散模型影像合成

最新趨勢是使用擴散模型產生合成影像資料：

```python
from diffusers import StableDiffusionPipeline
import torch

pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-1",
    torch_dtype=torch.float16
)
pipe = pipe.to("mps")  # Apple Silicon

# 生成不同場景的合成影像
prompts = [
    "A retail store interior with shelves of products",
    "A warehouse with stacked boxes and workers",
    "A street view of a busy city intersection",
]

for i, prompt in enumerate(prompts):
    image = pipe(prompt).images[0]
    image.save(f"synthetic_scene_{i}.png")
    print(f"已生成: synthetic_scene_{i}.png")
```

## 結語

合成資料正在從「不得已的替代方案」轉變為「主動的資料策略」。無論是解決隱私合規問題、擴增少樣本類別、還是產生邊緣案例的測試資料，合成資料都將在 AI 資料工程中扮演越來越重要的角色。

---

**延伸閱讀**

- [SDV 合成資料庫](https://www.google.com/search?q=Synthetic+Data+Vault+SDV)
- [Faker 資料生成庫](https://www.google.com/search?q=Faker+Python+library)
- [合成資料在 ML 的應用](https://www.google.com/search?q=synthetic+data+machine+learning)
