# Notebook 互動介面

## ipywidgets 基礎

ipywidgets 是 Jupyter 的互動式 UI 元件庫：

```bash
pip install ipywidgets
jupyter nbextension enable --py widgetsnbextension
```

## 基本 Widget

### IntSlider

```python
from ipywidgets import interact, IntSlider

@interact(x=(0, 100, 5))
def show(x=50):
    return x ** 2
```

### Dropdown

```python
@interact(fruit=['蘋果', '香蕉', '橘子'])
def show_fruit(fruit='蘋果'):
    return f"你選擇了：{fruit}"
```

### Checkbox

```python
@interact(show_square=False)
def toggle(square):
    if square:
        return "顯示平方"
    return "隱藏平方"
```

## 手動建立 Widget

```python
import ipywidgets as widgets

# 建立元件
slider = widgets.IntSlider(value=50, min=0, max=100)
button = widgets.Button(description='點擊')
output = widgets.Output()

# 事件處理
def on_click(b):
    with output:
        output.clear_output()
        print(f"按鈕被點擊！目前數值：{slider.value}")

button.on_click(on_click)

# 顯示
display(slider, button, output)
```

## Layout 控制

```python
# 垂直佈局
from ipywidgets import VBox, HBox

left_box = VBox([widgets.Label("左側"), widgets.IntSlider()])
right_box = VBox([widgets.Label("右側"), widgets.IntSlider()])

HBox([left_box, right_box])
```

## Box Layout 選項

```python
# 百分比寬度
box = widgets.Box([
    widgets.IntSlider(),
    widgets.IntSlider()
])
box.layout.flex = '1 1 auto'
box.layout.width = '100%'

# 對齊方式
box.layout.justify_content = 'space-between'
box.layout.align_items = 'center'
```

## 觀察者模式

```python
text = widgets.Text(
    placeholder='輸入文字',
    description='文字:'
)

result = widgets.HTML()

def on_change(change):
    result.value = f"<b>你輸入了：</b>{change['new']}"

text.observe(on_change, names='value')

display(text, result)
```

## 常用 Widget 類型

| Widget | 用途 |
|--------|------|
| IntSlider | 整數滑桿 |
| FloatSlider | 浮點數滑桿 |
| Dropdown | 下拉選單 |
| Checkbox | 核取方塊 |
| RadioButtons | 單選按鈕 |
| ToggleButton | 切換按鈕 |
| Text | 文字輸入 |
| Textarea | 多行文字 |
| Button | 按鈕 |
| Output | 輸出區域 |

## 參考資源

- https://www.google.com/search?q=ipywidgets+interactive+widgets+Jupyter+tutorial+2020
- https://www.google.com/search?q=jupyter+widgets+slider+dropdown+button+example+2020
- https://www.google.com/search?q=ipywidgets+layout+box+flex+jupyter+2020