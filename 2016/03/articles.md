# 文章索引

## 漏洞防護實戰（article1–5）

這五篇文章專注於最常見的 Web 安全漏洞及其防護方法，包括 SQL 注入、XSS、CSRF 等。

| # | 主題 | 說明 |
|---|------|------|
| 1 | [SQL 注入防護](article1.md) | 參數化查詢、輸入驗證、ORM 安全使用 |
| 2 | [XSS 跨站腳本攻擊](article2.md) | 輸出編碼、內容安全政策、HTTPOnly Cookie |
| 3 | [CSRF 跨站請求偽造](article3.md) | CSRF Token、同源政策、SameSite Cookie |
| 4 | [密碼雜湊與儲存](article4.md) | bcrypt、scrypt、Argon2、鹽值管理 |
| 5 | [JWT 身份驗證](article5.md) | JWT 結構、署名驗證、過期時間設定 |

## 進階安全實戰（article6–10）

這五篇文章涵蓋傳輸安全、API 安全、日誌監控與漏洞掃描。

| # | 主題 | 說明 |
|---|------|------|
| 6 | [HTTPS 與 TLS 設定](article6.md) | TLS 配置、HSTS、憑證管理、混合內容 |
| 7 | [檔案上傳安全](article7.md) | 副檔名驗證、MIME 類型檢查、惡意檔案偵測 |
| 8 | [API 安全設計](article8.md) | 速率限制、OAuth 2.0、API Key 管理 |
| 9 | [日誌與入侵偵測](article9.md) | 安全日誌、異常偵測、SOC 運作 |
| 10 | [漏洞掃描工具](article10.md) | OWASP ZAP、Burp Suite、Nessus、自動化掃描 |

## 閱讀建議

資訊安全是一個需要持續關注的領域。建議先從 article1 到 article3 了解最常見的漏洞類型與防護方法，再根據實際需求深入特定主題。所有開發者都應該熟悉基本的安全漏洞成因與防護原則。

本期提供的 `_code/pw_check.py` 腳本可用於檢測密碼強度，幫助建立更好的密碼習慣。