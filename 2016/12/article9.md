# 雲端運算的 2016

## 前言

2016 年是雲端運算持續爆發的一年。AWS、Azure 和 Google Cloud Platform 三大公有雲提供商競爭激烈，湧現了許多新服務和功能。

## 三大雲端提供商

```python
cloud_providers = {
    'AWS': {
        'company': 'Amazon',
        'strengths': ['最成熟', '服務最多', '生態完善'],
        'key_2016': ['Lambda', 'ECS', 'EKS', 'Athena'],
    },
    'Azure': {
        'company': 'Microsoft',
        'strengths': ['企業市場', 'Windows 整合', '混合雲'],
        'key_2016': ['Azure Functions', 'Service Fabric', 'Cosmos DB'],
    },
    'GCP': {
        'company': 'Google',
        'strengths': ['機器學習', '資料分析', 'Kubernetes'],
        'key_2016': ['Cloud Functions', 'BigQuery', 'TensorFlow on GCP'],
    },
}
```

## AWS 生態

### 核心服務

```python
aws_services = {
    'compute': ['EC2', 'Lambda', 'ECS', 'EKS', 'Lightsail'],
    'storage': ['S3', 'EBS', 'EFS', 'Glacier'],
    'database': ['RDS', 'DynamoDB', 'ElastiCache', 'Redshift'],
    'networking': ['VPC', 'Route 53', 'ELB', 'CloudFront'],
    'ai': ['Rekognition', 'Polly', 'Lex', 'SageMaker'],
}
```

### Lambda 無伺服器計算

```python
import boto3

def lambda_handler(event, context):
    """AWS Lambda 處理函式"""
    s3 = boto3.client('s3')

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    response = s3.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')

    return {
        'statusCode': 200,
        'body': f'Processed {key}, {len(content)} bytes'
    }
```

```yaml
# serverless.yml (使用 Serverless Framework)
service: my-service

provider:
  name: aws
  runtime: python3.9
  stage: dev
  region: us-east-1

functions:
  hello:
    handler: handler.hello
    events:
      - http:
          path: hello
          method: get
  processS3:
    handler: handler.process_s3
    events:
      - s3:
          bucket: my-bucket
          event: s3:ObjectCreated:*
```

### ECS 容器服務

```python
# ECS 任務定義
task_definition = {
    'family': 'myapp',
    'containerDefinitions': [
        {
            'name': 'web',
            'image': 'myrepo/myapp:latest',
            'memory': 256,
            'cpu': 256,
            'essential': True,
            'portMappings': [
                {
                    'containerPort': 80,
                    'hostPort': 80,
                    'protocol': 'tcp'
                }
            ]
        }
    ]
}

# 創建服務
ecs = boto3.client('ecs')
ecs.register_task_definition(**task_definition)
ecs.update_service(
    cluster='mycluster',
    service='myapp',
    taskDefinition='myapp',
    desiredCount=3
)
```

## Azure 生態

### 核心服務

```python
azure_services = {
    'compute': ['Virtual Machines', 'Azure Functions', 'App Service', 'Service Fabric'],
    'storage': ['Blob Storage', 'Queue Storage', 'Table Storage', 'Files'],
    'database': ['SQL Database', 'Cosmos DB', 'Redis Cache', 'SQL Data Warehouse'],
    'networking': ['Virtual Network', 'Load Balancer', 'Application Gateway', 'VPN Gateway'],
}
```

### Azure Functions

```python
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}")
    else:
        return func.HttpResponse(
            "Please pass a name on the query string or in the request body",
            status_code=400
        )
```

## Google Cloud Platform

### 核心服務

```python
gcp_services = {
    'compute': ['Compute Engine', 'App Engine', 'Cloud Functions', 'Kubernetes Engine'],
    'storage': ['Cloud Storage', 'Bigtable', 'Firestore', 'Dataflow'],
    'ai': ['Vision AI', 'Natural Language API', 'Speech-to-Text', 'AI Platform'],
    'bigdata': ['BigQuery', 'Dataflow', 'Dataproc', 'Pub/Sub'],
}
```

### BigQuery

```python
from google.cloud import bigquery

client = bigquery.Client()

query = """
SELECT
  COUNT(*) as total_rows,
  AVG(price) as avg_price
FROM `myproject.mydataset.mytable`
WHERE date >= '2026-01-01'
"""

query_job = client.query(query)
results = query_job.result()

for row in results:
    print(f"Total rows: {row.total_rows}, Avg price: {row.avg_price}")
```

## 容器化服務

### 雲端容器編排

```python
container_services = {
    'AWS': {
        'ECS': 'EC2 Container Service',
        'EKS': 'Elastic Container Service for Kubernetes',
        'Fargate': 'Serverless container platform',
    },
    'Azure': {
        'ACS': 'Azure Container Service',
        'AKS': 'Azure Kubernetes Service',
    },
    'GCP': {
        'GKE': 'Google Kubernetes Engine',
    },
}
```

## 雲端資料庫

```python
database_comparison = {
    'RDS': {'provider': 'AWS', 'type': '關聯式', 'engines': ['MySQL', 'PostgreSQL', 'Oracle', 'SQL Server']},
    'Aurora': {'provider': 'AWS', 'type': '關聯式', 'engines': ['MySQL', 'PostgreSQL']},
    'DynamoDB': {'provider': 'AWS', 'type': 'NoSQL', 'consistent': 'Eventually consistent']},
    'Cosmos DB': {'provider': 'Azure', 'type': 'NoSQL', 'apis': ['SQL', 'MongoDB', 'Cassandra']},
    'Bigtable': {'provider': 'GCP', 'type': 'Wide-column', 'use_cases': ['IoT', 'Analytics']},
    'BigQuery': {'provider': 'GCP', 'type': 'Data Warehouse', 'sql': True},
}
```

## Serverless 架構

```python
serverless_pattern = """
Serverless 架構模式：

┌─────────────┐
│   Client    │
└──────┬──────┘
       │
┌──────▼──────┐
│  API Gateway │
└──────┬──────┘
       │
┌──────▼──────┐
│   Functions │
│  (Lambda)   │
└──────┬──────┘
       │
┌──────▼──────┐
│  Cloud DB    │
│  (DynamoDB)  │
└─────────────┘

優點：
- 無需管理伺服器
- 自動擴縮
- 按使用付費
- 快速部署
"""
```

## 雲端安全

```python
cloud_security = {
    'IAM': '身份和訪問管理',
    'VPC': '虛擬私有雲',
    'Security Groups': '網路安全組',
    'KMS': '密鑰管理服務',
    'CloudTrail': '審計日誌',
    'WAF': 'Web 應用防火牆',
}
```

## 成本優化

```python
cost_optimization = {
    '策略': [
        '使用 Spot Instances 處理批次工作',
        '設置預留實例應對基本負載',
        '使用生命週期策略管理儲存',
        '啟用資源標籤追蹤成本',
        '使用 Auto Scaling 避免過度資源',
    ],
    '監控': [
        'AWS Cost Explorer',
        'Azure Cost Management',
        'GCP Billing Dashboard',
    ],
}
```

## 小結

2016 年雲端運算呈現三大趨勢：容器化服務的成熟、Serverless 架構的興起，以及 AI/ML 服務的普及。選擇雲端提供商時應根據具體需求，考慮服務完整性、定價模式和生態整合。

---

**延伸閱讀**

- [AWS Documentation](https://www.google.com/search?q=AWS+documentation)
- [Azure Documentation](https://www.google.com/search?q=Azure+documentation)
- [Google Cloud Documentation](https://www.google.com/search?q=Google+Cloud+documentation)