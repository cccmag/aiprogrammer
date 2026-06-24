# Google App Engine 與 PaaS：雲端平台

## PaaS 的概念

### 平台即服務

```markdown
# PaaS 提供

1. 運行環境
   - 語言執行環境
   - 框架支援

2. 自動擴展
   - 根據流量自動擴展
   - 負載均衡

3. 托管服務
   - 資料庫
   - 快取
   - 儲存
```

## Google App Engine

### 支援語言

```python
# 2009 年 GAE 支援

# Python（首發）
# - Django（有限支援）
# - webapp 框架
# - datastore

# Java（2009 年新增）
# - Servlet
# - Spring
# - JPA
```

### 限制

```python
# GAE 限制（2009年）

# 請求處理時間：30 秒
# 檔案上傳：1 MB
# 回應大小：10 MB
# Datastore 項目：1 MB
# 無檔案系統寫入
# 無長期執行緒
```

## 其他 PaaS

```markdown
# 2009 年的 PaaS 選項

1. Google App Engine
   - Python, Java

2. Heroku
   - Ruby, Node.js

3. Engine Yard
   - Ruby

4. Windows Azure (preview)
   - .NET
```

## 結語

PaaS 簡化了部署和運維，讓開發者專注於程式碼。

---

*本篇文章為「AI 程式人雜誌 2009 年 11 月號」焦點系列之一。*