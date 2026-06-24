# 文章 7：AWS EC2 與 RDS

## 部署運算與資料庫服務

AWS EC2 提供可擴展的虛擬伺服器，而 RDS 則簡化了關聯式資料庫的管理。本文示範如何在 AWS 上部署 EC2 與 RDS。

### EC2 執行個體設定

#### 啟動 EC2

```javascript
import { EC2, DescribeInstancesCommand } from '@aws-sdk/client-ec2'
import { SSM } from '@aws-sdk/client-ssm'

const ec2 = new EC2({ region: 'ap-northeast-1' })

async function launchWebServer() {
  const result = await ec2.runInstances({
    ImageId: 'ami-0abcdef1234567890',
    InstanceType: 't3.micro',
    MinCount: 1,
    MaxCount: 1,
    KeyName: 'my-key',
    SecurityGroups: ['web-sg'],
    UserData: Buffer.from(`#!/bin/bash
      yum update -y
      yum install -y nodejs
      mkdir -p /home/ec2-user/app
      cd /home/ec2-user/app
      npm init -y
      npm install express pg
    `).toString('base64'),
    TagSpecifications: [{
      ResourceType: 'instance',
      Tags: [{ Key: 'Name', Value: 'web-server-1' }]
    }]
  })

  const instanceId = result.Instances[0].InstanceId
  console.log('EC2 啟動中:', instanceId)

  // 等待執行個體就緒
  await ec2.waitFor('instanceRunning', { InstanceIds: [instanceId] })
  const desc = await ec2.describeInstances({ InstanceIds: [instanceId] })
  const publicIp = desc.Reservations[0].Instances[0].PublicIpAddress
  console.log('Public IP:', publicIp)

  return { instanceId, publicIp }
}
```

#### 安全群組設定

```javascript
import { EC2 } from '@aws-sdk/client-ec2'
const ec2 = new EC2({ region: 'ap-northeast-1' })

async function createWebSecurityGroup() {
  const { GroupId } = await ec2.createSecurityGroup({
    GroupName: 'web-sg',
    Description: 'Web server security group'
  })

  await ec2.authorizeSecurityGroupIngress({
    GroupId,
    IpPermissions: [
      {
        IpProtocol: 'tcp',
        FromPort: 22,
        ToPort: 22,
        IpRanges: [{ CidrIp: '203.0.113.0/32', Description: 'SSH' }]
      },
      {
        IpProtocol: 'tcp',
        FromPort: 80,
        ToPort: 80,
        IpRanges: [{ CidrIp: '0.0.0.0/0', Description: 'HTTP' }]
      },
      {
        IpProtocol: 'tcp',
        FromPort: 443,
        ToPort: 443,
        IpRanges: [{ CidrIp: '0.0.0.0/0', Description: 'HTTPS' }]
      }
    ]
  })

  return GroupId
}
```

### RDS 資料庫設定

```javascript
import { RDS } from '@aws-sdk/client-rds'

const rds = new RDS({ region: 'ap-northeast-1' })

async function createDatabase() {
  const result = await rds.createDBInstance({
    DBInstanceIdentifier: 'app-db',
    DBInstanceClass: 'db.t3.micro',
    Engine: 'postgres',
    EngineVersion: '16.1',
    MasterUsername: 'dbadmin',
    MasterUserPassword: process.env.DB_PASSWORD,
    AllocatedStorage: 20,
    StorageType: 'gp3',
    VpcSecurityGroupIds: ['sg-database'],
    DBSubnetGroupName: 'my-subnet-group',
    BackupRetentionPeriod: 7,
    PreferredBackupWindow: '03:00-04:00',
    PreferredMaintenanceWindow: 'Sun:05:00-Sun:06:00',
    MultiAZ: true,
    StorageEncrypted: true,
    DeletionProtection: true
  })

  const endpoint = result.DBInstance.Endpoint
  console.log('RDS Endpoint:', endpoint.Address)

  return endpoint
}
```

### EC2 連線 RDS

```javascript
import pg from 'pg'

async function connectAppToDB() {
  const pool = new pg.Pool({
    host: process.env.RDS_ENDPOINT,
    port: 5432,
    database: 'appdb',
    user: 'dbadmin',
    password: process.env.DB_PASSWORD,
    ssl: { rejectUnauthorized: true },
    max: 10
  })

  // 測試連線
  const { rows: [{ version }] } = await pool.query('SELECT version()')
  console.log('RDS 連線成功:', version)

  return pool
}
```

### 自動擴展設定

```javascript
import { AutoScaling } from '@aws-sdk/client-auto-scaling'

const asg = new AutoScaling({ region: 'ap-northeast-1' })

async function setupAutoScaling() {
  // 建立啟動模板
  await asg.createAutoScalingGroup({
    AutoScalingGroupName: 'web-asg',
    LaunchTemplate: {
      LaunchTemplateName: 'web-template',
      Version: '$Default'
    },
    MinSize: 2,
    MaxSize: 10,
    DesiredCapacity: 2,
    VPCZoneIdentifier: 'subnet-xxx,subnet-yyy',
    TargetGroupARNs: ['arn:aws:elasticloadbalancing:...']
  })

  // 擴展策略
  await asg.putScalingPolicy({
    AutoScalingGroupName: 'web-asg',
    PolicyName: 'cpu-target',
    PolicyType: 'TargetTrackingScaling',
    TargetTrackingConfiguration: {
      PredefinedMetricSpecification: {
        PredefinedMetricType: 'ASGAverageCPUUtilization'
      },
      TargetValue: 70
    }
  })
}
```

延伸閱讀：https://www.google.com/search?q=AWS+EC2+RDS+tutorial+deploy+2024
https://www.google.com/search?q=AWS+auto+scaling+best+practices
