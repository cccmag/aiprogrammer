# 程式碼範例：卷積神經網路實作

## 程式碼說明

本目錄包含 CNN 的實現範例，從基本的卷積層到完整的 CNN 模型。

## 檔案清單

- `cnn.py` - CNN 基礎實現
- `test.sh` - 測試腳本

## 卷積層實現

卷積層接受輸入特徵圖與卷積核，輸出加權後的特徵圖：

```python
def convolve2d(image, kernel, stride=1, padding=0):
    if padding > 0:
        image = np.pad(image, padding, mode='constant')

    kh, kw = kernel.shape
    ih, iw = image.shape

    out_h = (ih - kh) // stride + 1
    out_w = (iw - kw) // stride + 1

    output = np.zeros((out_h, out_w))
    for i in range(out_h):
        for j in range(out_w):
            output[i, j] = np.sum(
                image[i*stride:i*stride+kh, j*stride:j*stride+kw] * kernel
            )
    return output
```

## 池化層實現

最大池化取區域最大值：

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

## CNN 訓練流程

```python
# 前向傳播
conv1_out = relu(conv2d(input, kernel1))
pool1_out = max_pooling(conv1_out)

conv2_out = relu(conv2d(pool1_out, kernel2))
pool2_out = max_pooling(conv2_out)

# 展平與分類
flatten = pool2_out.flatten()
output = softmax(FC(flatten))

# 計算損失並反向傳播
loss = cross_entropy(output, target)
# ... (反向傳播更新權重)
```

## 使用方式

```bash
python3 cnn.py
```

## 延伸學習

- 嘗試增加卷積層數量
- 實現不同的激活函數
- 使用真實數據集訓練模型