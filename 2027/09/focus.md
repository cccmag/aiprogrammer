# 本期焦點

## AI 原生資料庫 — 從向量搜尋到 AI 驅動的資料管理

### 引言

傳統資料庫是為精確查詢設計的——你要找的資料就在那裡，用 SQL 就能找到。但 AI 時代的資料需求完全不同：你需要找的是「相似的」而非「相等的」，你需要的是語義搜尋而非關鍵字匹配，你需要的是能理解資料內容而不僅僅是儲存資料的系統。

這催生了 AI 原生資料庫的興起。從 Pinecone、Weaviate、Qdrant 等向量資料庫，到 Postgres 加上 pgvector 擴展，再到 Notion 和 Obsidian 中內建的 AI 搜尋——資料庫正在從儲存引擎轉變為智慧引擎。

本期將從向量搜尋的核心演算法開始，深入 AI 原生資料庫的架構設計，並探討如何將 AI 整合到資料管理的工作流程中。

---

## 大綱

* [程式：從零實作向量資料庫](focus_code.md)
   - 向量索引與相似度搜尋
   - HNSW 近似最近鄰演算法
   - 過濾與混合搜尋
   - 簡單 RAG 整合

1. [從關聯式資料庫到 AI 原生資料庫（1970-2026）](focus1.md)
   - 資料庫演化史
   - 向量資料庫的誕生
   - AI 原生資料庫的定義

2. [向量嵌入與語義搜尋（2013-2026）](focus2.md)
   - 嵌入模型與語義表示
   - 相似度度量（cosine、euclidean、dot product）
   - 多模態嵌入

3. [近似最近鄰搜尋演算法（2011-2026）](focus3.md)
   - 暴力搜尋 vs ANN
   - IVF、HNSW、PQ 演算法
   - 準確率 vs 速度的權衡

4. [向量資料庫架構（2019-2026）](focus4.md)
   - 儲存引擎設計
   - 過濾與混合搜尋
   - 分散式架構

5. [AI 驅動的資料管理（2022-2026）](focus5.md)
   - 自動資料分類與標籤
   - 資料品質監控
   - RAG 系統的資料管線

6. [向量資料庫選型指南（2020-2026）](focus6.md)
   - Pinecone vs Weaviate vs Qdrant vs Chroma
   - pgvector 與 PostgreSQL
   - 效能與成本比較

7. [AI 輔助資料庫開發（2024-2026）](focus7.md)
   - LLM 生成查詢與 Schema
   - 自然語言查詢資料庫
   - 自動索引建議

## 延伸閱讀

- [向量資料庫比較](https://www.google.com/search?q=vector+database+comparison+2026)
- [HNSW 演算法](https://www.google.com/search?q=HNSW+algorithm+explained)
- [pgvector](https://www.google.com/search?q=pgvector+PostgreSQL)
- [RAG 資料管線](https://www.google.com/search?q=RAG+data+pipeline+best+practices)
