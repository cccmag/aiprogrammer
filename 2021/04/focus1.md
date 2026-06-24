# Focus 1：NumPy 2021 — 向量化計算與陣列 API

## NumPy 的核心地位

NumPy 是 Python 科學計算的基石，其影響力遠超資料科學領域。從 TensorFlow 到 pandas，幾乎所有 Python 數值計算庫都建立在 NumPy 之上。NumPy 的核心創新是 N 維陣列（ndarray），提供同質、高效、連續記憶體的資料結構，搭配向量化運算，讓原本需要迴圈的計算得以用簡潔的陣列運算表達。

## 向量化思維

向量化是 NumPy 的核心思維。以元素級加法為例，傳統 Python 需要迴圈，而 NumPy 直接用陣列加法：`c = a + b`。這種設計不僅程式碼更簡潔，底層更利用 SIMD 指令和記憶體預取，效能遠超 Python 迴圈。廣播機制進一步延伸向量化能力，讓不同形狀的陣列能自動擴充後計算。

## 2021 年版本演進

NumPy 在 2021 年持續優化。1.21 LTS 版本提供更穩定的 API，新的隨機數生成器模組更加現代化。Windows 上的構建體驗顯著改善，終於擺脫「在 Windows 上編譯 NumPy 是噩夢」的困擾。SIMD 加速持續改進，特定運算的效能提升可達 20%。

## 陣列儲存順序

NumPy 支援兩種主要的記憶體儲存順序：C-order（row-major）和 F-order（column-major）。預設為 C-order，適用於大多數場景。理解儲存順序對效能至關重要——當運算涉及多個陣列時，保持一致的儲存順序可避免隱性的資料拷貝。`np.ascontiguousarray()` 和 `np.asfortranarray()` 可強制轉換儲存順序。

## 關鍵程式碼模式

```python
import numpy as np

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

c = a + b  # 元素級加法
d = np.dot(a, b)  # 矩陣乘法
e = a @ b  # 等價於 dot
```

## 參考資源

- NumPy 官方網站：https://www.google.com/search?q=NumPy+official+website
- NumPy v1.21 Release Notes：https://www.google.com/search?q=NumPy+1.21+release+notes