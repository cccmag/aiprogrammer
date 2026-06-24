# JupyterLab 延伸模組

## 延伸模組系統

JupyterLab 1.x 的延伸模組系統允許新增功能。延伸模組使用 TypeScript/JavaScript 編寫。

## 安裝延伸模組

### 基本語法

```bash
jupyter labextension install <extension-name>
```

### 常用延伸模組

#### 1. 檔案總管增強

```bash
jupyter labextension install @jupyterlab/docmanager-extension
```

#### 2. Git 整合

```bash
jupyter labextension install @jupyterlab/git
pip install jupyterlab-git
```

#### 3. 目錄生成

```bash
jupyter labextension install @jupyterlab/toc
```

#### 4. 調試器（需要 IPython 7.18+）

```bash
jupyter labextension install @jupyterlab/debugger
```

#### 5. 變數檢視器

```bash
jupyter labextension install @jupyterlab/variableinspector
```

## 管理延伸模組

```bash
# 列出已安裝
jupyter labextension list

# 更新
jupyter labextension update @jupyterlab/git

# 卸載
jupyter labextension uninstall @jupyterlab/git
```

## 主題延伸模組

```bash
# 安裝深色主題
jupyter labextension install @jupyterlab/theme-dark

# 安裝其它主題
jupyter labextension install @deathbear/brown-light-theme
```

## 建立自己的延伸模組（進階）

```bash
# 安裝工具
npm install -g cookiecutter

# 建立專案
cookiecutter https://github.com/jupyterlab/extension-cookiecutter-ts
cd my-extension
npm install
jupyter labextension install .
```

## 延伸模組相容性

JupyterLab 1.x 與 JupyterLab 0.x 的延伸模組不相容。安裝前請確認版本。

## 推薦組合

1. **教學用途**：`toc` + `git` + `variableinspector`
2. **資料分析**：`toc` + `debugger` + 互動式 widgets
3. **簡報用途**：`drawio` + 簡報相關延伸模組

## 參考資源

- https://www.google.com/search?q=JupyterLab+extensions+installation+tutorial+2020
- https://www.google.com/search?q=jupyterlab+theme+dark+light+extensions+2020
- https://www.google.com/search?q=jupyterlab+extension+development+typescript+2020