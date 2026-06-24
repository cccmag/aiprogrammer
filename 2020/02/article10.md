# Jupyter 安全與部署

## 安全考量

### 程式碼執行風險

Jupyter 允許執行任意 Python 程式碼，這帶來安全風險：

1. **惡意程式碼**：使用者可能執行有害程式碼
2. **資源耗盡**：執行過度運算可能影響伺服器
3. **資料外洩**：存取敏感性資料

## 防護措施

### 限制功能

```python
# jupyterhub_config.py

# 禁用終端機
c.Spawner.env_keep.append('JUPYTER_ALLOW_INSECURE_WRITES')

# 限制能夠啟動的核心
c.KernelSpecManager.ensure_native_kernel = False
```

### 資源限制

```python
# 記憶體限制
c.Spawner.mem_limit = '2G'

# CPU 限制
c.Spawner.cpu_limit = 1

# 最大程序數
c.Spawner.jupyterlab_arg = ['--ServerApp.max_body_length = 100000000']
```

## 網路安全

### 使用 SSL/TLS

```bash
# 產生自我簽署憑證
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes

# 啟動 JupyterHub（使用 HTTPS）
jupyterhub --ssl-key key.pem --ssl-cert cert.pem
```

### 防火牆設定

```bash
# 只允許 SSH 和必要的連接埠
sudo ufw allow 22    # SSH
sudo ufw allow 8000  # JupyterHub
sudo ufw enable
```

## 部署選項

### 1. 反向代理（Nginx）

```nginx
location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

### 2. Docker 部署

```bash
docker run -d \
  --name jupyterhub \
  -p 443:443 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v jupyterhub_config.py:/srv/jupyterhub/jupyterhub_config.py \
  jupyterhub/jupyterhub
```

### 3. Kubernetes 部署

使用 Z2JH（Zero to JupyterHub）Helm chart：

```bash
helm install jhub jupyterhub/jupyterhub \
  --set hub.image.name=jupyter/scipy-notebook \
  --set hub.image.tag=latest
```

## 監控

```bash
# 安裝監控延伸模組
pip install jupyterlab-system-monitor

# 或使用 nbresuse
pip install nbresuse
```

## 清理與維護

```bash
# 清理未使用的容器
docker system prune -f

# 清理 Jupyter 快取
jupyter notebook --clean
```

## 參考資源

- https://www.google.com/search?q=Jupyter+security+best+practices+2020
- https://www.google.com/search?q=JupyterHub+deployment+nginx+ssl+security+2020
- https://www.google.com/search?q=jupyter+notebook+security+protection+limitations+2020