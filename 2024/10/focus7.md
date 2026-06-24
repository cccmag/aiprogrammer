# 專題 7：資料庫遷移與備份

## 確保資料安全與業務連續性

資料庫遷移與備份是資料庫管理中最重要的兩個主題。無論是升級資料庫版本、更換資料庫平台，還是建立災難復原方案，都需要完善的遷移與備份策略。

### 資料庫遷移

#### 遷移類型

- **版本升級**：在同一資料庫產品中升級版本
- **平台遷移**：在不同資料庫產品之間遷移（如 MySQL 到 PostgreSQL）
- **架構遷移**：從自建到雲端託管（如 EC2 自建到 RDS）
- **雲端遷移**：從本地資料中心遷移到雲端

#### 遷移流程

```javascript
// 使用 Node.js 進行資料庫遷移腳本範例
async function migrateData() {
  const sourcePool = new pg.Pool({ connectionString: 'postgres://source/db' })
  const targetPool = new pg.Pool({ connectionString: 'postgres://target/db' })

  try {
    // 1. 建立目標資料表
    await targetPool.query(`CREATE TABLE IF NOT EXISTS users (
      id SERIAL PRIMARY KEY,
      name VARCHAR(100),
      email VARCHAR(255),
      created_at TIMESTAMP DEFAULT NOW()
    )`)

    // 2. 分批讀取來源資料
    let offset = 0
    const limit = 1000
    while (true) {
      const { rows } = await sourcePool.query(
        'SELECT * FROM users ORDER BY id LIMIT $1 OFFSET $2',
        [limit, offset]
      )
      if (rows.length === 0) break

      // 3. 寫入目標資料庫
      for (const row of rows) {
        await targetPool.query(
          'INSERT INTO users (id, name, email, created_at) VALUES ($1, $2, $3, $4) ON CONFLICT (id) DO NOTHING',
          [row.id, row.name, row.email, row.created_at]
        )
      }
      offset += limit
      console.log(`已遷移 ${offset} 筆資料`)
    }
    console.log('遷移完成')
  } finally {
    await sourcePool.end()
    await targetPool.end()
  }
}
```

#### 遷移工具

- **pg_dump/pg_restore**：PostgreSQL 內建工具
- **mongodump/mongorestore**：MongoDB 內建工具
- **AWS DMS**：AWS 資料庫遷移服務
- **Liquibase/Flyway**：版本控制資料庫遷移工具
- **Prisma Migrate**：Prisma 的資料庫遷移工具

### 資料庫備份

#### 備份策略類型

- **完整備份 (Full Backup)**：備份整個資料庫
- **增量備份 (Incremental Backup)**：僅備份上次備份後的變更
- **差異備份 (Differential Backup)**：備份上次完整備份後的變更
- **時間點恢復 (PITR)**：還原到特定時間點的資料狀態

#### 備份排程策略

```javascript
// 備份腳本範例
async function backupDatabase() {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
  const backupFile = `/backups/mydb_${timestamp}.sql`

  // 執行 pg_dump
  const { execSync } = require('child_process')
  execSync(
    `pg_dump -U admin -h localhost mydb > ${backupFile}`,
    { env: { PGPASSWORD: 'password' } }
  )

  // 上傳到 S3
  const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3')
  const s3 = new S3Client({ region: 'ap-northeast-1' })
  const fs = require('fs')

  await s3.send(new PutObjectCommand({
    Bucket: 'my-backup-bucket',
    Key: `databases/mydb_${timestamp}.sql`,
    Body: fs.createReadStream(backupFile)
  }))

  console.log('備份完成，已上傳至 S3')
}
```

### 備份最佳實踐

1. **3-2-1 規則**：至少 3 份備份，儲存在 2 種不同媒體，1 份在異地
2. **定期測試還原**：定期驗證備份的可用性
3. **自動化備份**：使用 cron 或雲端服務排程
4. **加密備份**：備份檔案應加密儲存
5. **監控告警**：設定備份失敗的通知機制
6. **版本保留**：根據業務需求設定備份保留策略

### 還原測試腳本

```javascript
async function testRestore() {
  const { execSync } = require('child_process')
  execSync('psql -U admin -h localhost mydb_test < /backups/latest.sql')
  const result = execSync('psql -U admin -h localhost mydb_test -c "SELECT count(*) FROM users"')
  console.log('還原測試結果:', result.toString())
}
```

延伸閱讀：https://www.google.com/search?q=database+migration+strategy+best+practices
https://www.google.com/search?q=database+backup+3-2-1+rule+guide
