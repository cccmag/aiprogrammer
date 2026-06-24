# GAN 在其他領域的應用

## 前言

雖然 GAN 最初是為影像生成而設計，但其對抗訓練的思想已經擴展到多個領域。本篇文章將探討 GAN 在文字、語音、藥物發現等非影像領域的應用。

## 文字生成

### 文字 GAN 的挑戰

將 GAN 應用於文字生成面臨獨特挑戰：

```
┌─────────────────────────────────────────────────────────┐
│          文字 GAN 的主要挑戰                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 離散輸出                                            │
│     - 影像：連續像素值（可微）                          │
│     - 文字：離散token（難以反向傳播）                   │
│                                                         │
│  2. 序列生成                                            │
│     - 需要 RNN/LSTM 而非 CNN                            │
│     - 長期依賴問題                                       │
│                                                         │
│  3. 評估困難                                            │
│     - 文字品質難以用簡單指標衡量                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### SeqGAN

SeqGAN 是將 GAN 應用於序列生成的早期嘗試：

```python
#!/usr/bin/env python3
"""SeqGAN concept demonstration"""

import torch
import torch.nn as nn
import numpy as np

class Generator(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)

    def forward(self, x, hidden=None):
        # x: (batch, seq_len)
        embedded = self.embedding(x)  # (batch, seq_len, embed_dim)
        output, hidden = self.lstm(embedded, hidden)
        return output, hidden

    def sample(self, start_token, length, hidden=None):
        """Sampling from the generator"""
        tokens = [start_token]
        for _ in range(length - 1):
            output, hidden = self.forward(torch.tensor([[tokens[-1]]]), hidden)
            probs = torch.softmax(output[:, -1, :], dim=-1)
            token = torch.multinomial(probs, 1).item()
            tokens.append(token)
        return tokens

class Discriminator(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.conv1 = nn.Conv1d(embed_dim, hidden_dim, 3)
        self.conv2 = nn.Conv1d(hidden_dim, hidden_dim, 3)
        self.fc = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        # x: (batch, seq_len)
        embedded = self.embedding(x).transpose(1, 2)  # (batch, embed, seq)
        conv1 = torch.relu(self.conv1(embedded))
        conv2 = torch.relu(self.conv2(conv1))
        pooled = torch.max(conv2, dim=-1)[0]
        return torch.sigmoid(self.fc(pooled))
```

### 強化學習視角

SeqGAN 將生成器視為強化學習中的 policy，判別器給予 reward：

```python
# SeqGAN 的強化學習訓練
def train_step(generator, discriminator, optimizer_G, optimizer_D,
                real_seqs, start_token):
    batch_size = real_seqs.size(0)
    seq_len = real_seqs.size(1)

    # 1. 訓練判別器
    fake_seqs = []
    for i in range(batch_size):
        fake_seq = generator.sample(start_token, seq_len - 1)
        fake_seqs.append(fake_seq)
    fake_seqs = torch.tensor(fake_seqs)

    real_output = discriminator(real_seqs)
    fake_output = discriminator(fake_seqs.detach())

    d_loss = -torch.mean(torch.log(real_output + 1e-8)
                      + torch.log(1 - fake_output + 1e-8))

    optimizer_D.zero_grad()
    d_loss.backward()
    optimizer_D.step()

    # 2. 計算 Monte Carlo 回饋
    rewards = []
    for i in range(batch_size):
        mc_seqs = [fake_seqs[i:i+1]]  # 簡化版本
        mc_output = discriminator(torch.cat(mc_seqs, dim=0))
        rewards.append(mc_output.mean().item())

    # 3. 訓練生成器（Policy Gradient）
    generator.zero_grad()
    # 使用 REINFORCE 演算法
    log_probs = []
    hidden = None
    for t in range(seq_len - 1):
        output, hidden = generator(
            torch.tensor([[fake_seqs[i][t] for i in range(batch_size)]]).unsqueeze(1),
            hidden
        )
        probs = torch.softmax(output.squeeze(1), dim=-1)
        action = torch.tensor([fake_seqs[i][t+1] for i in range(batch_size)])
        log_prob = torch.log(probs.gather(1, action.unsqueeze(1)) + 1e-8)
        log_probs.append(log_prob)

    # 計算策略梯度
    policy_loss = 0
    for log_prob, reward in zip(log_probs, rewards):
        policy_loss -= log_prob * reward

    policy_loss.backward()
    optimizer_G.step()
```

## 語音合成

### WaveNet 與 GAN

2017 年 DeepMind 發布的 WaveNet 開創了原始音訊生成的新時代。雖然原始 WaveNet 不是 GAN，但後續研究將 GAN 應用於語音增強。

```python
class AudioGenerator(nn.Module):
    def __init__(self, latent_dim, num_channels):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv1d(latent_dim, 256, 25, stride=4, padding=12),
            nn.ReLU(),
            nn.Conv1d(256, 512, 25, stride=4, padding=12),
            nn.ReLU(),
            nn.Conv1d(512, 512, 25, stride=4, padding=12),
            nn.ReLU(),
            nn.Conv1d(512, num_channels, 25, stride=4, padding=12),
            nn.Tanh()
        )

    def forward(self, z):
        # z: (batch, latent_dim)
        # 需要調整維度以適應 Conv1d
        return self.net(z.unsqueeze(-1))
