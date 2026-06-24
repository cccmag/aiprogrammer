# 對比學習的原理

對比學習是自監督學習的重要方法。

## 1. 基本思想

相似的樣本應該有相似的表示，不相似的樣本應該有差異化的表示。

## 2. Contrastive Loss

```python
def contrastive_loss(z_i, z_j, temperature=0.5):
    similarity = torch.matmul(z_i, z_j.T) / temperature
    labels = torch.arange(len(z_i))
    loss = F.cross_entropy(similarity, labels)
    return loss
```

## 3. 代表方法

- SimCLR：簡單的對比框架
- MoCo：動態負樣本
- CLIP：文字-圖像對比

---

## 延伸閱讀

- [SimCLR 論文](https://www.google.com/search?q=SimCLR+a+simple+framework+contrastive+learning)
- [對比學習綜述](https://www.google.com/search?q=contrastive+learning+self-supervised+survey)