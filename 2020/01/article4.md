# conda 環境匯出與重現

## 基本匯出

```bash
# 匯出完整環境（包含所有相依）
conda env export > environment.yml

# 只匯出明確安裝的套件
conda env export --from-history > environment.yml
```

## environment.yml 範例

```yaml
name: my-project
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.7
  - numpy=1.17
  - pandas=0.25
  - pip
  - pip:
    - jupyterlab
    - black
```

## 從檔案重建環境

```bash
# 建立新環境
conda env create --file environment.yml

# 更新現有環境
conda env update --file environment.yml
```

## conda-forge 使用

```bash
# 加入 conda-forge
conda config --add channels conda-forge
conda config --set channel_priority strict

# 搜尋套件
conda search numpy

# 安裝
conda install numpy
```

## 環境克隆

```bash
# 複製環境
conda create --clone old-env --name new-env

# 刪除環境
conda env remove --name myenv
```

## pip 與 conda 混合環境

最佳實踐是在 environment.yml 中分開宣告：

```yaml
dependencies:
  - python=3.7
  - numpy
  - pandas
  - pip
  - pip:
    - black
    - flake8
    - my-package-from-pypi
```

## 環境清理

```bash
# 清理下載快取
conda clean --all

# 檢查環境大小
du -sh ~/anaconda3/envs/
```

## 參考資源

- https://www.google.com/search?q=conda+environment+export+import+yml+reproduce+2020
- https://www.google.com/search?q=conda-forge+channel+install+packages+2020
- https://www.google.com/search?q=conda+pip+mix+environment+best+practices