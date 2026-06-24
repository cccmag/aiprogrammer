# 6. Notebook 與 VS Code

## VS Code 的 Jupyter 支援

VS Code 的 Python 擴充包含了完整的 Jupyter Notebook 支援。可以在 VS Code 中編輯、執行與除錯 Notebook。

## 安裝

1. 安裝 VS Code
2. 安裝 Python 擴充
3. 安裝 Jupyter 擴充

## 核心功能

### 細胞編輯
VS Code 中的 Notebook 介面與瀏覽器版本非常相似，支援：
- 細胞新增、刪除、拖拽
- 程式碼補全
- 語法高亮

### 互動式輸出
在 VS Code 中執行細胞，輸出結果直接顯示在下方：

```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4])
plt.ylabel('some numbers')
plt.show()
```

### 變數總覽
內建的變數總覽面板顯示所有已定義的變數及其類型與值。

### 除錯支援
可以在 VS Code 中設定中斷點、除錯變數，優於瀏覽器版的 Jupyter。

## 資料檢視

VS Code 支援直接在 IDE 中檢視 Pandas DataFrame：

```python
import pandas as pd

df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})
# 在 VS Code 中檢視：點擊 df 變數旁的「Data Viewer」按鈕
```

## Git 整合

VS Code 的 Git 支援讓 Notebook 版本控制更簡單。但注意：Notebook 的 JSON 格式在合併時可能有衝突。

## Python Interactive 視窗

即使不開啟 `.ipynb` 檔案，也可以在 VS Code 中使用互動式 Python（如同 Jupyter）：

```python
# 在 .py 檔案中
# 使用 # %% 分隔細胞
# 點擊 "Run Cell" 或 Shift+Enter 執行
```

## 與傳統 Jupyter 的差異

| 特性 | VS Code | 瀏覽器 Jupyter |
|------|---------|----------------|
| 本地檔案存取 | 直接 | 需要上傳 |
| Git 整合 | 優秀 | 需要外掛 |
| 除錯 | 完整 | 基本 |
| 共同作業 | 需要擴充 | 即時共同作業（需 JupyterHub） |

## 參考資源

- https://www.google.com/search?q=VS+Code+Jupyter+Notebook+Python+extension+2020
- https://www.google.com/search?q=VS+Code+Python+interactive+window+data+viewer+2020
- https://www.google.com/search?q=VS+Code+Jupyter+Notebook+differences+comparison+2020