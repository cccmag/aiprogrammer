# NoSQL 資料庫的 CAP 定理

## CAP 定理

```
一個分散式系統無法同時滿足：
- Consistency（一致性）
- Availability（可用性）
- Partition Tolerance（分區容錯）
```

## NoSQL 的取捨

| 資料庫 | 取捨 | 說明 |
|--------|------|------|
| Cassandra | AP | 可用性優先 |
| HBase | CP | 一致性優先 |
| Dynamo | AP | 可用性優先 |

## 結論

理解 CAP 定理有助於選擇適合的資料庫。

---

**延伸閱讀**

- [Dynamo 分散式設計](focus2.md)