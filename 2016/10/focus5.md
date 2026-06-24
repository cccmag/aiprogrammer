# CI/CD 與自動化測試（2010-2016）

## 前言

持續整合（Continuous Integration）與持續交付（Continuous Delivery）改變了軟體部署的方式，自動化測試是其核心。

## CI/CD 流程

```
程式碼提交 → 自動化建置 → 自動化測試 → 部署至測試環境 → 部署至正式環境
     ↓            ↓            ↓              ↓
   Git Hook    Build Server   CI Server     CD Pipeline
```

## 常見 CI 工具

### Jenkins 2.0 Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                sh 'npm install'
                sh 'npm run build'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'npm test'
            }
            post {
                always {
                    junit 'reports/*.xml'
                }
            }
        }
        stage('Deploy') {
            when {
                branch 'master'
            }
            steps {
                echo 'Deploying...'
                sh 'npm run deploy'
            }
        }
    }
}
```

### Travis CI

```yaml
# .travis.yml
language: node_js
node_js:
  - "6"
script:
  - npm test
  - npm run e2e
after_success:
  - npm run coverage
```

### CircleCI

```yaml
# circle.yml
machine:
  node:
    version: 6
dependencies:
  override:
    - npm install
test:
  override:
    - npm test
```

## 自動化測試鉤子

### Git Pre-commit Hook

```bash
#!/bin/sh
# .git/hooks/pre-commit

echo "Running pre-commit tests..."

# 執行單元測試
npm test
if [ $? -ne 0 ]; then
    echo "Tests failed! Commit aborted."
    exit 1
fi

# 執行 linter
npm run lint
if [ $? -ne 0 ]; then
    echo "Linting failed! Commit aborted."
    exit 1
fi

echo "All checks passed!"
```

## GitHub Pull Request 自動化

```python
# .github/workflows/test.yml (2016 年使用 CI 服務)
# 此為概念範例
```

## 自動化部署

### Docker 自動化部署

```bash
#!/bin/bash
# deploy.sh
IMAGE_NAME="myapp"
TAG=$(git rev-parse --short HEAD)

# 建置映像
docker build -t $IMAGE_NAME:$TAG .

# 推送至 registry
docker push $IMAGE_NAME:$TAG

# 在伺服器上部署
ssh deploy@server "docker pull $IMAGE_NAME:$TAG"
ssh deploy@server "docker-compose up -d"
```

## CI/CD 監視

```python
# build_monitor.py
import requests
from datetime import datetime

class BuildMonitor:
    def __init__(self, ci_url, token):
        self.url = ci_url
        self.token = token
    
    def get_last_build_status(self, job_name):
        response = requests.get(
            f"{self.url}/job/{job_name}/lastBuild/api/json",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        data = response.json()
        return {
            "number": data["number"],
            "result": data.get("result", "running"),
            "timestamp": datetime.fromtimestamp(data["timestamp"] / 1000)
        }
```

## 相關資源

- [Jenkins 2.0 Pipeline 文檔](https://www.google.com/search?q=jenkins+2.0+pipeline+tutorial+2016)
- [Travis CI 教學](https://www.google.com/search?q=travis+ci+tutorial+2016)
- [CI/CD 最佳實踐](https://www.google.com/search?q=ci+cd+best+practices+2016)

## 結語

CI/CD 將測試自動化推向極致，讓每次提交都能自動驗證、部署，大幅提升開發效率與軟體品質。

---

*本篇文章為「AI 程式人雜誌 2016 年 10 月號」軟體測試系列之一。*