# 多模態嵌入的對齊與訓練

## 前言

多模態 AI 的核心挑戰是讓不同模態（文字、圖片、音訊、影片）的資料在同一向量空間中具有可比性。多模態嵌入的對齊（Alignment）是解決這個問題的關鍵技術。本文將介紹主流的多模態對齊方法，並透過 Python 示範如何訓練對齊模型。

---

## 一、為何需要多模態對齊

不同模態的原始資料分布完全不同：文字是離散符號，圖片是連續像素，音訊是一維波形。多模態對齊的目標是學會一個嵌入函數 \( f \)，使得語義相近的跨模態樣本在嵌入空間中距離接近。

## 二、對比式對齊：CLIP 風格

最常見的對齊方法是對比學習，目標是最大化正配對的相似度，最小化負配對的相似度：

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class MultiModalAligner(nn.Module):
    def __init__(self, text_dim=768, image_dim=512, proj_dim=256):
        super().__init__()
        self.text_proj = nn.Linear(text_dim, proj_dim)
        self.image_proj = nn.Linear(image_dim, proj_dim)

    def forward(self, text_feats, image_feats):
        # 投影到共同空間並正規化
        t = F.normalize(self.text_proj(text_feats), dim=1)
        i = F.normalize(self.image_proj(image_feats), dim=1)
        return t, i

def multimodal_contrastive_loss(t, i, temperature=0.07):
    # t, i: (batch_size, proj_dim)
    logits = t @ i.T / temperature  # (batch, batch)
    labels = torch.arange(len(t))
    loss_t = F.cross_entropy(logits, labels)
    loss_i = F.cross_entropy(logits.T, labels)
    return (loss_t + loss_i) / 2
```

## 三、三模態對齊：ImageBind

Meta 的 ImageBind 將對齊擴展到六種模態（圖片、文字、音訊、深度、熱成像、IMU），核心想法是使用圖片作為繫結模態（binding modality）：

```python
class ImageBindAligner(nn.Module):
    def __init__(self, dims={"vision": 512, "text": 768, "audio": 512}, proj_dim=256):
        super().__init__()
        self.projectors = nn.ModuleDict({
            mod: nn.Linear(dim, proj_dim)
            for mod, dim in dims.items()
        })

    def embed(self, features, modality):
        proj = self.projectors[modality]
        return F.normalize(proj(features), dim=1)

    def compute_loss(self, batch):
        # 對齊所有模態到視覺錨點
        vision_feat = self.embed(batch["vision"], "vision")
        total_loss = 0

        for modality in ["text", "audio"]:
            if modality not in batch:
                continue
            other_feat = self.embed(batch[modality], modality)
            logits = vision_feat @ other_feat.T / 0.07
            labels = torch.arange(len(vision_feat))
            total_loss += F.cross_entropy(logits, labels)

        return total_loss / len(batch)
```

## 四、跨模態檢索評估

訓練後需要評估對齊品質，常見指標是 Recall@K：

```python
def recall_at_k(text_embs, image_embs, k=5):
    """文字檢索圖片的 Recall@K"""
    n = len(text_embs)
    sims = text_embs @ image_embs.T  # (n, n)
    correct = 0

    for i in range(n):
        # 第 i 個文字的正確配對是第 i 張圖片
        top_k_indices = sims[i].topk(k).indices
        if i in top_k_indices:
            correct += 1

    return correct / n

def evaluate_alignment(text_embs, image_embs):
    r1 = recall_at_k(text_embs, image_embs, k=1)
    r5 = recall_at_k(text_embs, image_embs, k=5)
    r10 = recall_at_k(text_embs, image_embs, k=10)
    print(f"R@1: {r1:.4f}, R@5: {r5:.4f}, R@10: {r10:.4f}")
    return r1, r5, r10
```

## 五、對齊訓練的注意事項

1. **負樣本採樣**：隨機負樣本可能太簡單（easy negatives），建議使用 hard negative mining
2. **佇列式負樣本**：MoCo 風格維護一個負樣本佇列，讓 batch size 不受 GPU 記憶體限制
3. **多尺度對齊**：不同層級的語義需要不同粒度（全域 vs 局部）的對齊
4. **蒸餾（Distillation）**：用教師模型的嵌入來引導學生模型的對齊學習

```python
class MoCoQueue:
    """動態負樣本佇列"""
    def __init__(self, dim=256, queue_size=65536):
        self.queue = torch.randn(queue_size, dim)
        self.queue = F.normalize(self.queue, dim=1)
        self.ptr = 0

    def enqueue(self, features):
        batch_size = features.shape[0]
        self.queue[self.ptr:self.ptr + batch_size] = features
        self.ptr = (self.ptr + batch_size) % len(self.queue)
```

---

## 結語

多模態嵌入的對齊是建構跨模態理解的基石。從 CLIP 的雙模態對齊到 ImageBind 的多模態擴展，再到最新的多模態大型語言模型（MLLM），對齊技術一直在持續演進。掌握對比學習與嵌入對齊的原理，就能理解多模態 AI 的核心運作機制。

---

**參考資料**

- ImageBind 論文：https://arxiv.org/abs/2305.05665
- CLIP 論文：https://arxiv.org/abs/2103.00020
- MoCo 論文：https://arxiv.org/abs/1911.05722
- 多模態對齊技術：https://www.google.com/search?q=multimodal+embedding+alignment+contrastive+learning
