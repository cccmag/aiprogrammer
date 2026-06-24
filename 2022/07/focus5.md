# Common Crawl 與開源語料

## 千萬網頁的處理之道

### Common Crawl 簡介

Common Crawl 是一個非營利組織，每月對整個網際網路進行一次大規模爬取，並將結果免費公開。自 2008 年啟動以來，Common Crawl 已積累了超過 250 PB 的資料，成為世界上最大的開源網頁語料庫。

許多知名語言模型都依賴 Common Crawl：

- **GPT-3**：使用經過過濾的 Common Crawl 版本
- **T5**：使用 C4（Colossal Clean Crawled Corpus），即 Common Crawl 的清洗版本
- **Bloom**：ROOTS 語料庫包含從 Common Crawl 篩選的多語言資料
- **LLaMA**：使用經過多層過濾的 Common Crawl 資料

### WARC/WAT/WET 格式

Common Crawl 的資料以三種格式儲存：

**WARC（Web ARChive）：** 完整的爬取記錄，包含 HTTP 請求頭、回應頭、原始回應內容（含 HTML）。這是最大的格式，約占總儲存空間的 80%。

**WAT（Web Archive Transformation）：** 從 WARC 提取的元數據，包含頁面結構資訊、連結、語言偵測結果等。約為 WARC 大小的 10%。

**WET（Web Archive Extraction）：** 從 WARC 提取的純文字內容，已移除 HTML 標籤。這是大多數研究人員使用的格式，約為 WARC 大小的 5%。

### 存取 Common Crawl 資料

Common Crawl 的資料存放在 Amazon S3 上，可以透過 AWS CLI 或 HTTP 直接存取：

```python
import requests

# 取得 WET 檔案列表
url = "https://data.commoncrawl.org/crawl-data/CC-MAIN-2022-33/wet.paths.gz"
# 下載並解壓後，逐行讀取 WET 檔案路徑
```

每個月的爬取產量約 200-400 TB 的 WARC 資料，約 20-40 TB 的 WAT 資料，約 10-20 TB 的 WET 資料。

### 從 Common Crawl 建構語料庫

要從 Common Crawl 建構可用的訓練語料，需要經過以下步驟：

1. **選擇爬取月份**：根據需求選擇特定時間範圍的爬取
2. **下載 WET 檔案**：從 S3 下載對應的 WET 檔案
3. **語言過濾**：使用語言偵測工具（如 fastText、langdetect）篩選目標語言
4. **品質過濾**：去除垃圾內容、重複內容、低品質頁面
5. **清洗與正規化**：執行標準的文字清洗流程
6. **格式轉換**：轉換為 JSONL 或 Parquet 格式

### C4 語料庫的啟發

Google 的 C4（Colossal Clean Crawled Corpus）是從 Common Crawl 中篩選的經典範例。其過濾規則包括：

- 移除頁面包含 JavaScript 警告或「Lorem ipsum」等佔位文字
- 移除包含骯髒詞彙的頁面
- 移除不完整的句子（不包含句點結束）
- 行去重（保留網域內的唯一行）
- 使用 langdetect 過濾非英文頁面

C4 的經驗告訴我們：過濾規則的設計比過濾規則的數量更重要。一條好的規則可以移除大量低品質內容，而過多的規則可能誤傷有價值的內容。

### OSCAR 與其他開源語料

除了 Common Crawl，還有其他重要的開源語料：

- **OSCAR**：從 Common Crawl 中篩選的多語言語料，支援 166 種語言
- **mC4**：Google 發布的多語言 C4 版本，覆蓋 101 種語言
- **Pile**：由 EleutherAI 彙編的 825 GB 英文語料庫，包含學術論文、書籍等多元來源
- **ROOTS**：BigScience 計畫的 1.6 TB 多語言語料庫

---

## 延伸閱讀

- [Common Crawl 官方網站](https://www.google.com/search?q=Common+Crawl+official+website)
- [C4 資料集：Colossal Clean Crawled Corpus](https://www.google.com/search?q=C4+dataset+Google)
- [OSCAR 多語言語料庫](https://www.google.com/search?q=OSCAR+corpus+multilingual)
