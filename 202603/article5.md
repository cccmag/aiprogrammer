# SQLite 4.0 內建向量搜尋：輕量級資料庫的新局面

## 前言

2026 年 3 月，SQLite 專案發布了 4.0 alpha 版本，帶來了可能是 SQLite 歷史上最具革命性的功能——內建向量搜尋。這項更新讓 SQLite 從傳統關聯式資料庫一躍成為邊緣 AI 應用的理想選擇。本文深入解析這項新能力及其應用場景。

## 向量搜尋的興起

### 什麼是向量搜尋？

向量搜尋是一種基於向量相似度的資訊檢索技術。當我們將文字、圖像或任何資料轉換為向量（稱為 embedding）後，就可以使用向量搜尋來找到「語義上相似」的內容。

```python
# 使用 embedding 模型將文字轉為向量
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
texts = ["AI 是未來", "機器學習很強大", "今天天氣很好"]

# 產生向量
embeddings = model.encode(texts)
# embeddings[0] ≈ embeddings[1]  # AI 和機器學習語義相似
# embeddings[2] 與前兩者差異較大
```

### 為什麼需要 SQLite 向量搜尋？

傳統上，要實現向量搜尋需要專門的向量資料庫如 Pinecone、Weaviate 或 Qdrant。這些服務雖然功能強大，但需要額外的基礎設施。SQLite 4.0 讓我們可以直接在本地進行向量搜尋：

- 零額外依賴
- 單一檔案搞定關係型資料和向量
- 離線可用
- 完美支援邊緣裝置

## SQLite 4.0 向量功能

### 基本語法

```sql
-- 建立帶向量欄位的表
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    content TEXT,
    embedding FLOAT[384]  -- 384 維向量，取決於 embedding 模型
);

-- 插入向量資料
INSERT INTO documents (content, embedding) VALUES (
    '人工智慧將改變世界',
    '[0.123, -0.456, 0.789, ...]'
);

-- 向量相似度搜尋
SELECT content, cosine_distance(embedding, '[0.1, -0.4, 0.7, ...]') as distance
FROM documents
ORDER BY distance
LIMIT 5;
```

### 支援的距離度量

SQLite 4.0 支援多種向量距離計算方式：

| 函式 | 用途 | 適用場景 |
|------|------|----------|
| `cosine_distance` | 餘弦相似度 | 文字相似度、推薦系統 |
| `euclidean_distance` | 歐氏距離 | 影像特徵比對 |
| `dot_product` | 點積 | 需要考慮向量大小的場景 |
| `manhattan_distance` | 曼哈頓距離 | 異常偵測 |

```sql
-- 餘弦相似度搜尋（常用於語意搜尋）
SELECT id, content,
    cosine_distance(embedding, ?) as similarity
FROM documents
WHERE similarity < 0.5  -- 相似度閾值
ORDER BY similarity;

-- 歐氏距離搜尋（常用於圖像比對）
SELECT id, image_name,
    euclidean_distance(feature_vector, ?) as dist
FROM images
ORDER BY dist
LIMIT 10;
```

### HNSW 索引

對於大型資料集，暴力搜尋會變慢。SQLite 4.0 支援 HNSW（Hierarchical Navigable Small World）索引：

```sql
-- 建立 HNSW 索引
CREATE VECTOR INDEX article_embeddings_idx 
ON articles(embedding) USING HNSW(dimensions=384, m=16, ef_construction=200);

-- 向量搜尋（使用索引加速）
SELECT id, title, content
FROM articles
WHERE embedding IN range_search(
    (SELECT embedding FROM articles WHERE id = ?),
    distance_limit = 0.3
)
ORDER BY vector_distance(embedding, (SELECT embedding FROM articles WHERE id = ?));
```

## 實際應用場景

### RAG（檢索增強生成）

```python
import sqlite3
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

conn = sqlite3.connect('knowledge.db')
cursor = conn.cursor()

# 初始化資料庫和表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS knowledge_base (
        id INTEGER PRIMARY KEY,
        question TEXT,
        answer TEXT,
        embedding FLOAT[384]
    )
''')

# 建立索引
cursor.execute('''
    CREATE VECTOR INDEX IF NOT EXISTS kb_idx 
    ON knowledge_base(embedding) USING HNSW(dimensions=384)
''')

def add_knowledge(question: str, answer: str):
    embedding = model.encode(question).tolist()
    cursor.execute(
        'INSERT INTO knowledge_base (question, answer, embedding) VALUES (?, ?, ?)',
        (question, answer, str(embedding))
    )
    conn.commit()

def search_knowledge(query: str, top_k: int = 3):
    query_embedding = model.encode(query).tolist()
    cursor.execute('''
        SELECT question, answer,
            cosine_distance(embedding, ?) as distance
        FROM knowledge_base
        ORDER BY distance
        LIMIT ?
    ''', (str(query_embedding), top_k))
    
    return cursor.fetchall()

# 使用
add_knowledge(
    "什麼是機器學習？",
    "機器學習是人工智慧的一個分支，專注於讓電腦從資料中學習。"
)

results = search_knowledge("電腦怎麼學習？")
for q, a, d in results:
    print(f"問題: {q}\n答案: {a}\n相似度距離: {d}\n")
```

