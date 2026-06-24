# Helm Charts 與應用發布

## Helm 簡介

Helm 是 Kubernetes 的套件管理器，用於定義、安裝和升級複雜的 Kubernetes 應用。Charts 是 Helm 的部署包，包含所有必要的資源定義。

## 基本概念

- **Chart**：一個 Kubernetes 應用的包裝
- **Release**：Chart 的運行實例
- **Repository**：儲存和分發 Charts 的地方

## 安裝 Helm

```bash
brew install helm

# 添加官方 Charts 倉庫
helm repo add stable https://charts.helm.sh/stable
helm repo update
```

## 使用現有 Chart

```bash
# 搜尋 Chart
helm search repo mysql

# 安裝
helm install my-mysql stable/mysql

# 查看 release
helm list

# 升級
helm upgrade my-mysql stable/mysql

# 解除安裝
helm uninstall my-mysql
```

## 建立 Chart

```bash
helm create mychart
```

產生的目錄結構：

```
mychart/
  Chart.yaml          # Chart 元資料
  values.yaml         # 預設配置值
  charts/             # 依賴的子 Charts
  templates/         # K8s 資源模板
    deployment.yaml
    service.yaml
    _helpers.tpl      # 模板幫助函式
```

## Chart.yaml

```yaml
apiVersion: v2
name: mychart
description: My first Helm chart
type: application
version: 1.0.0
appVersion: "1.0"
```

## values.yaml

```yaml
replicaCount: 2

image:
  repository: myapp
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: LoadBalancer
  port: 8000

resources:
  limits:
    memory: 128Mi
    cpu: 500m
  requests:
    memory: 64Mi
    cpu: 250m
```

## 模板變數

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-deployment
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Chart.Name }}
  template:
    metadata:
      labels:
        app: {{ .Chart.Name }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: {{ .Values.image.repository }}:{{ .Values.image.tag }}
        ports:
        - containerPort: {{ .Values.service.port }}
```

## 條件和迴圈

```yaml
{{- if .Values.service.type }}
service:
  type: {{ .Values.service.type }}
{{- end }}

{{- range .Values.env }}
- name: {{ .name }}
  value: {{ .value }}
{{- end }}
```

## 升級與回滾

```bash
# 升級
helm upgrade myapp ./mychart -f values.yaml

# 查看歷史
helm history myapp

# 回滾
helm rollback myapp 1
```

## 結論

Helm 大幅簡化了複雜應用在 Kubernetes 上的部署和管理。學會使用和創建 Charts，是 K8s 進階的必備技能。