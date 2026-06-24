# Robots.txt 與爬蟲倫理

## 網路爬蟲的法律與道德框架

### Robots.txt 協定

Robots.txt 是網站的「爬蟲守則」，它告訴爬蟲程式哪些路徑可以存取，哪些不可以。這個協定起源於 1994 年，至今仍是網路爬蟲最基本的禮儀規範。

Robots.txt 檔案位於網站的根目錄，格式如下：

```
User-agent: *
Disallow: /private/
Disallow: /api/

User-agent: Googlebot
Allow: /public/
Disallow: /private/
```

- `User-agent`：指定此規則適用的爬蟲
- `Disallow`：禁止存取的路徑
- `Allow`：允許存取的路徑（用於覆蓋 Disallow）

### 爬蟲的法律框架

不同國家對網路爬蟲有不同的法律規範：

**美國：** hiQ Labs v. LinkedIn 案（2019-2022）是爬蟲法律領域的里程碑。法院裁定，存取公開可用的網站資料不違反 CFAA（Computer Fraud and Abuse Act）。但這並不代表所有爬蟲行為都合法。

**歐盟：** GDPR 對個人資料的收集和處理有嚴格限制。爬蟲在收集包含個人資料的網頁時，需要特別注意合規問題。

**台灣：** 目前尚無專門針對網路爬蟲的法律，但可能涉及著作權法、個人資料保護法等。

### 爬蟲倫理原則

除了法律要求，負責任的爬蟲應該遵循以下倫理原則

1. **尊重 Robots.txt**：始終檢查並遵守目標網站的 robots.txt 規則
2. **限制請求頻率**：避免對伺服器造成過大負擔
3. **識別自己**：在 User-Agent 中加入聯絡資訊，讓網站管理員可以聯繫你
4. **尊重版權**：注意網站的授權條款，部分內容禁止用於商業用途
5. **負責任的發布**：在公開爬取的語料庫時，遮罩個人資訊

### 實務中的 Robots.txt 處理

Python 中可以使用 `robotparser` 模組來解析 robots.txt：

```python
from urllib.robotparser import RobotFileParser

rp = RobotFileParser()
rp.set_url('https://example.com/robots.txt')
rp.read()

if rp.can_fetch('MyCrawler/1.0', 'https://example.com/page'):
    print("Allowed to crawl")
else:
    print("Not allowed")
```

### 常見的爭議場景

**公共資料與私有資料的界線：**
即使資料是公開可存取的，也不代表它可以被任意使用。例如，社交媒體上的個人貼文雖然是公開的，但批量爬取和發布可能侵犯隱私。

**學術研究的例外：**
許多國家對學術研究用途的爬蟲有特殊規定。但「學術用途」不應成為規避法律的藉口。

**付費牆後的內容：**
繞過付費牆存取內容，即使使用爬蟲技術可以做到，仍可能違反法律和道德的界線。

### 負責任的爬蟲文化

作為語料庫建構者，我們有責任建立和維護負責任的爬蟲文化。這不僅是為了避免法律風險，更是為了維護整個網路生態系統的健康發展。當爬蟲行為導致網站營運成本增加或用戶體驗下降時，最終受損的是所有依賴網路資料的人。

---

## 延伸閱讀

- [Robots.txt 官方規範](https://www.google.com/search?q=robots+txt+protocol+specification)
- [hiQ Labs v. LinkedIn 案分析](https://www.google.com/search?q=hiQ+Labs+v+LinkedIn+web+scraping)
- [GDPR 對資料爬取的影響](https://www.google.com/search?q=GDPR+web+scraping+compliance)
