# 無伺服器運算（Serverless）

## Serverless 簡介

Serverless 不是沒有伺服器，而是開發者無需管理伺服器。雲端供應商負責基礎設施配置、容量規劃和維護。開發者只專注於程式碼。

## 主要的 FaaS 平台

| 平台 | 雲端供應商 |
|------|-----------|
| AWS Lambda | Amazon Web Services |
| Google Cloud Functions | Google Cloud |
| Azure Functions | Microsoft Azure |
| Cloud Run | Google Cloud |

## AWS Lambda 範例

```python
import json

def lambda_handler(event, context):
    name = event.get('name', 'World')
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'Hello, {name}!'
        })
    }
```

## 觸發器

Serverless 函式可以被各種事件觸發：

```yaml
# AWS SAM 模板
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.handler
      Runtime: python3.9
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /hello
            Method: get
        S3Event:
          Type: S3
          Properties:
            Bucket: my-bucket
            Events: s3:ObjectCreated:*
```

## 冷啟動問題

Serverless 的冷啟動是指函式在閒置後首次被調用時的延遲。可以通過：
- 保持函式小型
- 減少依賴
- 使用 Provisioned Concurrency

## 成本模型

Serverless 按實際執行時間收費：

```python
# AWS Lambda 定價示例
# 前 100 億 GB-秒免費
# 之後每 GB-秒 $0.0000166667
```

這使得 Serverless 特別適合間歇性工作負載。

## 應用場景

- 即時檔案處理
- Webhook 處理
- 事件驅動的資料處理
- 自動化任務

## 限制

- 執行時間限制（Lambda 最長 15 分鐘）
- 請求/回應大小限制
- 冷啟動延遲
- 供應商鎖定

## 結論

Serverless 是雲端原生架構的重要補充，特別適合事件驅動和工作負載波動大的場景。理解其優勢和限制，有助於做出正確的架構決策。