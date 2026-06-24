# SQL 查詢處理與最佳化：從語法分析到執行計劃（1980s-2010s）

## SQL 查詢的生命週期

當使用者輸入一條 SQL 查詢時，資料庫內部會經歷一系列複雜的處理步驟：

```
SQL 查詢的旅程：
─────────────────

SELECT e.name, d.name 
FROM employee e JOIN department d ON e.dept_id = d.id
WHERE e.salary > 50000

                    │
                    ▼
    ┌─────────────────────────────┐
    │ 1. 語法分析（Parser）        │
    │    SQL 字串 → 解析樹         │
    └────────────┬────────────────┘
                 ▼
    ┌─────────────────────────────┐
    │ 2. 語義分析（Analyzer）      │
    │    解析樹 → 邏輯計劃（LOG） │
    │    檢查權限、型別            │
    └────────────┬────────────────┘
                 ▼
    ┌─────────────────────────────┐
    │ 3. 查詢重寫（Rewriter）      │
    │    邏輯最佳化                │
    │    檢視擴展、述詞下推        │
    └────────────┬────────────────┘
                 ▼
    ┌─────────────────────────────┐
    │ 4. 查詢最佳化（Optimizer）   │
    │    邏輯計劃 → 實體計劃       │
    │    選擇最佳 JOIN 順序        │
    │    選擇索引                  │
    └────────────┬────────────────┘
                 ▼
    ┌─────────────────────────────┐
    │ 5. 執行（Executor）          │
    │    執行實體計劃              │
    │    從儲存引擎讀取資料        │
    └────────────┬────────────────┘
                 ▼
            查詢結果
```

## 語法分析與語義分析

### SQL 解析器

第一階段是將 SQL 字串轉化為資料庫可以理解的內部表示——解析樹（Parse Tree）：

```sql
SELECT e.name, d.name 
FROM employee e JOIN department d ON e.dept_id = d.id
WHERE e.salary > 50000
```

解析後的樹狀結構：

```
                ┌──────────┐
                │  SELECT   │
                └────┬─────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   ┌────┴────┐  ┌────┴────┐  ┌────┴────┐
   │ Target  │  │  FROM   │  │ WHERE   │
   │ List    │  │         │  │         │
   │ e.name  │  │ JOIN    │  │ e.salary│
   │ d.name  │  │ e.dept_ │  │ > 50000 │
   └─────────┘  │ id = d. │  └─────────┘
                │ id      │
                └─────────┘
```

### 語義分析與型別檢查

解析後，資料庫檢查查詢的語義正確性：

```python
# 語義分析的偽碼
def analyze(parse_tree, catalog):
    # 1. 檢查表格是否存在
    for table_ref in parse_tree.tables:
        if table_ref.name not in catalog:
            raise Error(f"Table {table_ref.name} does not exist")
    
    # 2. 檢查欄位是否存在
    for column_ref in parse_tree.columns:
        if column_ref.name not in resolve_table(column_ref.table):
            raise Error(f"Column {column_ref.name} not found")
    
    # 3. 型別檢查
    for condition in parse_tree.where:
        left_type = get_type(condition.left)
        right_type = get_type(condition.right)
        if not type_compatible(left_type, right_type):
            raise Error(f"Type mismatch")
    
    # 4. 權限檢查
    check_permissions(current_user, parse_tree)
```

## 查詢重寫

查詢重寫（Query Rewriting）在邏輯層面進行最佳化，不依賴於資料的統計資訊：

```sql
-- 原始查詢
SELECT * FROM employee 
WHERE salary > 50000 AND salary > 60000;

-- 重寫後（合併冗餘條件）
SELECT * FROM employee 
WHERE salary > 60000;
```

常見的查詢重寫技術：

