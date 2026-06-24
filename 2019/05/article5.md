# RESTful API 設計：Flask 實踐

## 前言

Flask 是 Python 常用的輕量級 Web 框架，適合快速構建 ML 模型的 API 服務。

## 基本 Flask 應用

```python
from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = np.array(data['features'])

    # ML 推理
    prediction = model.predict(features)

    return jsonify({
        'prediction': prediction.tolist(),
        'status': 'success'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## RESTful 設計原則

```python
# 資源導向
@app.route('/api/v1/models/<model_name>/predict', methods=['POST'])

# 正確的 HTTP 方法
# GET: 獲取資源
# POST: 創建資源
# PUT: 更新資源
# DELETE: 刪除資源
```

## 錯誤處理

```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500
```

## 延伸閱讀

- [Flask 文件](https://www.google.com/search?q=Flask+RESTful+API+tutorial)