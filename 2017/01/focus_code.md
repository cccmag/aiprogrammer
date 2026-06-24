# Python 生態系常用工具

## 程式實作目錄

本期程式中包含 Python 生態系核心工具的使用範例，涵蓋：

1. **pip 與虛擬環境**：`pip_demo.py`
2. **NumPy 基礎**：`numpy_demo.py`
3. **Pandas 資料處理**：`pandas_demo.py`
4. **Matplotlib 視覺化**：`matplotlib_demo.py`

## 執行方式

```bash
cd _code/
python3 pip_demo.py
python3 numpy_demo.py
python3 pandas_demo.py
python3 matplotlib_demo.py
```

或執行 `bash test.sh` 來運行所有範例。

---

## pip 與虛擬環境示例

### pip_demo.py

```python
#!/usr/bin/env python3
"""pip 與虛擬環境使用示範"""

def demo():
    print("=" * 60)
    print("pip 與虛擬環境使用示範")
    print("=" * 60)

    print("\n1. 常用 pip 命令：")
    print("   pip install <package>          # 安裝套件")
    print("   pip install <package>==1.0.0   # 安裝特定版本")
    print("   pip install -r requirements.txt # 從檔案安裝")
    print("   pip list                        # 列出已安裝套件")
    print("   pip show <package>              # 顯示套件資訊")
    print("   pip uninstall <package>         # 卸載套件")
    print("   pip freeze > requirements.txt   # 產出依賴檔案")

    print("\n2. 虛擬環境命令：")
    print("   python3 -m venv myenv           # 創建虛擬環境")
    print("   source myenv/bin/activate       # 激活（Linux/macOS）")
    print("   myenv\\Scripts\\activate         # 激活（Windows）")
    print("   deactivate                      # 退出虛擬環境")

    print("\n3. 現代替代方案：pipenv")
    print("   pip install pipenv              # 安裝 pipenv")
    print("   pipenv install <package>       # 安裝套件")
    print("   pipenv shell                    # 激活環境")
    print("   pipenv run python script.py     # 直接執行腳本")

    print("\n4. 示例虛擬環境工作流：")
    print("   $ python3 -m venv myproject_env")
    print("   $ source myproject_env/bin/activate")
    print("   (myproject_env) $ pip install numpy pandas matplotlib")
    print("   (myproject_env) $ pip freeze > requirements.txt")
    print("   (myproject_env) $ python my_script.py")
    print("   (myproject_env) $ deactivate")

if __name__ == "__main__":
    demo()
```

## NumPy 示例

### numpy_demo.py

```python
#!/usr/bin/env python3
"""NumPy 基礎操作示範"""

import numpy as np

def demo():
    print("=" * 60)
    print("NumPy 基礎操作示範")
    print("=" * 60)

    # 創建陣列
    print("\n1. 創建陣列：")
    a = np.array([1, 2, 3, 4, 5])
    print(f"   a = np.array([1, 2, 3, 4, 5]) → {a}")
    print(f"   a.shape = {a.shape}, a.dtype = {a.dtype}")

    b = np.zeros((3, 4))
    print(f"   np.zeros((3, 4)) =\n{b}")

    c = np.arange(0, 10, 2)
    print(f"   np.arange(0, 10, 2) = {c}")

    d = np.random.randn(2, 3)
    print(f"   np.random.randn(2, 3) =\n{d}")

    # 基本運算
    print("\n2. 基本運算：")
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    print(f"   x = {x}, y = {y}")
    print(f"   x + y = {x + y}")
    print(f"   x * y = {x * y}")
    print(f"   x @ y = {x @ y} (dot product)")

    # 矩陣運算
    print("\n3. 矩陣運算：")
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    print(f"   A @ B = \n{A @ B}")
    print(f"   A.T = \n{A.T}")  # 轉置

    # 索引與切片
    print("\n4. 索引與切片：")
    arr = np.arange(12).reshape(3, 4)
    print(f"   arr (3x4):\n{arr}")
    print(f"   arr[1, 2] = {arr[1, 2]}")
    print(f"   arr[:, 1] = {arr[:, 1]}")
    print(f"   arr[arr > 5] = {arr[arr > 5]}")

if __name__ == "__main__":
    demo()
```

