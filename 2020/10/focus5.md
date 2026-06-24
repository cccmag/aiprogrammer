# 部署到雲端平台：Heroku、AWS Lambda 與 GCP

## 雲端部署概述

### 為什麼選擇雲端？

```
雲端部署優勢：
────────────────────────────────

成本效益：
  ├── 按需付費（無需預先購買硬體）
  ├── 彈性擴展（流量高峰時自動擴展）
  └── 維護成本低（無需管理實體伺服器）

可靠性：
  ├── 多區域部署（提高可用性）
  ├── 自動備份（資料安全）
  └── 故障轉移（高可用性）

便利性：
  ├── 快速部署（幾分鐘即可上線）
  ├── 管理介面（Web 控制台）
  └── API 管理（基礎設施即程式碼）
```

## Heroku

### Heroku 平台特色

Heroku 是最簡單的 Python 部署平台之一，支援多種語言，提供完善的平台服務：

```bash
# 安裝 Heroku CLI
brew install heroku/brew/heroku

# 登入
heroku login

# 建立應用
heroku create my-python-app

# 部署（Git 推送自動觸發部署）
git push heroku main
```

### Flask 部署到 Heroku

```python
# app.py
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({'message': 'Hello from Heroku!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

```bash
# 建立必要檔案
touch Procfile requirements.txt

# Procfile
web: gunicorn app:app --workers 2

# requirements.txt
flask==1.1.2
gunicorn==20.0.4

# 部署
git init
git add .
git commit -m "Initial commit"
heroku create my-flask-app
git push heroku master
```

### Heroku 附加服務

```bash
# 新增 PostgreSQL 資料庫
heroku addons:create heroku-postgresql:hobby-dev

# 新增 Redis 快取
heroku addons:create heroku-redis:hobby-dev

# 查看環境變數
heroku config

# 設定環境變數
heroku config:set SECRET_KEY=my-secret-key
```

## AWS Lambda

### 無伺服器運算

AWS Lambda 讓你无需管理伺服器即可執行程式碼：

```python
# lambda_function.py
import json

def lambda_handler(event, context):
    # 從 API Gateway 獲取請求
    name = event.get('queryStringParameters', {}).get('name', 'World')
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'Hello, {name}!'
        })
    }
```

### 部署 Lambda 函數

```bash
# 使用 AWS CLI 部署
aws lambda create-function \
    --function-name my-python-function \
    --runtime python3.8 \
    --role arn:aws:iam::123456789012:role/lambda-role \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://function.zip
```

### 框架支援

使用 Zappa 部署 Flask/Django 到 Lambda：

```bash
# 安裝
pip install zappa

# 初始化
zappa init

# 部署
zappa deploy production

# 更新
zappa update production

# 刪除
zappa undeploy production
```

### SAM CLI

AWS SAM（Serverless Application Model）提供了更好的開發體驗：

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.lambda_handler
      Runtime: python3.8
      Events:
        Api:
          Type: Api
          Properties:
            Path: /{proxy+}
            Method: ANY
```

```bash
# 建構
sam build

# 本地測試
sam local start-api

# 部署
sam deploy --guided
```

## Google Cloud Platform

### Cloud Run

Cloud Run 是 GCP 的無容器服務平台，支援任何語言：

```dockerfile
# Dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV PORT=8080
CMD ["python", "app.py"]
```

```bash
# 建構並部署
gcloud builds submit --tag gcr.io/PROJECT_ID/myapp
gcloud run deploy --image gcr.io/PROJECT_ID/myapp --platform managed
```

### App Engine

App Engine 是 GCP 的 PaaS 平台：

```yaml
# app.yaml
runtime: python38
env: standard
instance_class: F2

handlers:
- url: .*
  script: auto
```

```bash
# 部署
gcloud app deploy
gcloud app browse
```

### Cloud Functions

GCP 的無伺服器函數服務：

```python
# main.py
def hello_world(request):
    request_json = request.get_json()
    name = request_json.get('name', 'World')
    return f'Hello, {name}!'
```

```bash
# 部署
gcloud functions deploy hello_world \
    --runtime python38 \
    --trigger-http \
    --allow-unauthenticated
```

## 比較與選擇

### 平台比較

| 特性 | Heroku | AWS Lambda | GCP Cloud Run |
|------|--------|------------|---------------|
| 價格模型 | 按小時計費 | 按呼叫計費 | 按使用計費 |
| 冷啟動 | 快 | 較慢 | 快 |
| 最大執行時間 | 無限制 | 15 分鐘 | 15 分鐘 |
| 免費額度 | 550 小時/月 | 100 萬請求/月 | 200 萬請求/月 |
| 學習曲線 | 低 | 中 | 低 |
| 擴展性 | 自動擴展 | 自動擴展 | 自動擴展 |

### 選擇建議

**選擇 Heroku**：
- 想要快速上手
- 需要完整的平台服務（資料庫、Redis 等）
- 小型到中型應用

**選擇 AWS Lambda**：
- 需要與 AWS 服務深度整合
- 有短暫的工作負載
- 想要最精細的成本控制

**選擇 GCP Cloud Run**：
- 想要容器化的靈活性
- 需要跨雲端部署
- 喜歡 Knative 的標準化

## 延伸閱讀

- [Heroku Python 部署指南](https://www.google.com/search?q=Heroku+Python+deployment+guide)
- [AWS Lambda Python 文件](https://www.google.com/search?q=AWS+Lambda+Python+documentation)
- [Zappa 部署 Flask](https://www.google.com/search?q=Zappa+deploy+Flask+AWS+Lambda)
- [Google Cloud Run Python](https://www.google.com/search?q=Cloud+Run+Python+deployment)
- [無伺服器架構比較](https://www.google.com/search?q=serverless+Python+comparison+2020)

---

*本篇文章為「AI 程式人雜誌 2020 年 10 月號」歷史回顧系列之一。*