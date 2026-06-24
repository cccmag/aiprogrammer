# 5. Docker 容器化 AI 應用

## 為什麼 AI 需要 Docker？

AI 專案的環境相依性極其複雜：特定的 CUDA 版本、cuDNN 版本、Python 套件組合，稍有差異就可能導致程式無法執行。Docker 將整個環境打包成映像，確保開發、測試、生產環境完全一致。這在團隊協作與 CI/CD 流程中尤其重要。

## Docker 基本概念

- **映像（Image）**：唯讀的模板，包含作業系統、程式碼與相依套件。映像由多層組成，每一層代表 Dockerfile 中的一條指令。
- **容器（Container）**：映像的執行實例，可讀寫。容器之間互相隔離，擁有獨立的檔案系統與網路。
- **Dockerfile**：描述如何建立映像的腳本，每一行指令都會建立一個新層。

```dockerfile
FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "train.py"]
```

## GPU 支援

Docker 透過 NVIDIA Container Toolkit 讓容器存取 GPU。安裝後使用 `--gpus` 參數：

```bash
# 安裝 NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | tee /etc/apt/sources.list.d/nvidia-docker.list

apt-get update && apt-get install -y nvidia-container-toolkit
systemctl restart docker

# 執行 GPU 容器
docker run --gpus all -it pytorch/pytorch:latest python -c "
import torch
print(torch.cuda.is_available())
"
```

## 資料管理

使用資料掛載（bind mount）或資料卷（volume）來管理訓練資料與模型輸出：

```bash
docker run --gpus all -v /mnt/data:/data -v $(pwd)/models:/models pytorch/pytorch:latest
```

## 參考資源

- https://www.google.com/search?q=Docker+container+GPU+deep+learning+setup+tutorial
- https://www.google.com/search?q=NVIDIA+Container+Toolkit+installation+guide+Linux
- https://www.google.com/search?q=Docker+AI+workflow+bind+mount+volume+GPU
