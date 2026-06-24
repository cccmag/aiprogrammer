# Batch Normalization 原論文發布兩年

## 前言

Batch Normalization 論文於 2015 年發表，兩年後的 2017 年，它已成為深度學習的標準技術。本篇文章回顧 BatchNorm 的影響。

## BatchNorm 的核心思想

```python
class BatchNorm2d(nn.Module):
    def __init__(self, num_features, eps=1e-5, momentum=0.1):
        super().__init__()
        self.gamma = nn.Parameter(torch.ones(num_features))
        self.beta = nn.Parameter(torch.zeros(num_features))
        self.eps = eps
        self.momentum = momentum
        self.running_mean = torch.zeros(num_features)
        self.running_var = torch.ones(num_features)

    def forward(self, x):
        if self.training:
            # 計算 mini-batch 統計
            mean = x.mean(dim=(0, 2, 3))
            var = x.var(dim=(0, 2, 3), unbiased=False)

            # 更新移動平均
            self.running_mean = self.momentum * self.running_mean + \
                               (1 - self.momentum) * mean
            self.running_var = self.momentum * self.running_var + \
                              (1 - self.momentum) * var
        else:
            mean = self.running_mean
            var = self.running_var

        # 標準化
        x_norm = (x - mean.view(1, -1, 1, 1)) / \
                torch.sqrt(var.view(1, -1, 1, 1) + self.eps)

        # 縮放和平移
        return self.gamma.view(1, -1, 1, 1) * x_norm + \
               self.beta.view(1, -1, 1, 1)
```

## 為什麼 BatchNorm 有效？

```
┌─────────────────────────────────────────────────────────┐
│              BatchNorm 穩定訓練的機制                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 減少內部協變量轉移                                  │
│     - 每層輸入分佈穩定                                  │
│     - 解決「多層」依賴問題                               │
│                                                         │
│  2. 緩解梯度消失                                        │
│     - 輸出分佈穩定                                      │
│     - 允許更激進的學習率                                │
│                                                         │
│  3. 提供輕微正則化                                      │
│     - Mini-batch 統計有噪聲                             │
│     - 替代 Dropout 的某些功能                           │
│                                                         │
│  4. 減少對初始化的敏感                                  │
│     - 權重初始化不再那麼關鍵                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## BatchNorm 的應用

```python
#幾乎所有現代 CNN 都使用 BatchNorm
model = nn.Sequential(
    nn.Conv2d(3, 64, 7, stride=2, padding=3),
    nn.BatchNorm2d(64),
    nn.MaxPool2d(3, stride=2, padding=1),

    # ... 更多 ResNet 區塊
    ResidualBlock(64, 64),
    ResidualBlock(64, 128, stride=2),  # 維度變化
    # BatchNorm 在每個捲積後
)
```

## 變體

| 變體 | 發布年份 | 特點 |
|------|----------|------|
| BatchNorm | 2015 | 原始版本 |
| LayerNorm | 2016 | RNN友好 |
| InstanceNorm | 2017 | 風格遷移 |
| GroupNorm | 2018 | 小批次友好 |

## 在 2017 年的地位

到 2017 年，BatchNorm 已經成為：

1. **幾乎所有影視模型的必備组件**
2. **深度學習教程的標準內容**
3. **框架的默認最佳實踐**

```python
# PyTorch 中預訓練模型都使用 BatchNorm
import torchvision.models as models

# ResNet, VGG, DenseNet 等都包含 BatchNorm
resnet = models.resnet50(pretrained=True)
print(resnet)  # 可以看到大量 BatchNorm2d 層
```

---

**延伸閱讀**

- [Batch Normalization Paper (Ioffe & Szegedy, 2015)](https://www.google.com/search?q=batch+normalization+ioffe+2015)
- [BatchNorm in Practice](https://www.google.com/search?q=batch+norm+deep+learning+practice)

---

*本篇文章為「AI 程式人雜誌 2017 年 11 月號」AI 相關文章之一。*