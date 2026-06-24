# ResNet 架構詳解

ResNet 是深度學習領域的里程碑論文。

## 1. 核心思想

ResNet 提出了殘差連接（skip connection）的概念：

```python
class ResidualBlock(nn.Module):
    def forward(self, x):
        identity = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = F.relu(out)
        out = self.conv2(out)
        out = self.bn2(out)
        out += identity
        return F.relu(out)
```

## 2. 為什麼殘差有效？

- 梯度可以直接流向較低層
- 網路可以學習恆等映射
- 緩解深度網路的退化問題

## 3. 變體

- Pre-act ResNet：激活函數放在殘差之前
- SE-ResNet：加入通道注意力
- ResNeXt：引入 cardinality

---

## 延伸閱讀

- [ResNet 原始論文](https://www.google.com/search?q=ResNet+deep+residual+learning+image+recognition+He)
- [殘差網路詳解](https://www.google.com/search?q=residual+networks+explained+deep+learning)