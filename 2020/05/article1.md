# CUDA 安裝與環境設定

## 檢查現有環境

```bash
# 查看 NVIDIA 驅動版本
nvidia-smi

# 查看 CUDA 版本
nvcc --version

# 輸出應該類似：
# Driver Version: 450.36.34
# CUDA Version: 11.0
```

## 安裝 CUDA Toolkit

### 方法 1：從 NVIDIA 官網下載

```bash
# 下載 CUDA 11.0 安裝包
wget https://developer.download.nvidia.com/compute/cuda/11.0.2/local_installers/cuda_11.0.2_450.51.05_linux.run

# 執行安裝
sudo sh cuda_11.0.2_450.51.05_linux.run
```

### 方法 2：使用 conda

```bash
conda install cudatoolkit=11.0
```

## 安裝 cuDNN

cuDNN 是深度學習必備的 GPU 加速庫：

1. 從 NVIDIA 官網下載 cuDNN（需要註冊）
2. 解壓並複製：

```bash
tar -xzvf cudnn-11.0-linux-x64-v8.0.4.30.tgz
sudo cp cuda/include/* /usr/local/cuda/include/
sudo cp cuda/lib64/* /usr/local/cuda/lib64/
```

## 驗證安裝

```python
import torch
print(f"PyTorch 版本: {torch.__version__}")
print(f"CUDA 可用: {torch.cuda.is_available()}")
print(f"CUDA 版本: {torch.version.cuda}")
print(f"GPU 數量: {torch.cuda.device_count()}")
for i in range(torch.cuda.device_count()):
    print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
```

## 環境變數設定

```bash
# 將以下內容加入 ~/.bashrc 或 ~/.zshrc
export CUDA_HOME=/usr/local/cuda
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
```

## Docker 方式（推薦）

使用 NVIDIA Docker 容器，避免環境衝突：

```bash
# 安裝 nvidia-docker
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install nvidia-container-toolkit

# 執行容器
docker run --gpus all -it nvidia/cuda:11.0-cudnn8-runtime-ubuntu20.04
```

## 常見問題

1. **CUDA out of memory**：減少批次大小或使用梯度累積
2. **GPU not found**：檢查驅動是否正確安裝
3. **版本不匹配**：確認 PyTorch 與 CUDA 版本相容

## 參考資源

- https://www.google.com/search?q=CUDA+installation+Ubuntu+Linux+2020+complete+guide
- https://www.google.com/search?q=PyTorch+CUDA+compatibility+version+check+installation
- https://www.google.com/search?q=nvidia+cuDNN+installation+docker+setup+deep+learning