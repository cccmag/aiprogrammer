# Google 的分散式運算傳奇

## 前言

Google 以其強大的搜尋能力聞名，但支撐這一能力的幕後英雄是革命性的分散式運算技術。2003 至 2006 年間，Google 發表了三篇經典論文，奠定了現代巨量資料處理技術的基礎。

## Google File System (GFS)

### 論文發表

2003 年，Google 發表了「The Google File System」論文，介紹了專為大型、分散式檔案操作設計的檔案系統。

### 設計目標

GFS 的設計基於以下觀察：

- 元件故障是常態而非例外
- 檔案巨大（GB 等級）
- 大多數檔案透過新增內容而非覆蓋來修改
- 應用程式與檔案系統 API 的協同設計

### 架構特點

GFS 採用主從架構：

```
┌────────────────────────────────────────┐
│            GFS 叢集                      │
├────────────────────────────────────────┤
│                                        │
│    ┌─────────────┐                     │
│    │   Master    │                     │
│    │  (元數據)    │                     │
│    └──────┬──────┘                     │
│           │                             │
│     ┌─────┴─────┐                      │
│     ↓           ↓                      │
│  ┌──────┐   ┌──────┐    ┌──────┐      │
│  │Chunk │   │Chunk │    │Chunk │      │
│  │Server│   │Server│    │Server│      │
│  └──────┘   └──────┘    └──────┘      │
│                                        │
└────────────────────────────────────────┘
```

### 創新點

1. **單一 Master**：簡化設計，利用大資料局部性
2. **不看客戶端快取**：批評傳統方法，堅持直接操作
3. **原子性的記錄附加**：支援併發寫入

## MapReduce

### 論文發表

2004 年，Google 發表了「MapReduce: Simplified Data Processing on Large Clusters」論文。

### 核心思想

MapReduce 的核心是「分而治之」：

- **Map**：將輸入分割為獨立的工作單元
- **Reduce**：彙總所有與同一鍵關聯的結果

### 設計理念

MapReduce 隐藏了分散式系統的複雜性：

- 自動化分割輸入資料
- 排程與硬體故障處理
- 負載均衡

### 應用範例

```
文字處理：Count = Map(+1) → Shuffle → Reduce(sum)
網頁索引：Pages = Map(url, content) → Shuffle → Reduce(inverted index)
```

## BigTable

### 論文發表

2006 年，Google 發表了「Bigtable: A Distributed Storage System for Structured Data」論文。

### 設計目標

BigTable 是一個稀疏的、分散式的、持久化的多維排序映射：

- 行鍵（Row Key）：唯一識別
- 列鍵（Column Key）：結構化存取
- 時間戳記（Timestamp）：版本控制

### 資料模型

```
           Column Families
           ┌─────────────┬─────────────┐
  Row Key  │   contents  │   anchor    │
           │  html:...   │  cnnsi.com:1│
  "com.cnn │             │  my.look.ca:2│
  /stanford"│             │              │
           └─────────────┴─────────────┘
```

### Tablet 分割

BigTable 將表格分割為 Tablet（約 100MB），每個 Tablet 由單一 tablet server 提供服務。

## 對產業的影響

### 開源實現

Google 的三篇論文催生了多個開源專案：

| Google 技術 | 開源實現 |
|------------|----------|
| GFS | HDFS |
| MapReduce | Hadoop MapReduce |
| BigTable | HBase |

### 雲端服務

Amazon EMR、Google Dataproc 等服務建立在此基礎上。

### 新興公司

- Cloudera（2008 年成立）
- Hortonworks
- MapR

## 結論

Google 的三篇論文開創了巨量資料處理的新時代。雖然具體實現各有不同，但核心思想——分散式儲存與運算——已成為現代資料工程的基石。

---

**延伸閱讀**

- [MapReduce 分散式運算](focus1.md)
- [HDFS 分散式檔案系統](focus2.md)
- [Google+MapReduce+paper](https://www.google.com/search?q=Google+MapReduce+paper)