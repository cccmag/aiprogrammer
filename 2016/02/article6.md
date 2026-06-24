# CI/CD 整合 Docker

## CI/CD 的概念

CI（持續整合）與 CD（持續部署）是現代軟體開發的基本實踐。CI 確保每次程式碼提交都會觸發自動化建置與測試；CD 將通過測試的程式碼自動部署到各環境。

## Jenkins 整合

Jenkins 是最流行的 CI/CD 工具之一，透過 Docker 插件可將 Docker 整合到建置流程中。

### 安裝 Docker 插件

在 Jenkins 管理頁面安裝「Docker」與「Docker Commons」插件。

### Pipeline 範例

```groovy
pipeline {
    agent {
        docker {
            image 'python:3.9-slim'
            args '-u root'
        }
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'pytest tests/'
            }
        }
        stage('Build Image') {
            steps {
                sh '''
                    docker build -t myapp:${GIT_COMMIT} .
                    docker tag myapp:${GIT_COMMIT} myregistry.com/myapp:latest
                '''
            }
        }
        stage('Push') {
            steps {
                sh '''
                    echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USERNAME} --password-stdin
                    docker push myregistry.com/myapp:${GIT_COMMIT}
                '''
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }
}
```

## Travis CI 整合

Travis CI 是 GitHub 專案常用的 CI 服務。

### .travis.yml 設定

```yaml
language: python

services:
  - docker

before_install:
  - docker pull postgres:13
  - docker pull redis:6-alpine

script:
  - docker build -t myapp .
  - docker run -d --name app myapp
  - docker run --link app --link postgres:db --link redis myapp pytest

after_success:
  - |
    if [ "$TRAVIS_BRANCH" == "master" ]; then
      docker tag myapp myregistry.com/myapp:$TRAVIS_COMMIT
      docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
      docker push myregistry.com/myapp
    fi
```

## GitLab CI 整合

GitLab CI 是 GitLab 內建的 CI/CD 功能。

### .gitlab-ci.yml

```yaml
stages:
  - build
  - test
  - deploy

variables:
  IMAGE: myregistry.com/myapp

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $IMAGE:$CI_COMMIT_SHA .
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker push $IMAGE:$CI_COMMIT_SHA

test:
  stage: test
  image: python:3.9
  script:
    - pip install -r requirements.txt
    - pytest tests/

deploy:
  stage: deploy
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker run -d --name app $IMAGE:$CI_COMMIT_SHA
  only:
    - master
```

## Docker Hub 自動建置

Docker Hub 支援從 GitHub 或 Bitbucket 自動建置映象。

1. 連結 GitHub 帳戶
2. 選擇要建置的儲存庫
3. 設定建置規則（分支、標籤）
4. 每次推送都會自動觸發建置

## 多階段建置與小型映象

在 CI/CD 中使用多階段建置可大幅縮小最終映象：

```dockerfile
# 建置階段
FROM golang:1.16 AS builder
WORKDIR /src
COPY . .
RUN go build -o myapp

# 執行階段
FROM alpine:latest
COPY --from=builder /src/myapp .
CMD ["./myapp"]
```

最終映象只有一個可執行檔案，大小可能只有 10MB 左右。

## 參考資源

- https://www.google.com/search?q=Docker+CI+CD+Jenkins+Travis+GitLab+整合+自動化+2016
- https://www.google.com/search?q=Docker+Jenkins+Pipeline+建置+測試+部署+自動化+範例
- https://www.google.com/search?q=多階段建置+Dockerfile+small+image+CI+CD+優化