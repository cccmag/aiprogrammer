# 4. conda 環境管理

## conda 與 pip 的差異

conda 不僅是 Python 套件管理器，而是一個跨語言的環境管理系統。pip 只能管理 Python 套件，conda 還能管理 R、Ruby、Scala 等其他語言的套件。對於需要編譯依賴（如 NumPy、SciPy）的科學計算專案，conda 的二進制預編譯套件可以大幅節省安裝時間。

## 基本操作

```bash
# 建立環境
conda create --name myenv python=3.7
conda create --name myenv python=3.7 numpy pandas

# 啟動環境（Windows）
conda activate myenv

# 啟動環境（Linux/macOS）
source activate myenv

# 停用
conda deactivate

# 刪除環境
conda env remove --name myenv
```

## 環境匯出與重現

```bash
# 匯出環境到檔案
conda env export > environment.yml

# 從檔案建立環境
conda env create --file environment.yml

# 只匯出直接安裝的套件（不含相依）
conda env export --from-history > environment.yml
```

environment.yml 範例：
```yaml
name: my-project
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.7
  - numpy=1.17
  - pandas=1.0
  - pip
  - pip:
    - some-pip-package
```

## pip 與 conda 混合使用

```bash
# conda 安裝後使用 pip
conda install numpy pandas
pip install jupyterlab

# 建立乾淨的 pip 環境
conda create --name myenv python=3.7
source activate myenv
pip install -r requirements.txt
```

## conda-forge 與 channels

預設的 conda 庫可能沒有最新的套件。conda-forge 是社群維護的套件庫，更新更快：

```bash
# 加入 conda-forge
conda config --add channels conda-forge
conda config --set channel_priority strict

# 搜尋套件
conda search numpy
```

## conda 環境複製

```bash
# 複製環境
conda create --clone myenv --name myenv-copy

# 列出所有環境
conda env list
```

## pip 在 conda 中的最佳實踐

建議在 environment.yml 中明確區分 conda 與 pip 套件：

```yaml
dependencies:
  - python=3.7
  - numpy
  - pip:
    - black
    - isort
```

這樣的格式讓環境重建時更容易重現。

## 常見問題

1. **conda 與 pip 衝突**：盡量保持一個環境只用一種方式安裝
2. **環境過大**：使用 `conda clean --all` 清理快取
3. **安裝過慢**：加入 conda-forge 或使用 mamba（conda 的替代實作）

## 參考資源

- https://www.google.com/search?q=conda+environment+management+tutorial+2020
- https://www.google.com/search?q=conda+pip+best+practices+mixing+dependencies+2020
- https://www.google.com/search?q=conda-forge+channel+package+installation+guide