# 雲端安全與存取控制

## 雲端安全的基礎

雲端安全包括身份識別、資料保護、網路安全和合規性。雲端供應商和客戶共同分擔安全責任。

## 身份與存取管理（IAM）

### 基本概念

- **身份（Identity）**：用戶、服務或系統
- **權限（Permission）**：允許的動作
- **角色（Role）**：權限的集合

### AWS IAM 範例

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::mybucket/*"
    }
  ]
}
```

## 最小權限原則

只授予執行任務所需的最小權限：

```yaml
# Kubernetes RBAC
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-reader
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list"]
```

## 密鑰管理

### 使用密鑰管理服務

```python
import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']
```

###  Kubernetes Secrets

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
data:
  password: cGFzc3dvcmQ=  # base64 編碼
```

## 網路安全

### 網路隔離

```yaml
# VPC 網路設定
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    name: production
```

### 輸入流量控制

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 8000
```

## 容器安全

### 不要以 root 執行

```dockerfile
FROM python:3.9-slim
RUN useradd -m appuser
USER appuser
CMD ["python", "app.py"]
```

### 映像檔掃描

```bash
# 使用 Trivy 掃描漏洞
trivy image myapp:latest
```

## 合規性與審計

- 啟用所有服務的審計日誌
- 定期審查存取權限
- 使用雲端安全態勢管理（CSPM）工具

## 結論

雲端安全是每個使用雲端服務的組織都需要關注的問題。實施最小權限原則、加密敏感資料、定期審計，是保護雲端環境的關鍵。