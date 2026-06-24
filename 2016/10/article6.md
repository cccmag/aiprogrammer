# 持續整合實踐

## 前言

持續整合（CI）將程式碼提交、自動化建置與測試整合成一個流暢的工作流程。2016 年，CI 已成為專業軟體開發的標準實踐。

## CI 基本原則

1. **頻繁提交**：每天至少提交一次
2. **自動化建置**：按鈕即建置
3. **快速回饋**：發現問題立即通知
4. **透明可见**：所有人都能看到狀態

## Jenkins 2.0 Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source...'
                checkout scm
            }
        }
        stage('Build') {
            steps {
                echo 'Building application...'
                sh 'npm install'
                sh 'npm run build'
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'npm test'
            }
            post {
                always {
                    junit 'test-results/**/*.xml'
                    publishHTML target: [
                        reportDir: 'coverage',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ]
                }
            }
        }
        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                echo 'Deploying to staging...'
                sh 'npm run deploy:staging'
            }
        }
        stage('Deploy to Production') {
            when {
                branch 'master'
            }
            steps {
                echo 'Deploying to production...'
                sh 'npm run deploy:production'
            }
        }
    }
    post {
        failure {
            slackSend channel: '#devops',
                      message: "Build failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
        success {
            slackSend channel: '#devops',
                      message: "Build succeeded: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
    }
}
```

## Travis CI

```yaml
# .travis.yml
language: node_js
node_js:
  - "6"
  - "5"

cache:
  directories:
    - node_modules

install:
  - npm install

script:
  - npm run lint
  - npm test
  - npm run coverage

after_success:
  - npm run codecov

deploy:
  provider: heroku
  api_key: $HEROKU_API_KEY
  app: my-app-staging
  on:
    branch: develop
```

## GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy

variables:
  NODE_VERSION: "6"

cache:
  key: ${CI_COMMIT_REF_NAME}
  paths:
    - node_modules/

build:
  stage: build
  script:
    - npm install
    - npm run build
  artifacts:
    paths:
      - dist/

test:
  stage: test
  script:
    - npm test
    - npm run e2e
  coverage: '/Coverage: \d+\.\d+%/'

deploy_staging:
  stage: deploy
  script:
    - npm run deploy:staging
  only:
    - develop

deploy_production:
  stage: deploy
  script:
    - npm run deploy:production
  only:
    - master
```

## 自動化鉤子

### Pre-commit Hook

```bash
#!/bin/sh
# .git/hooks/pre-commit

echo "Running pre-commit checks..."

# 執行 Lint
npm run lint
if [ $? -ne 0 ]; then
    echo "Lint failed!"
    exit 1
fi

# 執行單元測試
npm test
if [ $? -ne 0 ]; then
    echo "Tests failed!"
    exit 1
fi

echo "All checks passed!"
```

### Post-receive Hook

```bash
#!/bin/sh
# .git/hooks/post-receive

DEPLOY_BRANCH="production"

if [ "$CI_BRANCH" = "$DEPLOY_BRANCH" ]; then
    echo "Deploying to production..."
    ./deploy.sh production
fi
```

## CI 監視與通知

```python
# ci_monitor.py
import requests
from datetime import datetime

class CINotifier:
    def __init__(self, slack_webhook):
        self.webhook = slack_webhook
    
    def notify(self, job_name, build_number, status, duration):
        color = 'good' if status == 'success' else 'danger'
        message = {
            'attachments': [{
                'color': color,
                'fields': [
                    {'title': 'Job', 'value': job_name, 'short': True},
                    {'title': 'Build', 'value': str(build_number), 'short': True},
                    {'title': 'Status', 'value': status.upper(), 'short': True},
                    {'title': 'Duration', 'value': f'{duration}s', 'short': True}
                ]
            }]
        }
        requests.post(self.webhook, json=message)
```

## 延伸閱讀

- [Jenkins 2.0 教學](https://www.google.com/search?q=jenkins+2.0+pipeline+tutorial+2016)
- [Travis CI 自動化部署](https://www.google.com/search?q=travis+ci+deployment+tutorial+2016)
- [CI/CD 最佳實踐](https://www.google.com/search?q=ci+cd+best+practices+2016)

---

*本篇文章為「AI 程式人雜誌 2016 年 10 月號」軟體測試系列之一。*