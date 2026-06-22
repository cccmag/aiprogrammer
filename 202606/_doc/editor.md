# AI 輔助雜誌編輯實戰手冊 — 六月號

## 前言

本文記錄使用 AI（OpenCode + Big Pickle）編輯《AI 程式人雜誌》2026 年 6 月號的完整流程與技巧。本月主題是「資料庫系統的奧秘：從檔案系統到 AI 原生資料庫」。

---

## 一、專案結構設計

### 1.1 目錄規劃

```
202606/                    # 當期雜誌目錄
├── _code/                 # 程式範例目錄
│   └── minisql.py        # MiniSQL 資料庫引擎實作
├── focus.md               # 本期主題概覽
├── focus1-7.md           # 主題深入文章
├── focus_code.md         # 主題程式碼文件
├── news.md               # 本月新知
├── article1-10.md       # 精選文章
├── articles.md          # 文章索引
├── end.md              # 結語
└── README.md           # 雜誌總索引
```

### 1.2 命名慣例

與前幾期保持一致。

---

## 二、AI 協作流程

### 2.1 任務分解策略

1. **先建立骨架**：READ ME、news、focus 大綱
2. **再填入內容**：focus1-7 -> focus_code + code -> articles -> end
3. **平行寫作**：用 Task tool 同時寫程式文章和 AI 文章

### 2.2 分階段寫作順序

```
Phase 1: 結構檔案（5 分鐘）
├── mkdir 202606/_code 202606/_doc
├── README.md（目錄）
├── news.md（本月新知）
└── focus.md（主題概覽）

Phase 2: 主題文章（連續寫作）
├── focus1.md（打孔卡→檔案系統）
├── focus2.md（Codd→SQL）
├── focus3.md（B-tree→LSM-Tree）
├── focus4.md（查詢處理→最佳化）
├── focus5.md（CAP→NoSQL）
├── focus6.md（雲端→Lakehouse）
└── focus7.md（AI→向量資料庫）

Phase 3: 程式專案
├── _code/minisql.py（實作+測試）
└── focus_code.md（文件）

Phase 4: 文章（平行 Task）
├── 5 篇程式文章
├── 5 篇 AI 文章
├── articles.md（索引）
└── end.md（結語）
```

---

## 三、程式碼處理技巧

### 3.1 MiniSQL 引擎設計

MiniSQL 資料庫引擎包含以下元件：
1. **Lexer**：SQL 詞法分析器，將 SQL 字串轉為 Token 串流
2. **Parser**：語法分析器，將 Token 串流轉為 AST（CreateTable, InsertInto, Select, Delete, DropTable）
3. **Database**：執行引擎，包含 CREATE, INSERT, SELECT, DELETE, DROP 的實作
4. **QueryResult**：查詢結果的格式化輸出（表格樣式）

### 3.2 測試策略

```python
def test():
    db = Database()
    sqls = [
        "CREATE TABLE employee (id INT, name TEXT, salary INT);",
        "INSERT INTO employee VALUES (1, 'Alice', 75000);",
        "SELECT * FROM employee WHERE salary > 75000;",
        "DELETE FROM employee WHERE name = 'Eve';",
        "DROP TABLE employee;",
    ]
    for sql in sqls:
        lexer = Lexer(sql)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        stmt = parser.parse()
        result = db.execute(stmt)
        print(result)
```

### 3.3 常見除錯

**問題**：`SELECT name, salary` 顯示了錯誤的數值
**原因**：選取特定欄位時仍回傳完整 row（而非只回傳選取欄位）
**解決**：在 `_select` 方法中過濾 col_indices 並只回傳選取欄位

---

## 四、文件一致性維護

### 4.1 連結檢查清單

- [ ] README.md 的目錄連結
- [ ] focus.md 的大綱連結
- [ ] articles.md 的文章連結
- [ ] 所有交叉引用是否正確

### 4.2 主題間的交叉引用

本月焦點（資料庫）與多篇文章有自然關聯：
- article1（PostgreSQL 20）←→ focus2（關聯式資料庫）、focus7（AI 資料庫）
- article2（SQLite 4.0）←→ focus3（儲存引擎）
- article4（DuckDB）←→ focus6（雲端資料庫）
- article7（GraphRAG）←→ focus7（向量資料庫）
- article9（自主資料庫）←→ focus7（AI 驅動最佳化）

---

## 五、資料庫主題的寫作經驗

### 5.1 歷史脈絡的把握

資料庫主題從 1890 年代至今，需要把握關鍵節點：
- 1890：打孔卡（Hollerith）
- 1956：磁碟儲存（IBM RAMAC）
- 1970：關聯式模型（Codd）
- 1974：SQL 誕生（System R）
- 1980s：B-tree、Oracle、DB2
- 1990s：查詢最佳化成熟
- 2006：Bigtable（NoSQL 開端）
- 2012：Spanner（NewSQL）
- 2014：Snowflake（雲端資料倉儲）
- 2020：Lakehouse 架構
- 2023-2026：向量資料庫、AI 原生資料庫

### 5.2 程式碼範例的設計

MiniSQL 的設計考量：
1. **簡單易懂**：使用 Python，不需要額外依賴
2. **功能完整**：支援 CREATE、INSERT、SELECT（含 WHERE）、DELETE、DROP
3. **可視化輸出**：查詢結果以表格樣式顯示
4. **可測試**：完整的 test() 函式
5. **可擴展**：可加入 B-tree 索引、ORDER BY、JOIN 等進階功能

### 5.3 技術深度與可讀性的平衡

- 用資料流圖說明查詢處理流程
- 用 SQL 範例代替冗長解釋
- 將理論（Codd 12 條規則）與實際（CREATE TABLE）連結

---

## 六、常用指令參考

```bash
# 測試 MiniSQL
python3 _code/minisql.py

# REPL 模式
python3 _code/minisql.py repl

# 檢查語法
python3 -m py_compile _code/minisql.py
```

---

## 七、最佳實踐總結

1. **分層建構**：先結構、後內容、最後除錯
2. **平行寫作**：利用 Task tool 平行處理大量文章
3. **立即測試**：寫完程式碼立即執行測試
4. **連結檢查**：修改後立即驗證所有引用
5. **程式碼除錯**：當程式碼出錯時，先理解錯誤訊息，再定位到對應的程式碼修正
6. **歷史脈絡**：複雜主題從故事開始，逐步深入

---

*本文為《AI 程式人雜誌》編輯技巧記錄*
