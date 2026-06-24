# 焦點文章 3：池化層與特徵圖

## 前言

池化層（Pooling Layer）是 CNN 的重要組成部分，負責壓縮特徵圖、减少計算量，同時提供一定程度的平移不變性。本章節介紹池化操作與特徵圖的概念。

## 為什麼需要池化層

1. **減少參數**：降低特徵圖解析度，減少後續層的計算量
2. **控制過擬合**：提供輕微的正則化效果
3. **提供平移不變性**：小幅平移不影響輸出
4. **擴大感受野**：讓後續卷積能看到更大的區域

## 最大池化（Max Pooling）

取池化窗口中的最大值：

```python
def max_pooling(feature_map, pool_size=2, stride=2):
    h, w = feature_map.shape
    out_h = h // stride
    out_w = w // stride

    pooled = np.zeros((out_h, out_w))
    for i in range(out_h):
        for j in range(out_w):
            h_start = i * stride
            w_start = j * stride
            pooled[i, j] = np.max(
                feature_map[h_start:h_start+pool_size, w_start:w_start+pool_size]
            )
    return pooled
```

視覺化：
```
輸入:          輸出 (2x2 max):
[1, 2, 3, 4]    [4, 4]
[5, 6, 7, 8]  → [8, 8]
[1, 2, 3, 4]
[5, 6, 7, 8]
```

## 平均池化（Average Pooling）

取池化窗口中的平均值：

```python
def avg_pooling(feature_map, pool_size=2, stride=2):
    h, w = feature_map.shape
    out_h = h // stride
    out_w = w // stride

    pooled = np.zeros((out_h, out_w))
    for i in range(out_h):
        for j in range(out_w):
            h_start = i * stride
            w_start = j * stride
            pooled[i, j] = np.mean(
                feature_map[h_start:h_start+pool_size, w_start:w_start+pool_size]
            )
    return pooled
```

## 全域池化（Global Pooling）

在每個特徵圖上做全局平均或最大值：

- **全域平均池化**：將每個特徵圖平均成一個值
- **全域最大池化**：將每個特徵圖最大成一個值

常用於替代全連接層：
```
Input: 7 × 7 × 512
Global Avg Pool: 1 × 1 × 512
```

## 池化層的特點

1. **無需學習參數**：只是固定的操作
2. **超參數**：pool_size、stride
3. **通常不填充**：輸出 size = input size / stride

## 特徵圖（Feature Map）

卷積層的輸出稱為特徵圖（Feature Map）：

| 層次 | 特徵圖含義 |
|------|------------|
| 浅層卷積 | 邊緣、紋理 |
| 中層卷積 | 形狀、部件 |
| 深層卷積 | 物體類別 |

## 特徵圖視覺化

```python
import matplotlib.pyplot as plt

def visualize_feature_maps(model, layer_index, image):
    intermediate_model = Model(inputs=model.input,
                               outputs=model.layers[layer_index].output)
    feature_maps = intermediate_model.predict(image)

    fig, axes = plt.subplots(4, 8, figsize=(12, 6))
    for i, ax in enumerate(axes.flat):
        if i < feature_maps.shape[-1]:
            ax.imshow(feature_maps[0, :, :, i], cmap='viridis')
        ax.axis('off')
    plt.show()
```

## 總結

池化層通過下採樣減少特徵圖尺寸，降低計算複雜度並提供平移不變性。全域池化則是替代全連接層的有效方案。

## 延伸閱讀

- https://www.google.com/search?q=max+pooling+average+pooling+CNN
- https://www.google.com/search?q=feature+map+visualization+CNN