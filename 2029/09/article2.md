# 生成式 AI 在藥物發現

## 從大海撈針到定向設計

傳統藥物開發平均耗時 10-15 年、花費 26 億美元。生成式 AI 正在從頭改造這個流程，讓科學家從隨機篩選轉向理性設計。

## 分子生成模型

變分自編碼器（VAE）、生成對抗網路（GAN）和擴散模型是三大主流方法。這些模型在化學空間中學習分子分佈，然後生成符合藥物化學規則的新分子。REINVENT 和 MolGAN 是代表性開源工具。

```python
# 使用簡易 VAE 生成分子指紋
import numpy as np

class MoleculeVAE:
    def __init__(self, latent_dim=32):
        self.latent_dim = latent_dim
        # 編碼器權重（示意）
        self.encoder_w = np.random.randn(128, latent_dim) * 0.1
    
    def encode(self, fingerprint):
        latent = fingerprint @ self.encoder_w
        return latent
    
    def decode(self, latent):
        return np.tanh(latent @ np.random.randn(latent_dim, 128))
    
    def generate(self, n=5):
        z = np.random.randn(n, self.latent_dim)
        return self.decode(z)

vae = MoleculeVAE()
new_mols = vae.generate(3)
print(f"生成 {len(new_mols)} 個候選分子")
print(f"指紋維度: {new_mols.shape}")
```

## ADMET 預測與優化

生成式 AI 不僅創造分子，還能同時優化吸收、分佈、代謝、排泄、毒性（ADMET）性質。多目標優化框架如多任務學習和 Pareto 優化，可同時滿足藥效和安全性要求。

## 實際案例

Insilico Medicine 利用生成式 AI 發現的纖維化藥物已進入 II 期臨床試驗。Recursion Pharmaceuticals 則整合高通量影像與 AI 模型進行表型藥物發現。這些案例證明 AI 能大幅壓縮早期發現時間。

> 參考資料：https://www.google.com/search?q=generative+AI+drug+discovery+2025
