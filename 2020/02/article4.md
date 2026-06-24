# Voilà 快速上手

## 安裝 Voilà

```bash
pip install voila
```

## 基本使用

### 從命令列

```bash
# 啟動 Voilà（預設埠 8866）
voila mynotebook.ipynb

# 指定埠號
voila mynotebook.ipynb --port 8080

# 指定位址
voila mynotebook.ipynb --ip=0.0.0.0
```

### 透過 JupyterLab

```bash
pip install voila
jupyter labextension install @jupyterlab/voila
```

然後在 JupyterLab 中可以看到 Voilà 按鈕，點擊即可預覽。

## 建立儀表板

### 1. 基礎 Slider

```python
import ipywidgets as widgets
from IPython.display import display

# 建立滑桿
slider = widgets.IntSlider(
    value=10,
    min=0,
    max=100,
    step=1,
    description='數值:',
    style={'description_width': '50px'}
)

# 建立輸出區
output = widgets.Output()

# 建立更新函數
def update(change):
    with output:
        output.clear_output()
        print(f"選擇的數值：{change['new']}")
        print(f"平方：{change['new'] ** 2}")

slider.observe(update, names='value')

# 顯示元件
display(slider, output)
```

### 2. 下拉選單

```python
dropdown = widgets.Dropdown(
    options=[('加法', '+'), ('減法', '-'), ('乘法', '*')],
    value='+',
    description='運算:',
)

number1 = widgets.IntText(value=10, description='數字1:')
number2 = widgets.IntText(value=5, description='數字2:')
result = widgets.Label()

def calculate(change):
    a = number1.value
    b = number2.value
    op = dropdown.value
    if op == '+':
        result.value = str(a + b)
    elif op == '-':
        result.value = str(a - b)
    else:
        result.value = str(a * b)

dropdown.observe(calculate, names='value')
number1.observe(calculate, names='value')
number2.observe(calculate, names='value')

display(dropdown, number1, number2, result)
```

## Voilà 模板

```bash
# 使用 gridstack 模板（網格佈局）
voila mynotebook.ipynb --template=gridstack

# 使用 vuetify 模板（Material Design）
voila mynotebook.ipynb --template=vuetify
```

## 部署到 Binder

```bash
# 1. 在 GitHub 建立 repository
# 2. 加入 environment.yml
# 3. 在 mybinder.org 開啟
```

## 離線使用

```bash
voila mynotebook.ipynb --enable_download=False
```

## 參考資源

- https://www.google.com/search?q=voila+jupyter+dashboard+tutorial+interactive+2020
- https://www.google.com/search?q=voila+ipywidgets+slider+dropdown+example+2020
- https://www.google.com/search?q=voila+deployment+binder+heroku+2020