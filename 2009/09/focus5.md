# CAP 理論與最終一致性：分散式系統基礎

## CAP 理論的起源

### Eric Brewer 的猜測

2000 年，UC Berkeley 的 Eric Brewer 教授在 PODC（分散式系統原理研討會）上提出了 CAP 猜測。2002 年，Seth Gilbert 和 Nancy Lynch 證明了這個猜測，形成了 CAP 定理。

```markdown
CAP 定理：

任何分散式系統只能同時滿足以下三個特性中的兩個：

1. Consistency（一致性）
   - 所有節點看到相同的資料
   - 所有讀取返回最新寫入

2. Availability（可用性）
   - 每個請求都得到回應
   - 系統持續可用

3. Partition Tolerance（分割容錯）
   - 網路分割時系統仍可運作
   - 節點之間可以斷開連線
```

## CAP 視覺化

```
           C / A
           ╱ ╲
          ╱   ╲
         ╱  P  ╲
        ╱  ╲   ╱
       ╱    ╲ ╱
      ──────────────
      Consistency / Availability

在網路分割（Partition）發生時：
- 必須在一致性（C）和可用性（A）之間選擇
```

## 一致性 vs 可用性

### 傳統 RDBMS 的選擇

```python
# 傳統資料庫選擇一致性

# 當網路分割發生時：
# - 資料庫選擇犧牲可用性
# - 拒絕寫入直到分割恢復
# - 確保資料一致性

# 銀行轉帳範例：
# - 如果網路分割
# - 轉帳操作會被拒絕
# - 使用者無法轉帳
# - 但帳戶餘額是正確的
```

### NoSQL 的選擇

```python
# NoSQL 資料庫選擇可用性

# 當網路分割發生時：
# - 資料庫選擇犧牲一致性
# - 允許讀取可能過時的資料
# - 寫入最終會同步

# 社交網路範例：
# - 如果網路分割
# - 使用者仍可發文
# - 某些人可能短時間看不到
# - 但最終所有用戶都會看到
```

## 一致性模型

### 強一致性

```python
# 強一致性：所有讀取都看到最新寫入

# 線性一致性（Linearizability）
# - 讀寫操作看起來是原子的
# - 任何讀取都返回最近寫入的值

# 實現方式：
# - 單一领导者（Single Leader）
# - 共識演算法（Raft, Paxos）
# - 同步複製
```

### 最終一致性

```python
# 最終一致性：系統保證如果沒有新寫入，最終所有副本將一致

# 特點：
# - 讀取可能返回過時資料
# - 衝突需要解決
# - 系統最終收斂

# 應用場景：
# - 社交網路
# - 部落格評論
# - 即時分析

# 參數：
# - 「最近」是多久？
# - 應用可以接受多長時間的不一致？
```

### 其他一致性模型

```markdown
一致性光譜：

強一致性 ←→ 最終一致性

1. 線性一致性（Linearizability）
   - 最強
   - 所有操作即時排序

2. 順序一致性（Sequential Consistency）
   - 所有進程看到相同順序

3. 因果一致性（Causal Consistency）
   - 保持因果關係

4. 讀寫一致性（Read-your-writes Consistency）
   - 讀取自己之前的寫入

5. 會話一致性（Session Consistency）
   - 同一會話內保證

6. 最終一致性（Eventual Consistency）
   - 最弱
   - 最終收斂
```

## 分割發生時的策略

### 悲觀策略

```python
# 分割檢測時停止寫入

# 當網路分割發生時：
# 1. 檢測到分割
# 2. 停止寫入服務
# 3. 顯示「系統維護中」
# 4. 等待分割恢復

# 優點：保證一致性
# 缺點：犧牲可用性
```

### 樂觀策略

```python
# 分割時繼續服務

# 當網路分割發生時：
# 1. 檢測到分割
# 2. 兩個分割都繼續服務
# 3. 寫入本地副本
# 4. 分割恢復後同步
# 5. 解決衝突

# 優點：保持可用性
# 缺點：需要衝突解決
```

## 衝突解決

### 衝突檢測

```python
# CouchDB 的衝突處理

# 衝突文件
{
  "_id": "doc1",
  "_rev": "2-xxx",
  "value": "original"
}

# 複本 1
{
  "_id": "doc1",
  "_rev": "3-yyy",
  "value": "modified1"
}

# 複本 2
{
  "_id": "doc1",
  "_rev": "3-zzz",
  "value": "modified2"
}

# CouchDB 將第一個版本保留為主版本
# 其他版本標記為衝突
# 應用層負責解決
```

### 衝突解決策略

```python
# 衝突解決策略

# 1. Last Write Wins（最後寫入優先）
# 基於時間戳或版本號
def resolve_last_write_wins(local, remote):
    if local.timestamp > remote.timestamp:
        return local
    return remote

# 2. 應用層合併
def resolve_application_merge(local, remote):
    # 業務邏輯合併
    merged = {
        "name": local.name or remote.name,
        "emails": list(set(local.emails + remote.emails)),
        "last_modified": max(local.timestamp, remote.timestamp)
    }
    return merged

# 3. 保留所有版本
def resolve_keep_all(local, remote):
    return {
        "versions": [local, remote],
        "conflict": True
    }
```

## 結語

CAP 理論是理解分散式系統的基礎。2009 年的 NoSQL 運動讓更多開發者理解了這些權衡。

下一篇文章將介紹 MongoDB 的副本集和分片機制。

---

## 延伸閱讀

- [CAP 理論原始論文](https://www.google.com/search?q=CAP+theorem+Brewer+2000)
- [CAP 理論解釋](https://www.google.com/search?q=CAP+theorem+explained)
- [最終一致性模型](https://www.google.com/search?q=eventual+consistency+model)
- [衝突解決策略](https://www.google.com/search?q=conflict+resolution+strategies)

---

*本篇文章為「AI 程式人雜誌 2009 年 9 月號」焦點系列之一。*