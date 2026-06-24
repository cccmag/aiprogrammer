# 機器學習環境建置

## Python ML 環境概覽

Python 是機器學習的主流語言，2019 年初的生態系包括 NumPy、SciPy、Pandas、scikit-learn、Matplotlib 等工具。

## 基礎環境設定

### 建立虛擬環境

```bash
python3 -m venv ml-env
source ml-env/bin/activate  # macOS/Linux
# ml-env\Scripts\activate   # Windows
```

### 安裝核心套件

```bash
pip install numpy scipy pandas matplotlib scikit-learn
```

## NumPy 基礎

```python
import numpy as np

# 建立陣列
a = np.array([1, 2, 3, 4, 5])
b = np.zeros((3, 3))
c = np.random.rand(2, 2)

# 矩陣運算
dot_product = np.dot(a, a)
matrix_mult = np.matmul(b, c)
```

## Pandas 資料處理

```python
import pandas as pd

# 建立 DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Carol'],
    'score': [90, 85, 88]
})

# 讀取 CSV
# df = pd.read_csv('data.csv')

# 基本統計
print(df.describe())
print(df.mean())
```

## Matplotlib 視覺化

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y)
plt.title('Sin Wave')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.grid(True)
plt.show()
```

## scikit-learn 快速範例

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 載入資料
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2
)

# 訓練模型
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

# 預測與評估
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"準確率：{accuracy:.2%}")
```

## 環境驗證腳本

```python
import sys
import numpy as np
import pandas as pd
import matplotlib
import sklearn

def check_ml_environment():
    print(f"Python: {sys.version}")
    print(f"NumPy: {np.__version__}")
    print(f"Pandas: {pd.__version__}")
    print(f"Matplotlib: {matplotlib.__version__}")
    print(f"scikit-learn: {sklearn.__version__}")

    # 基本測試
    arr = np.array([1, 2, 3])
    print(f"NumPy 測試: {arr * 2}")

    df = pd.DataFrame({'a': [1, 2, 3]})
    print(f"Pandas 測試: {df.head()}")

    from sklearn.linear_model import LinearRegression
    X = np.array([[1], [2], [3]])
    y = np.array([2, 4, 6])
    model = LinearRegression().fit(X, y)
    print(f"sklearn 測試: 係數 = {model.coef_[0]:.1f}")

if __name__ == "__main__":
    check_ml_environment()
```

##  Jupyter 整合

```bash
pip install jupyter notebook
jupyter notebook
```

```python
# 在 Notebook 中
%matplotlib inline
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [4, 5, 6])
```

## 參考資源

- https://www.google.com/search?q=Python+machine+learning+environment+setup+2019+numpy+scikit-learn
- https://www.google.com/search?q=scikit-learn+tutorial+iris+RandomForest+2019
- https://www.google.com/search?q=Python+data+science+environment+Anaconda+vs+pip+2019