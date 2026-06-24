# PyTorch 起源與發展（2016-2018）

## 從 Torch 到 PyTorch

### 前言

PyTorch 的前身 Torch 是一個基於 Lua 語言的機器學習庫，由 Ronan Collobert、Sergey Karochkintsev 等人開發。Facebook AI Research 在 2016 年推出了 Python 版本——PyTorch。

### 歷史沿革

| 年份 | 事件 |
|------|------|
| 2002 | Torch 發布 |
| 2011 | Twitter 採用 Torch |
| 2016 | PyTorch 開源（Facebook AI Research） |
| 2017 | PyTorch 0.2 發布，支援分散式訓練 |
| 2018 | PyTorch 1.0 預覽版發布 |

### PyTorch 的設計目標

1. **Python 優先** — 完全融入 Python 生態
2. **動態計算** — 與 Python 程式碼無縫整合
3. **研究導向** — 快速實驗和原型開發
4. **高效能** — 底層最佳化確保執行效率

### 與 NumPy 的無縫整合

```python
import torch
import numpy as np

# NumPy 陣列直接轉換
np_array = np.random.randn(3, 4)
torch_tensor = torch.from_numpy(np_array)

# 反向轉換
np_array_back = torch_tensor.numpy()

# 兩者 API 設計相似
torch.sum(torch_tensor)  # 等價於 np.sum(np_array)
torch.mean(torch_tensor, dim=1)  # 等價於 np.mean(np_array, axis=1)
```

### 核心元件

| 元件 | 用途 |
|------|------|
| torch.Tensor | 張量運算 |
| torch.autograd | 自動微分 |
| torch.nn | 神經網路模組 |
| torch.optim | 優化器 |
| torch.utils.data | 資料處理 |

### 社群人數成長

2018 年中，PyTorch 在 GitHub 上的星標數已超過 20,000，成為最受歡迎的深度學習框架之一。

### 小結

PyTorch 的成功在於「為研究人員設計」的理念。動態計算圖、Python 優先、和直覺的 API，讓它迅速成為學術界的首選工具。

---

**下一步**：[動態計算圖 vs 靜態計算圖](focus2.md)

## 延伸閱讀

- [PyTorch Official Website](https://www.google.com/search?q=PyTorch+official+tutorial+2018)
- [Torch History](https://www.google.com/search?q=Torch+deep+learning+history+lua)