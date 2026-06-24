# 蛋白質結構預測（2020-2029）

## 蛋白質摺疊問題

蛋白質摺疊問題被譽為「生物學的聖杯」：給定胺基酸序列，如何預測其三維結構？這個問題困擾了科學界超過半個世紀。

## AlphaFold — 轉折點

2020 年 11 月，DeepMind 的 AlphaFold2 在 CASP14 比賽中取得驚人成績，原子座標 RMSD 中位數達到 0.96 Å，接近實驗精度。

```
CASP 歷史成績（GDT_TS 評分）：
2016: 40-50% (傳統方法)
2018: ~60% (AlphaFold1)
2020: ~90% (AlphaFold2)
2022: ~92% (AlphaFold2 改進版)
2024+: ~95% (AlphaFold3 / RoseTTAFold All-Atom)
```

## 技術原理

AlphaFold2 的核心是 Evoformer 架構，它交替處理序列和結構資訊：

```python
class EvoformerBlock(nn.Module):
    def __init__(self, c_m=256, c_z=128):
        super().__init__()
        self.msa_attn = MultiheadAttention(c_m)
        self.pair_attn = MultiheadAttention(c_z)
        self.msa_trans = FeedForward(c_m)
        self.pair_trans = FeedForward(c_z)
        self.msa_to_pair = Linear(c_m, c_z)

    def forward(self, msa, pair):
        # MSA 行注意力
        msa = msa + self.msa_attn(msa)
        # 配對表示更新
        pair = pair + self.pair_attn(pair)
        pair = pair + self.msa_to_pair(msa.mean(dim=1))
        return msa, pair
```

## 後 AlphaFold 時代

**2024** — AlphaFold3 發布，支援蛋白質-配體、蛋白質-DNA/RNA 的複合物結構預測，將應用範圍大幅擴展。

**2025** — ESMFold 和 ProstT5 等基於語言模型的方法出現，直接用蛋白質語言模型預測結構，不再需要 MSA 搜尋。

```python
from transformers import AutoModel, AutoTokenizer

model = AutoModel.from_pretrained("facebook/esm2_t33_650M")
tokenizer = AutoTokenizer.from_pretrained("facebook/esm2_t33_650M")
sequence = "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHF"
inputs = tokenizer(sequence, return_tensors="pt")
outputs = model(**inputs)
print(f"嵌入維度: {outputs.last_hidden_state.shape}")
```

**2027-2029** — 動態結構預測崛起，AI 不僅預測靜態結構，還能模擬蛋白質的摺疊過程和構象變化。結構生物學正在從「觀測」走向「預測」。

## 參考資源

- [AlphaFold2 原始論文](https://www.google.com/search?q=AlphaFold2+Nature+2021+protein+structure)
- [ESMFold 語言模型](https://www.google.com/search?q=ESMFold+protein+language+model)
- [CASP 蛋白質結構預測競賽](https://www.google.com/search?q=CASP+protein+structure+prediction)
