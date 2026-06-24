# GAN 實戰：生成對抗網路基礎

## 前言

生成對抗網路（GAN）是生成模型的重要突破，可用於生成影像、文字等多種資料。

## GAN 原理

```
       生成器 (G)              鑑別器 (D)
         │                        │
    隨機噪音 ──► 生成影像 ──► 判斷真假
                      │            │
                      │        真/假
                      │            │
                      ▼            ▼
                   輸入真實圖像 ◄──┘
```

### 對抗訓練

```python
# 目標函數
# D: 最大化 log(D(x)) + log(1 - D(G(z)))
# G: 最小化 log(1 - D(G(z)))

def generator_loss(fake_output):
    return -torch.mean(torch.log(fake_output + 1e-10))

def discriminator_loss(real_output, fake_output):
    real_loss = -torch.mean(torch.log(real_output + 1e-10))
    fake_loss = -torch.mean(torch.log(1 - fake_output + 1e-10))
    return (real_loss + fake_loss) / 2
```

## DCGAN 實作

```python
class Generator(nn.Module):
    def __init__(self, nz, ngf, nc):
        super().__init__()
        self.main = nn.Sequential(
            nn.ConvTranspose2d(nz, ngf*8, 4, 1, 0),
            nn.BatchNorm2d(ngf*8),
            nn.ReLU(True),
            nn.ConvTranspose2d(ngf*8, ngf*4, 4, 2, 1),
            nn.BatchNorm2d(ngf*4),
            nn.ReLU(True),
            nn.ConvTranspose2d(ngf*4, nc, 4, 2, 1),
            nn.Tanh()
        )

    def forward(self, x):
        return self.main(x)
```

## 應用場景

- 影像生成（StyleGAN）
- 影像超解析度（SRGAN）
- 風格遷移（CycleGAN）
- 資料增強

## 延伸閱讀

- [GAN 原始論文](https://www.google.com/search?q=GAN+Goodfellow+2014)
- [DCGAN 論文](https://www.google.com/search?q=DCGAN+Radford+2015)