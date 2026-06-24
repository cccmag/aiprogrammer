# 焦點文章 5：GRU：閘門循環單元

## 前言

GRU（Gated Recurrent Unit）是另一種解決長期依賴問題的 RNN 變體。相比 LSTM，GRU 更簡潔，但同樣有效。

## GRU 的簡化設計

GRU 只有兩個門：
- **更新門（Update Gate）**：取代 LSTM 的輸入門與遺忘門
- **重置門（Reset Gate）**：控制如何結合新輸入與過去記憶

## GRU 公式

```
z_t = σ(W_z · [h_{t-1}, x_t])              # 更新門
r_t = σ(W_r · [h_{t-1}, x_t])              # 重置門
h̃_t = tanh(W · [r_t × h_{t-1}, x_t])       # 候選隱藏狀態
h_t = (1 - z_t) × h_{t-1} + z_t × h̃_t       # 新隱藏狀態
```

## Python 實現

```python
class GRUCell:
    def __init__(self, input_size, hidden_size):
        self.hidden_size = hidden_size

        # 權重矩陣
        self.Wz = np.random.randn(hidden_size, input_size + hidden_size) * 0.1
        self.Wr = np.random.randn(hidden_size, input_size + hidden_size) * 0.1
        self.Wh = np.random.randn(hidden_size, input_size + hidden_size) * 0.1

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def forward(self, x_t, h_prev):
        self.x_t = x_t
        self.h_prev = h_prev

        concat = np.vstack((h_prev, x_t))

        # 更新門
        self.z_t = self.sigmoid(np.dot(self.Wz, concat))

        # 重置門
        self.r_t = self.sigmoid(np.dot(self.Wr, concat))

        # 候選隱藏狀態
        concat_r = np.vstack((self.r_t * h_prev, x_t))
        self.h̃_t = np.tanh(np.dot(self.Wh, concat_r))

        # 新隱藏狀態
        self.h_t = (1 - self.z_t) * h_prev + self.z_t * self.h̃_t

        return self.h_t
```

## LSTM vs GRU

| 特性 | LSTM | GRU |
|------|------|-----|
| 門數量 | 3 個（輸入、遺忘、輸出） | 2 個（更新、重置） |
| 記憶機制 | 記憶細胞 + 隱藏狀態 | 只有隱藏狀態 |
| 參數數量 | 較多 | 較少 |
| 計算成本 | 較高 | 較低 |

## 何時使用哪個

### 選擇 LSTM 的情況
- 資料集較大
- 需要更靈活的記憶控制
- 訓練資料充足

### 選擇 GRU 的情況
- 資料集較小
- 訓練速度重要
- 資源有限

## GRU 的記憶機制

更新門 z_t 控制過去資訊的保留程度：

- z_t 接近 1：傾向保留過去（輸入被忽略）
- z_t 接近 0：傾向接受新輸入（過去被忽略）

這種設計使網路能夠動態調整記憶策略。

## 實驗結果

多項研究表明，GRU 在多個任務上與 LSTM 性能相當：

- 語音辨識
- 機器翻譯
- 文字生成

但 GRU 訓練更快、參數更少。

## 總結

GRU 是 LSTM 的簡化版本，在保持性能的同時减少了參數數量與計算成本。兩者都是處理序列資料的有效工具。

## 延伸閱讀

- https://www.google.com/search?q=GRU+gated+recurrent+unit+explained
- https://www.google.com/search?q=LSTM+vs+GRU+comparison