# 專題 5：AWS 雲端服務概覽

## 亞馬遜雲端服務生態系統

AWS（Amazon Web Services）是全球最大的雲端服務平台，提供超過 200 項雲端服務，涵蓋運算、儲存、資料庫、機器學習、分析等領域。

### 核心服務分類

#### 運算服務

- **EC2 (Elastic Compute Cloud)**：可調整規模的虛擬伺服器，支援多種執行個體類型
- **Lambda**：無伺服器函數運算，按執行次數計費
- **ECS/EKS**：容器編排服務，支援 Docker 與 Kubernetes
- **Elastic Beanstalk**：平台即服務，簡化應用部署

```javascript
// AWS SDK 建立 EC2 執行個體
import { EC2 } from '@aws-sdk/client-ec2'
const ec2 = new EC2({ region: 'ap-northeast-1' })

async function createInstance() {
  const result = await ec2.runInstances({
    ImageId: 'ami-0abcdef1234567890',
    InstanceType: 't3.micro',
    MinCount: 1,
    MaxCount: 1,
    KeyName: 'my-key-pair',
    SecurityGroups: ['web-server-sg']
  })
  console.log('EC2 Instance ID:', result.Instances[0].InstanceId)
}
```

#### 資料庫服務

- **RDS (Relational Database Service)**：託管關聯式資料庫，支援 MySQL、PostgreSQL、MariaDB、Oracle、SQL Server
- **DynamoDB**：全託管 NoSQL 鍵值與文件資料庫
- **ElastiCache**：託管 Redis 與 Memcached 快取服務
- **Aurora**：與 MySQL/PostgreSQL 相容的高效能關聯式資料庫
- **Redshift**：雲端資料倉儲服務

```javascript
// 建立 RDS 執行個體
import { RDS } from '@aws-sdk/client-rds'
const rds = new RDS({ region: 'ap-northeast-1' })

await rds.createDBInstance({
  DBInstanceIdentifier: 'mydb',
  DBInstanceClass: 'db.t3.micro',
  Engine: 'postgres',
  MasterUsername: 'admin',
  MasterUserPassword: 'password123',
  AllocatedStorage: 20
})
```

#### 儲存與內容傳遞

- **S3 (Simple Storage Service)**：物件儲存，無限擴展
- **CloudFront**：內容傳遞網路 (CDN)
- **EBS (Elastic Block Store)**：區塊儲存，用於 EC2
- **EFS (Elastic File System)**：共用檔案系統

### 安全與身分

- **IAM (Identity and Access Management)**：使用權限管理
- **KMS (Key Management Service)**：加密金鑰管理
- **WAF (Web Application Firewall)**：Web 應用防火牆
- **Security Hub**：安全狀態集中管理

### AWS 架構最佳實踐

1. **高可用性**：跨可用區部署，使用負載平衡器
2. **自動擴展**：根據負載自動調整資源
3. **成本最佳化**：使用預留執行個體與節點類型
4. **安全防護**：最小權限原則，啟用加密
5. **可觀測性**：使用 CloudWatch 監控與日誌

### 學習路徑

1. 從 AWS Free Tier 開始免費試用
2. 完成 AWS 數位課程與實作實驗室
3. 取得 AWS 認證（如 Solutions Architect Associate）
4. 參與 AWS re:Invent 年度大會

延伸閱讀：https://www.google.com/search?q=AWS+cloud+services+overview+2024
https://www.google.com/search?q=AWS+database+services+comparison
