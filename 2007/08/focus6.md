# 主題六：開放原始碼商業模式

## 永續經營的探索

開源軟體如何盈利？這是 2007 年許多開源公司和創業者最關心的問題。經過多年的探索，開源軟體的商業模式已經逐漸清晰，但仍需要在商業利益和開源精神之間找到平衡。

## 開源軟體公司的類型

### 1. 開放核心模式

```markdown
# 開放核心 (Open Core)
# 核心代碼開源，商業版提供額外功能

模式：
開源版：基礎功能 + 原始碼
商業版：進階功能 + 支援 + 服務

範例：
- MySQL：社群版 vs 企業版
- Redis：開源 vs Redis Enterprise
- Elastic：開源 vs Elastic Cloud
```

### 2. 雙重授權模式

```python
"""
MySQL 雙重授權模式示意
"""

def license_model():
    print("""
MySQL 授權選項：

1. GPL 授權（免費）
   - 適用於開源專案
   - 必須公開修改的原始碼
   - 不能用於商業產品

2. 商業授權（付費）
   - 可用於專有軟體
   - 不需要公開原始碼
   - 提供技術支援

定價參考（2007 年）：
- 基本支援：$595/年起
- 企業級：$3,995/年起
    """)

license_model()
```

### 3. 支援和服務訂閱

```markdown
# 支援訂閱模式
# 軟體本身免費，但提供有償支援

Red Hat 模式：
- 訂閱費用：取決於伺服器數量和服務等級
- 提供內容：安全更新、錯誤修正、技術支援
- 訂閱者的權利：使用預編譯的 RPM、存取知識庫

Canonical 模式：
- 桌上型：免費
- 伺服器：根據援助等級收費
- 雲端：Ubuntu Advantage 服務
```

### 4. 雲端服務模式

```bash
# 軟體即服務 (SaaS)
# 不賣軟體，賣服務

範例：
- Google Apps (基於開源軟體)
- GitHub (基於開源 Git)
- SourceForge (開源專案託管)

優勢：
- 無需安裝維護
- 按使用量收費
- 自動更新
```

## 成功的開源公司案例

### Red Hat

```markdown
# Red Hat 商業模式

核心產品：
- Red Hat Enterprise Linux (RHEL)
- Red Hat Satellite
- Red Hat Directory Server

營收模式：
1. 訂閱收入
   - 伺服器訂閱：$349/年起（基本）
   - 桌上型訂閱：$49/年

2. 專業服務
   - 培訓
   - 諮詢
   - 客製化開發

2007 年營收：
- 年營收超過 5 億美元
- 成為第一家營收超過 10 億美元的開源公司
```

### MySQL AB

```markdown
# MySQL 商業模式

營收來源：
1. 軟體授權
   - GPL 授權（免費）
   - 商業授權（$595 起）

2. 支援和服務
   - MySQL 標準支援：$595/年起
   - 企業級支援：$5,000/年起

3. 培訓和認證
   - MySQL DBA 認證
   - 培訓課程

2007 年：
- 全球員工超過 400 人
- 超過 10,000 付費客戶
- 最終於 2008 年被 Sun Microsystems 收購
```

### Canonical

```markdown
# Canonical 商業模式

公司策略：
- Ubuntu 本身免費
- 透過服務獲利

營收來源：
1. Ubuntu 支援服務
   - Ubuntu Advantage
   - 伺服器：$750/伺服器/年
   - 雲端：按使用量收費

2. 雲端基礎設施
   - Ubuntu One
   - Launchpad 企業版

3. OEM 合作
   - 與硬體廠商合作預裝
```

## 硬體廠商模式

### IBM 和 Intel

```markdown
# 硬體廠商支援開源

IBM 的策略：
- 投入開源專案開發（如 Eclipse）
- 提供開源軟體的支援服務
- 將開源軟體作為硬體銷售的一部分

Intel 的策略：
- 開源顯示卡驅動
- 提供 Linux 最佳化
- 參與核心開發
```

## 基金會模式

### 開源基金會

```markdown
# 非營利組織

Apache Software Foundation (ASF)
- 管理 70+ 開源專案
- 會員費和贊助支持
- 保護開源專利

Mozilla Foundation
- Firefox 瀏覽器
- 主要收入：Google 搜尋合作
- 維持 Firefox 的獨立性

Free Software Foundation (FSF)
- 推動自由軟體
- GPL 授權守護者
- 募款支持開發者
```

## 混合模式

### 複合策略

```python
"""
多種營收來源結合
"""

def business_models():
    models = [
        {
            "name": "開放核心",
            "desc": "基礎免費，高階付費",
            "example": "MySQL, Redis, Elastic"
        },
        {
            "name": "訂閱支援",
            "desc": "軟體免費，支援收費",
            "example": "Red Hat, Canonical"
        },
        {
            "name": "雲端服務",
            "desc": "SaaS 訂閱收費",
            "example": "GitHub, GitLab"
        },
        {
            "name": "廣告/流量",
            "desc": "免費工具帶來流量",
            "example": "SourceForge, OpenOffice.org"
        },
        {
            "name": "硬體整合",
            "desc": "軟體帶動硬體銷售",
            "example": "Android, ChromeOS"
        },
        {
            "name": "基金會支援",
            "desc": "捐款和贊助",
            "example": "Apache, Mozilla"
        }
    ]

    print("開源軟體商業模式：")
    for m in models:
        print(f"\n{m['name']}:")
        print(f"  描述: {m['desc']}")
        print(f"  範例: {m['example']}")

business_models()
```

## 挑戰與批評

### 常見問題

```markdown
# 開源商業模式的挑戰

1. 誰來付費？
   - 開發者傾向免費使用
   - 企業想等社群版成熟
   - 免費替代品競爭激烈

2. 營收與社群平衡
   - 商業功能不應太重要
   - 不能忽視社群貢獻
   - 保持社群信任

3. 專利和侵權
   - 專利風險
   - 授權合規
   - 侵權訴訟

4. 人才招募
   - 開源社群 vs 傳統雇員
   - 報酬公平性
```

## 未來趨勢

### 2007 年的觀察

```markdown
# 趨勢預測：

1. 雲端化
   - 更多 SaaS 產品
   - 按需訂閱

2. 行動化
   - Android 的商業模式探索
   - 應用商店分紅

3. 企業化
   - 更多大企業參與開源
   - 企業級開源專案

4. 多元化
   - 新的商業模式探索
   - 結合多種收入來源
```

## 結語

開源軟體的商業化是一個持續演進的過程。2007 年，我們看到了多種成功的商業模式：Red Hat 的訂閱服務、MySQL 的雙重授權、Canonical 的雲端服務，以及各種基金會的非營利運作。雖然商業模式和開源精神之間存在張力，但成功的開源公司已經證明兩者可以共存。下一個十年將會有更多的創新和實驗。

---

*延伸閱讀：*
- [開源商業模式](https://developers.google.com/search/?q=open+source+business+models)
- [Red Hat 商業模式](https://developers.google.com/search/?q=red+hat+business+model)