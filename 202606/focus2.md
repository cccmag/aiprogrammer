# 關聯式資料庫的誕生：Codd 的革命與 SQL 的演化（1970s-1980s）

## E.F. Codd 與關聯式模型

### 改變世界的 12 頁論文

1970 年，IBM 聖荷西研究實驗室的 Edgar Frank Codd 發表了一篇 12 頁的論文：「A Relational Model of Data for Large Shared Data Banks」。這篇論文被認為是資料庫史上最重要的文獻。

```
Codd 的核心思想：
─────────────────

提出用數學中的「關聯」（Relation）來建模所有資料。

一個「關聯」就是一個二維表格：
- 每一行（Tuple）代表一個實體
- 每一列（Attribute）代表一個屬性

Employee 關聯：
┌─────────┬──────────┬────────┬──────────┐
│ emp_id  │ name     │ salary │ dept_id  │
├─────────┼──────────┼────────┼──────────┤
│ 101     │ Alice    │ 75000  │ D1       │
│ 102     │ Bob      │ 68000  │ D2       │
│ 103     │ Charlie  │ 82000  │ D1       │
└─────────┴──────────┴────────┴──────────┘
```

### Codd 的 12 條規則

Codd 在後續論文中定義了關聯式資料庫管理系統（RDBMS）應滿足的 12 條規則：

```
Codd 的 12 條規則（簡化版）：
─────────────────────────

0. 基礎規則：一個 RDBMS 必須完全透過關聯式能力來管理資料

1. 資訊規則：所有資訊都以表格中的資料值表示

2. 保證存取規則：每個資料值可以透過「表名 + 主鍵 + 欄位名」唯一確定

3. 空值規則：支援系統性的空值（NULL）處理

4. 動態目錄規則：資料庫的結構（後設資料）也以關聯式表格儲存

5. 完整子語言規則：至少支援一種完整的關聯式查詢語言（如 SQL）

6. 檢視更新規則：所有可以被查詢的檢視（View）也應該可以被更新

7. 高階插入、更新和刪除：支援集合層級的資料操作

8. 資料獨立性：應用程式不受儲存格式變化的影響

9. 邏輯獨立性：應用程式不受表格結構變化的影響

10. 完整性獨立性：完整性約束應在資料庫系統中定義，而非應用程式中

11. 分散式獨立性：應用程式不受資料分散在不同位置的影響

12. 非顛覆規則：如果提供低階語言，它不能用來繞過高階語言的完整性規則
```

### 關聯式代數

Codd 也定義了關聯式代數（Relational Algebra）——一組操作關聯的運算元：

```
關聯式代數的 8 個基本運算：
─────────────────────────

Π（投影，Projection）：選取特定欄位
   Π name, salary (Employee) → 只顯示 name 和 salary

σ（選擇，Selection）：選取特定資料行
   σ salary > 70000 (Employee) → 只顯示薪資 > 70000 的員工

×（笛卡兒積，Cartesian Product）：組合兩個關聯
   Employee × Department → 所有可能的員工-部門組合

∪（聯集，Union）：合併兩個關聯
   Employee2025 ∪ Employee2026 → 所有員工

−（差集，Difference）：找出在一個關聯但不在另一個的資料
   Employee − Manager → 不是主管的員工

ρ（重新命名，Rename）：改變關聯或欄位名稱
   ρ DeptName (Department.name) → 將 Department 的 name 改為 DeptName

∩（交集，Intersection）：找出同時在兩個關聯中的資料
   Customer ∩ VIP → 既是客戶又是 VIP 的人

⋈（連接，Join）：根據條件組合兩個關聯
   Employee ⋈ DeptID=DeptID Department → 員工連同其部門資訊
```

## System R 與 SQL 的誕生

### IBM System R

1974 年，IBM 啟動了 System R 專案——這是第一個實作關聯式模型的資料庫系統。System R 引入了許多至今仍在使用的概念：

```
System R 的創新：
─────────────────

1. SQL（最初稱為 SEQUEL）
   世界上第一個關聯式查詢語言

2. 雙引擎架構
   - RDS（Relational Data System）：SQL 解析與最佳化
   - RSS（Research Storage System）：底層儲存管理

3. 交易管理
   - 鎖定（Locking）：樂觀鎖和悲觀鎖
   - 日誌（Logging）：Write-Ahead Logging

4. 查詢最佳化
   基於成本的查詢最佳化器——根據統計資訊選擇最佳執行計劃
```

### SQL 的誕生

1974 年，Donald Chamberlin 和 Raymond Boyce 在 System R 專案中設計了 SEQUEL（Structured English Query Language），後來因商標問題改名為 SQL。

```sql
-- 最初的 SEQUEL 語法（1974）
SELECT NAME, SALARY
FROM EMPLOYEE
WHERE SALARY > 50000;

-- 這在當年是革命性的：
-- 1. 宣告式：使用者說「要什麼」，而不是「怎麼要」
-- 2. 類英語：即使非程式設計師也能理解
-- 3. 集合層級：一次操作多筆資料
```

### SQL 的標準化

