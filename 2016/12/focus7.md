# 主題七：AI 和深度學習

## 2016 年：AI 突破元年

2016 年是人工智慧發展史上具有里程碑意義的一年。AlphaGo 的勝利、深度學習框架的繁榮，以及 AI 在各領域的應用突破，共同開啟了 AI 發展的新時代。

### 重要里程碑

```python
ai_2016_highlights = {
    'AlphaGo': '擊敗世界冠軍李世乭',
    'TensorFlow': '1.0 版本發布',
    'GAN': '生成對抗網路受到廣泛關注',
    'Deep RL': '強化學習取得突破',
    'ML Frameworks': 'Caffe2、PyTorch 相繼開源',
}
```

## AlphaGo 與深度強化學習

### AlphaGo 的技術架構

```
AlphaGo 系統架構：

┌─────────────────────────────────────────┐
│              AlphaGo                     │
├─────────────────────────────────────────┤
│                                          │
│  策略網路 (Policy Network)               │
│    - 預測下一步棋                        │
│    - 減少搜尋寬度                        │
│                                          │
│  價值網路 (Value Network)                │
│    - 評估局面勝率                        │
│    - 減少搜尋深度                        │
│                                          │
│  Monte Carlo Tree Search (MCTS)          │
│    - 結合策略和價值網路                  │
│    - 模擬大量對局                        │
│                                          │
└─────────────────────────────────────────┘
```

### 深度強化學習原理

```python
deep_rl_concepts = {
    'Policy Gradient': '直接學習策略函式',
    'Q-Learning': '學習狀態-動作值函式',
    'Actor-Critic': '結合策略和價值函式',
    'DDPG': '連續動作空間的深度強化學習',
    'A3C': '非同步優勢 Actor-Critic',
}
```

## 深度學習框架生態

### TensorFlow

```python
import tensorflow as tf

class SimpleNN(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.dense1 = tf.keras.layers.Dense(64, activation='relu')
        self.dense2 = tf.keras.layers.Dense(10, activation='softmax')

    def call(self, x):
        x = self.dense1(x)
        return self.dense2(x)

# 訓練
model = SimpleNN()
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
model.fit(train_data, epochs=10)
```

### PyTorch

```python
import torch
import torch.nn as nn

class SimpleNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = x.view(-1, 784)
        x = self.relu(self.fc1(x))
        return self.fc2(x)

model = SimpleNN()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters())

for epoch in range(10):
    for data, target in dataloader:
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
```

### Caffe2

```python
# Caffe2 範例
from caffe2.python import workspace, model_helper

def create_model():
    model = model_helper.ModelHelper(name="my_model")
    fc1 = model.FC("input", "fc1", dim_in=784, dim_out=128)
    relu = model.Relu(fc1, "relu1")
    fc2 = model.FC(relu, "fc2", dim_in=128, dim_out=10)
    return model
```

## 經典模型架構

### CNN (卷積神經網路)

```python
cnn_architecture = """
典型 CNN 架構：

1. 卷積層 (Conv)
   - 提取局部特徵
   - 使用濾波器掃描輸入

2. 池化層 (Pooling)
   - 降維
   - 增加對平移的魯棒性

3. 全連接層 (FC)
   - 整合特徵
   - 輸出分類或預測
"""
```

### RNN 和 LSTM

```python
rnn_structure = """
RNN 的問題：長期依賴

解決方案：LSTM (Long Short-Term Memory)

LSTM 門：
- 輸入門：控制新資訊進入
- 遺忘門：控制舊資訊丟失
- 輸出門：控制輸出什麼
"""
```

## 自然語言處理

### Word Embeddings

```python
word_embeddings = {
    'Word2Vec': '預測詞周圍的詞',
    'GloVe': '基於共現矩陣',
    'FastText': '考虑子詞資訊',
}
```

### Sequence-to-Seq

```python
seq2seq_concept = """
Sequence-to-Sequence 模型：

輸入序列 → 編碼器 → 上下文向量 → 解碼器 → 輸出序列

應用：
- 機器翻譯
- 文字摘要
- 對話系統
"""
```

## 電腦視覺

### 物體檢測

```python
detection_models = {
    'R-CNN': '區域提案 + CNN 分類',
    'Fast R-CNN': '共享特徵圖',
    'Faster R-CNN': '端到端訓練',
    'YOLO': '單階段檢測，更快',
    'SSD': '多尺度特徵圖',
}
```

### 語義分割

```python
segmentation_models = {
    'FCN': '全卷積網路',
    'U-Net': '編碼器-解碼器架構',
    'DeepLab': '空洞卷積 + CRF',
}
```

## 生成模型

### GAN (生成對抗網路)

```python
gan_concept = """
GAN 架構：

┌────────────────────────────────────────┐
│              Generator                  │
│   生成假樣本，試圖欺騙判別器           │
└────────────────┬───────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────┐
│            Discriminator               │
│   判斷樣本是真實還是假的               │
└────────────────────────────────────────┘

對抗訓練：Generator 和 Discriminator 交替優化
"""
```

### VAE (變分自編碼器)

```python
vae_concept = """
VAE 原理：

編碼器 → 潛在空間分佈 → 解碼器

損失函式：
- 重構損失：輸出接近輸入
- KL 散度：潛在分佈接近先驗
"""
```

## 遷移學習

```python
transfer_learning = """
遷移學習的步驟：

1. 在大型資料集（如 ImageNet）上預訓練模型
2. 凍住淺層權重
3. 只訓練最後幾層
4. 可選：微調整個網路

好處：
- 减少訓練資料需求
- 加速收斂
- 提高效能
"""
```

## 深度學習的挑戰

```python
challenges = {
    '計算資源': '需要 GPU/TPU 加速',
    '資料需求': '大型標註資料集',
    '可解釋性': '模型决策難以解釋',
    '超參數': '需要大量調參',
    '過擬合': '訓練資料不足時容易過擬合',
}
```

## 小結

2016 年是深度學習爆發的一年。從 AlphaGo 的歷史性勝利到各大框架的開源，AI 正在以前所未有的速度發展。TensorFlow、PyTorch、Caffe2 等框架的繁榮降低了深度學習的進入門檻，讓更多研究者、開發者能夠參與到 AI 的發展中來。

---

**延伸閱讀**

- [Deep Learning Textbook](https://www.google.com/search?q=deep+learning+textbook+goodfellow)
- [TensorFlow Tutorials](https://www.google.com/search?q=TensorFlow+tutorials)
- [AlphaGo Paper](https://www.google.com/search?q=AlphaGo+Nature+paper+2016)