# 4. GPU 與 CUDA 設定

## GPU 在 AI 中的角色

深度學習的核心是大量的矩陣乘法與卷積運算。CPU 雖然時脈高，但核心數有限（通常 4–16 核心），無法有效率地處理大規模平行運算。GPU 擁有數千個小型核心，能同時執行大量運算，將訓練時間從數週縮短至數小時。NVIDIA 的 CUDA 是專用的並行運算平台，深度學習框架透過 CUDA 呼叫 GPU 資源進行張量運算。

## 驅動程式與 CUDA 版本

正確安裝需要三層元件：

1. **NVIDIA 顯示驅動**：最低版本需符合 CUDA 工具包的要求。可使用 `nvidia-smi` 檢查當前驅動版本與支援的最高 CUDA 版本。
2. **CUDA 工具包**：包含 nvcc 編譯器、GPU 加速函式庫與開發工具。深度學習框架在編譯時連結特定版本的 CUDA 函式庫。
3. **cuDNN**：針對深度神經網路最佳化的 GPU 加速函式庫，提供卷積、池化、正規化等運算的快速實作。

```bash
# 檢查驅動版本與 CUDA 版本
nvidia-smi

# 輸出範例
# NVIDIA-SMI 560.94  Driver Version: 560.94  CUDA Version: 12.6
```

## PyTorch 與 CUDA 版本對應

```python
import torch
print(f"PyTorch 版本: {torch.__version__}")
print(f"對應 CUDA 版本: {torch.version.cuda}")
print(f"GPU 可用: {torch.cuda.is_available()}")
print(f"GPU 數量: {torch.cuda.device_count()}")
print(f"GPU 名稱: {torch.cuda.get_device_name(0)}")
```

## 常見陷阱

nvidia-smi 顯示的 CUDA Version 是驅動支援的最高版本，不代表已安裝的 CUDA 工具包版本。PyTorch 等框架使用自己打包的 CUDA 函式庫，與系統 CUDA 版本無關。因此可能出現 nvidia-smi 顯示 CUDA 12.6，但 PyTorch 使用 CUDA 11.8 的情況，這是正常且正確的。只要驅動版本高於框架所需的 CUDA 版本即可。

## 參考資源

- https://www.google.com/search?q=NVIDIA+GPU+driver+CUDA+compatibility+installation+guide+Linux
- https://www.google.com/search?q=PyTorch+CUDA+version+compatibility+check+table+2026
- https://www.google.com/search?q=nvidia-smi+CUDA+version+vs+installed+CUDA+toolkit+difference
