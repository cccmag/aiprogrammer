# 資料版本控制與血緣（2018-2028）

## 為什麼需要資料版本控制？

程式碼有 Git 做版本控制。但資料呢？資料集不斷變化——新資料加入、舊資料修正、特徵重新計算——如果沒有版本控制，ML 實驗就不可能重現。

2017 年的一項研究指出：**超過 60% 的 ML 團隊無法重現三個月前的實驗結果**，主要原因是無法追溯到當時使用的訓練資料。

## DVC：資料版本控制

DVC（Data Version Control）是 2018 年由 Iterative.ai 推出的開源專案，將 Git 的版本控制概念延伸到資料：

```
# DVC 工作流程
git add data.csv        ← 大檔案不能這樣做

# 改用 DVC
dvc add data.csv        ← 建立 data.csv.dvc 指針檔
git add data.csv.dvc    ← 只提交指針
dvc push                 ← 把真實資料推上 S3
```

DVC 的核心設計模式：**中繼資料（指針檔）進 Git，真實資料進物件儲存**。

```yaml
# data.csv.dvc
outs:
- md5: d3b07384d113edec49eaa6238ad5ff00
  size: 134217728
  path: data.csv
```

## LakeFS：資料湖版本控制

2020 年開源的 LakeFS 採用了完全不同的方法——將 Git 的語義直接實作在資料湖上。你可以對 S3 上的資料做 branch、commit、merge、revert：

```
lakefs branch create experiment1
lakefs commit main -m "2028-04-01 batch"
lakefs merge experiment1 main
```

這在實務上極為有用：
- **實驗分支**：在分支上測試新的特徵工程，不影響主線資料
- **時間旅行**：回到任何歷史版本的資料
- **零拷貝**：Git 風格的 diff，未修改的資料不複製

## 資料血緣

資料血緣（Data Lineage）追溯資料從源頭到最終使用的完整路徑：

```
原始日誌 → ETL 清洗 → 特徵計算 → 訓練資料集 → 模型 → 推論結果
    ↑          ↑          ↑            ↑          ↑        ↑
  來源      轉換步驟    特徵版本    資料集版本  模型版本  推論記錄
```

OpenLineage（2019 年開源）是這個領域的標準規範，提供了統一的血緣中繼資料模型。

## Python 範例：DVC 風格的版本控制

```python
import hashlib, json

class DataVersion:
    def __init__(self, storage_path: str = "./data"):
        self.storage = storage_path
        self.manifest = {}

    def add(self, name: str, data: list) -> str:
        content = json.dumps(data, sort_keys=True).encode()
        hash_id = hashlib.sha256(content).hexdigest()[:12]
        path = f"{self.storage}/{hash_id}.json"
        with open(path, "w") as f:
            f.write(content)
        self.manifest[name] = {"hash": hash_id, "path": path}
        return hash_id

    def load(self, name: str) -> list:
        entry = self.manifest.get(name)
        if not entry:
            return []
        with open(entry["path"]) as f:
            return json.load(f)
```

## 延伸閱讀

- [DVC: Data Version Control](https://www.google.com/search?q=DVC+data+version+control)
- [LakeFS: Git for Data Lakes](https://www.google.com/search?q=LakeFS+data+lake+version+control)
- [OpenLineage](https://www.google.com/search?q=OpenLineage+data+lineage+standard)

---

*本篇文章為「AI 程式人雜誌 2028 年 4 月號」資料工程系列之四。*
