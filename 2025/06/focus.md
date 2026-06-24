# 本期焦點

## 資料庫與 SQL 實戰：從理論到實作

### 引言

資料庫是現代軟體系統的基石。無論是手機 App、網站後端、企業系統，還是 AI 應用，資料庫都扮演著儲存、查詢和管理資料的核心角色。而 SQL（Structured Query Language）則是與資料庫溝通的通用語言。

2026 年的資料庫生態系統比以往任何時候都更加豐富：傳統的關聯式資料庫（PostgreSQL、MySQL）持續進化，嵌入式資料庫（SQLite、DuckDB）不斷突破，NoSQL 資料庫（MongoDB、Redis）各展所長，新型的向量資料庫也加入了戰局。

然而，不論技術如何演進，**SQL 的核心概念和操作技巧**始終是每個程式設計師必須掌握的基礎技能。本期雜誌將帶領讀者從零開始，系統性地學習資料庫系統和 SQL 語言。

---

## 大綱

* [程式：實作資料庫操作範例](focus_code.md)
   - Python + SQLite 實戰
   - CREATE TABLE、INSERT、SELECT
   - JOIN、GROUP BY、子查詢

1. [資料庫系統導論](focus1.md)
   - 資料庫的歷史演進
   - 關聯式資料模型
   - ACID 交易特性

2. [SQL 基礎：CREATE、INSERT、SELECT](focus2.md)
   - DDL 與 DML 的區別
   - 建立資料庫與表格
   - 插入與查詢資料

3. [資料過濾與排序](focus3.md)
   - WHERE 子句的條件運算子
   - ORDER BY 排序
   - LIMIT 與 OFFSET 分頁

4. [表格關聯與 JOIN](focus4.md)
   - 外鍵與表格關聯
   - INNER JOIN、LEFT JOIN
   - 多對多關係實作

5. [聚合函數與 GROUP BY](focus5.md)
   - COUNT、SUM、AVG、MAX、MIN
   - GROUP BY 分組
   - HAVING 過濾群組

6. [子查詢與 CTE](focus6.md)
   - 標量子查詢
   - 關聯子查詢
   - Common Table Expressions

7. [資料庫正規化與設計](focus7.md)
   - 第一到第三正規化
   - BCNF 與其他正規化
   - 實務設計取捨

---

## 濃縮回顧

### 為什麼需要資料庫

在檔案系統中儲存資料雖然簡單，但會遇到許多問題：資料重複、不一致、並發存取衝突、缺乏查詢能力等。資料庫系統透過結構化儲存、索引、交易管理和查詢語言解決了這些問題。

關聯式資料庫的核心思想是 E.F. Codd 在 1970 年提出的關聯式模型（Relational Model）。他建議將資料組織成表格（關係），每個表格由行（記錄）和列（欄位）組成，表格之間透過鍵值關聯。

### SQL 語言的重要性

SQL 是資料庫操作的標準語言，分為四大類：

- **DDL（Data Definition Language）**：CREATE、ALTER、DROP
- **DML（Data Manipulation Language）**：SELECT、INSERT、UPDATE、DELETE
- **DCL（Data Control Language）**：GRANT、REVOKE
- **TCL（Transaction Control Language）**：BEGIN、COMMIT、ROLLBACK

其中 SELECT 是最複雜也最強大的指令，支援過濾（WHERE）、排序（ORDER BY）、分組（GROUP BY）、連接（JOIN）和子查詢等功能。

### 從 SQL 到資料庫設計

學會 SQL 語法只是第一步，良好的資料庫設計同樣重要。正規化（Normalization）是一套減少資料重複的設計原則，而反正規化（Denormalization）則是在效能和儲存之間做取捨。

### 資料庫的未來

2026 年的資料庫技術正在融合：關聯式資料庫開始支援向量搜尋，NoSQL 資料庫增加了 SQL 相容層，嵌入式資料庫的效能不斷提升。無論趨勢如何變化，**SQL 作為資料查詢的通用語言，地位將持續穩固**。

---

## 結論與展望

資料庫技術雖然已有超過 50 年的歷史，但它在 AI 時代迎來了新的生命。Text-to-SQL 技術讓自然語言查詢資料庫成為可能，向量資料庫為 RAG 應用提供了基礎設施，而嵌入式資料庫讓邊緣運算裝置也能擁有強大的資料處理能力。

對於程式設計師而言，掌握資料庫和 SQL 不僅能有效處理資料，更能理解現代軟體系統的運作原理。本期的七篇焦點文章將從基礎到進階，系統性地介紹這個重要的領域。

---

## 延伸閱讀

- [資料庫系統導論](focus1.md)
- [SQL 基礎](focus2.md)
- [資料過濾與排序](focus3.md)
- [表格關聯與 JOIN](focus4.md)
- [聚合函數與 GROUP BY](focus5.md)
- [子查詢與 CTE](focus6.md)
- [資料庫正規化與設計](focus7.md)

---

*本期焦點到此結束。下期我們將聚焦人工智慧的另一個重要主題，敬請期待。*
