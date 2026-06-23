# 模型逆向工程與提取攻擊

## 1. 引言

模型提取攻擊（Model Extraction Attack）的目的是竊取或重建目標模型的內部參數、架構或訓練資料。這類攻擊威脅到模型所有者的智慧財產權和使用者資料的隱私。

## 2. 攻擊類型

### 功能提取（Functional Extraction）

攻擊者透過大量 API 查詢來訓練一個功能等價的替代模型。這是最常見也最易實施的提取攻擊。

```python
def extract_model(target_api, num_queries=100000):
    """透過反覆查詢 API，收集 (input, output) 訓練替代模型"""
    queries, responses = [], []
    for _ in range(num_queries):
        query = generate_random_prompt()
        responses.append(target_api.chat(query))
        queries.append(query)
    surrogate = MLPClassifier()
    surrogate.fit(vectorize(queries), responses)
    return surrogate
```

### 參數提取（Parameter Extraction）

更精密的攻擊嘗試重建模型的實際權重。這在模型開放了某種程度的內部狀態（如梯度資訊）時才可能實施。

### 成員推理（Membership Inference）

攻擊者判斷特定資料樣本是否在訓練集中。原理是訓練集樣本的 loss 通常低於非訓練集樣本，對醫療、金融等隱私敏感領域構成嚴重威脅。

## 3. 攻擊效益評估

| 攻擊類型 | 所需查詢數 | 成功率 | 可檢測性 |
|---------|-----------|-------|---------|
| 功能提取 | 10⁴-10⁵ | 高（>90% 準確率） | 低 |
| 參數提取 | 10⁶-10⁸ | 中（取決於模型結構） | 中 |
| 成員推理 | 10³-10⁴ | 中（60-80%） | 低 |

## 4. 防禦策略

### 查詢限制

限制單一使用者的 API 查詢頻率和總量。對異常查詢模式（如隨機輸入、高頻率查詢）進行監控和阻擋。

### 差分隱私輸出

在模型回應中加入雜訊，增加攻擊者重建模型的難度。這是精確度與隱私之間的權衡。

### 模型水印

在模型中嵌入不易察覺的水印，被盜用時可以證明所有權：

```python
def embed_watermark(weights, key):
    rng = np.random.default_rng(key)
    pos = rng.choice(len(weights.flatten()), size=100, replace=False)
    w = weights.copy().flatten()
    w[pos] += 0.01
    return w.reshape(weights.shape)
```

### 梯度遮罩

在聯邦學習場景中，只分享更新後的權重而非梯度，或使用安全聚合協定。

## 5. 結語

模型提取攻擊的本質矛盾在於：AI 服務需要開放 API 才能產生價值，但每一次 API 查詢都可能是提取攻擊的一環。防禦的核心在於提升攻擊成本——讓攻擊者需要的查詢數量和品質超過其能負擔的程度。

---

## 延伸閱讀

- [模型提取攻擊調查](https://www.google.com/search?q=model+extraction+attack+survey)
- [成員推理攻擊](https://www.google.com/search?q=membership+inference+attack+machine+learning)
- [Google Cloud 模型保護指引](https://www.google.com/search?q=Google+Cloud+AI+model+protection+best+practices)
