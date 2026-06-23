# 量子經典混合訓練

## 前言

NISQ（含噪聲中等規模量子）時代的現實限制使混合量子-經典訓練成為當前量子 ML 的主流方法。

## 混合訓練框架

混合架構將參數化量子電路（PQC）嵌入到古典深度學習模型中，量子部分負責高維特徵提取，古典部分負責後處理。

## 使用 PyTorch 實現

```python
import torch
import torch.nn as nn
import numpy as np

class QuantumLayer(nn.Module):
    """模擬量子層：參數化旋轉 + 糾纏"""
    def __init__(self, n_qubits):
        super().__init__()
        self.n_qubits = n_qubits
        self.theta = nn.Parameter(torch.randn(n_qubits * 2))
    
    def forward(self, x):
        batch = x.shape[0]
        # 編碼輸入到旋轉角度
        angles = x * torch.pi
        
        # 模擬量子電路輸出
        # 應用 Ry 旋轉 + 糾纏效應
        out = torch.zeros(batch, self.n_qubits)
        for i in range(self.n_qubits):
            phase = self.theta[2*i] + angles[:, i] * self.theta[2*i + 1]
            out[:, i] = torch.sin(phase)
        
        return out

class HybridModel(nn.Module):
    def __init__(self, n_qubits=4, n_classes=2):
        super().__init__()
        self.quantum = QuantumLayer(n_qubits)
        self.classical = nn.Sequential(
            nn.Linear(n_qubits, 16),
            nn.ReLU(),
            nn.Linear(16, n_classes)
        )
    
    def forward(self, x):
        x = self.quantum(x)
        x = self.classical(x)
        return x
```

## 訓練循環

```python
from torch.utils.data import DataLoader, TensorDataset

model = HybridModel(n_qubits=4, n_classes=2)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# 合成資料
X = torch.randn(200, 4)
y = (X.sum(dim=1) > 0).long()

dataset = TensorDataset(X, y)
loader = DataLoader(dataset, batch_size=16, shuffle=True)

for epoch in range(30):
    for batch_x, batch_y in loader:
        optimizer.zero_grad()
        pred = model(batch_x)
        loss = criterion(pred, batch_y)
        loss.backward()
        optimizer.step()
    
    if epoch % 5 == 0:
        acc = (pred.argmax(1) == batch_y).float().mean()
        print(f"Epoch {epoch}: loss={loss.item():.4f}, acc={acc:.3f}")
```

## 混合訓練的優勢

1. **減少量子資源需求**：只用少量 qubit 處理最難的部分
2. **雜訊容忍度高**：古典層可補償量子雜訊
3. **可擴展性**：量子層數量可根據硬體能力調整
4. **梯度穩定**：古典層的激活函數可防止梯度消失

## 結語

混合量子-經典訓練是近期量子 ML 最實際的範式，讓研究者在現有量子硬體限制下仍能探索量子優勢。

---

**延伸閱讀**

- [Hybrid Quantum-Classical 論文](https://www.google.com/search?q=hybrid+quantum+classical+neural+network)
- [Quantum Circuit Learning](https://www.google.com/search?q=quantum+circuit+learning+mitsuda+2016)
- [PennyLane 混合訓練](https://www.google.com/search?q=PennyLane+hybrid+quantum+classical+training)
