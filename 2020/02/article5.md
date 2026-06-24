# JupyterHub 架設

## 系統需求

- Linux/macOS（Windows 需要 Docker）
- Python 3.6+
- 建議 4GB+ RAM
- Node.js 12+（用於 proxy）

## 基本安裝

### pip 安裝

```bash
pip install jupyterhub

# 安裝 spawner（可選）
pip install dockerspawner
```

### 啟動 JupyterHub

```bash
# 產生設定檔
jupyterhub --generate-config

# 啟動
jupyterhub
```

預設 URL：`http://localhost:8000`

## 驗證設定

### 測試模式（DummyAuth）

```python
# jupyterhub_config.py
c.JupyterHub.authenticator_class = 'dummy'
c.DummyAuthenticator.create_system_users = True
```

### LDAP 驗證

```bash
pip install jupyterhub-ldap
```

```python
c.JupyterHub.authenticator_class = 'ldapauthenticator.LDAPAuthenticator'
c.LDAPAuthenticator.server_address = 'ldap://ldap.example.com'
c.LDAPAuthenticator.bind_dn_template = 'uid={username},ou=users,dc=example,dc=com'
```

### OAuth 驗證（GitHub 為例）

```bash
pip install oauthenticator
```

```python
c.JupyterHub.authenticator_class = 'oauthenticator.GitHubOAuthenticator'
c.GitHubOAuthenticator.oauth_callback_url = 'https://yourhub.com/hub/oauth_callback'
c.GitHubOAuthenticator.client_id = 'your-client-id'
c.GitHubOAuthenticator.client_secret = 'your-client-secret'
```

## DockerSpawner

為每個使用者建立獨立 Docker 容器：

```bash
pip install dockerspawner
```

```python
# jupyterhub_config.py
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# 使用的映像
c.DockerSpawner.container_image = 'jupyter/scipy-notebook:latest'

# 容器名稱前綴
c.DockerSpawner.container_name_prefix = 'jupyter'
```

## Systemd 服務

將 JupyterHub 設定為開機啟動：

```ini
# /etc/systemd/system/jupyterhub.service
[Unit]
Description=JupyterHub
After=network.target

[Service]
User=root
ExecStart=/usr/local/bin/jupyterhub -f /etc/jupyterhub/jupyterhub_config.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable jupyterhub
sudo systemctl start jupyterhub
```

## 資源限制

```python
# jupyterhub_config.py
c.Spawner.mem_limit = '2G'      # 記憶體限制
c.Spawner.cpu_limit = 1.0        # CPU 限制
c.Spawner.env_keep = ['OMP_NUM_THREADS']
```

## Nginx 反向代理

```nginx
# /etc/nginx/sites-available/jupyterhub
location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

## 參考資源

- https://www.google.com/search?q=JupyterHub+installation+setup+tutorial+2020
- https://www.google.com/search?q=JupyterHub+DockerSpawner+authentication+ldap+2020
- https://www.google.com/search?q=JupyterHub+systemd+nginx+deployment+2020