# 程式碼安全生成

## 1. 引言

AI 生成的程式碼可能含有安全漏洞——這是 LLM 輔助開發的核心風險之一。模型訓練資料來自公開儲存庫，其中包含大量含有漏洞的程式碼。如果開發者不加審查地採用 AI 生成的程式碼，可能將已知的安全弱點引入生產環境。本文探討如何確保 AI 生成的程式碼是安全的。

## 2. AI 生成程式碼的常見漏洞

研究表明，AI 生成的程式碼中常見的安全漏洞包括：

| 漏洞類型 | CWE | 發生率 |
|---------|-----|-------|
| SQL 注入 | CWE-89 | 15% |
| XSS（跨站腳本） | CWE-79 | 12% |
| 路徑遍歷 | CWE-22 | 8% |
| 命令注入 | CWE-78 | 7% |
| Integer Overflow | CWE-190 | 5% |

```python
# 不安全的 AI 生成程式碼
def get_user(user_id: str) -> dict:
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    # SQL 注入風險！
    return db.execute(query).fetchone()

# 安全的版本
def get_user(user_id: str) -> dict:
    query = "SELECT * FROM users WHERE id = ?"
    return db.execute(query, (user_id,)).fetchone()
```

## 3. 安全生成策略

### 3.1 提示中的安全規範

在提示詞中加入安全要求是最直接的方法：

```
請生成安全的程式碼：
1. 使用參數化查詢，不要字串串接 SQL
2. 對所有用戶輸入進行驗證和消毒
3. 使用 HTTPS 而非 HTTP
4. 不硬編碼密碼或 API 金鑰
5. 實作 rate limiting
```

### 3.2 安全專用模型

2025-2026 年出現了專門為安全程式碼生成訓練的模型：

- **Security Copilot (Microsoft)**：整合安全知識
- **CodeSec (Snyk)**：專注於安全程式碼生成
- **SecureCoder**：在安全程式碼資料集上微調的模型

### 3.3 生成後審查管線

最可靠的策略是「生成-掃描-修正」的循環：

```python
# 安全管線示意
def secure_generate(prompt: str) -> str:
    code = llm.generate(prompt)
    vulnerabilities = security_scan(code)
    if vulnerabilities:
        fix_prompt = f"以下程式碼有漏洞：\n{code}\n漏洞：{vulnerabilities}\n請修復"
        code = llm.generate(fix_prompt)
    return code
```

## 4. 安全掃描工具整合

| 工具 | 類型 | 支援語言 |
|------|------|---------|
| Semgrep | 靜態分析 | 30+ 語言 |
| Snyk Code | SAST + AI | 主要語言 |
| CodeQL | 語意分析 | C++、Java、Python |
| Bandit | Python 專用 | Python |
| SonarQube | 品質閘道 | 30+ 語言 |

## 5. 實戰案例

以下是一個提示詞工程的對比：

```python
# 不安全提示
"實作一個檔案上傳 API"

# 安全提示
"實作一個安全的檔案上傳 API，要求：
- 限制檔案類型為 .jpg、.png、.pdf
- 限制檔案大小為 10MB
- 檔案名稱消毒，防止 path traversal
- 儲存到非 web 可存取的目錄
- 回傳 UUID 重新命名的檔案路徑"
```

## 6. 結語

程式碼安全生成不是一個可以事後才考慮的問題。2026 年的最佳實踐是「安全左移」——在提示詞設計階段就將安全性納入考量。未來的發展方向包括安全的程式碼向量資料庫、即時漏洞分析系統、以及可以自動生成安全測試案例的工具。開發者需要記住：AI 是工具，安全是最終的責任。

---

## 延伸閱讀

- [OWASP Top 10](https://www.google.com/search?q=OWASP+Top+10+2026)
- [Snyk AI 安全報告](https://www.google.com/search?q=Snyk+AI+code+security+report)
- [Microsoft Security Copilot](https://www.google.com/search?q=Microsoft+Security+Copilot)
- [AI 生成程式碼安全分析](https://www.google.com/search?q=security+analysis+of+AI+generated+code+paper)
