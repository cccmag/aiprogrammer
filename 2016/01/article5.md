# Lambda 無伺服器運算

## Lambda 核心概念

AWS Lambda 讓你無需管理伺服器就能執行程式碼。你只需要上傳程式碼，Lambda 會自動配置所需的運算資源，並在事件觸發時執行。這就是「無伺服器」的核心價值：你專注於程式碼本身，而非基礎設施。

## 第一個 Lambda 函數

使用 Python 撰寫簡單的 Lambda 函數：

```python
import json

def lambda_handler(event, context):
    name = event.get('name', 'World')
    return {
        'statusCode': 200,
        'body': json.dumps(f'Hello, {name}!')
    }
```

部署方式：
1. 在 AWS Console 進入 Lambda服務
2. 點選「建立函數」→「從頭開始撰寫」
3. 輸入函數名稱，選擇 Python 3.8 執行階段
4. 粘貼程式碼，點選「部署」
5. 點選「測試」，輸入事件資料，檢視輸出

## 觸發器設定

Lambda 可與多種 AWS 服務整合，事件觸發時自動執行：

**API Gateway**：建立 RESTful API，HTTP 請求時觸發 Lambda 函數。

**S3**：檔案上傳或刪除時觸發，可用於影像處理、資料轉換。

**DynamoDB**：資料表項目異動時觸發，可用於即時分析或更新相關資料。

**CloudWatch Events**：定時觸發，適合排程任務如資料庫清理、報表產生。

```yaml
# API Gateway 觸發設定範例（在 Lambda Console 中設定）
事件來源: API Gateway
HTTP 方法: GET
路徑: /hello
```

## 定價計算

Lambda 依以下兩項收費：

**請求費用**：每月前 100 萬個請求免費，超出部分每 100 萬個請求收 $0.20。

**運算費用**：依實際執行時間收費，以 100ms 為單位。記憶體 128MB 為例，每 GB-秒收 $0.0000166667。

## 限時與記憶體

Lambda 函數有嚴格的資源限制：執行時間最長 900 秒（15 分鐘），記憶體最多 3008MB。這些限制是出於安全與資源管理的考量。設計函數時應確保能在限制內完成，或考慮拆分為多個較小的函數。

## 適合的使用場景

Lambda 適合事件驅動、間歇性、不需要長時間執行的任務。影像縮圖產生、CSV 資料處理、 webhook 回應、自動化工作是常見的應用場景。不適合需要長時間運行或有狀態的應用。

## 參考資源

- https://www.google.com/search?q=AWS+Lambda+無伺服器+Python+第一個函數+教學+建立+2016
- https://www.google.com/search?q=Lambda+觸發器+API+Gateway+S3+DynamoDB+CloudWatch+設定
- https://www.google.com/search?q=Lambda+定價+費用+計算+請求+運算時間+mapping+template