### 本地 AI 聊天機器人

```python
import sqlite3
import ollama

conn = sqlite3.connect('chat_history.db')

# 對話歷史也變成可搜尋的向量
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        role TEXT,
        content TEXT,
        embedding FLOAT[384]
    )
''')

def save_message(role: str, content: str, embedding):
    cursor.execute(
        'INSERT INTO messages (role, content, embedding) VALUES (?, ?, ?)',
        (role, content, str(embedding))
    )
    conn.commit()

def retrieve_relevant_context(query: str, limit: int = 5):
    query_emb = model.encode(query).tolist()
    cursor.execute('''
        SELECT content FROM messages
        ORDER BY cosine_distance(embedding, ?)
        LIMIT ?
    ''', (str(query_emb), limit))
    return [row[0] for row in cursor.fetchall()]

def chat(query: str):
    # 檢索相關上下文
    context = retrieve_relevant_context(query)
    
    # 組合 prompt
    prompt = f"""
相關對話上下文：
{chr(10).join(context)}

使用者問題：{query}

請根據上下文回答：
"""
    
    # 呼叫本地 LLM
    response = ollama.chat(model='llama4', messages=[
        {'role': 'user', 'content': prompt}
    ])
    
    # 儲存對話
    save_message('user', query, model.encode(query).tolist())
    save_message('assistant', response['message']['content'], 
                 model.encode(response['message']['content']).tolist())
    
    return response['message']['content']
```

### 圖像相似度搜尋

```python
import sqlite3
import torch
from torchvision import models, transforms
from PIL import Image

model = models.resnet50(pretrained=True)
model = torch.nn.Sequential(*list(model.children())[:-1])  # 移除分類頭
model.eval()

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                         std=[0.229, 0.224, 0.225])
])

conn = sqlite3.connect('image_features.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY,
        filename TEXT,
        feature FLOAT[2048]
    )
''')

def extract_features(image_path: str) -> list:
    img = Image.open(image_path).convert('RGB')
    tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        features = model(tensor).squeeze().tolist()
    return features

def find_similar_images(query_image: str, limit: int = 5):
    query_features = extract_features(query_image)
    cursor.execute('''
        SELECT filename, euclidean_distance(feature, ?) as dist
        FROM images
        ORDER BY dist
        LIMIT ?
    ''', (str(query_features), limit))
    return cursor.fetchall()
```

## 效能考量

### 何時使用索引

```sql
-- 小型資料集：暴力搜尋更快
SELECT * FROM documents
ORDER BY cosine_distance(embedding, ?)
LIMIT 10;

-- 大型資料集：使用 HNSW 索引
CREATE VECTOR INDEX idx ON documents(embedding) USING HNSW(dimensions=384);
```

### 記憶體使用

HNSW 索引的記憶體佔用約為原始向量的 1.5-2 倍。對於記憶體受限的環境，建議：

- 選擇較小的 embedding 模型（如 384 維而非 1536 維）
- 使用量化向量
- 控制索引參數（降低 `m` 和 `ef_construction`）

## 限制與未來

### 目前限制

- Alpha 版本尚未完全穩定
- 尚不支援 IVF-Flat 以外的索引類型
- 跨平台的預編譯二進制尚未提供

### 未來發展

根據 SQLite 團隊的路線圖：

- Q3 2026：支援向量更新和刪除
- Q4 2026：支援 IVF-Flat 和 PQ 量化
- 2027：支援混合搜尋（向量 + 傳統 SQL 過濾）

## 結語

SQLite 4.0 的向量搜尋功能為本地 AI 應用開闢了新的可能性。從 RAG 系統到智慧聊天機器人，開發者現在可以在不增加額外依賴的情況下，輕鬆實現強大的向量搜尋能力。這對於注重隱私、需要在邊緣裝置運行、或希望降低基礎設施成本的應用來說，無疑是重大利好。

---

**延伸閱讀**

- [SQLite 4.0 官方文件](https://www.sqlite.org/draft/vecs.html)
- [HNSW 演算法原理](https://arxiv.org/abs/1603.09320)
- [Embedding 模型選擇指南](https://huggingface.co/sentence-transformers)
