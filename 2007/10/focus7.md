# 雲端運算的實際應用案例

## 雲端服務使用場景

### 1. 靜態網站托管

```python
# 使用 S3 托管靜態網站
# 1. 建立 S3 bucket
# 2. 上傳 HTML/CSS/JS 檔案
# 3. 設定靜態网站托管
# 4. 設定 CloudFront CDN

bucket = s3.create_bucket('my-static-website')
for file in ['index.html', 'style.css', 'app.js']:
    key = bucket.new_key(file)
    key.set_contents_from_filename(file)
    key.set_acl('public-read')
```

### 2. 資料備份

```python
# 雲端備份策略
# 1. 本地資料加密
# 2. 上傳到 S3
# 3. 設定生命週期策略
# 4. 跨區域複寫

import hashlib

def backup_to_cloud(local_file, bucket):
    with open(local_file, 'rb') as f:
        data = f.read()
    hash = hashlib.sha256(data).hexdigest()
    key = bucket.new_key(f'backups/{hash}')
    key.set_contents_from_string(data)
    return hash
```

### 3. 巨量資料處理

```python
# 使用 EC2 + Hadoop 處理巨量資料
# 1. 啟動 EC2 叢集
# 2. 安裝 Hadoop
# 3. 執行 MapReduce 任務
# 4. 關閉叢集

class EMRJob:
    def __init__(self):
        self.cluster_id = None

    def start_cluster(self, num_instances=10):
        self.cluster_id = emr.run_jobflow(
            instances=num_instances,
            ami_version='2.0'
        )
        return self.cluster_id

    def run_mapreduce(self, mapper, reducer, input_data):
        # 執行 MapReduce 任務
        pass
```

### 4. 彈性 Web 服務

```python
# 使用 EC2 + Auto Scaling
# 1. 建立 Launch Configuration
# 2. 建立 Auto Scaling Group
# 3. 設定 Scale Out/In 策略
# 4. 關聯 Load Balancer

class AutoScaling:
    def __init__(self):
        self.min_size = 1
        self.max_size = 10
        self.desired_capacity = 2

    def scale_out(self):
        if self.desired_capacity < self.max_size:
            self.desired_capacity += 1

    def scale_in(self):
        if self.desired_capacity > self.min_size:
            self.desired_capacity -= 1
```

## 成本優化策略

```bash
# 雲端成本優化
# 1. 使用 Reserved Instances
# 2. 選擇適當的 instance type
# 3. 使用 Spot Instances 處理批次任務
# 4. 開啟 VPC endpoints 避免流量費用
# 5. 設定 billing alerts
```

## 結語

雲端運算的價值在於彈性和成本效益。透過適當的架構設計，可以充分發揮雲端的優勢。

---

## 延伸閱讀

- [cloud+computing+use+cases+2007](https://www.google.com/search?q=cloud+computing+use+cases+2007)
- [aws+s3+ec2+applications](https://www.google.com/search?q=aws+s3+ec2+applications)

---