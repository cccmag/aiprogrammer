# EfficientNet 論文解析

EfficientNet 提出了複合縮放的智慧方法。

## 1. 複合縮放

EfficientNet 同時縮放三個維度：

```python
def scale_model(model, width_coef, depth_coef, resolution_coef):
    model.backbone.scale_width(width_coef)
    model.backbone.scale_depth(depth_coef)
    model.input_scale_resolution(resolution_coef)
```

## 2. 複合係數

α=1.2, β=1.2, γ=1.2 滿足 α × β² × γ² ≈ 2

## 3. 效率對比

EfficientNet-B0 比 ResNet-50 更好的準確率，同時使用更少參數。

---

## 延伸閱讀

- [EfficientNet 論文](https://www.google.com/search?q=EfficientNet+convolutional+neural+networks+compound+scaling+Tan)
- [MobileNet 詳解](https://www.google.com/search?q=MobileNets+efficient+convolutional+neural+networks+Howard)