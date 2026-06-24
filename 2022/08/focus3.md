# 模型平行 ModelParallel

## 基本原理

模型平行將神經網路的不同層分配到不同 GPU 上。例如，一個12層的 Transformer 可以將第1-4層放在 GPU0、第5-8層放在 GPU1、第9-12層放在 GPU2。資料依序通過各 GPU，前向傳播時層層傳遞，反向傳播時反向傳遞。

## 實作方式

在 PyTorch 中，模型平行可透過將不同子模型分配到不同裝置實作：

```
class ModelParallelModel(nn.Module):
    def __init__(self):
        self.seq1 = nn.Sequential(...).to('cuda:0')
        self.seq2 = nn.Sequential(...).to('cuda:1')

    def forward(self, x):
        x = x.to('cuda:0')
        x = self.seq1(x)
        x = x.to('cuda:1')
        x = self.seq2(x)
        return x
```

## GPU 利用率的問題

模型平行有一個重大缺點：在任何時刻，只有一個 GPU 處於活躍狀態。當 GPU0 運算時，GPU1 在等待；當 GPU1 運算時，GPU0 已閒置。這導致 GPU 利用率極低，且加速比可能小於1。

## 何時使用模型平行

儘管效率不高，模型平行在以下情境仍然必要：
- 單一 GPU 記憶體完全無法容納模型
- 作為管線平行或張量平行的基礎元件
- 原型開發與測試階段

模型平行通常不單獨使用，而是與其他平行策略（如資料平行）結合。

[搜尋 Model Parallelism PyTorch](https://www.google.com/search?q=model+parallelism+PyTorch)
[搜尋模型平行化深度學習](https://www.google.com/search?q=model+parallelism+deep+learning+neural+network)
