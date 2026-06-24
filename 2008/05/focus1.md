# BigTable 論文與列式儲存

## BigTable 概述

Google 在 2006 年發表 BigTable 論文，介紹了一個用於處理 PB 等級資料的分散式儲存系統。

### 設計目標

- **大規模**：支援 PB 等級資料
- **高效能**：每秒百萬級讀寫
- **高可用**：支援大量併發讀寫
- **自動擴展**：無縫新增節點

## 列式儲存概念

### 與行式儲存的比較

```
行式儲存（RDBMS）：
Row1: id=1, name=John, age=30, city=Taipei
Row2: id=2, name=Mary, age=25, city=Tokyo

列式儲存（BigTable）：
id:    1, 2
name:  John, Mary
age:   30, 25
city:  Taipei, Tokyo
```

### 列式儲存的優勢

| 特性 | 行式 | 列式 |
|------|------|------|
| 讀取效率 | 讀取整行快 | 只讀需要的列 |
| 壓縮 | 困難 | 相同值連續 |
| 查詢 | 全表掃描 | 只讀相關列 |
| 寫入 | 單次寫入 | 需要寫多列 |

## 資料模型

### 多維映射

```python
(row:string, column:string, time:int64) → string
```

### 行鍵（Row Key）

- 唯一識別每一行
- 按照字典順序儲存
- 設計應考慮資料局部性

```python
# 好的行鍵設計
"user:12345:profile"
"timestamp:1234567890:event"

# 不好的設計
"12345"  # 無法局部性
```

### 列族（Column Family）

```bash
# 列族語法
Table: Users
├── profile:name
├── profile:email
├── settings:theme
└── settings:language
```

### 時間戳記

每個單元格可以有多個版本：

```python
# 讀取特定版本
get "user123", "profile:email", timestamp=1234567890

# 讀取最新版本
get "user123", "profile:email"
```

## 架構設計

### Tablet

BigTable 將表格分割為 Tablet：

```
表格
├── Tablet 1 (a-m)
├── Tablet 2 (n-z)
└── ...
```

每個 Tablet 約 100MB-200MB。

### SSTable

儲存格式為 SSTable（Sorted String Table）：

```
┌─────────────────────────────┐
│          SSTable             │
├─────────────────────────────┤
│  Index                      │
├─────────────────────────────┤
│  Data Block 1               │
│  Data Block 2               │
│  ...                        │
│  Bloom Filter               │
└─────────────────────────────┘
```

### 系統架構

```
┌──────────────────────────────────────────────┐
│              BigTable 架構                    │
├──────────────────────────────────────────────┤
│                                              │
│   ┌─────────┐    ┌─────────────────────┐   │
│   │ Chubby  │    │    Master Server    │   │
│   │ (鎖服務) │    │   (元數據管理)       │   │
│   └─────────┘    └──────────┬──────────┘   │
│                              │               │
│   ┌────────────────────────────────────────┐ │
│   │           Tablet Server 叢集           │ │
│   │  ┌─────────┐ ┌─────────┐ ┌─────────┐│ │
│   │  │ Tablet  │ │ Tablet  │ │ Tablet  ││ │
│   │  │ (a-m)   │ │ (n-z)   │ │ (...)   ││ │
│   │  └─────────┘ └─────────┘ └─────────┘│ │
│   └────────────────────────────────────────┘ │
│                                              │
│              ┌───────────────┐              │
│              │   GFS / Colossus│              │
│              │  (實際資料儲存) │              │
│              └───────────────┘              │
└──────────────────────────────────────────────┘
```

## 開源實現

### HBase

Apache HBase 是 BigTable 的開源實現：

```bash
# 建立 HBase 表
create 'users', 'profile', 'settings'

# 寫入資料
put 'users', 'user123', 'profile:name', 'John'
put 'users', 'user123', 'profile:email', 'john@example.com'

# 讀取資料
get 'users', 'user123'
```

### Cassandra

Facebook 貢獻的 Cassandra 結合了 BigTable 和 Dynamo 的特性。

## 結論

BigTable 的列式儲存和分散式架構為處理巨量資料提供了新思路。其設計理念影響了眾多開源專案。

---

**延伸閱讀**

- [Dynamo 分散式設計](focus2.md)
- [HBase 即時資料庫](focus6.md)
- [BigTable+paper](https://www.google.com/search?q=BigTable+Google+paper)