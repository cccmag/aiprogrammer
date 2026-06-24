# Google Apps 企業套件

## Google Apps 概述

Google Apps（現 Google Workspace）是一套雲端辦公軟體。

### 包含服務

| 服務 | 說明 |
|------|------|
| Gmail | 企業郵件 |
| Calendar | 線上日曆 |
| Docs | 線上文檔、試算表、簡報 |
| Drive | 雲端儲存 |
| Sites | 網站建立 |
| Hangouts | 視訊會議 |

## Google Apps for Business

### 方案

```python
# Google Apps 版本
editions = {
    'Free': '基本功能，有限儲存',
    'Standard': '每用戶 $5/月，30GB',
    'Business': '每用戶 $10/月，無限儲存'
}
```

### 管理控制台

```python
# 管理功能
admin_features = [
    '使用者管理',
    '網域設定',
    '安全政策',
    '行動裝置管理',
    '報告和分析'
]
```

## API 存取

### Google Data API

```python
# 使用 gdata 庫存取 Google Docs
import gdata.spreadsheet.service

client = gdata.spreadsheet.service.SpreadsheetsService()
client.ClientLogin('email', 'password')
```

### Google Calendar API

```python
# 新增事件
event = {
    'summary': '會議',
    'start': { 'dateTime': '2008-07-15T10:00:00' },
    'end': { 'dateTime': '2008-07-15T11:00:00' }
}
```

## Google Apps Marketplace

### 第三方應用

2008 年 Google 推出 Marketplace，允許企業安裝第三方應用：

```python
# Marketplace 應用類型
marketplace_apps = [
    'CRM 整合',
    '專案管理',
    '人力資源',
    '財務工具',
    '分析報表'
]
```

## 與 Microsoft Office 比較

| 功能 | Google Docs | Microsoft Office |
|------|-------------|------------------|
| 文檔編輯 | 線上 | 本地 |
| 協作 | 即時 | 需要 SharePoint |
| 格式相容 | 基本 | 完全 |
| 離線 | 需設定 | 完全支援 |
| 價格 | 低（免費/付費） | 高（授權費用） |

## 結論

Google Apps  democratized 辦公軟體，讓小型企業也能使用企業級工具。

---

**延伸閱讀**

- [SaaS 的興起與發展](focus1.md)
- [Salesforce 與 CRM 雲端化](focus2.md)
- [Google+Apps+enterprise](https://www.google.com/search?q=Google+Apps+enterprise+2008)