# CI/CD 與雲端部署流水線

## CI/CD 的意義

持續整合（CI）確保每次程式碼變更都自動建構和測試。持續交付/部署（CD）自動將、通過測試的程式碼部署到各種環境。CI/CD 是雲端原生開發的核心實踐。

## 現代 CI/CD 流程

```
程式碼提交 -> 建構 -> 測試 -> 部署到 Staging -> 部署到 Production
     |         |        |            |               |
   觸發鉤子   編譯    單元測試    整合測試        自動/手動部署
```

## GitHub Actions

```yaml
name: Deploy to Cloud

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1
      - name: Build and push
        uses: docker/build-push-action@v2
        with:
          push: true
          tags: myapp:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Kubernetes
        uses: azure/k8s-deploy@v1
        with:
          manifests: |
            manifests/deployment.yaml
            manifests/service.yaml
          images: |
            myapp:latest
```

## GitLab CI

```yaml
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script:
    - docker build -t myapp:$CI_COMMIT_SHA .
    - docker push myapp:$CI_COMMIT_SHA

test:
  stage: test
  script:
    - docker run myapp:$CI_COMMIT_SHA pytest

deploy:
  stage: deploy
  script:
    - kubectl apply -f k8s/
  only:
    - main
```

## Argo CD（GitOps）

Argo CD 實現 GitOps 流程：

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myapp
    targetRevision: HEAD
    path: deploy/k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## 部署策略

### 滾動更新

逐步替換舊版本 Pod：

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

### Blue-Green 部署

同時運行兩套環境，切換流量：

```yaml
spec:
  replicas: 5
---
# v2 版本
spec:
  replicas: 5
```

### Canary 部署

逐步將流量導向新版本：

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
spec:
  analysis:
    interval: 1m
    threshold: 5
    stepWeight: 10
```

## 結論

CI/CD 流水線是雲端原生開發的必備基礎設施。選擇合適的工具並建立穩定的部署流程，是實現快速、可靠交付的關鍵。