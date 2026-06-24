# 雲端運算崛起：Amazon AWS 持續擴張

## 前言

2007 年，Amazon Web Services（AWS）已經成立一年多，雲端運算的概念正在從新興技術轉變為企業 IT 架構的主流選擇。

## AWS 的發展歷程

### 2006-2007 年的關鍵服務

```
┌────────────────────────────────────────────────────────┐
│            Amazon Web Services 時間線                  │
├────────────────────────────────────────────────────────┤
│                                                        │
│  2006：                                               │
│  - S3 (Simple Storage Service) 發布                   │
│  - EC2 (Elastic Compute Cloud) Beta                  │
│                                                        │
│  2007：                                               │
│  - EC2 正式發布                                       │
│  - SimpleDB 加入                                      │
│  - SQS (Simple Queue Service) 加入                    │
│  - SNS (Simple Notification Service) 加入            │
│  - VPC (Virtual Private Cloud) 概念提出               │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 核心服務介紹

### Amazon S3

```python
# Boto - Python 的 AWS SDK
import boto

# 連接到 S3
conn = boto.connect_s3()

# 創建 bucket
bucket = conn.create_bucket('my-data-2007')

# 上傳檔案
from boto.s3.key import Key
k = Key(bucket)
k.key = 'data.csv'
k.set_contents_from_filename('local.csv')

# 下載檔案
k.get_contents_to_filename('downloaded.csv')

# S3 的用途
S3_USE_CASES = {
    "靜態網站托管": "HTML、圖片、影片",
    "備份與歸檔": "低成本長期儲存",
    "資料湖": "大規模資料存放",
    "靜態資源": "CDN 原始伺服器"
}
```

### Amazon EC2

```python
# 啟動 EC2 執行個體
import boto.ec2

conn = boto.ec2.connect_to_region('us-east-1')

# 啟動一個執行個體
reservation = conn.run_instances(
    'ami-12345678',  # Amazon Linux AMI
    key_name='my-key-pair',
    instance_type='m1.small',
    security_groups=['default']
)

instance = reservation.instances[0]
print("Instance ID:", instance.id)

# 等待執行個體運行
instance.update()
while instance.state != 'running':
    time.sleep(5)
    instance.update()

# 終止執行個體
# instance.terminate()
```

### SimpleDB

```python
# SimpleDB - NoSQL 資料庫服務
import boto.sdb

conn = boto.sdb.connect_to_region('us-east-1')

# 創建網域（類似資料表）
domain = conn.create_domain('Products')

# 新增項目
domain.put_attributes('item1', {
    'name': 'Widget',
    'price': 29.99,
    'category': 'Tools'
})

# 查詢
results = domain.select("SELECT * FROM Products WHERE price < 50")

for item in results:
    print(item.name, item['name'], item['price'])
```

## 雲端運算的商業模式

### 為何選擇雲端

```
┌────────────────────────────────────────────────────────┐
│            傳統 IT vs 雲端運算                         │
├────────────────────────────────────────────────────────┤
│                                                        │
│  傳統 IT：                                            │
│  - 預先購買硬體                                        │
│  - 需要預測容量                                        │
│  - 硬體採購數週到貨                                    │
│  - 閒置資源浪費                                        │
│  - 需要 IT 員工維護                                    │
│                                                        │
│  雲端運算：                                            │
│  - 按需使用                                             │
│  - 彈性擴展                                            │
│  - 幾分鐘內啟動                                        │
│  - 只付使用量                                           │
│  - 免費維護基礎設施                                    │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### AWS 的定價模型

```python
# EC2 按需定價範例（2007 年）
EC2_PRICING_2007 = {
    "Small Instance (m1.small)": "$0.10/hour",
    "Large Instance (m1.large)": "$0.40/hour",
    "Extra Large Instance (m1.xlarge)": "$0.80/hour"
}

# S3 定價
S3_PRICING_2007 = {
    "Storage": "$0.15/GB-month",
    "PUT requests": "$0.01/1000 requests",
    "GET requests": "$0.01/10000 requests"
}
```

