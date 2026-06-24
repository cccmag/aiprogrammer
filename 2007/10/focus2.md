# AWS S3 與 EC2：Amazon 的雲端服務

## Amazon Web Services 概述

2006 年 3 月，Amazon 推出了 S3（Simple Storage Service）；2006 年 8 月，推出了 EC2（Elastic Compute Cloud）。到 2007 年，AWS 已成為雲端運算的事實標準。

## Amazon S3

### S3 的核心概念

```python
# S3 基本操作（使用 boto）
import boto
import boto.s3

# 連接到 S3
conn = boto.connect_s3('AWS_ACCESS_KEY', 'AWS_SECRET_KEY')

# 建立桶（Bucket）
bucket = conn.create_bucket('my-unique-bucket-name')

# 上傳檔案
key = bucket.new_key('photos/vacation.jpg')
key.set_contents_from_filename('vacation.jpg')
key.set_acl('public-read')
```

### S3 的定價模型

```bash
# S3 定價（2007 年）
# 儲存：$0.15/GB/月
# 傳入：$0.10/GB
# 傳出：$0.10-$0.18/GB（根據數量）
# PUT/DELETE/GET：$0.01-$0.0001（根據請求數）
```

### S3 的用途

```python
# 常見用途
# 1. 靜態網站托管
# 2. 資料備份
# 3. 檔案分享
# 4. 媒體儲存
# 5. 日誌儲存
```

## Amazon EC2

### EC2 的核心概念

```python
# EC2 基本操作
import boto.ec2

# 啟動實例
conn = boto.ec2.connect_to_region('us-east-1')
reservation = conn.run_instances(
    'ami-12345',           # AMI ID
    key_name='my-key',
    instance_type='t1.micro',
    security_groups=['default']
)

instance = reservation.instances[0]
print('Instance ID:', instance.id)
```

### EC2 的彈性

```bash
# EC2 的彈性特性
# - 可以根據需求啟動/終止實例
# - 可以動態調整實例數量
# - 支援多種實例類型
# - 按小時計費
```

### Amazon Machine Image (AMI)

```bash
# AMI 的類型
# 1. Amazon 提供的 AMI
# 2. 社群 AMI
# 3. 自訂 AMI

# 建立自訂 AMI
ec2.create_image(instance_id, 'My Custom AMI')
```

## AWS 的影響

### AWS 的創新

```
AWS 的創新：
─────────────
1. 按使用量計費
2. 自助式服務
3. 全球分布
4. API 驅動
5. 開放生態系統
```

## 結語

Amazon AWS 的成功催生了雲端運算產業。S3 和 EC2 證明了雲端服務的可行性，為後續的 Google App Engine、Microsoft Azure 等樹立了典範。

---

## 延伸閱讀

- [Amazon+AWS+S3+EC2+2007](https://www.google.com/search?q=Amazon+AWS+S3+EC2+2007)

---