```
查詢重寫技術：
─────────────────

1. 檢視擴展（View Expansion）
   將檢視（View）展開為基礎表格查詢

2. 述詞下推（Predicate Pushdown）
   將 WHERE 條件盡量靠近資料來源
   └── 先過濾再 JOIN，而非 JOIN 再過濾

3. 投影下推（Projection Pushdown）
   只讀取需要的欄位
   └── 減少從儲存引擎讀取的資料量

4. 恆真條件消除
   WHERE 1=1 → 刪除

5. 子查詢解嵌套
   將相關子查詢轉化為 JOIN

6. 合併過濾條件
   冗餘條件的合併和消除
```

## 基於成本的查詢最佳化

### 為什麼需要最佳化器？

```sql
-- 以下三種寫法語義完全相同，但效能可能天差地遠
SELECT e.name, d.name 
FROM employee e, department d 
WHERE e.dept_id = d.id AND e.salary > 50000;

SELECT e.name, d.name 
FROM employee e JOIN department d ON e.dept_id = d.id
WHERE e.salary > 50000;

SELECT e.name, d.name 
FROM (SELECT * FROM employee WHERE salary > 50000) e
JOIN department d ON e.dept_id = d.id;
```

最佳化器的工作就是從眾多可能的執行計劃中選擇成本最低的一個。

### 成本模型

```
查詢執行成本估算：
─────────────────

Cost = CPU_Cost + I/O_Cost + Network_Cost

I/O Cost 是最重要的因素（磁碟存取比 CPU 慢幾個數量級）

估算依賴於統計資訊：
├── 表格大小（行數、頁數）
├── 每個欄位的不同值數量
├── 資料分布（直方圖）
├── NULL 值的比例
└── 索引資訊
```

### 統計資訊的收集

```sql
-- PostgreSQL 收集統計資訊
ANALYZE employee;

-- 查看統計資訊
SELECT attname, n_distinct, most_common_vals 
FROM pg_stats 
WHERE tablename = 'employee';
```

### 執行計劃的選擇

對於簡單的查詢，最佳化器需要決定使用哪個索引和哪種 JOIN 方法：

```sql
-- 範例：不同的索引選擇
CREATE INDEX idx_salary ON employee(salary);
CREATE INDEX idx_dept ON employee(dept_id);

SELECT * FROM employee 
WHERE salary > 50000 AND dept_id = 'D1';

-- 最佳化器的選擇：
-- 選項 A：使用 idx_salary 過濾，再檢查 dept_id
-- 選項 B：使用 idx_dept 過濾，再檢查 salary
-- 選項 C：全表掃描
-- → 根據統計資訊選擇成本最低的
```

### JOIN 順序的最佳化

對於多表 JOIN，不同的 JOIN 順序會產生截然不同的執行成本：

```sql
-- 三表 JOIN，可能的執行順序有 3! = 6 種
SELECT * FROM a JOIN b ON a.id = b.a_id 
             JOIN c ON b.id = c.b_id
WHERE a.type = 'X' AND c.date > '2026-01-01';

-- 最佳化策略：
-- 1. 先過濾每個表格（述詞下推）
--    → a (type='X'), b (無過濾), c (date>'2026-01-01')
-- 2. 選擇最小的中間結果作為第一個 JOIN
--    → 如果過濾後的 a 很小，先 JOIN a-b
--    → 如果過濾後的 c 很小，先 JOIN c-b
```

對於 n 個表的 JOIN，可能的 JOIN 順序數量是 Catalan 數 O(4^n)。最佳化器使用動態規劃來找到最佳計劃：

```python
# 動態規劃搜尋最佳 JOIN 順序（簡化版）
def find_best_plan(tables):
    # dp[mask] = 處理 mask 表示的表集合的最佳計劃
    dp = {}
    
    for i, table in enumerate(tables):
        mask = 1 << i
        dp[mask] = Plan(cost=estimate_scan(table), 
                        expression=table.name)
    
    for size in range(2, len(tables) + 1):
        for mask in all_masks_with_size(size):
            best = INFINITY
            for submask in subsets(mask):
                if submask == 0 or submask == mask:
                    continue
                other = mask ^ submask
                cost = dp[submask].cost + dp[other].cost
                cost += estimate_join(dp[submask].result, 
                                      dp[other].result)
                if cost < best:
                    best = cost
                    dp[mask] = combine(dp[submask], dp[other])
    
    return dp[(1 << len(tables)) - 1]
```

