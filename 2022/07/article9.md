# 資料集管理：Hugging Face Datasets

## 使用 Hugging Face Datasets 管理語料庫

### 為什麼選擇 Hugging Face Datasets

Hugging Face Datasets 已成為 NLP 領域管理資料集的標準工具，提供統一的 API 存取和處理資料集。核心優勢包括：統一的程式碼在不同資料集上皆可運作、使用 Apache Arrow 記憶體映射支援大於記憶體的資料、自動快取下載的資料集、完善的版本控制。

### 基本用法

```python
from datasets import load_dataset

dataset = load_dataset("imdb", split="train")
print(dataset)
# Dataset({ features: ['text', 'label'], num_rows: 25000 })

# 存取樣本
print(dataset[0])
# {'text': 'I really liked...', 'label': 1}

# 切片與過濾
subset = dataset.select(range(100))
filtered = dataset.filter(lambda x: x['label'] == 1)

# 映射轉換
def add_word_count(example):
    example['word_count'] = len(example['text'].split())
    return example
dataset = dataset.map(add_word_count)
```

### 處理本地語料庫

```python
# 從 JSONL 載入
dataset = load_dataset('json', data_files='corpus.jsonl', split='train')
# 從 CSV 載入
dataset = load_dataset('csv', data_files='corpus.csv', delimiter='\t', split='train')
# 從 Parquet 載入
dataset = load_dataset('parquet', data_files='corpus.parquet', split='train')
```

### 資料集處理

`map` 函式可高效處理大規模資料集，支援多執行緒：

```python
def clean_text(example):
    import re
    example['text'] = re.sub(r'<[^>]+>', '', example['text'])
    return example

cleaned = dataset.map(clean_text, num_proc=4, remove_columns=['html'])
```

### 資料集分割與共享

```python
# 訓練/測試分割
splits = dataset.train_test_split(test_size=0.1, seed=42)

# 上傳到 Hugging Face Hub
dataset.push_to_hub("your-username/your-dataset")
```

### 實務建議

使用 Parquet 或 Arrow 格式取代 JSON/CSV 提升效率；對大規模資料使用批次處理和 `num_proc` 參數；定期清理快取目錄 `~/.cache/huggingface/datasets`；為資料集撰寫 README 卡片記錄來源、處理流程和授權資訊。

---

## 延伸閱讀

- [Hugging Face Datasets 文檔](https://www.google.com/search?q=huggingface+datasets+library+documentation)
- [Apache Arrow 格式介紹](https://www.google.com/search?q=apache+arrow+columnar+format)
- [Hugging Face Hub 資料集上傳指南](https://www.google.com/search?q=huggingface+hub+upload+dataset)
