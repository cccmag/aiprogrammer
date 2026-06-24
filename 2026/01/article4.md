# NVIDIA 驅動與 CUDA 安裝

## 前置檢查

安裝前先確認硬體與作業系統的相容性。

```bash
# 確認 GPU 型號
lspci | grep -i nvidia

# 確認系統架構與發行版
uname -m && cat /etc/os-release

# 檢查目前是否已有 NVIDIA 驅動
nvidia-smi
```

## 安裝 NVIDIA 驅動

### Ubuntu / Debian（自動安裝）

```bash
# 自動檢測硬體並安裝推薦驅動
ubuntu-drivers devices
sudo apt install nvidia-driver-560

# 重啟系統
sudo reboot

# 驗證驅動
nvidia-smi
```

### 手動安裝（精確控制版本）

從 NVIDIA 官方網站下載對應的 `.run` 檔案，關閉 X server 後安裝：

```bash
# 停止圖形介面
sudo systemctl isolate multi-user.target

# 安裝驅動
sudo sh NVIDIA-Linux-x86_64-560.94.run

# 重啟
sudo reboot
```

## 安裝 CUDA 工具包

### 方式一：NVIDIA 官方 runfile

```bash
wget https://developer.download.nvidia.com/compute/cuda/12.6.0/local_installers/cuda_12.6.0_xxx_linux.run
sudo sh cuda_12.6.0_xxx_linux.run

# 設定環境變數
echo 'export PATH=/usr/local/cuda-12.6/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.6/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

### 方式二：使用 conda

conda 會自動處理 CUDA 的相依性，適合需要快速建置的場景：

```bash
conda install -c nvidia cuda-toolkit
```

## 安裝 cuDNN

```bash
tar -xzvf cudnn-linux-x86_64-8.9.7.29_cuda12-archive.tar.xz
sudo cp cudnn-*/include/cudnn*.h /usr/local/cuda/include
sudo cp cudnn-*/lib/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn*.h /usr/local/cuda/lib64/libcudnn*
```

## 完整驗證

```bash
nvcc --version   # CUDA 編譯器版本
nvidia-smi       # 驅動版本與 GPU 狀態
```

## 參考資源

- https://www.google.com/search?q=NVIDIA+driver+installation+Ubuntu+Linux+guide+steps
- https://www.google.com/search?q=CUDA+toolkit+12+installation+Linux+runfile+guide
- https://www.google.com/search?q=cuDNN+install+Ubuntu+CUDA+copy+files+guide
