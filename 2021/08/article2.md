# PyTorch Vision 實作

torchvision 提供了電腦視覺常用的模型和工具。

## 1. 預訓練模型

```python
import torchvision.models as models

resnet = models.resnet18(pretrained=True)
alexnet = models.alexnet(pretrained=True)
vgg = models.vgg16(pretrained=True)
```

## 2. 資料集

```python
from torchvision import datasets

train_dataset = datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
test_dataset = datasets.CIFAR10(root='./data', train=False, transform=transform)
```

## 3. 模型推論

```python
from torchvision import transforms
from PIL import Image

model = models.resnet18(pretrained=True)
model.eval()

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

img = Image.open('photo.jpg')
input_tensor = preprocess(img).unsqueeze(0)
output = model(input_tensor)
```

---

## 延伸閱讀

- [torchvision 官方文檔](https://www.google.com/search?q=torchvision+official+documentation)
- [PyTorch Vision Models](https://www.google.com/search?q=pretrained+models+torchvision+pytorch)