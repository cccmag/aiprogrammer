# 文章 9：資料庫備份策略

## 保護你的資料資產

資料備份是資料庫管理中最關鍵的任務之一。完善的備份策略能在災難發生時將資料損失降到最低。本文探討各種資料庫備份方法與實作。

### 備份類型

#### 邏輯備份
以 SQL 語句或 JSON 格式匯出資料，適合跨版本或跨平台遷移。

```javascript
import { execSync } from 'child_process'
import fs from 'fs'
import path from 'path'

// PostgreSQL pg_dump 邏輯備份
async function logicalBackup(config) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
  const filename = `backup_${config.dbName}_${timestamp}.sql`
  const filepath = path.join('/backups', filename)

  try {
    execSync(
      `pg_dump -h ${config.host} -U ${config.user} ` +
      `-d ${config.dbName} -F p -f ${filepath}`,
      { env: { PGPASSWORD: config.password } }
    )

    const stats = fs.statSync(filepath)
    console.log(`邏輯備份完成: ${filename} (${(stats.size / 1024 / 1024).toFixed(2)} MB)`)

    return filepath
  } catch (err) {
    console.error('備份失敗:', err.message)
    throw err
  }
}

// MongoDB mongodump
function mongoBackup(uri, outputDir) {
  execSync(
    `mongodump --uri="${uri}" --out=${outputDir}`,
    { stdio: 'inherit' }
  )
}
```

#### 實體備份
直接複製資料庫檔案，還原速度快，適合大型資料庫。

```javascript
// PostgreSQL 實體備份 (使用 pg_basebackup)
async function physicalBackup(config) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
  const backupDir = `/backups/physical_${timestamp}`

  execSync(
    `pg_basebackup -h ${config.host} -U ${config.user} ` +
    `-D ${backupDir} -F t -z -P --wal-method=stream`,
    { env: { PGPASSWORD: config.password } }
  )

  console.log(`實體備份完成: ${backupDir}`)
  return backupDir
}
```

### 自動化備份系統

```javascript
class BackupManager {
  constructor(config) {
    this.config = config
    this.s3 = new S3Client({ region: config.awsRegion })
  }

  async runFullBackup() {
    const filepath = await logicalBackup(this.config)

    // 上傳到 S3
    const key = `backups/${this.config.dbName}/full/${path.basename(filepath)}`
    await this.uploadToS3(filepath, key)

    // 上傳到備用區域
    if (this.config.replicaRegion) {
      await this.uploadToS3(filepath, key, this.config.replicaRegion)
    }

    // 清理舊備份
    await this.cleanupOldBackups()

    return { filepath, key }
  }

  async uploadToS3(filepath, key, region) {
    const s3 = region
      ? new S3Client({ region })
      : this.s3

    await s3.send(new PutObjectCommand({
      Bucket: this.config.s3Bucket,
      Key: key,
      Body: fs.createReadStream(filepath),
      ServerSideEncryption: 'AES256',
      StorageClass: 'STANDARD_IA'
    }))

    console.log(`上傳完成: s3://${this.config.s3Bucket}/${key}`)
  }

  async cleanupOldBackups() {
    const retentionDays = this.config.retentionDays || 30
    const cutoff = new Date(Date.now() - retentionDays * 86400000)

    const { Contents } = await this.s3.send(new ListObjectsV2Command({
      Bucket: this.config.s3Bucket,
      Prefix: `backups/${this.config.dbName}/full/`
    }))

    const toDelete = Contents
      .filter(obj => obj.LastModified < cutoff)
      .map(obj => ({ Key: obj.Key }))

    if (toDelete.length > 0) {
      await this.s3.send(new DeleteObjectsCommand({
        Bucket: this.config.s3Bucket,
        Delete: { Objects: toDelete }
      }))
      console.log(`清理了 ${toDelete.length} 個舊備份`)
    }
  }
}
```

### 還原測試

定期測試備份的可用性至關重要：

```javascript
async function testRestore(config, backupFile) {
  const testDbName = `${config.dbName}_test_restore`

  // 建立測試資料庫
  execSync(`createdb -h ${config.host} -U ${config.user} ${testDbName}`, {
    env: { PGPASSWORD: config.password }
  })

  try {
    // 還原備份到測試資料庫
    execSync(
      `psql -h ${config.host} -U ${config.user} -d ${testDbName} -f ${backupFile}`,
      { env: { PGPASSWORD: config.password } }
    )

    // 驗證資料完整性
    const result = execSync(
      `psql -h ${config.host} -U ${config.user} -d ${testDbName} ` +
      `-c "SELECT count(*) AS total_tables FROM information_schema.tables WHERE table_schema = 'public'"`,
      { env: { PGPASSWORD: config.password } }
    )
    console.log('還原測試結果:', result.toString())
  } finally {
    // 清理測試資料庫
    execSync(`dropdb -h ${config.host} -U ${config.user} ${testDbName}`, {
      env: { PGPASSWORD: config.password }
    })
  }
}
```

### 備份策略總結

| 策略 | RPO (復原點目標) | RTO (復原時間目標) | 適合場景 |
|------|-----------------|-------------------|---------|
| 每日完整備份 | 24 小時 | 2-4 小時 | 小型資料庫 |
| 完整+增量 | 1 小時 | 4-8 小時 | 中型資料庫 |
| 完整+WAL 歸檔 | 秒級 | 1-2 小時 | 大型重要資料庫 |
| 持續複寫 | 秒級 | 分鐘級 | 關鍵業務系統 |

延伸閱讀：https://www.google.com/search?q=database+backup+strategy+best+practices+2024
https://www.google.com/search?q=disaster+recovery+database+RPO+RTO+guide
