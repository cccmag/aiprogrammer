# 程式碼範例

## 圖像處理基礎

```python
#!/usr/bin/env python3
"""圖像處理基礎示範"""

import numpy as np

def convolution2d(image, kernel):
    """簡單的 2D 卷積"""
    out_h = len(image) - len(kernel) + 1
    out_w = len(image[0]) - len(kernel[0]) + 1
    output = np.zeros((out_h, out_w))

    for i in range(out_h):
        for j in range(out_w):
            region = [row[j:j+len(kernel[0])] for row in image[i:i+len(kernel)]]
            output[i, j] = sum(sum(a*b for a, b in zip(r, k))
                             for r, k in zip(region, kernel))
    return output

def demo():
    image = np.array([
        [10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10],
        [0, 0, 0, 0, 0],
        [20, 20, 20, 20, 20],
        [20, 20, 20, 20, 20],
    ])

    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

    result = convolution2d(image, sobel_x)

    print("=" * 50)
    print("圖像處理基礎示範")
    print("=" * 50)
    print("\n原始圖像邊緣:")
    print(image)
    print("\nSobel X 邊緣偵測結果:")
    print(result)
```

## CNN 特徵圖概念

```python
#!/usr/bin/env python3
"""CNN 特徵圖概念示範"""

import numpy as np

def max_pooling(image, pool_size=2):
    """最大池化"""
    h, w = image.shape[:2]
    out_h, out_w = h // pool_size, w // pool_size
    output = np.zeros((out_h, out_w))

    for i in range(out_h):
        for j in range(out_w):
            i_start, j_start = i * pool_size, j * pool_size
            output[i, j] = np.max(
                image[i_start:i_start+pool_size, j_start:j_start+pool_size]
            )
    return output

def demo():
    feature_map = np.array([
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ], dtype=float)

    pooled = max_pooling(feature_map, pool_size=2)

    print("=" * 50)
    print("CNN 最大池化示範")
    print("=" * 50)
    print("\n特徵圖:")
    print(feature_map)
    print("\n2x2 最大池化結果:")
    print(pooled)
```

## IoU 計算

```python
#!/usr/bin/env python3
"""IoU 計算示範"""

def compute_iou(box1, box2):
    """計算兩個邊界框的 IoU"""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    intersection = max(0, x2 - x1) * max(0, y2 - y1)

    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union = area1 + area2 - intersection

    return intersection / (union + 1e-6)

def demo():
    print("=" * 50)
    print("IoU 計算示範")
    print("=" * 50)

    box1 = [10, 10, 50, 50]  # (x1, y1, x2, y2)
    box2 = [30, 30, 70, 70]

    iou = compute_iou(box1, box2)
    print(f"\nBox1: {box1}")
    print(f"Box2: {box2}")
    print(f"IoU: {iou:.4f}")

    box3 = [100, 100, 150, 150]  # 不重疊
    iou_no_overlap = compute_iou(box1, box3)
    print(f"\nBox3 (不重疊): {box3}")
    print(f"IoU: {iou_no_overlap:.4f}")
```

## 簡化物體偵測流程

```python
#!/usr/bin/env python3
"""簡化物體偵測流程示範"""

import numpy as np

def demo():
    print("=" * 50)
    print("物體偵測流程概念")
    print("=" * 50)

    print("\n1. 輸入圖像:")
    print("   640 x 480 像素 RGB 圖像")

    print("\n2. 特徵提取 (CNN):")
    print("   輸入 → Conv + Pool → Conv + Pool → ... → 特徵圖")
    print("   輸出: 20 x 15 x 256 特徵圖")

    print("\n3. 區域提議 (RPN):")
    print("   每個位置產生 9 個 anchor boxes")
    print("   總共: 20 x 15 x 9 = 2700 anchors")

    print("\n4. 分類 + 回歸:")
    print("   對每個 anchor 預測: 類別 + 邊界框偏移")

    print("\n5. NMS (非極大值抑制):")
    print("   去除重疊的框，保留最終結果")

    print("\n6. 輸出:")
    print("   [(邊界框, 類別, 信心度), ...]")
```

## OpenCV 概念操作

```python
#!/usr/bin/env python3
"""OpenCV 概念操作示範"""

import numpy as np

def demo():
    print("=" * 50)
    print("OpenCV 概念操作")
    print("=" * 50)

    # 模擬圖像
    img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)

    print("\n1. 讀取圖像:")
    print(f"   Shape: {img.shape}")
    print(f"   Dtype: {img.dtype}")

    print("\n2. 灰階轉換 (概念):")
    gray = np.mean(img, axis=2).astype(np.uint8)
    print(f"   Gray Shape: {gray.shape}")

    print("\n3. 調整大小 (概念):")
    print(f"   原始: {img.shape[:2]}")
    print(f"   目標: (50, 50)")

    print("\n4. 邊緣偵測 (Canny 概念):")
    print("   高斯模糊 → Sobel → 非極大值抑制 → 雙閾值")

    print("\n5. 輪廓偵測:")
    print("   findContours → drawContours")

if __name__ == "__main__":
    demo()
```

```python
#!/usr/bin/env python3
"""IoU 計算示範"""

def compute_iou(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    intersection = max(0, x2 - x1) * max(0, y2 - y1)

    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union = area1 + area2 - intersection

    return intersection / (union + 1e-6)

def demo():
    print("=" * 50)
    print("IoU 計算示範")
    print("=" * 50)

    box1 = [10, 10, 50, 50]
    box2 = [30, 30, 70, 70]

    iou = compute_iou(box1, box2)
    print(f"\nBox1: {box1}")
    print(f"Box2: {box2}")
    print(f"IoU: {iou:.4f}")

if __name__ == "__main__":
    demo()
```