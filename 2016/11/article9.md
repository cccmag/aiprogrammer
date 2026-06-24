# 安全性整合 DevOps

## 前言

DevSecOps 將安全整合到 DevOps 流程中，讓安全成為每個人的責任，而非事後補救。

## 安全掃描整合

### CI Pipeline 安全檢查

```yaml
# .travis.yml
language: node_js
node_js:
  - "6"

script:
  - npm run lint
  - npm test
  - npm run security-scan

after_script:
  - npm run audit
```

### 自動化安全掃描

```bash
#!/bin/bash
# security-scan.sh

echo "Running security scans..."

# npm 安全稽核
npm audit --audit-level=high

# 靜態代碼安全分析
npm install -g eslint-plugin-security
eslint --plugin security -f stylish src/

# 容器安全掃描
docker scan myapp:latest || true
```

## 常見安全漏洞掃描

### 依賴漏洞

```python
# check_dependencies.py
import subprocess
import json

def check_npm_vulnerabilities():
    result = subprocess.run(
        ['npm', 'audit', '--json'],
        capture_output=True,
        text=True
    )
    
    data = json.loads(result.stdout)
    vulnerabilities = data.get('vulnerabilities', {})
    
    critical = sum(1 for v in vulnerabilities.values() 
                   if v.get('severity') == 'critical')
    
    if critical > 0:
        print(f"Found {critical} critical vulnerabilities!")
        return False
    return True
```

### Docker 安全

```dockerfile
# 安全增強的 Dockerfile
FROM node:6-alpine

# 建立非 root 用戶
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

WORKDIR /app
COPY --chown=appuser:appgroup . .

# 最小化權限
RUN chown -R appuser:appgroup /app

CMD ["node", "index.js"]
```

```yaml
# docker-compose.security.yml
version: '3'

services:
  app:
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
```

## OWASP Top 10 防護

### SQL 注入防護

```python
# sql_injection_prevention.py
from sqlalchemy import text

def safe_query(db, user_id):
    # 使用參數化查詢
    result = db.session.execute(
        text("SELECT * FROM users WHERE id = :id"),
        {"id": user_id}
    )
    return result.fetchone()
```

### XSS 防護

```python
# xss_prevention.py
from markupsafe import escape

def safe_render(user_input):
    # HTML 轉義
    return escape(user_input)
```

## 機密管理

```yaml
# 安全部署設定
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  # base64 編碼
  DB_PASSWORD: c3VwZXJfc2VjcmV0X3Bhc3N3b3Jk
```

## 滲透測試工具

```bash
# 安裝滲透測試工具
brew install nmap
brew install owasp-zap

# 基本掃描
nmap -sV localhost -p 3000

# OWASP ZAP
zap-cli quick-scan http://localhost:3000
```

## 安全檢查清單

- [ ] 所有輸入都有驗證
- [ ] SQL 查詢使用參數化
- [ ] 輸出內容適當編碼
- [ ] 認證與授權正確實作
- [ ] HTTPS 保護所有敏感連接
- [ ] 機密資訊不在程式碼中
- [ ] 依賴套件無已知漏洞
- [ ] 容器不以 root 執行
- [ ] 錯誤訊息不洩漏敏感資訊

## 延伸閱讀

- [OWASP Top 10](https://www.google.com/search?q=owasp+top+10+2016)
- [DevSecOps 實踐](https://www.google.com/search?q=devsecops+2016)
- [容器安全掃描](https://www.google.com/search?q=container+security+scanning+2016)

---

*本篇文章為「AI 程式人雜誌 2016 年 11 月號」DevOps 系列之一。*