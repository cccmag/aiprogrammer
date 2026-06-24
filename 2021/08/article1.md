# Python 影像處理基礎

Python 提供了多種影像處理工具，本文介紹基本操作。

## 1. PIL/Pillow

Python Imaging Library 是最基本的影像處理庫：

```python
from PIL import Image

img = Image.open('photo.jpg')
img_resized = img.resize((224, 224))
img_cropped = img.crop((0, 0, 224, 224))
img.save('output.jpg')
```

## 2. OpenCV

OpenCV 提供了更強大的功能：

```python
import cv2

img = cv2.imread('photo.jpg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(img, (5, 5), 0)
```

## 3. torchvision transforms

PyTorch 提供了常用的影像轉換：

```python
from torchvision import transforms

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])
```

---

## 延伸閱讀

- [PIL Documentation](https://www.google.com/search?q=PIL+Pillow+Python+imaging+library)
- [OpenCV Python Tutorials](https://www.google.com/search?q=OpenCV+Python+tutorial+basics)