# 深度學習推理優化

## 推理加速

```python
# ONNX Runtime
import onnxruntime as ort
session = ort.InferenceSession('model.onnx')
output = session.run(None, {'input': data})
```

## 結論

推理優化對於部署至關重要。

---

**延伸閱讀**

- [ONNX+Runtime](https://www.google.com/search?q=ONNX+Runtime+inference)