# Visual Studio Code 1.37：Remote Development 支援

## 前言

Visual Studio Code 1.37 於 2019 年 8 月正式發布。這個版本的最大亮點是對 Remote Development 擴展的正式支援，讓開發者能夠無縫地在容器、SSH 和 WSL 中進行開發。

## Remote Development 擴展套件

### 支援的遠端類型

1. **Remote - SSH**：連接到 SSH 伺服器進行開發
2. **Remote - Containers**：在 Docker 容器中開發
3. **Remote - WSL**：在 Windows Subsystem for Linux 中開發

### 安裝方式

```bash
# 從 VS Code Marketplace 安裝
code --install-extension ms-vscode-remote.remote-ssh
code --install-extension ms-vscode-remote.remote-containers
code --install-extension ms-vscode-remote.remote-wsl
```

---

## Remote - SSH

### 配置 SSH 連接

```bash
# 編輯 SSH 配置檔案
# ~/.ssh/config

Host my-server
    HostName 192.168.1.100
    User developer
    Port 22
    IdentityFile ~/.ssh/id_rsa
```

### 使用流程

1. 按下 `F1`，輸入 `Remote-SSH: Connect to Host`
2. 選擇或輸入 SSH 連接配置
3. VS Code 會在遠端伺服器上安裝 VS Code Server
4. 之後就可以像本地一樣編輯檔案

### 優勢

- **完整的功能體驗**：包括 IntelliSense、調試等
- **本地的網路資源**：連接到本地網路時延遲低
- **強大的計算能力**：利用伺服器算力

---

## Remote - Containers

### 開發容器配置

在專案根目錄創建 `.devcontainer/devcontainer.json`：

```json
{
    "name": "My Project Dev Container",
    "image": "mcr.microsoft.com/vscode/devcontainers/python:3.8",
    "settings": {
        "python.pythonPath": "/usr/local/bin/python"
    },
    "extensions": [
        "ms-python.python",
        "ms-vscode.vscode-typescript-next"
    ],
    "forwardPorts": [3000],
    "postCreateCommand": "pip install -r requirements.txt"
}
```

### 使用流程

1. 在專案目錄中按下 `F1`
2. 輸入 `Remote-Containers: Reopen in Container`
3. VS Code 會自動構建並啟動容器
4. 開發環境就緒

### docker-compose 支援

```json
{
    "dockerComposeFile": ["docker-compose.yml"],
    "service": "app",
    "workspaceFolder": "/workspace/app"
}
```

---

## Remote - WSL

### Windows 子系統 Linux

WSL（Windows Subsystem for Linux）允許在 Windows 上運行 Linux 環境：

```powershell
# 安裝 WSL
wsl --install

# 安裝後重啟系統
```

### VS Code 與 WSL

```bash
# 在 WSL 中打開 VS Code
code .

# 或在 Windows 上使用
code --remote wsl+ubuntu /home/user/project
```

---

## 其他新功能

### 1. 改進的 Minimap

1.37 版本優化了代碼地圖（Minimap）的渲染效能：

```json
{
    "editor.minimap.renderCharacters": false,
    "editor.minimap.maxColumn": 80
}
```

### 2.  時間緊縮邀請功能

新增「Time Traveler」風格的邀請功能，讓開發者可以邀請其他人觀看直播：

```
View → Start Time Travel View
```

### 3. TypeScript 3.6 支援

```json
{
    "typescript.tsdk": "./node_modules/typescript/lib"
}
```

---

## 效能優化

### 遠端開發的效能考量

1. **網路延遲**：SSH 連接的響應速度
2. **檔案同步**：大專案的同步時間
3. **擴展套件**：某些擴展可能需要特殊配置

### 最佳化建議

```json
{
    "remote.SSH.showLoginTerminal": true,
    "remote.extensionKind": {
        "ms-python.python": "ui"
    }
}
```

---

## 結語

VS Code 1.37 的 Remote Development 功能代表了一種新的開發模式：不受本地環境限制，隨時隨地進行開發。這對於 DevOps 工程師、數據科學家和需要跨平台開發的團隊特別有價值。

---

**延伸閱讀**

- [VS Code Remote Development](https://www.google.com/search?q=VS+Code+remote+development)
- [Remote Containers Tutorial](https://www.google.com/search?q=VS+Code+remote+containers+tutorial)
- [WSL + VS Code](https://www.google.com/search?q=WSL+VS+Code+remote+development)