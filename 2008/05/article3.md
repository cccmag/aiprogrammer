# MongoDB 與傳統 RDBMS 的比較

## 資料模型

### 傳統 RDBMS

```sql
-- 需要預先定義 Schema
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);
```

### MongoDB

```python
# 彈性文件結構
{
    'name': 'John',
    'email': 'john@example.com',
    'tags': ['python', 'mongodb']
}
```

## 擴展性

| 特性 | RDBMS | MongoDB |
|------|-------|---------|
| 水平擴展 | 困難 | 原生支援 |
| 副本集 | 需設定 | 簡單設定 |
| 分片 | 手動 | 自動 |

## 結論

MongoDB 適合需要彈性 Schema 和快速開發的場景，傳統 RDBMS 適合需要強一致性和複雜查詢的場景。

---

**延伸閱讀**

- [MongoDB 與 JSON 文件儲存](focus4.md)