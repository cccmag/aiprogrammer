# 深度學習可解釋性：從卷積到 Transformer

## 前言

深度神經網路是 2026 年 AI 應用最廣泛的模型，但它們也是最難解釋的——數百萬甚至數十億的參數讓「理解模型在做什麼」成為巨大挑戰。本文探討從 CNN 到 Transformer 的可解釋性技術。

## 卷積網路的可視化方法

### Grad-CAM：最直覺的局部解釋

Grad-CAM 利用最後一卷積層的梯度來產生熱力圖，標示影像中哪些區域影響了分類決策：

```python
import numpy as np


def grad_cam(feature_maps: np.ndarray, gradients: np.ndarray) -> np.ndarray:
    """Generate Grad-CAM heatmap from last conv layer."""
    # feature_maps: (C, H, W), gradients: (C, H, W)
    weights = np.mean(gradients, axis=(1, 2))  # Global average pooling
    cam = np.zeros(feature_maps.shape[1:], dtype=np.float32)
    for i, w in enumerate(weights):
        cam += w * feature_maps[i]
    cam = np.maximum(cam, 0)  # ReLU
    cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
    return cam


# Simulate feature maps and gradients
np.random.seed(42)
feature_maps = np.random.randn(64, 7, 7)
gradients = np.random.randn(64, 7, 7)

heatmap = grad_cam(feature_maps, gradients)
print(f"Grad-CAM heatmap shape: {heatmap.shape}")
print(f"Heatmap range: [{heatmap.min():.3f}, {heatmap.max():.3f}]")
```

### Integrated Gradients

一種滿足公理的可解釋性方法，透過沿著從基線到輸入的路徑積分梯度：

```python
def integrated_gradients(model, x: np.ndarray, baseline: np.ndarray,
                         steps: int = 50) -> np.ndarray:
    """Compute integrated gradients for input x."""
    scaled_inputs = [baseline + (float(i) / steps) * (x - baseline)
                     for i in range(steps + 1)]
    grads = []
    for inp in scaled_inputs:
        grads.append(model.compute_gradient(inp))
    avg_grads = np.mean(grads, axis=0)
    return (x - baseline) * avg_grads


class SimpleModel:
    def compute_gradient(self, x):
        return x / np.linalg.norm(x + 1e-8)


model = SimpleModel()
x = np.array([2.0, -1.0, 3.0])
baseline = np.zeros(3)
ig = integrated_gradients(model, x, baseline)
for i, v in enumerate(ig):
    print(f"IntegratedGrad[{i}] = {v:.3f}")
```

## Transformer 的可解釋性

Transformer 模型的解釋方法與 CNN 截然不同，主要針對注意力權重與特徵交互：

### 注意力歸因

```python
def attention_attribution(attention_weights: np.ndarray,
                          token_importance: np.ndarray) -> np.ndarray:
    """Propagate importance through attention layers."""
    # attention_weights: (n_heads, seq_len, seq_len)
    # token_importance: (seq_len,)
    n_heads, seq_len, _ = attention_weights.shape
    importance = np.zeros((seq_len, seq_len))
    for h in range(n_heads):
        for i in range(seq_len):
            for j in range(seq_len):
                importance[i, j] += (attention_weights[h, i, j]
                                     * token_importance[j])
    # Normalize by heads
    return importance / n_heads


# Simulate: 5 tokens, 8 attention heads
attn = np.random.rand(8, 5, 5)
token_imp = np.array([0.1, 0.5, 0.3, 0.05, 0.05])
result = attention_attribution(attn, token_imp)
print("Token-to-token importance matrix:")
print(np.round(result, 3))
```

### RQ-VAE 與概念解釋

2026 年最新趨勢是**概念可解釋性**——不再解釋單個特徵，而是解釋高層語義概念。透過 Vector Quantization（RQ-VAE）將特徵空間分解為可理解的概念單元：

```python
def concept_activation(model, x: np.ndarray, concept_dict: dict) -> dict:
    """Map activations to human-interpretable concepts."""
    activations = model.get_activations(x)
    concept_scores = {}
    for concept_name, concept_vector in concept_dict.items():
        similarity = np.dot(activations, concept_vector)
        similarity /= (np.linalg.norm(activations) * np.linalg.norm(concept_vector) + 1e-8)
        concept_scores[concept_name] = float(similarity)
    return concept_scores


concepts = {"edge": np.array([1, 0, 0]),
            "texture": np.array([0, 1, 0]),
            "shape": np.array([0, 0, 1])}
activation = np.array([0.8, 0.3, 0.9])
scores = concept_activation(SimpleModel(), activation, concepts)
for c, s in scores.items():
    print(f"Concept '{c}': {s:.3f}")
```

## 大語言模型的可解釋性挑戰

LLM 的可解釋性是 2026 年最活躍的研究領域：

- **Logit Lens**：檢查每層輸出的詞彙分布，理解模型何時做出最終決策。
- **Activation Patching**：干預特定層的活化值來測量其因果貢獻。
- **Sparse Autoencoders**：將活化值分解為稀疏的人類可讀特徵。

## 結語

深度學習的可解釋性沒有銀彈。CNN、Transformer、LLM 各自需要不同的方法。2026 年的關鍵認識是：**可解釋性不是一個附加功能，而是模型設計的一部分**。從選擇架構時就考慮可解釋性，遠比事後解釋來得有效。

---

**延伸閱讀**
- [Grad-CAM 原始論文](https://www.google.com/search?q=Grad+CAM+visual+explanations+deep+networks)
- [Integrated Gradients](https://www.google.com/search?q=integrated+gradients+axiomatic+attribution)
- [Transformer Explainability](https://www.google.com/search?q=transformer+explainability+attention+attribution)
