# 7. 資料視覺化整合

## matplotlib 整合

Jupyter 對 matplotlib 有原生支援，特別是 `inline` 模式：

```python
%matplotlib inline
import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4])
plt.ylabel('some values')
plt.show()
```

## 互動式繪圖

### Plotly

```bash
pip install plotly
```

```python
import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    'x': [1, 2, 3, 4],
    'y': [10, 11, 12, 13],
    'label': ['a', 'b', 'c', 'd']
})

fig = px.scatter(df, x='x', y='y', color='label')
fig.show()
```

### Bokeh

```bash
pip install bokeh
```

```python
from bokeh.plotting import figure, output_notebook, show

output_notebook()

p = figure(title="簡單範例", x_axis_label='x', y_axis_label='y')
p.line([1, 2, 3, 4], [10, 11, 12, 13], legend_label="資料", line_width=2)
show(p)
```

### Altair

```bash
pip install altair vega_datasets
```

```python
import altair as alt
import pandas as pd

df = pd.DataFrame({
    'x': [1, 2, 3, 4],
    'y': [10, 11, 12, 13]
})

alt.Chart(df).mark_point().encode(
    x='x',
    y='y'
).interactive()
```

## 3D 視覺化

### PyVista

```bash
pip install pyvista
```

```python
import pyvista as pv
import numpy as np

# 建立球體
sphere = pv.Sphere()
sphere.plot()
```

## 地圖視覺化

### Folium

```bash
pip install folium
```

```python
import folium

m = folium.Map(location=[25.03, 121.56], zoom_start=12)
folium.Marker([25.03, 121.56], popup='台北').add_to(m)
m
```

## 儀表板整合

使用 Voilà 與互動式元件建立儀表板：

```python
import ipywidgets as widgets
import matplotlib.pyplot as plt

slider = widgets.IntSlider(value=50, min=0, max=100)

def update(n):
    plt.figure(figsize=(4, 3))
    plt.hist([i**2 for i in range(n)])
    plt.show()

widgets.interact(update, n=slider)
```

## 動畫製作

```python
from matplotlib import animation
import numpy as np

fig, ax = plt.subplots()
line, = ax.plot([], [])

def init():
    ax.set_xlim(0, 10)
    ax.set_ylim(-1, 1)
    return line,

def animate(i):
    x = np.linspace(0, 10, 100)
    y = np.sin(x + i * 0.1)
    line.set_data(x, y)
    return line,

ani = animation.FuncAnimation(fig, animate, init_func=init, frames=100, interval=20)
plt.show()
```

## 參考資源

- https://www.google.com/search?q=Jupyter+matplotlib+inline+interactive+plotting+2020
- https://www.google.com/search?q=Python+plotly+bokeh+altair+visualization+comparison+2020
- https://www.google.com/search?q=voila+dashboard+interactive+widgets+python+2020