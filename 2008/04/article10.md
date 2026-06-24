# 雲端運算與大數據的結合

## 雲端運算概述

2008 年，雲端運算從概念走向實際應用。Amazon Web Services (AWS) 引領潮流，提供一系列雲端服務。

### 雲端服務模型

```
┌─────────────────────────────────────────────┐
│              雲端運算架構                      │
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │         SaaS（軟體即服務）             │   │
│  │      Google Apps, Salesforce         │   │
│  └─────────────────────────────────────┘   │
│  ┌─────────────────────────────────────┐   │
│  │         PaaS（平台即服務）             │   │
│  │     Google App Engine, Heroku        │   │
│  └─────────────────────────────────────┘   │
│  ┌─────────────────────────────────────┐   │
│  │         IaaS（基礎設施即服務）          │   │
│  │       AWS EC2, S3, Google Cloud       │   │
│  └─────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

## AWS 服務

### 彈性運算雲（EC2）

```python
import boto

# 啟動實例（示意）
ec2 = boto.connect_ec2()
reservation = ec2.run_instances(
    'ami-12345678',
    instance_type='m1.small',
    count=1
)
```

### 簡單儲存服務（S3）

```python
import boto

# 上傳檔案
s3 = boto.connect_s3()
bucket = s3.get_bucket('my-bucket')
key = bucket.new_key('data/file.txt')
key.set_contents_from_string('Hello, Cloud!')

# 下載檔案
content = key.get_contents_as_string()
```

### SimpleDB

```python
# 儲存與查詢
sdb = boto.connect_sdb()
domain = sdb.create_domain('my-domain')

# 儲存項目
domain.put_attributes('item1', {
    'name': 'test',
    'value': 100
})

# 查詢
results = domain.select("SELECT * FROM my-domain WHERE value > 50")
```

## 雲端大數據平台

### Amazon Elastic MapReduce

```python
# 創建 EMR 叢集
emr = boto.connect_emr()
cluster = emr.run_jobflow(
    name='My Hadoop Cluster',
    instances={
        'InstanceCount': 5,
        'MasterInstanceType': 'm1.small',
        'SlaveInstanceType': 'm1.small'
    },
    hive_interactive_steps=[],
    enable_debugging=True
)
```

### Google App Engine

- 自動擴展
- 無需伺服器管理
- 支援 Python、Java

## 大數據的雲端化優勢

### 彈性擴展

```python
# 根據負載自動調整
if current_load > threshold:
    scale_up()
else:
    scale_down()
```

### 成本優化

| 模型 | 優勢 |
|------|------|
| 按需付費 | 只需支付實際使用量 |
| 預留實例 | 長期使用折扣 |
| 競價實例 | 可中斷工作低價使用 |

### 快速部署

```bash
# 使用 Hadoop AMIs
aws emr create-cluster \
    --release-label emr-5.30.0 \
    --instance-type m5.xlarge \
    --instance-count 5
```

## 雲端機器學習

### Amazon Machine Learning

```python
import boto3

ml = boto3.client('machinelearning')

# 建立模型
ml.create_ml_model(
    MLModelId='my-model',
    MLModelType='REGRESSION',
    TrainingDataSourceId='my-datasource'
)
```

### 預訓練模型服務

- Google Prediction API
- Amazon Rekognition
- Microsoft Azure ML

## 安全與合規

### 雲端安全

```python
# 加密資料
s3.put_object(
    Bucket='my-bucket',
    Key='secure-data',
    Body=encrypted_data,
    ServerSideEncryption='AES256'
)
```

### 存取控制

```python
# IAM 政策
iam = boto3.client('iam')
policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": ["s3:GetObject"],
        "Resource": "arn:aws:s3:::my-bucket/*"
    }]
}
```

## 未來趨勢

### 多雲端策略

越來越多企業採用多雲端策略，避免供應商鎖定。

### 邊緣計算

在資料來源附近進行處理，減少延遲。

### 無伺服器架構

AWS Lambda、Google Cloud Functions 興起。

## 結論

雲端運算與大數據的結合，改變了企業處理和分析資料的方式。雲端平台提供了幾乎無限的計算和儲存能力，讓小規模團隊也能處理 PB 等級的資料。

---

**延伸閱讀**

- [Hadoop 與巨量資料處理](focus.md)
- [Cloud+computing+big+data](https://www.google.com/search?q=cloud+computing+big+data+2008)