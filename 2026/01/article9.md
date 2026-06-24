# VS Code 遠端開發

## Remote SSH

在本地 VS Code 中編輯遠端伺服器的檔案，如同在本機開發。

```bash
# 安裝 Remote SSH 擴充功能
code --install-extension ms-vscode-remote.remote-ssh

# 設定 SSH 連線
# 按 F1 → Remote-SSH: Connect to Host → 輸入 ssh user@remote-server
```

設定檔位於 `~/.ssh/config`：

```
Host ai-server
    HostName 192.168.1.100
    User developer
    IdentityFile ~/.ssh/id_rsa
    LocalForward 8888 localhost:8888
```

## Dev Containers

直接在 Docker 容器中進行開發，環境與部署完全一致。

```json
// .devcontainer/devcontainer.json
{
    "name": "AI Development",
    "image": "pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime",
    "runArgs": ["--gpus", "all"],
    "customizations": {
        "vscode": {
            "extensions": [
                "ms-python.python",
                "ms-toolsai.jupyter",
                "GitHub.copilot"
            ]
        }
    },
    "postCreateCommand": "pip install -r requirements.txt",
    "forwardPorts": [8888, 8000]
}
```

## 遠端 Jupyter

VS Code 可以直接連接到遠端的 Jupyter 伺服器：

```python
# 在遠端啟動 Jupyter
jupyter notebook --no-browser --port=8888
```

在 VS Code 中：F1 → Jupyter: Specify Jupyter Server URI → 輸入 `http://localhost:8888/?token=xxx`

## 同步設定

使用 Settings Sync 或將其納入專案 `.vscode/settings.json`：

```json
{
    "python.defaultInterpreterPath": ".venv/bin/python",
    "jupyter.kernels.filter": ["python3"],
    "remote.SSH.path": "/usr/bin/ssh"
}
```

## 參考資源

- https://www.google.com/search?q=VS+Code+Remote+SSH+development+setup+guide
- https://www.google.com/search?q=VS+Code+Dev+Containers+AI+development
