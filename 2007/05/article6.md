# 類神經網路的早期復興：深度學習的前夜

## 前言

2006 年，Hinton 發表了深度信念網路（DBN）的論文，開啟了深度學習的復興。

## 早期深度學習概念

```python
# 深度信念網路的簡化概念
# 使用貪心層級預訓練

def pretrain_layer(rbm, data, layers):
    hidden = data
    for layer in layers:
        rbm = RestrictedBoltzmannMachine(
            n_visible=hidden.shape[1],
            n_hidden=layer
        )
        # 對比散度訓練
        hidden = rbm.train(hidden)
    return hidden
```

## 結語

2007 年的研究為 2012 年 AlexNet 的成功奠定了基礎。

---

## 延伸閱讀

- [deep+belief+networks+Hinton+2006](https://www.google.com/search?q=deep+belief+networks+Hinton+2006)

---