## 現代查詢執行引擎

### 火山模型（Volcano Model）

1970 年代提出的疊代器模型至今仍是大多數資料庫的執行引擎基礎：

```
火山模型：每個運算子都是一個疊代器
─────────────────────────────

結果 ← 每個運算元實作 next() 介面
  ▲
  │
┌─┴────────┐
│ Hash Join │  ← 從子節點讀取資料
└────┬─────┘
     │
┌────┴─────┐
│ Table Scan│  ← 實際讀取資料
└──────────┘

每個運算元提供三個方法：
- open()：初始化
- next()：回傳下一筆資料
- close()：清理資源
```

### 向量化執行（Vectorized Execution）

現代資料庫（尤其是分析型資料庫）使用向量化執行來提升效能：

```
一次一筆記錄（傳統火山模型）：
for each row:
    check condition
    compute expression
    output row
→ 每次迭代都有虛擬函式呼叫開銷

一次一批記錄（向量化執行）：
for each batch (1024 rows):
    check condition on batch  ← SIMD 加速
    compute expression on batch
    output batch
→ 減少了虛擬函式呼叫，可利用 SIMD 指令
```

### 插入式執行（Compiled Execution）

最新的趨勢是將查詢編譯為機器碼執行：

```
插入式執行的三種形式：
─────────────────

1. 即時編譯（JIT Compilation）
   PostgreSQL、Oracle 等將查詢編譯為 LLVM IR
   再編譯為機器碼

2. 原生編譯（Native Compilation）
   SAP HANA、SingleStore 直接生成機器碼

3. 中介碼（Intermediate Representation）
   Hyper、DuckDB 使用自定義 IR

效能提升：2-10x 相比傳統火山模型
```

## 查看執行計劃

### 實用技巧：閱讀執行計劃

```sql
-- PostgreSQL
EXPLAIN ANALYZE 
SELECT e.name, d.name 
FROM employee e JOIN department d ON e.dept_id = d.id
WHERE e.salary > 50000;
```

輸出範例：

```
Hash Join  (cost=25.00..75.00 rows=100 width=120)
  Hash Cond: (e.dept_id = d.id)
  ->  Seq Scan on employee e  
      (cost=0.00..40.00 rows=100 width=80)
      Filter: (salary > 50000)
  ->  Hash  (cost=15.00..15.00 rows=500 width=40)
      ->  Seq Scan on department d  
          (cost=0.00..15.00 rows=500 width=40)
```

理解執行計劃的關鍵：
- `cost`：第一個值是啟動成本，第二個是總成本
- `rows`：估計回傳的行數
- `width`：每行的平均寬度（位元組）
- 從內到外閱讀（縮排最深的先執行）

## 結語

SQL 查詢處理與最佳化是資料庫系統中最複雜、最智慧的部分。從語法分析到執行計劃的生成，每一步都在追求同一個目標：**用最少的資源（CPU、I/O、記憶體）得到使用者想要的結果**。

現代資料庫已經從「固定的執行策略」走向了「基於資料驅動的自適應最佳化」——而最新的發展是引入深度學習來輔助最佳化決策，這將在 AI 時代的資料庫主題中探討。

下一篇文章將跳出單機資料庫的框架，介紹分散式資料庫與 NoSQL 的崛起。

---

## 延伸閱讀

- [PostgreSQL 查詢最佳化](https://www.google.com/search?q=PostgreSQL+query+optimization+internals)
- [MySQL 執行計劃分析](https://www.google.com/search?q=MySQL+EXPLAIN+execution+plan)
- [SQLite 查詢規劃](https://www.google.com/search?q=SQLite+query+planner+internals)
- [資料庫系統概論](https://www.google.com/search?q=database+system+concepts+query+optimization)

---

*本篇文章為「AI 程式人雜誌 2026 年 6 月號」歷史回顧系列之一。*
