# LSTM 與 GRU 序列建模

## 長期依賴的挑戰

RNN 的梯度消失問題使其難以學習長期依賴。舉例來說，句子「我小時候住在台灣，雖然後來搬到美國，但我仍然會說_____」——預測「中文」需要追溯到句子開頭的資訊。

## LSTM：長短期記憶

LSTM（Long Short-Term Memory）由 Hochreiter 和 Schmidhuber 在 1997 年提出，透過**門控機制**解決了梯度消失問題：

```
輸入門：i_t = sigmoid(W_i @ [h_{t-1}, x_t] + b_i)
遺忘門：f_t = sigmoid(W_f @ [h_{t-1}, x_t] + b_f)
輸出門：o_t = sigmoid(W_o @ [h_{t-1}, x_t] + b_o)
候選記憶：c~_t = tanh(W_c @ [h_{t-1}, x_t] + b_c)
細胞狀態：c_t = f_t * c_{t-1} + i_t * c~_t
隱藏狀態：h_t = o_t * tanh(c_t)
```

**核心創新**：細胞狀態 `c_t` 是資訊的高速公路——遺忘門決定丟棄哪些舊資訊，輸入門決定添加哪些新資訊。梯度可以透過細胞狀態的加法結構順暢傳播。

## GRU：簡化版本

GRU（Gated Recurrent Unit）由 Cho 在 2014 年提出，是 LSTM 的簡化變體：

```
重置門：r_t = sigmoid(W_r @ [h_{t-1}, x_t])
更新門：z_t = sigmoid(W_z @ [h_{t-1}, x_t])
候選狀態：h~_t = tanh(W_h @ [r_t * h_{t-1}, x_t])
隱藏狀態：h_t = (1 - z_t) * h_{t-1} + z_t * h~_t
```

GRU 將 LSTM 的三個門（輸入、遺忘、輸出）簡化為兩個（重置、更新），參數更少，計算更快。

## LSTM vs GRU

| 特性 | LSTM | GRU |
|------|------|-----|
| 門控數量 | 3（輸入、遺忘、輸出） | 2（重置、更新） |
| 細胞狀態 | 有獨立記憶單元 | 無（隱藏狀態即記憶） |
| 參數量 | 較多 | 較少（約少 25%） |
| 過擬合風險 | 較高 | 較低 |
| 長序列表現 | 優秀 | 相近 |
| 訓練速度 | 較慢 | 較快 |

## 序列建模實戰

```python
class LSTMCell:
    def forward(self, x, h_prev, c_prev):
        combined = np.concatenate([h_prev, x])
        f = sigmoid(W_f @ combined + b_f)   # 遺忘門
        i = sigmoid(W_i @ combined + b_i)   # 輸入門
        o = sigmoid(W_o @ combined + b_o)   # 輸出門
        c_candidate = tanh(W_c @ combined + b_c)
        c = f * c_prev + i * c_candidate
        h = o * tanh(c)
        return h, c
```

## 在語言模型中的應用

LSTM 語言模型在 2015-2017 年間是 NLP 的標準工具，在機器翻譯、文本生成和語音識別等任務上取得了當時最佳結果。直到 Transformer 的出現，LSTM 才逐步被取代，但它在序列建模中的地位仍然不可忽視。

---

**下一步**：[Seq2Seq 與注意力機制](focus5.md)

## 延伸閱讀

- [LSTM 原始論文](https://www.google.com/search?q=Long+Short-Term+Memory+Hochreiter)
- [GRU 論文](https://www.google.com/search?q=GRU+gated+recurrent+unit+Cho)
- [LSTM 視覺化解釋](https://www.google.com/search?q=understanding+LSTM+networks+colah)
