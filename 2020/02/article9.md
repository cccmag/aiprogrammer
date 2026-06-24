# Notebook 版本控制

## Notebook 的版本控制挑戰

Notebook 的 JSON 格式使得直接使用 Git 合併時會遇到困難。輸出一個小改變可能導致大量的雜訊。

## 解決方案

### 1. 去除輸出的預提交鈎

```bash
pip install nbconvert
```

在 `.git/hooks/pre-commit` 中加入：

```bash
#!/bin/bash
jupyter nbconvert --clear-output --inplace *.ipynb
```

### 2. nbdime（推薦）

nbdime 提供 Git 整合，智慧合併 Notebook：

```bash
pip install nbdime

# 設定 Git 整合
nbdime config-git --enable
```

設定後，`git diff` 與 `git merge` 會以視覺化方式呈現 Notebook 差異。

```bash
# 查看差異
nbdiff mynotebook.ipynb another.ipynb

# 合併
nbmerge base.ipynb mine.ipynb theirs.ipynb
```

## 在 Git 中追蹤 Notebook

建議 `.gitattributes` 設定：

```
*.ipynb filter=nbstripout
```

建立 `.gitconfig` 或在 repo 中設定 filter：

```bash
git config filter.nbstripout.clean 'jupyter nbconvert --clear-output --stdout --log-level ERROR'
git config filter.nbstripout.smudge 'cat'
```

## 自動化工具

### nbstripout

```bash
pip install nbstripout

# 初始化（會自動設定 filter）
nbstripout --install
```

## GitHub 整合

### 在 GitHub 中檢視

GitHub 原生支援 Notebook 視覺化預覽。

### 使用 Colab

Google Colab 可以直接開啟 GitHub 儲存庫中的 Notebook。

## 工作流程建議

1. **每次提交前**：確保執行過所有細胞
2. **使用 Cell ID**：追蹤細胞變化
3. **避免大輸出**：使用 `--clear-output` 或設定自動去除
4. **描述性訊息**：清楚說明變更內容

## CI/CD 整合

```yaml
# .github/workflows/notebook.yml
- name: Execute Notebooks
  run: |
    pip install nbconvert papermill
    for nb in $(find . -name "*.ipynb"); do
      jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 "$nb"
    done
```

## 參考資源

- https://www.google.com/search?q=jupyter+notebook+version+control+git+2020
- https://www.google.com/search?q=nbdime+nbstripout+jupyter+git+2020
- https://www.google.com/search?q=jupyter+notebook+git+workflow+best+practices+2020