```
SQL 標準化時間線：
─────────────────

1986  SQL-86 (SQL1)：第一個 ANSI 標準
      基本 Data Definition Language (DDL)
      基本 Data Manipulation Language (DML)

1989  SQL-89：小幅修訂

1992  SQL-92 (SQL2)：重大更新
      支援 JOIN、CASE、CHECK 約束
      ← 大多數資料庫至今仍以此版本為基礎

1999  SQL:1999 (SQL3)：引入
      遞迴查詢（WITH RECURSIVE）
      觸發器（TRIGGER）
      物件導向擴展

2003  SQL:2003：引入
      XML 相關功能
      WINDOW 函數
      SEQUENCE 物件

2011  SQL:2011：引入
      時間資料（Temporal Data）
      FETCH FIRST...PERCENT 等

2016  SQL:2016：引入
      JSON 支援
      POLYMORPHIC TABLE FUNCTIONS

2019  SQL:2019：新增
      ROW 模式匹配
      多型表函數

2023  SQL:2023：新增
      JSON 增強
      GRAPH 查詢（SQL/PGQ）
      屬性圖查詢

2026  SQL:2026：最新版
      GRAPH 查詢正式納入核心
      向量運算支援
      JSON 進一步增強
```

## 第一個商業關聯式資料庫

### Oracle（1979）

1977 年，Larry Ellison、Bob Miner 和 Ed Oates 創立了軟體開發實驗室（SDL），並於 1979 年發布了 Oracle 2——第一個商用 SQL 資料庫。

```
Oracle 2 (1979) 的革命：
─────────────────

1. 第一個商用 SQL 資料庫
2. 第一個支援交易的資料庫
3. 可移植的 C 語言實作
   （執行在 PDP-11、VAX、IBM 主機上）

有趣的事實：
Oracle 2 沒有版本 1——行銷團隊認為
「版本 1」聽起來不夠可靠
```

### IBM DB2（1983）

1983 年，IBM 發布了 DB2（Database 2）——基於 System R 研究成果的商業產品。DB2 引入了：

```
DB2 的 key 貢獻：
─────────────────

1. 完整實作 SQL
2. 基於成本的查詢最佳化器
3. 多版本併發控制（MVCC）的先驅
4. 分散式資料庫功能（DB2 後來的版本）
```

### 其他重要資料庫

```
1980s 的資料庫生態：
─────────────────

1984  Sybase 成立（後來與 Microsoft 合作開發 SQL Server）

1985  Informix 成立（第一個整合陣列處理的資料庫）

1986  PostgreSQL 的前身——加州大學柏克萊分校的 Postgres 專案啟動

1988  Microsoft SQL Server（與 Sybase 合作開發）

1989  SQL 標準化（SQL-89 發布）
```

## 關聯式模型的影響

### 為什麼關聯式模型如此成功？

關聯式模型成功的關鍵在於它提供了幾個重要的抽象：

```
抽象層次    傳統檔案系統           關聯式資料庫
────────────────────────────────────────────
查詢方式    用程式碼遍歷資料      用 SQL 宣告式查詢
資料組織    檔案 + 記錄           表格 + 關聯
關聯表達    程式碼中實作          外鍵 + JOIN
約束控制    應用程式自行處理       資料庫內建
併發控制    無（或自行實作）       交易 + 鎖定
```

**資料獨立性**是最核心的貢獻：

```sql
-- 應用程式只需要這個查詢
SELECT name, salary FROM Employee WHERE salary > 50000;

-- 底層可以任意改變：
-- 1. 加入索引 → 查詢變快，SQL 不變 ✓
-- 2. 分割表格 → 查詢不變 ✓
-- 3. 更改欄位名（透過 View）→ 查詢不變 ✓
-- 4. 移到不同的資料庫 → 查詢幾乎不變 ✓
```

### 關聯式模型的局限

儘管關聯式模型取得了巨大的成功，它也有其固有局限：

1. **阻抗不匹配（Impedance Mismatch）**：關聯式表格 vs 物件導向程式的資料結構
2. **水平擴展困難**：傳統 RDBMS 在跨多台機器時表現不佳
3. **半結構化資料處理**：JSON、XML 等格式支援不夠自然
4. **固定 Schema**：修改表格結構（ALTER TABLE）可能非常昂貴

## 結語

1970 年 Codd 的論文集為資料庫管理奠定了理論基礎。System R 將這個理論轉化為可工作的實作。Oracle 和 DB2 將關聯式資料庫帶入商業世界。SQL 則成為資料庫查詢的通用語言——至今仍是最廣泛使用的程式語言之一。

關聯式資料庫的誕生與 Codd 關聯式模型描述了資料庫最重要的概念，但是實務上必須透過儲存引擎和索引技術來實現高效查詢——這些技術的主題我們將在下一篇文章中介紹。

---

## 延伸閱讀

- [Codd 1970 論文](https://www.google.com/search?q=Codd+1970+A+Relational+Model+of+Data)
- [System R 歷史](https://www.google.com/search?q=IBM+System+R+database+history)
- [SQL 標準演進](https://www.google.com/search?q=SQL+standard+evolution+history)
- [Oracle 早期歷史](https://www.google.com/search?q=Oracle+database+early+history+Larry+Ellison)

---

*本篇文章為「AI 程式人雜誌 2026 年 6 月號」歷史回顧系列之一。*
