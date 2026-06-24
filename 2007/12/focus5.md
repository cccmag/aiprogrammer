# AI 與機器學習：深度學習的前夜

## 2007 年的 AI 現狀

### 傳統機器學習的主流

```python
# 2007 年主流的機器學習方法
ml_methods_2007 = {
    'SVM': '支援向量機，仍是主流',
    'Random Forest': '集成學習的好選擇',
    'Naive Bayes': '文字分類首選',
    'Decision Trees': '可解釋性強',
    'k-NN': '簡單有效'
};

# scikit-learn 在 2007 年的狀態
# scikit-learn 還在早期開發中（2007 年）
# 但預示了 Python 在 ML 領域的未來
```

### 深度學習的萌芽

```python
# 深度學習的早期信號
deep_learning_2007 = {
    'Geoffrey Hinton': '深度信念網路論文（2006）',
    'Yoshua Bengio': '深度學習理論研究',
    'Yann LeCun': '卷積神經網路持續改進',
    'GPU 計算': 'CUDA 允許更快訓練'
};

# 為什麼深度學習還沒爆發
# - 資料量不夠
# - 計算能力有限
# - 訓練不穩定
# - 理論理解不足
```

## 重要研究

### 深度信念網路（2006）

```python
# 深度信念網路的概念
# Hinton, Osindero, Teh (2006)
# "A fast learning algorithm for deep belief nets"

# 貪心層級預訓練
# 1. 訓練第一層 RBM
# 2. 固定第一層，訓練第二層
# 3. 重複直到完成
# 4. 最後用監督學習 fine-tune

def pretrain_dbn(layers, data):
    """貪心層級預訓練"""
    hidden = data
    for i, layer_size in enumerate(layers):
        rbm = RestrictedBoltzmannMachine(
            n_visible=hidden.shape[1],
            n_hidden=layer_size
        )
        hidden = rbm.train(hidden)
    return hidden
```

## 其他 AI 進展

### 電腦視覺

```python
# 2007 年電腦視覺進展
vision_2007 = {
    'ImageNet': 'Fei-Fei Li 開始建構（2007）',
    'PASCAL VOC': '視覺辨識競賽持續',
    'SIFT': '尺度不變特徵轉換成熟',
    'Face Detection': 'Viola-Jones 算法應用'
};
```

### 自然語言處理

```python
# NLP 2007
nlp_2007 = {
    '統計機器翻譯': 'IBM 模型仍是主流',
    '文字分類': 'TF-IDF + SVM 仍是標準',
    '問答系統': 'IBM Watson 開發中',
    '語音辨識': 'HTK 持續使用'
};
```

## 結語

2007 年是 AI 的過渡期——傳統方法仍然主流，但深度學習的基礎正在奠定。

2008 年將是更多準備的一年，而真正的突破將在 2012 年到來。

---

## 延伸閱讀

- [AI+machine+learning+2007+review](https://www.google.com/search?q=AI+machine+learning+2007+review)

---