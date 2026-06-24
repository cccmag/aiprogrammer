# RNN 語言模型

## 從固定視窗到循環

n-gram 和 NNLM 都使用固定大小的上下文視窗。但自然語言的本質是**無限的上下文依賴**——一個句子的開頭可能影響結尾的詞選擇。

循環神經網路（RNN）透過遞迴結構解決了這個問題：

```python
# RNN 的核心：隱藏狀態在時間步之間傳遞
h_t = tanh(Wxh @ x_t + Whh @ h_{t-1} + bh)
y_t = softmax(Why @ h_t + by)
```

隱藏狀態 `h_t` 可以視為「截至目前所有已見詞的摘要」。

## 機率建模

RNN 語言模型將序列的聯合機率分解為條件機率的乘積：

```
P(w_1, w_2, ..., w_n) = P(w_1) * P(w_2|w_1) * ... * P(w_n|w_1...w_{n-1})
```

每一步的條件機率由 RNN 的輸出層透過 softmax 給出：

```python
# 訓練目標：最大化正確下一個詞的對數機率
loss = -sum(log P(w_{t+1} | w_1...w_t))
```

## BPTT 訓練

RNN 的訓練使用 BPTT（Backpropagation Through Time），將循環結構展開為深層前饋網路：

```python
def train_rnn(inputs, targets, h_prev, lr=0.01):
    # 前向：計算所有時間步的隱藏狀態和輸出
    hs, ps = forward(inputs, h_prev)
    
    # 反向：從最後一個時間步向後傳播梯度
    dh_next = zeros
    for t in reversed(range(len(inputs))):
        dy = ps[t] - one_hot(targets[t])  # softmax 梯度
        dWhy += dy @ hs[t].T
        dh = Why.T @ dy + dh_next
        dtanh = (1 - hs[t]**2) * dh      # tanh 梯度
        dWxh += dtanh @ xs[t].T
        dWhh += dtanh @ hs[t-1].T
        dh_next = Whh.T @ dtanh
    
    # 更新權重
    Wxh -= lr * dWxh
    Whh -= lr * dWhh
    Why -= lr * dWhy
```

## 梯度消失與爆炸

RNN 的訓練面臨兩個核心挑戰：

**梯度消失**：當序列很長時，梯度在反向傳播中指數級衰減，導致模型無法學習長期依賴。詞與詞之間的距離越遠，模型越難捕捉它們的關聯。

**梯度爆炸**：梯度指數級增長，導致參數更新過大，訓練不穩定。解決方案是**梯度裁剪**（gradient clipping）：

```python
def clip_gradients(grads, max_norm=5.0):
    norm = sqrt(sum(g^2 for g in grads))
    if norm > max_norm:
        grads = [g * max_norm / norm for g in grads]
```

## 生成文本

訓練完成後的 RNN 語言模型可以用來生成新文本：

```python
def generate(model, seed, length=50):
    h = zeros
    for t in range(length):
        p = model.forward(seed[t-1], h)
        next_word = sample(p)      # 從機率分布中抽樣
        yield next_word
```

## 小結

RNN 語言模型是神經語言模型的重要里程碑。它解決了固定上下文視窗的限制，但也暴露了梯度消失等問題。這些問題促進了 LSTM 和 GRU 的發展。

---

**下一步**：[LSTM 與 GRU 序列建模](focus4.md)

## 延伸閱讀

- [RNN 語言模型教學](https://www.google.com/search?q=recurrent+neural+network+language+model+tutorial)
- [The Unreasonable Effectiveness of RNNs](https://www.google.com/search?q=unreasonable+effectiveness+of+recurrent+neural+networks)
- [BPTT 詳解](https://www.google.com/search?q=backpropagation+through+time+explained)
