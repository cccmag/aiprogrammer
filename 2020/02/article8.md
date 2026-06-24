# Nbconvert 轉換工具

## 安裝

```bash
pip install nbconvert
```

## 基本用法

### 轉換為 HTML

```bash
jupyter nbconvert --to html mynotebook.ipynb
```

### 轉換為 Markdown

```bash
jupyter nbconvert --to markdown mynotebook.ipynb
```

### 轉換為 PDF（需要 LaTeX）

```bash
jupyter nbconvert --to pdf mynotebook.ipynb
```

## 預處理器

### 執行 Notebook 並轉換

```bash
# 先執行再轉換
jupyter nbconvert --to html --execute mynotebook.ipynb
```

### 去除輸出

```bash
# 轉換但去除所有輸出
jupyter nbconvert --to html --clear-output mynotebook.ipynb
```

## 範本自訂

### 使用預設範本

```bash
jupyter nbconvert --to html --template classic mynotebook.ipynb
```

### 使用 full 範本（含完整 HTML）

```bash
jupyter nbconvert --to html --template full mynotebook.ipynb
```

## 程式碼語法高亮

```bash
# 指定語言
jupyter nbconvert --to html --HTMLExporter.theme=light mynotebook.ipynb
```

## 在 Python 中使用

```python
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

# 讀取 Notebook
with open('mynotebook.ipynb') as f:
    nb = nbformat.read(f, as_version=4)

# 執行 Notebook
ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
ep.preprocess(nb, {'metadata': {'path': '.'}})

# 寫回
with open('executed.ipynb', 'w') as f:
    nbformat.write(nb, f)
```

## 自動化腳本

```bash
#!/bin/bash
# convert.sh

for nb in *.ipynb; do
    echo "轉換：$nb"
    jupyter nbconvert --to html --execute --ExecutePreprocessor.timeout=600 "$nb"
done
```

## 與 Papermill 的差異

| 功能 | Nbconvert | Papermill |
|------|-----------|-----------|
| 執行 Notebook | 是 | 是 |
| 參數化執行 | 有限 | 完全支援 |
| 轉換格式 | 多種 | 有限 |

## 參考資源

- https://www.google.com/search?q=nbconvert+jupyter+notebook+convert+html+pdf+2020
- https://www.google.com/search?q=nbconvert+template+execute+preprocessor+2020
- https://www.google.com/search?q=jupyter+notebook+pdf+latex+conversion+2020