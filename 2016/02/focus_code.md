# 程式碼說明 — Docker 管理腳本

## 功能概述

`_code/docker_manage.py` 是一個 Docker 容器管理腳本，提供常見的容器操作功能，包括容器列表查詢、映象管理、資源使用統計等。

## 主要功能

### 1. 列出執行中的容器

使用 `docker ps` 指令獲取所有執行中的容器，解析輸出並以格式化方式呈現。

### 2. 映象列表

使用 `docker images` 指令列出本機所有映象，顯示映象名稱、標籤、ID、大小、建立時間。

### 3. 資源使用統計

使用 `docker stats` 指令即時獲取容器 CPU、記憶體、網路 IO、區塊 IO 的使用情況。

### 4. 映象清理

安全的清理機制，只刪除未被任何容器使用的映象，避免誤刪正在使用的映象。

### 5. 系統資訊

使用 `docker info` 指令獲取 Docker 系統資訊，包括版本、儲存驅動、容器數量等。

## 執行方式

```bash
cd _code
python3 docker_manage.py
```

## 輸出範例

```
====================================================
Docker 容器管理工具
====================================================

[容器列表]
CONTAINER ID   NAME      IMAGE   STATUS    PORTS
abc123def456   web       nginx   Up 2h     0.0.0.0:80->80/tcp
def456ghi789   db        mysql   Up 3h     3306/tcp

[映象列表]
REPOSITORY   TAG      IMAGE ID      SIZE
nginx        1.21     abc123        142MB
mysql        8        def456        545MB

[資源使用]
CONTAINER   CPU %   MEM USAGE / LIMIT
web         0.52    50.23MiB / 512MiB
db          1.23    256.12MiB / 1GiB

====================================================
```

## 錯誤處理

腳本會檢查 Docker 是否已安裝且 Daemon 是否正在運行。如果 Docker 未就緒，會顯示明確的錯誤訊息而非崩潰。

## 參考資源

- https://www.google.com/search?q=Python+subprocess+Docker+CLI+管理+腳本+容器+映象
- https://www.google.com/search?q=docker+ps+docker+images+docker+stats+輸出+解析+Python
- https://www.google.com/search?q=Docker+Python+SDK+container+management+API+範例