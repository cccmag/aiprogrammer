# Conda 環境管理

## 安裝 Miniconda

Miniconda 是 Anaconda 的精簡版，只包含 conda 與 Python，適合進階使用者。完整 Anaconda 安裝包約 3GB，Miniconda 僅約 100MB。

```bash
# Linux / macOS 安裝
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# 安裝完成後初始化
conda init

# 更新 conda
conda update -n base conda
```

## 環境操作

```bash
# 建立新環境（指定 Python 版本）
conda create -n ai_env python=3.10

# 啟動環境
conda activate ai_env

# 離開環境
conda deactivate

# 列出所有環境
conda env list

# 複製環境（用於測試升級）
conda create -n ai_env_backup --clone ai_env

# 移除環境
conda env remove -n ai_env
```

## 套件安裝

```bash
# 從 conda 預設頻道安裝
conda install numpy pandas matplotlib scikit-learn

# 從特定頻道安裝（pytorch 頻道有 GPU 支援的 PyTorch）
conda install pytorch torchvision cudatoolkit=11.8 -c pytorch -c nvidia

# 安裝特定版本
conda install numpy=1.24.3

# 同時使用 pip（注意：不要在 conda 安裝 pip 套件後又用 conda 安裝同套件）
pip install transformers datasets
```

## 環境匯出與重現

```bash
# 完整匯出（包含所有套件，可能跨平台不相容）
conda env export > environment.yml

# 僅匯出明確安裝的套件（跨平台相容性較佳）
conda env export --from-history > environment.yml

# 從檔案重建環境
conda env create -f environment.yml

# 更新已存在的環境
conda env update -f environment.yml
```

## Conda 最佳實踐

- 優先使用 conda 安裝套件，conda 沒有的再用 pip
- 不要在 base 環境安裝專案套件
- 使用 `--from-history` 匯出以提升跨平台相容性
- 定期使用 `conda clean --all` 清理快取節省磁碟空間

## 參考資源

- https://www.google.com/search?q=conda+environment+export+import+reproducible+workflow
- https://www.google.com/search?q=Miniconda+vs+Anaconda+install+guide+data+science
- https://www.google.com/search?q=conda+pip+mix+best+practices+dependency+management
