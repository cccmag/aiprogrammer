# 3. JupyterLab 1.x

## 為什麼用 JupyterLab？

JupyterLab 是 Jupyter Notebook 的下一代介面，提供了更現代、更靈活的使用者體驗。在 2019 年 12 月達到 1.0 穩定版後，已被視為未來主要的開發環境。

## 介面特色

### 分頁系統
如同現化的 IDE，可以在同一視窗中開啟多個 Notebook、終端機、文字檔案與 CSV 檢視器。

### 可拖拽面板
可以自由調整面板大小與位置，建立自訂的工作區配置。

### 整合終端機
內建終端機，無需切換到外部 terminal 視窗。

### 檔案總管
左側面板的檔案總管讓你可以直接管理專案檔案。

## 安裝與啟動

```bash
# 安裝
pip install jupyterlab

# 啟動
jupyter lab
```

## 延伸模組

JupyterLab 的延伸模組系統是其最大優勢之一：

### 安裝延伸模組

```bash
# 安裝延伸模組管理器
pip install jupyterlab-manager

# 安裝熱門延伸模組
jupyter labextension install @jupyterlab/git
jupyter labextension install @jupyterlab/debugger
jupyter labextension install @jupyterlab/toc
```

### 常用延伸模組

- `@jupyterlab/github`：GitHub 整合
- `@jupyterlab/debugger`：視覺化偵錯
- `@jupyterlab/toc`：自動目錄生成
- `@jupyterlab/geojson-viewer`：地理資料檢視
- `@phosphor/widgets`：豐富的 UI 元件

## 主題支援

JupyterLab 支援完整的主題切換：

```bash
# 安裝主題
jupyter labextension install @jupyterlab/theme-dark

# 切換主題（在 Settings > Theme）
```

## 效能改進

相比 Notebook，JupyterLab 1.x 提供了更好的效能與記憶體管理。對於處理大型 Notebook 或同時開啟多個文件時，差異特別明顯。

## 與 Notebook 的相容性

JupyterLab 完全相容現有的 Notebook 格式，可以直接開啟 `.ipynb` 檔案。也可以在 JupyterLab 中建立新的 Notebook 或切換回經典 Notebook 介面。

## 參考資源

- https://www.google.com/search?q=JupyterLab+1.0+release+December+2019+features+extensions
- https://www.google.com/search?q=JupyterLab+extensions+installation+tutorial+2020
- https://www.google.com/search?q=JupyterLab+vs+Notebook+differences+which+to+use+2020