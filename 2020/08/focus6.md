# Transformer 的變體與改進

## 效率改進

### 問題

標準 Transformer 的注意力機制複雜度為 O(n²)，處理長序列時計算代價極高。

### Sparse Attention

**BigBird (Google)**：使用稀疏注意力模式

```python
# 注意力結構
global_attention = attend_to_all_tokens  # 全域關注
window_attention = attend_to_local_neighbors  # 局部關注
random_attention = attend_to_random_tokens  # 隨機連接
```

### Linear Attention

**Performer, Linformer**：將 O(n²) 降到 O(n)

```python
# 線性注意力的近似
Attention(Q, K, V) ≈ φ(Q) (φ(K)^T V) / (φ(K)^T 1)
```

### Flash Attention

使用 IO-aware 的tiling技術，顯著加速且不犧牲精度。

---

## 長上下文

### Transformer-XL

提出片段循環機制：
```python
state = cache_previous_segment + current_segment
```

### Longformer

- 局部注意力（滑動窗口）
- 全域注意力（特定 token）
- 可以處理 16K token

### Reformer

使用局部敏感哈希（LSH）進行近似鄰居搜索。

---

## 架構創新

### 殘差連接的改進

**Pre-LN vs Post-LN**

```python
# Post-LN (原始)
x = x + LayerNorm(Sublayer(x))  # 但在深層網路訓練不穩定

# Pre-LN
x = x + Sublayer(LayerNorm(x))  # 訓練更穩定
```

### 位置編碼的改進

**ROPE (Rotary Position Embedding)**

```python
def rotate(x, m, theta):
    x1, x2 = x[..., :d//2], x[..., d//2:]
    return cat([x1*cos(m*theta) - x2*sin(m*theta),
                x2*cos(m*theta) + x1*sin(m*theta)], dim=-1)
```

### Feed-Forward 的改進

**SwiGLU, GLU Variants**

```python
# GLU 門控機制
output = Swish(W1(x)) * W2(x)
```

---

## 特定任務優化

### 對話系統：BlenderBot

- 編碼器-解碼器架構
- 長期記憶機制
- 技能對話

### 程式碼生成：Codex

- 在程式碼上預訓練
- 專門的位置編碼
- 語法感知注意力

### 多模態：CLIP

- 雙塔架構（文字+圖像）
- 對比學習預訓練
- 零樣本分類

---

## 未來方向

### 2020 年的發展趨勢

1. **更高效的注意力機制**
2. **更長的上下文**
3. **多模態融合**
4. **神经網路架構搜索（NAS）**

### 仍在進行中的挑戰

- O(n) 複雜度的完整 Transformer
- 完全可解釋的注意力
- 理論理解

---

**下一步**：[未來展望](focus7.md)

## 延伸閱讀

- [sparse+attention+transformer+efficiency](https://www.google.com/search?q=sparse+attention+transformer+efficiency+2020)
- [linear+attention+transformer+longformer](https://www.google.com/search?q=linear+attention+transformer+longformer+2020)
- [transformer+architecture+improvements+2020](https://www.google.com/search?q=transformer+architecture+improvements+2020)