## Pandas 示例

### pandas_demo.py

```python
#!/usr/bin/env python3
"""Pandas 基礎操作示範"""

import pandas as pd
import numpy as np

def demo():
    print("=" * 60)
    print("Pandas 基礎操作示範")
    print("=" * 60)

    # Series
    print("\n1. Series：")
    s = pd.Series([1, 3, 5, np.nan, 6, 8])
    print(f"   Series: {s.values}")
    print(f"   Index: {list(s.index)}")

    # DataFrame
    print("\n2. DataFrame：")
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'age': [25, 30, 35, 28],
        'score': [85.5, 90.0, 78.5, 92.0]
    })
    print(df)

    # 基本操作
    print("\n3. 基本操作：")
    print(f"   df['name'] = {list(df['name'])}")
    print(f"   df.describe():\n{df.describe()}")
    print(f"   df[df['age'] > 28]:\n{df[df['age'] > 28]}")

    # 讀寫 CSV
    print("\n4. 讀寫操作：")
    print("   pd.read_csv('file.csv')  # 讀取")
    print("   df.to_csv('output.csv')   # 寫入")

if __name__ == "__main__":
    demo()
```

## Matplotlib 示例

### matplotlib_demo.py

```python
#!/usr/bin/env python3
"""Matplotlib 基礎操作示範"""

import matplotlib
matplotlib.use('Agg')  # 非互動式後端
import matplotlib.pyplot as plt
import numpy as np

def demo():
    print("=" * 60)
    print("Matplotlib 基礎操作示範")
    print("=" * 60)

    x = np.linspace(0, 2 * np.pi, 100)

    # 創建圖表
    print("\n1. 創建圖表：")
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    axes[0, 0].plot(x, np.sin(x), 'b-')
    axes[0, 0].set_title('Sin(x)')
    axes[0, 0].grid(True)

    axes[0, 1].plot(x, np.cos(x), 'r-')
    axes[0, 1].set_title('Cos(x)')
    axes[0, 1].grid(True)

    axes[1, 0].plot(x, x**2, 'g-')
    axes[1, 0].set_title('x^2')
    axes[1, 0].grid(True)

    axes[1, 1].scatter(np.random.randn(50), np.random.randn(50), alpha=0.5)
    axes[1, 1].set_title('Scatter Plot')
    axes[1, 1].grid(True)

    plt.tight_layout()
    plt.savefig('/tmp/matplotlib_demo.png')
    print("   圖表已保存到 /tmp/matplotlib_demo.png")

    # 柱狀圖
    print("\n2. 柱狀圖：")
    categories = ['A', 'B', 'C', 'D']
    values = [23, 45, 56, 78]
    plt.figure()
    plt.bar(categories, values, color=['red', 'green', 'blue', 'orange'])
    plt.title('Category Performance')
    plt.xlabel('Category')
    plt.ylabel('Value')
    plt.savefig('/tmp/bar_demo.png')
    print("   柱狀圖已保存到 /tmp/bar_demo.png")

    print("\n注意：如需顯示圖表，請使用 plt.show() 或在 Jupyter 中使用 %matplotlib inline")

if __name__ == "__main__":
    demo()
```

---

## 延伸閱讀

- [pip 官方文檔](https://www.google.com/search?q=pip+python+package+manager+documentation)
- [NumPy 官方文檔](https://www.google.com/search?q=NumPy+tutorial+documentation)
- [Pandas 官方文檔](https://www.google.com/search?q=Pandas+tutorial+data+analysis)
- [Matplotlib 官方文檔](https://www.google.com/search?q=Matplotlib+tutorial+python+plotting)

---

*本期程式實作到此結束。*