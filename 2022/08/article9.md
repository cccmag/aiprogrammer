# 叢集管理：SLURM、Kubernetes

## SLURM

SLURM（Simple Linux Utility for Resource Management）是 HPC 領域最主流的資源管理系統。在學術機構和大型研究單位中，GPU 叢集幾乎都使用 SLURM 排程。

### 基本用法

```bash
# 申請 4 個 GPU 節點
salloc --nodes=4 --gres=gpu:8 --time=2:00:00

# 提交訓練任務
sbatch train.slurm
```

### SLURM 腳本範例

```bash
#!/bin/bash
#SBATCH --nodes=4
#SBATCH --gres=gpu:8
#SBATCH --ntasks-per-node=8
srun torchrun --nnodes=4 train.py
```

### 常見挑戰

- GPU 資源碎片化導致利用率下降
- 排隊時間不可預測
- 與深度學習框架的深度整合需要經驗

## Kubernetes

K8s 在深度學習領域的應用越來越廣，特別是搭配 Volcano 或 Kubeflow 等專用 operator。

### 優勢

- 動態資源調度與自動擴縮
- 容器化環境確保一致
- 支援 GPU 共享與 MIG 分割
- 豐富的監控與日誌生態

### Kubeflow

Kubeflow 是 Kubernetes 上的機器學習平台，提供 PyTorchJob、TFJob 等自訂資源，簡化分散式訓練的部署流程。

## 選擇建議

SLURM 適合固定叢集的批次訓練任務，管理成本低。Kubernetes 適合需要動態資源分配、多租戶隔離的生產環境。

[搜尋 SLURM GPU 分散式訓練](https://www.google.com/search?q=SLURM+GPU+distributed+training)
[搜尋 Kubernetes Kubeflow 深度學習](https://www.google.com/search?q=Kubernetes+Kubeflow+deep+learning+training)
