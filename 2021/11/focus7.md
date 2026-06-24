# 雲端原生儲存與資料管理

## 雲端儲存的類型

雲端儲存可分為：
- **區塊儲存**：提供原始磁碟區，適合資料庫
- **檔案儲存**：提供檔案系統介面，適合共享檔案
- **物件儲存**：通過 API 存取，適合非結構化資料

## Kubernetes 儲存抽象

### PersistentVolume（PV）

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  awsElasticBlockStore:
    volumeID: vol-12345678
    fsType: ext4
```

### PersistentVolumeClaim（PVC）

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

## StatefulSet

有狀態應用需要 StatefulSet：

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
spec:
  serviceName: mysql
  replicas: 3
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:8.0
        volumeMounts:
        - name: data
          mountPath: /var/lib/mysql
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

## 物件儲存

### S3 操作範例

```python
import boto3

s3 = boto3.client('s3')

# 上傳檔案
s3.upload_file('local.txt', 'my-bucket', 'remote.txt')

# 下載檔案
s3.download_file('my-bucket', 'remote.txt', 'local.txt')

# 生成預簽名 URL
url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'my-bucket', 'Key': 'remote.txt'}
)
```

## 資料備份策略

### Kubernetes 備份工具 Velero

```bash
# 安裝 Velero
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.2.0 \
  --bucket my-backups \
  --backup-location-config region=us-west-2 \
  --snapshot-location-config region=us-west-2

# 建立備份
velero backup create my-backup --include-namespaces myapp

# 恢復
velero restore create --from-backup my-backup
```

## 結論

雲端原生儲存需要仔細規劃：選擇合適的儲存類型、設計資料持久化策略、建立備份機制。這些都是確保應用資料安全的關鍵。