# Dockerfile 撰寫指南

## 基本結構

一個好的 Dockerfile 應該從穩定版本的基底映像開始，逐步加入應用程式的相依套件與原始碼。

```dockerfile
# 選擇特定版本的基底映像（避免使用 latest）
FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

# 中繼資料
LABEL maintainer="developer@example.com"
LABEL description="AI training environment"

# 設定工作目錄
WORKDIR /app

# 先複製依賴清單（善用 Docker 層級快取）
COPY requirements.txt .

# 安裝相依套件（--no-cache-dir 減少映像體積）
RUN pip install --no-cache-dir -r requirements.txt

# 複製原始碼（這一步會頻繁變動，放在後面）
COPY . .

# 暴露埠號（僅供文件說明）
EXPOSE 8888

# 設定預設指令
CMD ["python", "train.py"]
```

## 多階段建置

多階段建置將編譯環境與運行環境分離，大幅縮小最終映像體積：

```dockerfile
# 第一階段：建置環境
FROM python:3.10-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# 第二階段：運行環境
FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "train.py"]
```

## 快取最佳化

Docker 每一層都會被快取，只有當該層的指令或檔案變動時才會重建。將「經常變動」的檔案放在 Dockerfile 後面，可以最大化利用快取：

```dockerfile
# 錯誤：每次原始碼變動都會重新安裝套件
COPY . .
RUN pip install -r requirements.txt

# 正確：只有 requirements.txt 變動時才重新安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

## GPU 專用 Dockerfile

```dockerfile
FROM nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install torch torchvision torchaudio
WORKDIR /workspace
COPY . .
CMD ["python3", "train.py"]
```

## .dockerignore

```gitignore
.git/
.venv/
__pycache__/
*.pyc
data/
notebooks/
.DS_Store
```

## 參考資源

- https://www.google.com/search?q=Dockerfile+best+practices+multistage+build+optimization
- https://www.google.com/search?q=Docker+cache+layer+optimization+Python+dependencies
- https://www.google.com/search?q=NVIDIA+CUDA+Dockerfile+deep+learning+tutorial
