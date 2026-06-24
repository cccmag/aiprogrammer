# 本期焦點

## NoSQL 資料庫興起 — 分散式新時代

### 引言

隨著 Web 2.0 應用的爆發，傳統關聯式資料庫在擴展性方面面臨挑戰。Google 的 BigTable 和 Amazon 的 Dynamo 論文開創了新型資料庫的先河。

本期雜誌將帶您深入了解 NoSQL 資料庫的設計理念和技術特點。

---

## 大綱

* [NoSQL 程式實作](focus_code.md)
   - MongoDB CRUD 操作
   - CouchDB 文件操作

1. [BigTable 論文與列式儲存](focus1.md)
   - 列式儲存概念
   - 列族設計
   - 時間戳記版本

2. [Amazon Dynamo 的分散式設計](focus2.md)
   - 一致性雜湊
   - 最終一致性
   - 向量時鐘

3. [文件資料庫 CouchDB](focus3.md)
   - JSON 文件儲存
   - MapReduce 檢視
   - RESTful API

4. [MongoDB 與 JSON 文件儲存](focus4.md)
   - 文件導向模型
   - 查詢語言
   - 副本集

5. [Cassandra 列式資料庫](focus5.md)
   - 分散式架構
   - CQL 查詢語言
   - 寬欄儲存

6. [Redis 記憶體鍵值儲存](focus6.md)
   - 記憶體儲存
   - 豐富的資料結構
   - 發布/訂閱

7. [NoSQL 的未來發展](focus7.md)
   - NewSQL 的興起
   - 整合趨勢
   - 標準化

---

## 濃縮回顧

### NoSQL 資料庫分類

| 類型 | 特點 | 代表 |
|------|------|------|
| 鍵值儲存 | 簡單、高效能 | Redis, Dynamo |
| 文件儲存 | JSON/XML 文件 | MongoDB, CouchDB |
| 列式儲存 | 大規模資料 | HBase, Cassandra |
| 圖形儲存 | 複雜關係 | Neo4j, GraphDB |

### CAP 定理

```
CAP 定理：
一個分散式系統無法同時滿足三者

 Consistency（一致性）
      ↑       ↓
 Availability ← Partition Tolerance
    （可用性）    （分區容錯）

NoSQL 通常在 AP 和 CP 之間取捨
```

### 一致性層級

| 層級 | 說明 |
|------|------|
| 強一致性 | 所有節點同時看到相同資料 |
| 最終一致性 | 許久後最終一致 |
| 因果一致性 | 保持因果順序 |
| 讀你所寫 | 讀取自己寫入的結果 |

---

## 結論與展望

NoSQL 資料庫的興起反映了網路規模應用的需求。不同的 NoSQL 資料庫適用於不同的場景，開發者需要根據實際需求選擇。

---

## 延伸閱讀

- [BigTable 列式儲存](focus1.md)
- [Dynamo 分散式設計](focus2.md)
- [文件資料庫](focus3.md)

---

*本期焦點到此結束。下期我們將探討 jQuery 與前端工具，敬請期待。*