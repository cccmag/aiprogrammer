# PIL 圖像處理

## PIL 简介

PIL（Python Imaging Library）是 Python 影像處理的基礎庫。Pillow 是 PIL 的維護版本。

```bash
pip install Pillow
```

## 基本操作

```python
from PIL import Image
import numpy as np

# 讀取圖像
img = Image.open('image.jpg')

# 取得基本資訊
print(img.size)    # (width, height)
print(img.mode)    # 'RGB', 'L', etc.
print(img.format)  # 'JPEG', 'PNG', etc.

# 轉換模式
gray = img.convert('L')

# 儲存
img.save('output.png')
```

## 影像處理

```python
from PIL import Image, ImageFilter, ImageEnhance

# 調整大小
resized = img.resize((width, height))
resized = img.thumbnail((max_width, max_height))  # 保持比例

# 旋轉
rotated = img.rotate(45)  # 逆時針 45 度
rotated = img.transpose(Image.ROTATE_90)

# 裁剪
cropped = img.crop((left, top, right, bottom))
```

## 濾波器

```python
# 模糊
blurred = img.filter(ImageFilter.BLUR)

# 銳化
sharpened = img.filter(ImageFilter.SHARPEN)

# 邊緣
edges = img.filter(ImageFilter.FIND_EDGES)

# 其他濾波器
img.filter(ImageFilter.CONTOUR)
img.filter(ImageFilter.DETAIL)
img.filter(ImageFilter.EDGE_ENHANCE)
```

## 調整亮度與對比

```python
# 亮度
enhancer = ImageEnhance.Brightness(img)
brighter = enhancer.enhance(1.5)

# 對比度
enhancer = ImageEnhance.Contrast(img)
enhanced = enhancer.enhance(1.5)

# 銳利度
enhancer = ImageEnhance.Sharpness(img)
sharpened = enhancer.enhance(2.0)
```

## 繪圖

```python
from PIL import ImageDraw

draw = ImageDraw.Draw(img)

# 繪製線條
draw.line([(0, 0), (100, 100)], fill='red', width=5)

# 繪製矩形
draw.rectangle([50, 50, 150, 150], outline='blue', width=3)

# 繪製橢圓
draw.ellipse([50, 50, 150, 150], fill='green')

# 繪製文字
draw.text((10, 10), 'Hello', fill='white')
```

## 陣列轉換

```python
# PIL -> NumPy
img_array = np.array(img)

# NumPy -> PIL
img = Image.fromarray(img_array)
```

## 應用：建立縮圖

```python
def create_thumbnail(input_path, output_path, size=(128, 128)):
    with Image.open(input_path) as img:
        img.thumbnail(size)
        img.save(output_path)

create_thumbnail('large_image.jpg', 'thumb.jpg')
```

## 應用：圖像拼接

```python
def concat_images(images):
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)

    result = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for img in images:
        result.paste(img, (x_offset, 0))
        x_offset += img.width

    return result
```

## 總結

PIL/Pillow 是 Python 影像處理的基礎工具。支援讀寫多種格式、提供丰富的圖像處理與繪圖功能，是電腦視覺開發的好幫手。