```

## 藥物發現

GAN 在藥物發現領域展現出巨大潛力，可以用於生成新的分子結構：

```
┌─────────────────────────────────────────────────────────┐
│           藥物發現中的 GAN 應用                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   输入：已知藥物分子的 SMILES 表示                       │
│                                                         │
│   ┌───────┐                                           │
│   │  GAN  │ ────生成新的分子結構─────→ 候選藥物        │
│   └───────┘                                           │
│                                                         │
│   判別器：區分真實藥物分子和生成的分子                   │
│   生成器：生成具有特定性質的分子                         │
│                                                         │
│   應用：                                               │
│   - 抗生素候選分子                                     │
│   - 抗癌藥物設計                                       │
│   - 蛋白質結構預測                                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### MolGAN

MolGAN 是一個專門為分子生成設計的 GAN 架構：

```python
class MolecularGenerator(nn.Module):
    def __init__(self, latent_dim, max_atoms=9):
        super().__init__()
        self.latent_dim = latent_dim
        self.max_atoms = max_atoms

        self.net = nn.Sequential(
            nn.Linear(latent_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 512),
            nn.ReLU(),
            nn.Linear(512, max_atoms * max_atoms * 4)  # 鄰接矩陣 + 特徵
        )

    def forward(self, z):
        output = self.net(z)
        # 輸出分子的鄰接矩陣和原子特徵
        return output.view(-1, self.max_atoms, self.max_atoms, 4)
```

## 資料增強

GAN 還可以用於生成訓練資料，緩解數據不足的問題：

```python
class DataAugmentationGAN(nn.Module):
    """使用 GAN 生成額外的訓練資料"""

    def __init__(self, generator, classifier):
        super().__init__()
        self.generator = generator
        self.classifier = classifier

    def augment(self, real_data, labels, num_samples):
        """生成增強資料"""
        generated_data = []
        for label in labels.unique():
            # 只生成特定類別的資料
            label_mask = (labels == label)
            label_data = real_data[label_mask]

            if len(label_data) < num_samples:
                # 生成額外樣本
                noise = torch.randn(num_samples - len(label_data), 100)
                fake_samples = self.generator(noise, label)
                generated_data.append(fake_samples)

        return torch.cat([real_data] + generated_data, dim=0)
```

## 表格資料生成

GAN 也可以用於生成表格資料（如金融交易記錄）：

```python
class TabularGenerator(nn.Module):
    """表格資料生成器"""

    def __init__(self, latent_dim, num_features):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(latent_dim, 128),
            nn.ReLU(),
            nn.BatchNorm1d(128),
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.Linear(256, num_features),
            nn.Sigmoid()  # 假設所有特徵都正規化到 [0,1]
        )

    def forward(self, z):
        return self.net(z)
```

## 實驗展示

```python
#!/usr/bin/env python3
"""Non-image GAN applications demo"""

import torch
import torch.nn as nn

def demo():
    print("GAN Applications Beyond Images")
    print("=" * 50)

    print("\n1. Text Generation:")
    print("   - SeqGAN: Sequence generation with RL")
    print("   - TextGAN: Text generation with CNN")
    print("   - LeakGAN: Hierarchical generation")

    print("\n2. Speech Synthesis:")
    print("   - WaveNet: Raw audio generation")
    print("   - Parallel WaveNet: Fast generation")
    print("   - GAN-TTS: Speech enhancement")

    print("\n3. Drug Discovery:")
    print("   - MolGAN: Molecular graph generation")
    print("   - ORGAN: Objective-reinforced GAN")
    print("   - Latent GAN: Protein structure")

    print("\n4. Data Augmentation:")
    print("   - CTGAN: Tabular data")
    print("   - Signature GAN: Signature verification")
    print("   - Medical imaging: Rare disease data")

    print("\n5. Tabular Data:")
    print("   - TableGAN: Database augmentation")
    print("   - TGAN: Time-series generation")

    # Demo code structure
    print("\n6. Implementation Example:")

    latent_dim = 100
    seq_len = 20
    vocab_size = 10000

    class DummyGenerator(nn.Module):
        def __init__(self):
            super().__init__()
            self.embedding = nn.Embedding(vocab_size, 128)
            self.lstm = nn.LSTM(128, 256, batch_first=True)
            self.fc = nn.Linear(256, vocab_size)

        def forward(self, x, hidden=None):
            embedded = self.embedding(x)
            output, hidden = self.lstm(embedded, hidden)
            return self.fc(output)

    G = DummyGenerator()
    x = torch.randint(0, vocab_size, (4, seq_len))
    output = G(x)
    print(f"   Input shape: {x.shape}")
    print(f"   Output shape: {output.shape}")

    print("\nDemo completed!")

if __name__ == "__main__":
    demo()
```

## 應用領域對比

| 領域 | 模型 | 輸入 | 輸出 | 主要挑戰 |
|------|------|------|------|----------|
| 文字 | SeqGAN | 噪音 | 文字序列 | 離散輸出 |
| 語音 | WaveGAN | 噪音 | 音訊波形 | 時序依賴 |
| 藥物 | MolGAN | 藥物性質 | 分子結構 | 化學有效性 |
| 表格 | CTGAN | 噪音 | 表格資料 | 離散/連續混合 |
| 時間序列 | TimeGAN | 噪音 | 時間序列 | 多尺度依賴 |

---

## 延伸閱讀

- [Yu et al., 2017: SeqGAN](https://www.google.com/search?q=SeqGAN+Yu+2017)
- [Deac et al., 2019: MolGAN](https://www.google.com/search?q=MolGAN+molecular+generation)
- [CTGAN Paper](https://www.google.com/search?q=CTGAN+tabular+data+generation)

---

*本篇文章為「AI 程式人雜誌 2017 年 10 月號」 GAN 系列之六。*