# 文章 10：雲端成本最佳化

## 聰明使用雲端服務

隨著雲端採用率不斷提升，成本管理已成為企業關注的焦點。不當的雲端資源配置可能導致驚人的費用。本文分享雲端成本最佳化的策略與實務。

### 了解雲端計費模型

雲端供應商通常採用隨用隨付 (Pay-as-you-go) 模式，但不同服務的計價方式差異很大：

- **運算資源**：按執行個體類型與運行時間計費
- **儲存空間**：按儲存量、存取頻率與資料傳輸計費
- **資料庫服務**：按執行個體規格、儲存空間與 I/O 次數計費
- **網路傳輸**：區域內免費，跨區域與網際網路傳輸收費

```javascript
// AWS 成本分析工具
import { CostExplorer } from '@aws-sdk/client-cost-explorer'

const ce = new CostExplorer({ region: 'us-east-1' })

async function analyzeMonthlyCost() {
  const now = new Date()
  const startDate = new Date(now.getFullYear(), now.getMonth() - 1, 1)
    .toISOString().split('T')[0]
  const endDate = now.toISOString().split('T')[0]

  const result = await ce.getCostAndUsage({
    TimePeriod: { Start: startDate, End: endDate },
    Granularity: 'DAILY',
    Metrics: ['BlendedCost'],
    GroupBy: [{ Type: 'DIMENSION', Key: 'SERVICE' }]
  })

  result.ResultsByTime.forEach(day => {
    console.log(`日期: ${day.TimePeriod.Start}`)
    day.Groups.forEach(group => {
      const cost = parseFloat(group.Metrics.BlendedCost.Amount)
      if (cost > 0) {
        console.log(`  ${group.Keys[0]}: $${cost.toFixed(2)}`)
      }
    })
  })
}
```

### 運算成本最佳化

```javascript
// 使用 Spot 執行個體降低成本
async function launchSpotInstance() {
  const ec2 = new EC2({ region: 'ap-northeast-1' })

  const result = await ec2.requestSpotInstances({
    SpotPrice: '0.05',
    InstanceCount: 3,
    LaunchSpecification: {
      ImageId: 'ami-xxx',
      InstanceType: 't3.medium',
      SecurityGroups: ['web-sg']
    },
    ValidUntil: new Date(Date.now() + 86400000).toISOString()
  })

  console.log('Spot 請求已提交:', result.SpotInstanceRequests)
}

// 排程自動關閉非生產環境
// 使用 AWS Lambda + CloudWatch Events
async function scheduleInstanceManagement() {
  const ec2 = new EC2({ region: 'ap-northeast-1' })

  // 晚間 8 點停止開發環境
  const stopCommand = async () => {
    const { Reservations } = await ec2.describeInstances({
      Filters: [
        { Name: 'tag:Environment', Values: ['dev', 'staging'] },
        { Name: 'instance-state-name', Values: ['running'] }
      ]
    })

    const instances = Reservations.flatMap(r =>
      r.Instances.map(i => i.InstanceId)
    )

    if (instances.length > 0) {
      await ec2.stopInstances({ InstanceIds: instances })
      console.log(`已停止 ${instances.length} 個執行個體`)
    }
  }

  // 早上 8 點啟動開發環境
  const startCommand = async () => { /* 類似邏輯 */ }
}
```

### 資料庫成本最佳化

```javascript
// RDS 執行個體類型調整建議
class RDSCostOptimizer {
  constructor(rds) {
    this.rds = rds
  }

  async analyzeInstances() {
    const { DBInstances } = await this.rds.describeDBInstances()

    for (const instance of DBInstances) {
      const metrics = await this.getMetrics(instance.DBInstanceIdentifier)
      const recommendation = this.generateRecommendation(instance, metrics)

      if (recommendation.action) {
        console.log(`${instance.DBInstanceIdentifier}: ${recommendation.action}`)
      }
    }
  }

  generateRecommendation(instance, metrics) {
    const cpuAvg = metrics.CPUUtilization?.Average || 0
    const connectionsAvg = metrics.DatabaseConnections?.Average || 0

    // CPU 使用率持續低於 20%，建議降級
    if (cpuAvg < 20 && instance.DBInstanceClass.includes('large')) {
      return {
        action: '建議降級執行個體類型',
        current: instance.DBInstanceClass,
        suggestion: instance.DBInstanceClass.replace('large', 'small')
      }
    }

    // 空閒執行個體建議刪除
    if (cpuAvg < 1 && connectionsAvg < 1) {
      return {
        action: '建議刪除或停止閒置資料庫',
        instance: instance.DBInstanceIdentifier
      }
    }

    return { action: null }
  }

  async getMetrics(instanceId) {
    const cloudwatch = new CloudWatch({ region: 'ap-northeast-1' })
    // 實作 CloudWatch 指標查詢
    return {}
  }
}

// 使用預留執行個體節省成本
async function purchaseReservedInstance() {
  const rds = new RDS({ region: 'ap-northeast-1' })

  const result = await rds.purchaseReservedDBInstancesOffering({
    ReservedDBInstancesOfferingId: 'rio-xxx',
    DBInstanceCount: 2
  })

  console.log('預留執行個體已購買:', result.ReservedDBInstance)
}
```

### 儲存成本最佳化

```javascript
// S3 生命週期規則自動轉換儲存類別
async function setupLifecyclePolicy(bucketName) {
  const s3 = new S3({ region: 'ap-northeast-1' })

  await s3.putBucketLifecycleConfiguration({
    Bucket: bucketName,
    LifecycleConfiguration: {
      Rules: [
        {
          Id: 'transition-to-IA',
          Status: 'Enabled',
          Prefix: 'logs/',
          Transitions: [
            { Days: 30, StorageClass: 'STANDARD_IA' },
            { Days: 90, StorageClass: 'GLACIER' }
          ],
          Expiration: { Days: 365 }
        }
      ]
    }
  })

  console.log(`生命週期規則已套用至 ${bucketName}`)
}
```

### FinOps 最佳實踐

1. **可視性**：建立成本儀表板，即時監控雲端支出
2. **標籤管理**：為所有資源加上專案/環境/部門標籤
3. **預算告警**：設定預算上限與超額通知
4. **定期審查**：每週檢視異常用量與浪費
5. **右寸調整**：根據實際使用量調整執行個體大小
6. **承諾折扣**：利用預留執行個體與節省方案

```javascript
// 設定預算告警
async function setBudgetAlert() {
  const budgets = new Budgets({ region: 'us-east-1' })

  await budgets.createBudget({
    AccountId: process.env.AWS_ACCOUNT_ID,
    Budget: {
      BudgetName: 'monthly-cloud-budget',
      BudgetLimit: { Amount: 5000, Unit: 'USD' },
      BudgetType: 'COST',
      TimeUnit: 'MONTHLY',
      CostFilters: { TagKeyValue: ['project:myapp'] }
    },
    NotificationsWithSubscribers: [{
      Notification: {
        NotificationType: 'ACTUAL',
        ComparisonOperator: 'GREATER_THAN',
        Threshold: 80,
        ThresholdType: 'PERCENTAGE'
      },
      Subscribers: [{
        SubscriptionType: 'EMAIL',
        Address: 'team@example.com'
      }]
    }]
  })
}
```

延伸閱讀：https://www.google.com/search?q=cloud+cost+optimization+best+practices+2024
https://www.google.com/search?q=AWS+FinOps+tools+and+strategies
