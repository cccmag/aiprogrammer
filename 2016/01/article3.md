# S3 儲存服務操作

## S3 基本概念

Amazon S3（Simple Storage Service）是 AWS 最受歡迎的儲存服務，用於存放任意數量的資料。S3 的設計理念是 11 個 9 的可用性（99.999999999%），意即每年資料損失的機率極低。

**儲存桶（Bucket）**：S3 的最上層容器，用於組織物件。每個儲存桶名稱在全球 AWS 中必須唯一。

**物件（Object）**：儲存在儲存桶中的檔案，包含鑰匙（Key，類似檔案路徑）、值（Value，實際資料）、元資料（Metadata）。

## 使用 AWS CLI 操作 S3

```bash
# 建立儲存桶（選擇適合的區域可降低延遲與成本）
aws s3 mb s3://my-unique-bucket-name --region us-east-1

# 上傳檔案
aws s3 cp myfile.txt s3://my-unique-bucket-name/

# 上傳整個目錄
aws s3 sync my-folder/ s3://my-unique-bucket-name/my-folder/

# 列出儲存桶內容
aws s3 ls s3://my-unique-bucket-name/

# 下載檔案
aws s3 cp s3://my-unique-bucket-name/myfile.txt ./

# 刪除物件
aws s3 rm s3://my-unique-bucket-name/myfile.txt
```

## 靜態網站托管

S3 可作為靜態網站的主機，非常適合 HTML/CSS/JavaScript 構成的網站或 SPA（單頁應用）。

1. 在 S3 Console 中選擇儲存桶，點選「屬性」→「靜態網站托管」
2. 選擇「使用此儲存桶托管網站」，輸入索引文件（如 index.html）與錯誤文件
3. 設定公開存取權（點選「權限」）
4. 新增Bucket Policy允許公開讀取：

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::my-bucket-name/*"
        }
    ]
}
```

## 生命週期政策

設定自動將資料移動到較便宜的儲存層級：

```bash
aws s3api put-bucket-lifecycle-configuration \
    --bucket my-bucket-name \
    --lifecycle-configuration '{
        "Rules": [{
            "ID": "MoveToGlacierAfterOneYear",
            "Prefix": "logs/",
            "Status": "Enabled",
            "Transitions": [{
                "Days": 365,
                "StorageClass": "GLACIER"
            }]
        }]
    }'
```

## 儲存層級

| 層級 | 用途 | 費用 |
|------|------|------|
| Standard | 頻繁存取的資料 | 標準費用 |
| IA (Infrequent Access) | 每月存取少於一次的資料 | 較低存放費，但有取出費 |
| Glacier | 歸檔資料，幾分鐘到數小時才能取出 | 極低存放費 |

## 參考資源

- https://www.google.com/search?q=AWS+S3+儲存桶+物件+操作+CLI+上傳+下載+同步+2016
- https://www.google.com/search?q=S3+靜態網站+托管+設定+Bucket+Policy+CloudFront
- https://www.google.com/search?q=S3+生命週期+儲存層級+Glacier+Infrequent+Access+轉換