# Travis CI 與 GitLab CI（2014-2016）

## 前言

2016 年是雲端 CI 服務爆發的一年。Travis CI 與 GitLab CI 成為開源專案與小型團隊的首選。

## Travis CI 基礎設定

### .travis.yml 結構

```yaml
language: node_js
node_js:
  - "6"
  - "5"
  - "4"

cache:
  directories:
    - node_modules

install:
  - npm install

script:
  - npm run lint
  - npm test

after_success:
  - npm run coverage
  - bash <(curl -s https://codecov.io/bash)

notifications:
  email:
    on_success: change
    on_failure: always
  slack:
    rooms:
      - secure: "encrypted_token_here"
```

## 多環境測試

```yaml
language: python
python:
  - "2.7"
  - "3.4"
  - "3.5"
  - "3.6"

env:
  - DJANGO=1.8
  - DJANGO=1.9
  - DJANGO=1.10

install:
  - pip install -r requirements.txt

script:
  - python -m pytest tests/
  - pip install dj>=${DJANGO}

matrix:
  exclude:
    - python: "2.7"
      env: "DJANGO=1.10"
    - python: "3.4"
      env: "DJANGO=1.8"
```

## 部署配置

```yaml
deploy:
  provider: heroku
  api_key: $HEROKU_API_KEY
  app:
    master: myapp-production
    develop: myapp-staging
  run:
    - "npm run migrate"
    - "npm run seed"
  on:
    all_branches: true
  skip_cleanup: true

  provider: s3
  access_key_id: $AWS_ACCESS_KEY
  secret_access_key: $AWS_SECRET_KEY
  bucket: myapp-deployments
  region: ap-northeast-1
  local-dir: dist
  upload-dir: $TRAVIS_BRANCH/$TRAVIS_BUILD_NUMBER
```

## GitLab CI 基礎

### .gitlab-ci.yml 結構

```yaml
stages:
  - build
  - test
  - deploy

variables:
  NODE_VERSION: "6"
  DOCKER_DRIVER: overlay

cache:
  key: ${CI_COMMIT_REF_NAME}
  paths:
    - node_modules/

build:
  stage: build
  image: node:6-alpine
  script:
    - npm install
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 week

test:unit:
  stage: test
  image: node:6-alpine
  script:
    - npm install
    - npm run test:unit

test:integration:
  stage: test
  image: node:6-alpine
  services:
    - postgres:9.6
  script:
    - npm run test:integration

test:e2e:
  stage: test
  image: node:6-alpine
  script:
    - npm run test:e2e

deploy:staging:
  stage: deploy
  script:
    - ./deploy.sh staging
  only:
    - develop

deploy:production:
  stage: deploy
  script:
    - ./deploy.sh production
  when: manual
  only:
    - master
```

## GitLab CI Runner

```bash
# 安裝 Runner
curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-ci-multi-runner/script.deb.sh | sudo bash
sudo apt-get install gitlab-ci-multi-runner

# 註冊 Runner
sudo gitlab-ci-multi-runner register \
  --non-interactive \
  --url "https://gitlab.com/ci" \
  --token "$REGISTRATION_TOKEN" \
  --description "Docker Runner" \
  --executor "docker" \
  --docker-image "docker:latest" \
  --docker-privileged
```

## GitLab CI 進階功能

### 合併請求 Pipeline

```yaml
test:merge-request:
  stage: test
  only:
    - merge_requests
  script:
    - npm install
    - npm run test:ci
  artifacts:
    paths:
      - coverage/
    name: "coverage-${CI_COMMIT_REF_NAME}"
```

### 環境與部署

```yaml
deploy:production:
  stage: deploy
  environment:
    name: production
    url: https://myapp.com
    on_stop: stop:production
  script:
    - ./deploy.sh production

stop:production:
  stage: deploy
  environment:
    name: production
    action: stop
  script:
    - ./cleanup.sh production
  when: manual
```

### 俥床管道

```yaml
trigger:build:
  stage: trigger
  trigger:
    project: another/project
    strategy: depend
```

## 工具比較

| 功能 | Travis CI | GitLab CI |
|------|-----------|-----------|
| 私人專案 | 需付費 | 免費（自有 Runner） |
| 與 GitHub 整合 | 原生 | 需設定 |
| 與 GitLab 整合 | 有限 | 原生 |
| Pipeline 視覺化 | 基礎 | 進階 |
| Docker 支援 | 良好 | 優秀 |
| 價格 | 免費開源 | 免費開源 |

## 延伸閱讀

- [Travis CI 文檔](https://www.google.com/search?q=travis+ci+tutorial+2016)
- [GitLab CI 文檔](https://www.google.com/search?q=gitlab+ci+tutorial+2016)
- [CI 服務比較](https://www.google.com/search?q=travis+vs+gitlab+ci+2016)

## 結語

雲端 CI 服務讓小規模團隊也能享受自動化的好處。選擇適合的工具，開始你的 DevOps 之旅。

---

*本篇文章為「AI 程式人雜誌 2016 年 11 月號」DevOps 系列之一。*