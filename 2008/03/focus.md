# 本期焦點

## Python 網頁框架 — Django, TurboGears, Pylons

### 引言

2008 年是 Python 網頁框架蓬勃發展的一年。Django 的 MTV 模式、TurboGears 的元件整合、Pylons 的靈活設計，都代表著 Python Web 開發的不同方向。

本期雜誌將帶您深入了解這些框架的核心概念和設計理念。

---

## 大綱

* [Django 核心程式實作](focus_code.md)
   - MTV 模式實現
   - ORM 查詢
   - URL 路由

1. [Python 網頁框架概覽](focus1.md)
   - 框架發展歷史
   - 各框架比較
   - 選擇指南

2. [Django 入門](focus2.md)
   - 安裝與設定
   - 專案結構
   - 第一個 Django 專案

3. [MTV 設計模式](focus3.md)
   - Model-View-Template
   - Django 的 MVC 實現
   - 與傳統 MVC 的差異

4. [Django ORM 資料庫操作](focus4.md)
   - 定義模型
   - 查詢 API
   - 遷移管理

5. [URL 路由與 Views](focus5.md)
   - URL 配置
   - 函數型 Views
   - 請求和回應物件

6. [Templates 樣板系統](focus6.md)
   - 模板語法
   - 標籤和過濾器
   - 模板繼承

7. [Django 實戰：建立部落格](focus7.md)
   - 模型設計
   - Views 實作
   - 模板建立

---

## 濃縮回顧

### Python Web 框架版圖

```
Python Web 框架版圖（2008）：

全功能框架：
├── Django：MTV、Batteries included
├── TurboGears：元件整合、MochiKit
└── Pylons：WSGI、SQLAlchemy、很彈性

微框架：
├── CherryPy：簡單但功能完整
├── web.py：極簡主義
└── Bottle：後來者（2009）

CMS：
├── Plone：Zope 基礎
└── Diazo：視覺化 CMS
```

### Django 的設計哲學

```
Django 設計原則：

1. 快速開發 → 自動化管理介面
2. 明確而非隱晦 → 明確的檔案結構
3. 鬆耦合 → 各元件獨立
4. 一致性 → 統一的程式碼風格
```

### Django vs Rails

| 特性 | Django | Rails |
|------|--------|-------|
| 語言 | Python | Ruby |
| ORM | Django ORM | ActiveRecord |
| 模板 | Django Template | ERB |
| 社群 | 成長中 | 成熟 |
| 學習曲線 | 中等 | 較陡 |

---

## 結論與展望

Django 1.0 即將在 2008 年 9 月發布，這將是 Python Web 開發的重要里程碑。Python 網頁框架的生態將更加完善。

---

## 延伸閱讀

- [Python Web 框架概覽](focus1.md)
- [Django 入門](focus2.md)
- [MTV 模式](focus3.md)
- [ORM 操作](focus4.md)
- [URL 路由](focus5.md)
- [模板系統](focus6.md)
- [實戰部落格](focus7.md)

---

*本期焦點到此結束。*