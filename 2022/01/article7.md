# 循環神經網路 RNN

## 序列資料的挑戰

許多重要資料是序列形式的：文字、語音、時間序列、影片。MLP 和 CNN 無法有效處理序列資料，因為：
- 輸入長度可變
- 元素之間有順序依賴關係
- 需要長期記憶

## RNN 的核心思想

循環神經網路（Recurrent Neural Network, RNN）通過在時間步之間共享權重來處理序列資料。

```
    輸出：y_1       y_2       y_3       y_4
           ↑         ↑         ↑         ↑
隱藏狀態：h_0 → h_1 → h_2 → h_3 → h_4 → ...
           ↑         ↑         ↑         ↑
    輸入：x_1       x_2       x_3       x_4
```

### 數學表示

```
h_t = tanh(W_hh · h_(t-1) + W_xh · x_t + b_h)
y_t = W_hy · h_t + b_y
```

其中 W_hh 是循環權重，在不同時間步之間共享。

### PyTorch 實作

```python
import torch.nn as nn

rnn = nn.RNN(
    input_size=100,   # 輸入維度（如詞嵌入維度）
    hidden_size=256,  # 隱藏狀態維度
    num_layers=2,     # 疊加層數
    batch_first=True
)

# 輸入形狀：(batch, seq_len, input_size)
x = torch.randn(32, 10, 100)
output, h_n = rnn(x)
# output: (32, 10, 256) — 每個時間步的輸出
# h_n: (2, 32, 256) — 最後時間步的隱藏狀態
```

## 梯度問題

### 梯度消失與爆炸

RNN 的梯度需要沿時間方向傳播，經過多個時間步後：

```
∂L/∂W = Σ_t (∂L/∂h_t · ∂h_t/∂h_(t-1) · ... · ∂h_2/∂h_1 · ∂h_1/∂W)
```

如果時間步很長，這個連乘積會趨近於零（消失）或發散（爆炸）。

```
梯度連乘：
∂h_t/∂h_(t-1) = tanh'(W_hh · h_(t-1) + ... ) · W_hh

tanh' 最大為 1，但 W_hh 可能大於或小於 1：
- 如果 ||W_hh|| < 1，長期梯度消失
- 如果 ||W_hh|| > 1，長期梯度爆炸
```

## LSTM（長短期記憶）

LSTM 通過門控機制解決梯度問題：

```python
lstm = nn.LSTM(input_size=100, hidden_size=256, num_layers=2)
```

### LSTM 的內部結構

```
遺忘門：f_t = σ(W_f · [h_(t-1), x_t] + b_f)
輸入門：i_t = σ(W_i · [h_(t-1), x_t] + b_i)
候選：  C̃_t = tanh(W_c · [h_(t-1), x_t] + b_c)
細胞狀態：C_t = f_t ⊙ C_(t-1) + i_t ⊙ C̃_t
輸出門：o_t = σ(W_o · [h_(t-1), x_t] + b_o)
隱藏狀態：h_t = o_t ⊙ tanh(C_t)
```

關鍵創新：細胞狀態 C_t 的梯度可以直接流過（f_t 接近 1 時），避免梯度消失。

## GRU（門控循環單元）

GRU 是 LSTM 的精簡版本：

```
重置門：r_t = σ(W_r · [h_(t-1), x_t] + b_r)
更新門：z_t = σ(W_z · [h_(t-1), x_t] + b_z)
候選：  h̃_t = tanh(W_h · [r_t ⊙ h_(t-1), x_t] + b_h)
輸出：  h_t = (1 - z_t) ⊙ h_(t-1) + z_t ⊙ h̃_t
```

GRU 參數更少，計算更快，在許多任務上與 LSTM 表現相當。

## RNN 的應用

### 語言模型

```python
class LanguageModel(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)
    
    def forward(self, x):
        x = self.embedding(x)
        x, _ = self.lstm(x)
        x = self.fc(x)
        return x
```

### 機器翻譯（Seq2Seq）

```
編碼器：讀取來源語言句子，產生上下文向量
解碼器：根據上下文向量，逐步生成目標語言句子

編碼器：
    我  愛  AI  <EOS>
    ↓    ↓   ↓   ↓
   h_1 → h_2 → h_3 → h_4 （上下文向量）

解碼器：
   h_4 → h_5 → h_6 → h_7 → ...
          ↓    ↓    ↓
        I   love  AI  <EOS>
```

## Transformer 的衝擊

2017 年後，Transformer 在序列建模任務上全面超越 RNN：

- RNN：順序計算，無法平行化
- Transformer：並行計算，訓練速度快數倍

但 RNN 在以下場景仍有優勢：
- 低資源裝置（參數較少）
- 即時串流處理
- 可解釋的時間動態建模

---

## 延伸閱讀

- [RNN 教學](https://www.google.com/search?q=recurrent+neural+network+tutorial)
- [LSTM 論文 1997](https://www.google.com/search?q=Long+short-term+memory+Hochreiter+Schmidhuber)
- [GRU 論文 2014](https://www.google.com/search?q=Gated+recurrent+unit+Cho+2014)

*本篇文章為「AI 程式人雜誌 2022 年 1 月號」精選文章。*
