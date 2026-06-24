# 注意力機制的起源

## 從認知科學到神經網路

注意力（Attention）是我們認知系統的核心功能。當我們觀察世界時，大腦不會平等地處理所有資訊，而是動態地選擇性地聚焦於重要的部分。這種能力被稱為「注意力機制」。

本章將回顧注意力從認知科學概念到深度學習核心元件的演化歷程。

---

## 人類視覺注意力

### 選擇性注意力

人類視覺系統每時每刻都接收到大量的視覺資訊，但我們的意識只能處理其中一小部分：

```
┌─────────────────────────────────────────────────────┐
│              人類視覺注意力                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│   視野中的場景：                                     │
│                                                     │
│      樹        房子        汽車                     │
│       \        / \        /                        │
│        \      /   \      /                         │
│         \    /     \    /                          │
│          \  /       \  /                           │
│           聚焦       聚焦                          │
│                                                     │
│   只有聚焦區域的細節被完整處理                       │
│   其他區域使用周邊視覺的低解析度資訊                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 注意力在認知中的作用

心理學研究表明，注意力有幾個關鍵功能：

1. **篩選**：過濾不相關的資訊
2. **集中**：將認知資源分配到重要資訊
3. **切換**：在不同資訊來源之間移動

### 雞尾酒會效應

一個著名的注意力實驗：

> 在嘈雜的雞尾酒會上，你能夠專注於與某人的對話，即使周圍有很多人在說話。當有人叫你的名字時，你會立即注意到。

這種「選擇性聽覺」正是注意力機制的體現。

---

## 早期神經網路中的注意力

### 1980s-2000s：萌芽期

早期的類神經網路研究幾乎沒有明確的注意力機制。傳統的模式識別方法（如 MLP、SVM）將輸入視為一個固定的向量，沒有動態選擇的能力。

### 2000s：視覺注意力的計算模型

研究開始嘗試在視覺任務中引入注意力：

**1. 瞄準線模型（Fovea Model）**
```
輸入圖像 → 選擇區域 → 高解析處理 → 選擇下一區域 → ...
```

這種串列處理方式模擬了人類眼睛的瞄準動作，但計算效率很低。

**2. 空間 Transformer Networks（2015）**
這是早期將注意力思想融入深度學習的成功嘗試：

```python
# 空間轉換器網路
class SpatialTransformer(nn.Module):
    def __init__(self):
        self.localization = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=7),
            nn.MaxPool2d(2, stride=2),
            nn.ReLU(),
            nn.Conv2d(8, 10, kernel_size=5),
            nn.MaxPool2d(2, stride=2),
        )
        self.fc = nn.Linear(10 * 3 * 3, 6)

    def forward(self, x):
        xs = self.localization(x)
        xs = xs.view(-1, 10 * 3 * 3)
        theta = self.fc(xs)
        theta = theta.view(-1, 2, 3)

        grid = F.affine_grid(theta, x.size())
        x = F.grid_sample(x, grid)

        return x
```

---

## RNN 中的注意力：早期嘗試

### 解決 RNN 的記憶瓶頸

在注意力機制出現之前，RNN 面臨嚴重的長期記憶問題：

```
問題：
- 所有輸入資訊必須壓縮到固定維度的隱藏狀態
- 長期依賴難以學習
- 梯度消失問題
```

### 鍵值記憶網路

2014-2015 年，出現了鍵值記憶網路（Key-Value Memory Networks）：

```
┌─────────────────────────────────────────────────────┐
│              鍵值記憶網路                            │
├─────────────────────────────────────────────────────┤
│                                                     │
│   查詢 q ──► 計算注意力 ──► 讀取記憶               │
│                  │                                  │
│         ┌────────┴────────┐                        │
│         ▼                 ▼                        │
│    鍵記憶 K           值記憶 V                     │
│         │                 │                        │
│         └────────┬────────┘                        │
│                  ▼                                  │
│            加權輸出                                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

這是注意力機制的直接前身。

---

## 注意力機制的數學描述

### 通用注意力函式

注意力機制可以抽象為一個函式：

```python
def attention(query, keys, values):
    """
    注意力機制的通用形式

    Args:
        query: 查詢向量 [d_k]
        keys: 鍵向量矩陣 [n, d_k]
        values: 值向量矩陣 [n, d_v]

    Returns:
        加權輸出 [d_v]
    """
    # 1. 計算查詢與每個鍵的相似度
    scores = torch.matmul(query, keys.T)  # [n]

    # 2. 標準化為機率分佈
    weights = F.softmax(scores, dim=-1)  # [n]

    # 3. 用權重加權求和值
    output = torch.matmul(weights, values)  # [d_v]

    return output
```

### 注意力機制的種類

| 類型 | 公式 | 特點 |
|------|------|------|
| 加性注意力 | `score = v^T * tanh(W*q + U*k)` | 通用性強 |
| 點積注意力 | `score = q^T * k` | 計算簡單 |
| 縮放點積 | `score = (q^T * k) / sqrt(d)` | 數值穩定 |
| 雙線性注意力 | `score = q^T * W * k` | 可學習的相似度 |

---

## 視覺注意力在 CNN 中的應用

### CNN 的注意力改進

研究者將注意力機制引入 CNN，產生了多個重要的變體：

**1. Squeeze-and-Excitation (SE) 網路**

```python
class SEBlock(nn.Module):
    def __init__(self, channels, reduction=16):
        super().__init__()
        self.squeeze = nn.AdaptiveAvgPool2d(1)
        self.excitation = nn.Sequential(
            nn.Linear(channels, channels // reduction),
            nn.ReLU(),
            nn.Linear(channels // reduction, channels),
            nn.Sigmoid()
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.squeeze(x).view(b, c)
        y = self.excitation(y).view(b, c, 1, 1)
        return x * y.expand_as(x)
```

**2. CBAM（Convolutional Block Attention Module）**

結合了通道注意力和空間注意力。

**3. Non-Local Neural Networks**

將自注意力引入 CNN，用於影片分類等任務。

---

## 注意力機制的認知科學意義

### 資源分配理論

注意力機制體現了認知資源分配的優化原則：

```
認知資源是有限的
↓
必須選擇性地分配到最重要的資訊上
↓
動態調整，適應環境變化
```

### 稀疏性原則

神經元通常只對特定模式響應，這本身就是一種「硬注意力」。

### 組合結構

人類的認知系統能夠將注意力聚焦到物體的某個部分，同時保持對整體結構的感知。

---

## 總結

注意力機制的發展是認知科學與人工智慧交叉的成功案例：

1. **認知科學提供了直覺和理論基礎**：人類視覺注意力的研究給了我們啟發
2. **計算模型逐步成熟**：從鍵值記憶到通用注意力函式
3. **與深度學習結合**：催生了革命性的 Transformer 架構

下一章，我們將看到注意力如何解決 seq2seq 模型的瓶頸問題。

---

## 延伸閱讀

- [Human attention cognitive science](https://www.google.com/search?q=human+attention+cognitive+science)
- [Neural attention mechanism](https://www.google.com/search?q=neural+attention+mechanism+deep+learning)
- [Key+Value+Memory+Networks](https://www.google.com/search?q=key+value+memory+networks)

---

*本篇文章為「AI 程式人雜誌 2019 年 8 月號」注意力機制系列之一。*