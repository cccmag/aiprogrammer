# 5. JupyterHub 多使用者環境

## JupyterHub 是什麼？

JupyterHub 是一個多使用者 Jupyter 伺服器，支援數十到數百個使用者同時使用。每個使用者都有自己獨立的 Notebook 環境。

## 典型應用場景

1. **教學環境**：讓學生在各自環境中完成作業
2. **企業資料平台**：為分析師提供安全的 Jupyter 環境
3. **研究協作**：團隊成員共享計算資源

## 安裝方式

### 簡單安裝（適用於小型部署）

```bash
pip install jupyterhub
sudo npm install -g configurable-http-proxy

# 產生設定檔
jupyterhub --generate-config

# 啟動
jupyterhub
```

### Docker 安裝（建議用於生產環境）

```bash
docker run -d \
  --name jupyterhub \
  -p 8000:8000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jupyterhub/jupyterhub jupyterhub
```

## 基本設定

```python
# jupyterhub_config.py

c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000
c.JupyterHub_cookie_secret = b'your-secret-key'

# 驗證方式
c.JupyterHub.authenticator_class = 'dummy'  # 測試用
# c.JupyterHub.authenticator_class = 'oauthenticator.GitHubOAuthenticator'
```

## DockerSpawner

使用 Docker 為每個使用者建立獨立容器：

```bash
pip install dockerspawner

# jupyterhub_config.py
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.container_image = 'jupyter/scipy-notebook:latest'
```

## 系統服務

將 JupyterHub 設定為系統服務（systemd）：

```ini
# /etc/systemd/system/jupyterhub.service
[Unit]
Description=JupyterHub
After=network.target

[Service]
User=root
ExecStart=/usr/local/bin/jupyterhub -f /etc/jupyterhub/jupyterhub_config.py

[Install]
WantedBy=multi-user.target
```

## Z2JH (Zero to JupyterHub)

對於 Kubernetes 部署，Z2HH 提供了完整的指引：

```bash
# Helm chart
helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
helm install jhub jupyterhub/jupyterhub
```

## 效能考量

- 記憶體限制：為每個使用者設定記憶體上限
- CPU 限制：防止單一使用者佔用過多資源
- 儲存：使用持久化儲存保存使用者資料

## 參考資源

- https://www.google.com/search?q=JupyterHub+installation+setup+tutorial+2020
- https://www.google.com/search?q=JupyterHub+DockerSpawner+multi+user+setup+2020
- https://www.google.com/search?q=Zero+to+JupyterHub+Kubernetes+deployment+2020