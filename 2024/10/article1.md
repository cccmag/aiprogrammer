# 文章 1：雲端資料庫 vs 本地資料庫

## 如何選擇部署方式？

在規劃資料庫架構時，首要決定是採用雲端資料庫服務還是自行管理本地資料庫。兩者各有優缺，適合不同的使用情境。

### 雲端資料庫的優勢

1. **零維護負擔**：供應商負責硬體維護、作業系統更新、資料庫修補與備份
2. **彈性擴展**：按需調整運算與儲存資源，無需預估容量
3. **高可用性**：內建複寫、自動故障轉移與災難復原
4. **隨用隨付**：依實際使用量計費，無需前期投資

```javascript
// 雲端資料庫連線範例 (AWS RDS PostgreSQL)
import pg from 'pg'

const pool = new pg.Pool({
  host: process.env.RDS_HOSTNAME,
  port: 5432,
  database: process.env.RDS_DB_NAME,
  user: process.env.RDS_USERNAME,
  password: process.env.RDS_PASSWORD,
  ssl: { rejectUnauthorized: true },
  max: 20,
  idleTimeoutMillis: 30000
})

async function queryWithRetry(sql, params) {
  for (let i = 0; i < 3; i++) {
    try {
      return await pool.query(sql, params)
    } catch (err) {
      if (i === 2) throw err
      console.log('查詢失敗，重試中...', err.message)
      await new Promise(r => setTimeout(r, 1000 * (i + 1)))
    }
  }
}
```

### 本地資料庫的優勢

1. **完全控制**：自訂配置、調校參數、安裝擴展
2. **可預測成本**：固定硬體成本，不受使用量波動影響
3. **資料主權**：資料完全留在本地，符合特定法規需求
4. **低延遲**：無網路延遲，適合高效能需求

### 成本比較

| 項目 | 雲端資料庫 | 本地資料庫 |
|------|-----------|-----------|
| 前期成本 | 低 | 高（硬體採購） |
| 營運成本 | 隨使用量成長 | 固定 |
| 維護人力 | 低 | 高 |
| 擴展成本 | 立即按需 | 需採購週期 |

### 安全性考量

雲端資料庫的安全由共享責任模型定義。AWS/Azure/GCP 負責底層基礎設施安全，使用者負責資料存取控制、加密配置與網路設定。

### 混合方案

許多組織採用混合策略：將敏感資料保留在本地，同時利用雲端進行資料分析、備份或開發測試環境。

### 選擇決策樹

1. 組織是否有資料中心？→ 無 → 雲端優先
2. 是否有法規限制？→ 是 → 本地或混合部署
3. 流量是否高度波動？→ 是 → 雲端（彈性擴展）
4. 是否需要低延遲（<1ms）？→ 是 → 本地

延伸閱讀：https://www.google.com/search?q=cloud+database+vs+on-premise+comparison+2024
https://www.google.com/search?q=hybrid+database+deployment+strategy
