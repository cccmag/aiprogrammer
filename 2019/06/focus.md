# 本期焦點

## PyTorch 實戰：從張量到神經網路

### 引言

PyTorch 是 Facebook AI Research 開發的深度學習框架，以其動態計算圖和直覺的 Python 風格而聞名。自 2016 年開源以來，PyTorch 已在學術界和產業界獲得廣泛採用。

本期將帶領讀者從 PyTorch 基礎開始，深入了解張量運算、自動微分、神經網路建構和訓練流程，最終掌握使用 PyTorch 開發深度學習模型的核心技能。

---

## 大綱

* [程式：PyTorch 基礎操作實作](focus_code.md)
   - 張量創建和操作
   - 自動微分範例
   - 簡單神經網路實作

1. [PyTorch 介紹](focus1.md) -- 動態計算圖與設計哲學

2. [張量運算](focus2.md) -- 張量創建、操作、變換

3. [自動微分](focus3.md) -- autograd 機制詳解

4. [神經網路建構](focus4.md) -- nn.Module 與層

5. [資料處理](focus5.md) -- Dataset、DataLoader、transforms

6. [訓練流程](focus6.md) -- 前饋、損失、優化、迭代

7. [模型存取與部署](focus7.md) -- 保存、載入、 TorchScript

---

## 濃縮回顧

### PyTorch vs TensorFlow

| 特性 | PyTorch | TensorFlow |
|-----|---------|-----------|
| 計算圖 | 動態（即時定義） | 靜態（先定義後執行） |
| API 風格 | Python 原生 | 有點像 Keras |
| 除錯 | 直接用 Python 除錯 | 需要 tf debugger |
| 部署 | TorchScript | SavedModel |
| 社群 | 學術界較強 | 產業界較強 |

### 核心概念

```python
# PyTorch 核心流程
import torch

# 1. 張量：資料表示
x = torch.tensor([1.0, 2.0, 3.0])

# 2. 自動微分：梯度計算
x.requires_grad = True
y = x ** 2
y.backward()

# 3. 神經網路：模型定義
model = torch.nn.Linear(10, 1)

# 4. 優化器：參數更新
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
```

### PyTorch 1.x 重要特性

| 版本 | 主要功能 |
|-----|---------|
| 1.0 | TorchScript、Mobile、量化支援 |
| 1.1 | JIT 改進、TensorBoard 原生支援 |

### 本期重點

1. **張量是 PyTorch 的基礎** — 理解張量運算等於掌握一半 PyTorch
2. **動態計算圖是 PyTorch 的核心優勢** — 直覺的 debugging 和實驗
3. **nn.Module 是模型定義的標準方式** — 清晰的結構和复用性
4. **PyTorch 生态系统完善** — 從研究到部署都有良好支持

---

## 延伸閱讀

- [PyTorch 官方網站](https://pytorch.org/)
- [PyTorch 官方教程](https://pytorch.org/tutorials/)
- [PyTorch 官方文檔](https://pytorch.org/docs/)

---

*本期焦點到此結束。感謝閱讀 2019 年 AI 程式人雜誌。*