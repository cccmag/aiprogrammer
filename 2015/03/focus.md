# 本期焦點

## 資料庫與 SQL 基礎

### 引言

資料庫是現代資訊系統的核心。無論是網站、電子商務、企业資源規劃還是行動應用，都需要資料庫來儲存和管理資料。

本期將介紹關聯式資料庫的基本概念、SQL 查詢語法，以及三種主流開源資料庫（PostgreSQL、MySQL、SQLite）的特性。

---

## 大綱

* [程式：SQL 查詢實務](focus_code.md)
   - 常用 SQL 範例
   - 查詢技巧
   - 效能優化

1. [關聯式資料庫基礎](focus1.md)
   - 表格與欄位
   - 主鍵與外鍵
   - 關聯類型

2. [SQL 查詢語法](focus2.md)
   - SELECT 與 WHERE
   - JOIN 與 UNION
   - 聚合與分組

3. [PostgreSQL 詳解](focus3.md)
   - 特色功能
   - 效能優化
   - 擴充套件

4. [MySQL 與 MariaDB](focus4.md)
   - 架構設計
   - 儲存引擎
   - 複製設定

5. [SQLite 嵌入式資料庫](focus5.md)
   - 輕量級設計
   - 行動應用
   - 使用情境

6. [資料庫設計原則](focus6.md)
   - 正規化理論
   - 索引設計
   - 視圖與預存程序

7. [未來展望](focus7.md)
   - NoSQL 的衝擊
   - NewSQL 的興起
   - 雲端化趨勢

---

## 濃縮回顧

### 關聯式模型的力量

```
關聯式資料庫的核心概念：
────────────────────────

表格（Table）    → 一個實體類型（如：users）
列（Row）        → 一筆記錄（如：王小明的資料）
欄位（Column）   → 一個屬性（如：姓名、信箱）

主鍵（Primary Key）    → 唯一識別每筆記錄
外鍵（Foreign Key）    → 建立表格間的關聯
索引（Index）          → 加速查詢
```

### SQL 的普遍性

SQL 是資料庫的通用語言。無論你使用 PostgreSQL、MySQL 還是 SQL Server，SQL 語法大體相同。學會 SQL，就能操作幾乎所有關聯式資料庫。

### 三大開源資料庫的定位

```
PostgreSQL：功能最完整、擴充性強、適合復雜應用
MySQL：     廣泛使用、效能優秀、適合 Web 應用
SQLite：    輕量級、零設定、適合嵌入式和行動應用
```

---

## 結論與展望

關聯式資料庫在經歷了 NoSQL 的衝擊後，依然是大多數應用的首選。PostgreSQL 的功能越來越強大、MySQL 的效能持續優化、SQLite 繼續統治行動裝置。

未來的方向：
1. **混合式資料庫**：同時支援 SQL 和 NoSQL
2. **分散式架構**：應對海量資料
3. **雲端原生**：資料庫即服務

---

## 延伸閱讀

- [關聯式資料庫基礎](focus1.md)
- [SQL 查詢語法](focus2.md)
- [PostgreSQL 詳解](focus3.md)
- [MySQL 與 MariaDB](focus4.md)
- [SQLite 嵌入式資料庫](focus5.md)
- [資料庫設計原則](focus6.md)
- [未來展望](focus7.md)

---

*本期焦點到此結束。*