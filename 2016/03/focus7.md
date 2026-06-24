# 7. 安全開發生命週期

## 為什麼需要安全開發生命週期

傳統的做法是開發完成後再進行安全測試，但這往往導致兩個問題：修復成本極高，以及进度延遲。安全開發生命週期（SDL）將安全實踐融入整個開發流程，而非作為事後的補救。

## 安全開發生命週期的階段

### 1. 培訓階段

所有開發者都應該接受基本的安全培訓：

- OWASP Top 10 風隊與防護
- 安全編碼原則
- 常見漏洞類型與防範

### 2. 需求分析階段

**威脅建模（Threat Modeling）**

在設計階段就識別潜在的安全風險。常用的方法是 STRIDE 模型：

- **S**poofing（假冒）
- **T**ampering（篡改）
- **R**epudiation（否認）
- **I**nformation Disclosure（資訊洩露）
- **D**enial of Service（阻斷服務）
- **E**levation of Privilege（權限提升）

### 3. 設計階段

**安全設計原則**

**最小攻擊面（Attack Surface Reduction）**：只開放必要的功能與介面。

**預設安全（Secure by Default）**：系統預設應該是安全的，而非預設開放再關閉。

**縱深防禦（Defense in Depth）**：多層保護，單一防線失效不會導致全面淪陷。

**安全失敗（Fail Securely）**：發生錯誤時預設為拒絕存取，而非允許。

### 4. 開發階段

**安全編碼標準**

```python
# 輸入驗證（所有來自外部的資料都應驗證）
def process_input(data):
    # 白名單驗證
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-")
    if not all(c in allowed_chars for c in data):
        raise ValueError("Invalid input")
    return data

# 輸出編碼（根據輸出目標進行適當編碼）
import html
def render_html(untrusted_input):
    return html.escape(untrusted_input)
```

### 5. 測試階段

**自動化安全測試**

```bash
# 使用靜態分析工具檢查程式碼
bandit -r ./app

# 使用 OWASP ZAP 進行渗透測試
zap-cli quick-scan http://example.com
```

### 6. 部署階段

**安全部署檢查清單**

- 確認所有依賴是最新版本，無已知漏洞
- 確認 TLS 憑證有效且配置正確
- 確認錯誤訊息不透露系統資訊
- 確認日誌記錄已開啟
- 確認監控與警報已設定

### 7. 維護階段

**持續監控**

- 訂閱安全通告，及時修補漏洞
- 定期執行滲透測試
- 定期審查日誌，發現異常行為
- 建立事件應變計畫

## DevSecOps

DevSecOps 將安全整合到 DevOps 流程中，實現「安全即代碼」：

- 自動化安全測試
- 基礎設施即程式碼（IaC）包含安全設定
- 容器映象安全掃描
- 合規即程式碼

## 第三方元件安全

使用開源函式庫可加速開發，但也要承擔其中的安全風險：

```bash
# 使用 npm audit 檢查節點依賴漏洞
npm audit

# 使用 safety 檢查 Python 依賴漏洞
pip install safety
safety check
```

## 安全文化

技術工具只是輔助，真正的安全來自於團隊的安全意識：

- 將安全納入 Code Review
- 獎勵發現與報告安全問題
- 定期分享安全資訊
- 不因為赶進度而犧牲安全

## 參考資源

- https://www.google.com/search?q=安全開發生命週期+SDL+DevSecOps+OWASP+威脅建模+2016
- https://www.google.com/search?q=STRIDE+威脅建模+安全設計+原則+最佳實踐
- https://www.google.com/search?q=DevSecOps+安全+自動化+測試+CI+CD+整合+方法