## 雲端運算的用例

### 2007 年的典型應用

```python
# AWS 早期使用案例
EARLY_AWS_USE_CASES = {
    "靜態網站": [
        "個人部落格",
        "公司網站",
        " landing page"
    ],
    "開發/測試": [
        "快速環境架設",
        "自動測試",
        "原型開發"
    ],
    "資料處理": [
        "日誌分析",
        "備份",
        "科學計算"
    ],
    "Web 應用": [
        "電子商務",
        "SaaS 應用",
        "行動後端"
    ]
}
```

### 新創公司的最愛

雲端運算特別適合新創公司：

```
┌────────────────────────────────────────────────────────┐
│          新創公司使用雲端的優勢                         │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 最低前期成本                                       │
│     └─ 不需要購買伺服器                                 │
│                                                        │
│  2. 快速擴展                                          │
│     └─ 產品上線後可快速因應流量                        │
│                                                        │
│  3. 全球部署                                          │
│     └─ 幾分鐘內在多個地區部署                          │
│                                                        │
│  4. 專注產品                                           │
│     └─ 讓 AWS 處理基礎設施                             │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 競爭對手

### 2007 年的雲端市場

```python
# 2007 年雲端服務競爭者
CLOUD_COMPETITORS = {
    "Google": {
        "服務": "Google App Engine (2008)",
        "特點": "Python 支援、平台服務"
    },
    "Microsoft": {
        "服務": "Windows Azure (2008)",
        "特點": ".NET 整合、企業市場"
    },
    "Salesforce": {
        "服務": "Force.com",
        "特點": "SaaS 平台"
    },
    "Rackspace": {
        "服務": "Cloud Servers",
        "特點": "開放雲端"
    }
}
```

## 安全性與合規

### 早期的安全疑慮

2007 年，許多企業對雲端運算的安全性仍有疑慮：

```python
# 2007 年的安全考量
SECURITY_CONCERNS = {
    "資料保護": "資料存在第三方伺服器",
    "隱私": "是否會被存取",
    "合規": "是否滿足法規要求",
    "可用性": "網路中斷怎麼辦",
    "鎖定": "是否被單一廠商綁定"
}

# AWS 的回應
AWS_SECURITY_FEATURES = {
    "實體安全": "資料中心多重保護",
    "傳輸加密": "SSL/TLS 加密",
    " IAM": "身份存取管理（後來推出）",
    "防火牆": "Security Groups",
    "備份": "跨區域複製"
}
```

## 對產業的影響

### 雲端運算的長期影響

```
┌────────────────────────────────────────────────────────┐
│          雲端運算對 IT 產業的影響                       │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 降低進入門檻                                       │
│     └─ 任何人可以用低成本架設服務                       │
│                                                        │
│  2. 改變 IT 採購模式                                   │
│     └─ 從資本支出轉為運營支出                          │
│                                                        │
│  3. 推動 DevOps 運動                                  │
│     └─ 開發與維運的整合                                │
│                                                        │
│  4. 催生新商業模式                                     │
│     └─ SaaS、訂閱制                                   │
│                                                        │
│  5. 促進全球化                                         │
│     └─ 全球部署變得簡單                               │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 結論

2007 年是雲端運算從概念走向實際應用的關鍵一年。Amazon AWS 的先驅努力為這個產業樹立了標準，也為日後數十年的軟體部署方式奠定了基礎。

雲端運算不僅是技術創新，更是商業模式的創新。它改變了我們思考 IT 基礎設施的方式，讓任何人都能以低成本實現全球規模的服務。

---

## 延伸閱讀

- [Amazon AWS 歷史](https://www.google.com/search?q=Amazon+AWS+history+2007)
- [雲端運算概念](https://www.google.com/search?q=cloud+computing+basics)
- [EC2 發布](https://www.google.com/search?q=Amazon+EC2+launch+2007)

---

*本篇文章為「AI 程式人雜誌 2007 年 1 月號」文章集錦系列。*