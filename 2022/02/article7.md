# NVIDIA NGC 與 Docker GPU

## 容器化 GPU 工作負載的最佳實踐

### 為什麼需要容器化 GPU 工作負載

深度學習環境的依賴管理是公認的噩夢。不同專案需要不同版本的 CUDA、cuDNN、PyTorch 和 Python。手動管理這些依賴會導致「環境地獄」——升級一個庫可能破壞另一個專案的工作環境。

Docker 容器為 GPU 工作負載提供了完美的解決方案：將整個環境（包括 CUDA 驅動、cuDNN、框架）打包，確保開發、測試和生產環境的一致。

### NVIDIA Container Toolkit

NVIDIA Container Toolkit（nvidia-docker2）是讓 Docker 可以存取 GPU 的核心元件：

```bash
# 安裝 NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker

# 執行 GPU 容器
docker run --gpus all nvidia/cuda:11.6-base nvidia-smi
```

`--gpus` 選項有幾種用法：

```bash
# 使用所有 GPU
docker run --gpus all ...

# 使用特定 GPU
docker run --gpus '"device=0,1"' ...

# 使用特定數量 GPU
docker run --gpus 2 ...
```

### NVIDIA NGC Catalog

NVIDIA NGC（NVIDIA GPU Cloud）是 NVIDIA 的容器註冊表，提供預先配置好的 GPU 容器映像：

```
ngc.nvidia.com
  └── catalog
      ├── containers
      │   ├── pytorch:22.02-py3        # PyTorch + CUDA 11.6
      │   ├── tensorflow:22.02-tf2-py3  # TensorFlow 2.8
      │   ├── cuda:11.6-base            # 純 CUDA 環境
      │   └── cudnn:8.3-cuda11.6        # cuDNN 環境
      └── models
          ├── nvidia/bert-large
          └── nvidia/resnet-50
```

優點：
- **經過 NVIDIA 驗證**：所有容器都經過效能測試
- **可直接使用**：預裝 cuDNN、TensorRT 等最佳化庫
- **定期更新**：每月更新以配合最新 CUDA 版本

```bash
docker pull nvcr.io/nvidia/pytorch:22.02-py3
docker run --gpus all -it nvcr.io/nvidia/pytorch:22.02-py3 python -c "import torch; print(torch.cuda.is_available())"
```

### 自訂 Docker Image

在 NGC 映像基礎上建立自訂映像：

```dockerfile
FROM nvcr.io/nvidia/pytorch:22.02-py3

WORKDIR /workspace

# 安裝額外套件
RUN pip install transformers datasets wandb

# 複製程式碼
COPY . /workspace

ENTRYPOINT ["python", "train.py"]
```

```bash
docker build -t my-gpu-train:latest .
docker run --gpus all --shm-size=8g my-gpu-train:latest
```

`--shm-size` 參數很重要：PyTorch DataLoader 使用共享記憶體（/dev/shm）進行多程序資料載入，預設 64MB 太小，建議設為 8-16GB。

### 多容器協作：Docker Compose + GPU

```yaml
# docker-compose.yml
version: "3.8"
services:
  trainer:
    image: nvcr.io/nvidia/pytorch:22.02-py3
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
    shm_size: 16g
    volumes:
      - ./workspace:/workspace
      - ./data:/data
    command: python train.py --config config.yaml

  inference:
    image: nvcr.io/nvidia/tensorrt:22.02-py3
    runtime: nvidia
    ports:
      - "8000:8000"
    volumes:
      - ./models:/models
    command: tritonserver --model-repository=/models
```

### 實戰建議

- 使用 NGC 映像作為基礎，避免從頭配置 CUDA 環境
- 定期更新 CUDA 版本（每 6-12 個月）
- 將訓練資料掛載為 volume（而非複製到映像中）
- 使用 `--ipc=host` 或 `--shm-size` 解決共享記憶體問題
- 在 CI/CD 中使用 GPU runner 進行容器化測試

### 延伸閱讀

- [NVIDIA NGC Container](https://www.google.com/search?q=NVIDIA+NGC+container)
- [Docker GPU Support](https://www.google.com/search?q=docker+gpu+support+nvidia)
