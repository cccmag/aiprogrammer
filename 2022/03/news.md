# 本月新知

## 2022 年 3 月程式與 AI 技術動態

### Python 生態

**Python 3.11 開發進行中**

Python 3.11 正處於 Alpha 階段，預計 2022 年 10 月正式發布。本版本帶來了重大效能提升——CPython 團隊的「更快 CPython」專案（PEP 659）引入了基於特化的自適應解釋器，號稱平均提速 10-60%。此外，PEP 680 將 `tomllib` 納入標準庫，PEP 654 引入 ExceptionGroup 與 except* 語法。

**NumPy 1.22 發布**

NumPy 1.22 於 2022 年 1 月釋出，支援 Python 3.10，棄用了大量過時 API。新版本改進了 `np.pad` 和 `np.histogram` 的效能，並正式啟用 SIMD 最佳化路徑，讓陣列運算在 x86 和 ARM 架構上獲得顯著加速。

**Pandas 1.4 登場**

Pandas 1.4 帶來了多項新功能：改進的 `Styler` 支援、新的 `case_when` 方法、以及對 PyArrow 後端的實驗性支援。`df.value_counts()` 現在支援 `sort=False` 參數，`pd.concat` 的效能也有明顯改善。

**SciPy 1.8 新增功能**

SciPy 1.8 引入了新的 `scipy.fft` 子模組（基於 PyFFTW），以及改進的稀疏線性代數支援。`scipy.spatial` 新增了 Quickhull 演算法的 GPU 實作。

### 機器學習框架

**scikit-learn 1.0 後的生態發展**

scikit-learn 在 1.0 里程碑後持續更新，1.1 版預計加入 `HistGradientBoostingRegressor` 的分類支援、以及新的 `missing_values` 參數。社群正積極開發對 GPU 加速的支援。

**PyTorch 1.11 與 TensorFlow 2.9**

PyTorch 1.11 強化了函數式最佳化和分散式訓練功能。TensorFlow 2.9 則改進了 Keras API，並正式支援 Apple Silicon 的原生運算。

### AI 領域動態

**DALL-E 2 引發 AI 繪圖熱潮**

OpenAI 於 4 月初（2022 年 4 月）發布了 DALL-E 2，雖然在 3 月已有預告，其擴散模型架構引發了 AI 生成圖像的新浪潮。這項技術迅速影響了整個 AI 藝術領域。

**DeepMind 的 Gato 通用模型**

DeepMind 發表了 Gato——一個能玩遊戲、聊天、描述圖像、操作機器人的通用模型，為通用人工智慧（AGI）研究提供了新思路。

### 開發工具

**VS Code Python 擴展更新**

微軟持續更新 VS Code 的 Python 擴展，加入了 Jupyter Notebook 的改進支援、更好的 IntelliSense 以及實驗性的 Python 測試瀏覽器。

**JupyterLab 3.3 發布**

JupyterLab 3.3 引入了新的除錯器前端、改進的檔案瀏覽器，以及對 Jupyter Notebook 7 的相容性更新。

### 業界動態

- **GitHub Copilot** 正式開放付費使用，每月 10 美元
- **Streamlit 1.8** 加入 `st.chat` 組件，讓資料科學家快速建立聊天式介面
- **Anaconda** 發布了 Python 3.10 版的 Anaconda Distribution
- **NVIDIA** 宣布 cuDF 加速 Pandas 操作，GPU DataFrame 效能提升 10-50 倍

### 標準與規範

- 中國發布了《資料安全法》實施細則草案，影響資料科學應用的合規要求
- ECMAScript 2022 草案納入 Top-Level Await 和類別的靜態初始化區塊
