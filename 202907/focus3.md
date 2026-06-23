# 模型竊取與反向工程

## 當你的模型不再是你自己的（2022-2029）

### 模型竊取的風險

模型竊取（Model Stealing）攻擊的目標是：在沒有權限的情況下，複製一個專有模型的功能。2022 年後，隨著 LLM API 服務（OpenAI、Claude、Gemini）的普及，模型竊取成為一個現實的商業威脅。

```python
import openai
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def steal_model_decision_boundary(target_api, num_queries=10000):
    """透過 API 查詢竊取決策邊界"""
    X_stolen = []
    y_stolen = []

    for _ in range(num_queries):
        # 在輸入空間中隨機取樣
        x = np.random.randn(1, 784)  # 假設是 MNIST 大小的輸入
        # 查詢目標模型
        response = target_api(x)
        pred = np.argmax(response["probabilities"])
        X_stolen.append(x)
        y_stolen.append(pred)

    # 訓練替代模型
    surrogate = RandomForestClassifier(n_estimators=100)
    surrogate.fit(np.vstack(X_stolen), y_stolen)

    return surrogate
```

### LLM 模型蒸餾攻擊

對於 LLM，攻擊者可以透過 API 查詢來「蒸餾」出一個功能相似的模型：

```python
def distill_llm(teacher_api, student_model, num_samples=50000):
    """使用知識蒸餾竊取 LLM 的能力"""
    prompts = [
        "Translate to French: {s}",
        "Summarize: {s}",
        "Write a poem about {s}",
    ]
    topics = ["AI", "nature", "space", "ocean", "time"]

    dataset = []
    for _ in range(num_samples):
        prompt_template = np.random.choice(prompts)
        topic = np.random.choice(topics)
        full_prompt = prompt_template.format(s=topic)

        # 查詢教師模型
        response = teacher_api(full_prompt, max_tokens=100)
        teacher_output = response["choices"][0]["text"]

        dataset.append((full_prompt, teacher_output))

    # 在竊取的資料上微調學生模型
    student_model.train(dataset, epochs=3)
    return student_model
```

### 2024-2026：成員推斷攻擊

成員推斷（Membership Inference）攻擊試圖判斷特定資料點是否用於訓練模型——這對隱私敏感領域（如醫療 AI）是重大威脅：

```python
def membership_inference_attack(target_model, data_point, shadow_models):
    """基於 shadow model 的成員推斷攻擊"""
    # 對目標資料點進行預測
    target_conf = target_model.predict_proba([data_point])[0]
    target_loss = -np.log(target_conf[np.argmax(target_conf)])

    # 與 shadow model 的損失分布比較
    shadow_losses = []
    for shadow_model in shadow_models:
        shadow_conf = shadow_model.predict_proba([data_point])[0]
        shadow_loss = -np.log(shadow_conf[np.argmax(shadow_conf)])
        shadow_losses.append(shadow_loss)

    # 如果目標損失顯著低於 shadow 模型
    # 則很可能該資料點在訓練集中
    threshold = np.percentile(shadow_losses, 5)
    return target_loss < threshold
```

### 2027-2029：模型反向工程

最新的攻擊方向是從模型權重反向推導訓練資料、超參數，甚至是訓練演算法：

```python
def reverse_engineer_training_data(model, num_candidate=1000):
    """透過梯度匹配反向工程訓練資料"""
    import torch

    def gradient_similarity(x_candidate, model, target_gradient):
        """計算候選點的梯度與目標梯度的相似度"""
        model.zero_grad()
        output = model(x_candidate.unsqueeze(0))
        loss = output.sum()
        loss.backward()

        cand_grad = torch.cat([p.grad.flatten() for p in model.parameters()])
        return torch.cosine_similarity(cand_grad, target_gradient, dim=0)

    reconstructed = []
    target_gradients = extract_target_gradients(model)

    # 使用隨機搜尋或最佳化來重建訓練資料
    for grad in target_gradients:
        best_x = torch.randn(1, 3, 224, 224)
        best_score = -float("inf")

        for _ in range(num_candidate):
            x_candidate = best_x + 0.01 * torch.randn_like(best_x)
            score = gradient_similarity(x_candidate, model, grad)
            if score > best_score:
                best_score = score
                best_x = x_candidate.clone()

        reconstructed.append(best_x)

    return reconstructed
```

### 防禦策略

| 防禦方法 | 原理 | 代價 |
|---------|------|------|
| 輸出擾動 | 對預測結果添加噪音 | 降低準確率 |
| 查詢限制 | 限制每個使用者的 API 調用次數 | 影響正常使用 |
| 差分隱私訓練 | 訓練過程加入隱私保護 | 模型品質下降 |
| 浮水印 | 在模型中嵌入可追蹤標記 | 需要驗證機制 |
| 模型混淆 | 輸出部分資訊而非完整結果 | 功能受限 |

### 商業影響

到 2029 年，模型竊取已成為 AI 公司的核心商業風險。API 調用限制、速率限制、輸出擾動已成標準配置，但攻擊者仍然使用分散式查詢、代理池和對抗性適應來繞過防禦。

---

**下一步**：[供應鏈安全](focus4.md)

## 延伸閱讀

- [Model Stealing Attacks](https://www.google.com/search?q=model+stealing+attacks+machine+learning)
- [Membership Inference Attacks](https://www.google.com/search?q=membership+inference+attack+deep+learning)
- [Knowledge Distillation Security](https://www.google.com/search?q=knowledge+distillation+security+risks)
