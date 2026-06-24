# RDS 資料庫服務

## RDS 概述

Amazon RDS（Relational Database Service）是托管的關聯式資料庫服務，支援 MySQL、PostgreSQL、Oracle、SQL Server、MariaDB 等多種引擎。RDS 自動處理軟體更新、備份、效能調校，讓開發者專注於應用程式開發而非資料庫維運。

## 建立 RDS 執行個體

```bash
# 建立 MySQL 執行個體（範例參數）
aws rds create-db-instance \
    --db-instance-identifier mydbinstance \
    --db-instance-class db.t2.micro \
    --engine mysql \
    --allocated-storage 20 \
    --master-username admin \
    --master-user-password MyPassword123 \
    --db-name mydatabase
```

## 多可用區域部署

生產環境建議啟用 Multi-AZ 部署。RDS 會自動在另一個可用區域建立同步備援副本，Primary 發生故障時自動切換到 Standby，應用程式無需修改程式碼。

```
可用區域 A（Primary）<--同步複寫--> 可用區域 B（Standby）
         |                                    |
      讀寫流量                          備援待命
```

## 備份與還原

RDS 會自動進行每日備份，保留期限可設定（預設 1 天，最多 35 天）。也可手動建立快照。

```bash
# 建立快照
aws rds create-db-snapshot \
    --db-instance-identifier mydbinstance \
    --db-snapshot-identifier my-snapshot

# 從快照還原
aws rds restore-db-instance-from-db-snapshot \
    --db-instance-identifier restored-db \
    --db-snapshot-identifier my-snapshot
```

## 連線設定

RDS 的網路存取透過 Security Group 控制。確認 Security Group 允許來自應用伺服器的 3306（MySQL）或 5432（PostgreSQL）流量。

```python
import mysql.connector

conn = mysql.connector.connect(
    host="mydbinstance.abc123.us-east-1.rds.amazonaws.com",
    user="admin",
    password="MyPassword123",
    database="mydatabase"
)
cursor = conn.cursor()
cursor.execute("SELECT VERSION()")
print(cursor.fetchone())
```

## 參數群組

每個 RDS 引擎都有預設的參數群組，但有時需要根據應用需求調整。例如 MySQL 的 `max_connections`、`innodb_buffer_pool_size` 等。建立的參數群組修改後，可關聯到執行個體。

## 參考資源

- https://www.google.com/search?q=AWS+RDS+建立+管理+MySQL+PostgreSQL+備份+還原+Multi-AZ+2016
- https://www.google.com/search?q=RDS+Security+Group+連線+設定+參數群組+教學
- https://www.google.com/search?q=RDS+vs+EC2+自行架設+資料庫+比較+優缺點+選擇