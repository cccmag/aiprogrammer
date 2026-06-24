# 漏洞掃描工具

## 為什麼需要漏洞掃描

即使遵循安全開發實踐，人為錯誤在所難免。定期執行漏洞掃描可以發現被忽略的問題，是安全防護的重要補充。

## 靜態分析工具

在程式碼階段發現問題，不需要執行應用程式：

### Bandit（Python）

```bash
pip install bandit
bandit -r ./app
```

```bash
# 輸出範例
>> Issue: [B101:assert_used] Use of assert detected.
   Severity: Low   Confidence: High
   Location: app/views.py:10
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b101_assert_used.html
```

### SonarQube

支援多種語言的企業級靜態分析工具：

```bash
# 使用 Docker 執行
docker run -d --name sonarqube -p 9000:9000 sonarqube
```

## 動態掃描工具

在執行階段測試應用程式，發現執行時的漏洞：

### OWASP ZAP

最受歡迎的開源 Web 應用程式掃描器：

```bash
# Docker 執行
docker run -t owasp/zap2docker-stable zap-baseline.py -t https://example.com
```

```bash
# 完整掃描
docker run -t owasp/zap2docker-stable zap-full-scan.py \
    -t https://example.com \
    -r scan_report.html
```

### 使用 ZAP API 進行自動化掃描

```python
import requests

ZAP_API = 'http://localhost:8080'
API_KEY = 'your-api-key'

def spider_scan(target_url):
    # 啟動 spider
    requests.get(
        f'{ZAP_API}/JSON/spider/action/scan/',
        params={
            'url': target_url,
            'apikey': API_KEY
        }
    )

def active_scan(target_url):
    # 啟動主動掃描
    requests.get(
        f'{ZAP_API}/JSON/ascan/action/scan/',
        params={
            'url': target_url,
            'apikey': API_KEY
        }
    )

def get_alerts():
    # 取得掃描結果
    response = requests.get(
        f'{ZAP_API}/JSON/core/view/alerts/',
        params={'apikey': API_KEY}
    )
    return response.json()['alerts']
```

## 滲透測試工具

### Burp Suite

Web 滲透測試的業界標準工具：

```bash
# 啟動
java -jar burpsuite_pro.jar
```

常用功能：
- Proxy：攔截與修改 HTTP 請求
- Spider：自動發現網站結構
- Scanner：自動化漏洞掃描（專業版）
- Intruder：暴力破解與參數 fuzzing
- Repeater：手動修改並重放請求

### SQLMap

專門檢測 SQL 注入的工具：

```bash
# 基本掃描
sqlmap -u "https://example.com/product?id=1"

# 測試 POST 請求
sqlmap -u "https://example.com/login" \
    --data="username=admin&password=admin"

# 枚舉資料庫
sqlmap -u "https://example.com/product?id=1" --dbs

# 轉儲錨定資料
sqlmap -u "https://example.com/product?id=1" -D mydb -T users --dump
```

### Nmap

網路掃描與端口掃描：

```bash
# 基本掃描
nmap -sV example.com

# 作業系統偵測
nmap -O example.com

# 全面掃描
nmap -A -p- example.com
```

## 依賴漏洞掃描

### npm audit

```bash
npm audit
npm audit fix
```

### Safety（Python）

```bash
pip install safety
safety check
```

### OWASP Dependency-Check

```bash
dependency-check --project "My App" --scan ./lib
```

## 自動化 CI/CD 整合

將安全掃描整合到 CI/CD 流程：

```yaml
# .gitlab-ci.yml
stages:
  - test
  - security

bandit:
  stage: test
  script:
    - pip install bandit
    - bandit -r ./app -f json -o bandit-report.json

zap_scan:
  stage: security
  script:
    - docker run --rm owasp/zap2docker-stable zap-baseline.py -t $APP_URL -J zap-report.json
  artifacts:
    reports:
      security: zap-report.json
```

## 漏洞資料庫

- CVE（Common Vulnerabilities and Exposures）：通用漏洞披露
- NVD（National Vulnerability Database）：CVE 的美國國家資料庫
- CWE（Common Weakness Enumeration）：通用漏洞類型
- OWASP Top 10：最常見的 Web 安全風險

## 參考資源

- https://www.google.com/search?q=漏洞掃描+工具+OWASP+ZAP+Burp+Suite+Nmap+2016
- https://www.google.com/search?q=OWASP+ZAP+自動化+掃描+API+Python+整合
- https://www.google.com/search?q=SQLMap+SQL+注入+檢測+教學+範例+2016