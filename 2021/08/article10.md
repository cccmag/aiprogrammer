# 生成式圖像模型

生成式模型可以創造新圖像，本文介紹主要方法。

## 1. GAN

生成對抗網路由生成器和判別器組成：

```python
class Generator(nn.Module):
    def forward(self, z):
        return self.decoder(z)

class Discriminator(nn.Module):
    def forward(self, x):
        return self.classifier(x)
```

## 2. VAE

變分自編碼器學習潛在空間：

```python
class VAE(nn.Module):
    def encode(self, x):
        return self.encoder(x)

    def decode(self, z):
        return self.decoder(z)
```

## 3. Diffusion Model

逐步去噪生成圖像，2021-2022 年取得巨大成功。

---

## 延伸閱讀

- [GAN 綜述](https://www.google.com/search?q=generative+adversarial+networks+tutorial+goodfellow)
- [Diffusion Model 詳解](https://www.google.com/search?q=denoising+diffusion+probabilistic+models+Ho)