# 語料庫管理與版本控制

## DVC、Git LFS、資料集版本

### 為什麼需要版本控制

當語料庫達到 TB 級別時，傳統的版本控制工具面臨巨大挑戰：

- **Git** 無法處理大型二進位檔案
- 資料集的每一次更新都需要完整的檔案拷貝
- 團隊協作時難以追蹤資料的變更歷史
- 實驗的可重複性需要精確的資料版本記錄

為了解決這些問題，資料版本控制工具應運而生。

### DVC（Data Version Control）

DVC 是目前最受歡迎的資料版本控制工具。它的核心思路是將資料檔案儲存在遠端儲存（S3、GCS、本地磁碟），而在 Git 中只維護元數據檔案（.dvc 檔案）。

**基本工作流程：**

```bash
# 初始化 DVC
dvc init

# 加入資料檔案
dvc add data/corpus_2022.parquet

# 設定遠端儲存
dvc remote add -d myremote s3://my-bucket/corpus

# 推送資料
dvc push

# 提交元數據到 Git
git add data/corpus_2022.parquet.dvc .dvc/config
git commit -m "202207 corpus version 1"
```

DVC 的優點包括：

- **輕量級**：Git 倉庫不包含原始資料
- **可重複性**：每個資料版本對應一個 Git commit
- **靈活儲存**：支援 AWS S3、GCP、Azure、SSH 等後端
- **管線支援**：可以定義資料處理管線，自動追蹤依賴關係

### Git LFS（Large File Storage）

Git LFS 是另一種處理大檔案的方案。它將大檔案替換為文本指針，實際內容儲存在遠端伺服器。

```bash
# 安裝 Git LFS
git lfs install

# 指定要追蹤的檔案類型
git lfs track "*.parquet"
git lfs track "*.csv"

# 正常使用 Git 指令
git add data/corpus_2022.parquet
git commit -m "202207 corpus version 1"
git push
```

Git LFS 適合檔案大小在數十 MB 到數 GB 之間的場景。對於超過 100 GB 的超大檔案，DVC 通常更適合。

### Hugging Face Datasets 管理

Hugging Face Datasets 提供了一個統一的資料集存取介面，同時整合了版本控制：

```python
from datasets import load_dataset

# 載入資料集（自動下載和快取）
dataset = load_dataset("oscar", "unshuffled_deduplicated_zh", split="train")

# 資料集包含版本資訊
print(dataset.config_name)  # 資料集配置名稱
```

Hugging Face Datasets 使用 Apache Arrow 作為底層格式，支援：

- **記憶體映射**：不需要將整個資料集載入記憶體
- **懶加載**：只在需要時讀取特定樣本
- **快取**：下載後的資料集自動快取在本地
- **資料集卡片**：每個資料集包含詳細的說明文檔

### 資料溯源與授權管理

語料庫管理不僅是技術問題，還涉及法律和倫理考量：

**資料溯源：**
記錄每個資料樣本的來源 URL、爬取時間、處理歷史。這對於模型的可解釋性和法律合規至關重要。

**授權管理：**
不同網站的內容有不同的使用條款。Common Crawl 要求使用者遵守網站的 robots.txt 規範。創用 CC 授權的內容可以自由使用，但需要標註來源。

### 實用的管理實踐

1. **目錄結構標準化**：統一的資料集目錄結構便於自動化處理
2. **資料集清單**：維護一個 JSON 或 YAML 清單，記錄每個資料集的元數據
3. **自動化測試**：在資料集更新時自動執行品質檢查
4. **變更日誌**：記錄每次資料集更新的原因和範圍

---

## 延伸閱讀

- [DVC 官方文檔](https://www.google.com/search?q=DVC+data+version+control+documentation)
- [Git LFS 使用指南](https://www.google.com/search?q=Git+LFS+large+file+storage+tutorial)
- [Hugging Face Datasets 文檔](https://www.google.com/search?q=HuggingFace+Datasets+library+documentation)
