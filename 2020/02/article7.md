# widgets 與 ipywidgets

## 安裝與啟用

```bash
pip install ipywidgets
jupyter nbextension enable --py widgetsnbextension
```

## 裝飾器模式

### @interact

最基本的互動模式：

```python
@interact(x=10)
def f(x):
    print(x)
```

### @interact_manual

需要手動點擊才執行：

```python
from ipywidgets import interact_manual

@interact_manual(x=10)
def f(x):
    print(x ** 2)
```

### @interact.options

```python
@interact(x=[('一年', 1), ('兩年', 2), ('三年', 3)])
def period(x):
    return x
```

## 互動約束

```python
# 整數範圍
@interact(x=(0, 100, 5))  # 0-100，步進 5

# 浮點數範圍
@interact(y=(0.0, 10.0, 0.5))

# 布林值（自動生成 Checkbox）
@interact(enabled=True)
```

## 互動式回調

```python
from ipywidgets import interactive
import matplotlib.pyplot as plt
import numpy as np

def plot_sine(amplitude=1, frequency=1, phase=0):
    x = np.linspace(0, 4 * np.pi, 100)
    y = amplitude * np.sin(frequency * x + phase)
    plt.figure(figsize=(8, 4))
    plt.plot(x, y)
    plt.ylim(-5, 5)
    plt.show()

w = interactive(plot_sine,
    amplitude=(0.5, 3.0),
    frequency=(0.5, 3.0),
    phase=(0, np.pi, 0.1)
)
display(w)
```

## 建立自訂 Widget

```python
from ipywidgets import Widget
from traitlets import Unicode, Int

class MyWidget(Widget):
    _view_name = Unicode('MyWidgetView').tag(sync=True)
    _view_module = Unicode('mywidget').tag(sync=True)
    value = Int().tag(sync=True)
```

## 圖表整合

```python
import plotly.graph_objects as go
from ipywidgets import interact

@interact(n=(1, 10, 1))
def create_plot(n):
    fig = go.Figure(data=[go.Bar(x=list(range(n)), y=[i**2 for i in range(n)])])
    fig.show()
```

## 檔案上傳 Widget

```python
from ipywidgets import FileUpload

upload = FileUpload(accept='.csv', multiple=False)

def on_upload(change):
    content = list(change['new'].values())[0]['content']
    # 處理上傳的檔案

upload.observe(on_upload, names='data')
display(upload)
```

## 參考資源

- https://www.google.com/search?q=ipywidgets+tutorial+interact+decorator+2020
- https://www.google.com/search?q=ipywidgets+interactive+matplotlib+plotly+2020
- https://www.google.com/search?q=jupyter+custom+widget+python+2020+guide