# Jupyter 安裝與基本操作

## 安裝選項

### pip 安裝

```bash
# 安裝 Jupyter Notebook
pip install notebook

# 安裝 JupyterLab
pip install jupyterlab

# 兩者都安裝
pip install notebook jupyterlab
```

### conda 安裝

```bash
conda install jupyterlab notebook
```

### Anaconda

Anaconda 預設已包含 Jupyter Notebook 與 JupyterLab。下載安裝後即可使用。

## 啟動服務

### Jupyter Notebook

```bash
jupyter notebook
# 預設 URL：http://localhost:8888
```

### JupyterLab

```bash
jupyter lab
# 預設 URL：http://localhost:8888/lab
```

### 常用選項

```bash
# 指定埠號
jupyter lab --port 8889

# 不開啟瀏覽器
jupyter lab --no-browser

# 指定工作目錄
jupyter lab --notebook-dir=/path/to/dir

# 啟動並顯示存取權杖
jupyter lab --ServerApp.token='my-token'
```

## 細胞類型

### 程式碼細胞

```python
# 這是程式碼細胞
print("Hello, Jupyter!")
x = [1, 2, 3]
print(sum(x))
```

### Markdown 細胞

```markdown
# 標題
## 子標題

- 列表
- 另一項

**粗體** 與 *斜體*
```

### 原始儲存格

用於純文字，不會被執行：

```
這是原始儲存格，不會被 Jupyter 執行
```

## 執行流程

1. 在細胞中輸入程式碼或文字
2. 按 `Shift+Enter` 執行並跳到下一個細胞
3. 按 `Ctrl+Enter` 執行並停留在當前細胞
4. 輸出結果顯示在細胞下方

## 命令模式與編輯模式

- **Esc**：進入命令模式（邊框變藍）
- **Enter**：進入編輯模式（邊框變綠）
- **命令模式下**按 `H`：顯示所有快捷鍵

## 核心快捷鍵

| 快捷鍵 | 功能 |
|--------|------|
| Shift+Enter | 執行並跳到下一個 |
| Ctrl+Enter | 執行並停留 |
| A | 在上方插入細胞 |
| B | 在下方插入細胞 |
| DD | 刪除細胞 |
| M | 轉為 Markdown |
| Y | 轉為程式碼 |
| X | 剪下細胞 |
| V | 貼上細胞 |

## 核心安裝路徑

```bash
# 升級
pip install --upgrade jupyterlab

# 檢查版本
jupyter --version
```

## 參考資源

- https://www.google.com/search?q=Jupyter+Notebook+installation+setup+tutorial+2020
- https://www.google.com/search?q=Jupyter+Lab+installation+2020+beginner+guide
- https://www.google.com/search?q=Jupyter+keyboard+shortcuts+command+mode+edit+mode