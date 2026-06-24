# TensorFlow Serving 部署模型

## 生產環境的模型服務

### 為什麼需要 TensorFlow Serving？

模型訓練完成後，需要一個高效、易用的服務系統來託管和提供推論。TensorFlow Serving 就是為此而生：

- **高效能** — 支援千萬級請求
- **版本管理** — 自動熱更新模型
- **批量推論** — 最佳化吞吐量
- **REST/gRPC** — 支援多種協定

### 模型導出

先將訓練好的模型導出為 SavedModel 格式：

```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    tf.keras.layers.Dense(10, activation='softmax')
])

# 導出模型
version = 1
export_path = f'./model/{version}'

# 方式一：Keras 導出
model.save(export_path, save_format='tf')
```

### SavedModel 結構

```
model/
└── 1/
    ├── saved_model.pb        # 模型圖結構
    └── variables/
        ├── variables.data-00000-of-00001
        └── variables.index
```

### 安裝 TensorFlow Serving

```bash
# Ubuntu/Debian
echo "deb [arch=amd64] http://storage.googleapis.com/tensorflow-serving-apt stable tensorflow-model-server tensorflow-model-server-universal" | sudo tee /etc/apt/sources.list.d/tensorflow-serving.list
curl https://storage.googleapis.com/tensorflow-serving-apt/tensorflow-serving.release.pub.gpg | sudo apt-key add -
sudo apt-get update && sudo apt-get install tensorflow-model-server
```

### 啟動服務

```bash
tensorflow_model_server \
  --rest_api_port=8501 \
  --model_name=my_model \
  --model_base_path=/path/to/model
```

### REST API 呼叫

```python
import requests
import json

# 準備輸入資料
data = json.dumps({
    "instances": x_test[:1].tolist()
})

# 發送請求
response = requests.post(
    'http://localhost:8501/v1/models/my_model:predict',
    data=data,
    headers={'Content-Type': 'application/json'}
)

predictions = response.json()['predictions']
print(predictions)
```

### 模型版本管理

TensorFlow Serving 會自動監控模型目錄，新版本上傳後自動熱更新：

```bash
# 目錄結構
models/
├── my_model/
│   ├── 1/   # 版本 1
│   ├── 2/   # 版本 2
│   └── 3/   # 版本 3（最新）
```

### Benchmark

```python
# 使用 boto3 進行壓力測試
import time
import requests

url = 'http://localhost:8501/v1/models/my_model:predict'

times = []
for _ in range(1000):
    start = time.time()
    requests.post(url, data=json.dumps({"instances": [x_test[0].tolist()]}))
    times.append(time.time() - start)

print(f"Average latency: {sum(times)/len(times)*1000:.2f}ms")
```

### 小結

TensorFlow Serving 是將深度學習模型落地的重要工具，支援版本管理、熱更新、高效能推論，是企業級部署的首選方案。

---

**下一步**：[Estimator API 分散式訓練](focus5.md)