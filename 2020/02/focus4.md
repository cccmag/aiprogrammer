# 4. Voilà 互動式儀表板

## Voilà 是什麼？

Voilà 將 Jupyter Notebook 轉換為獨立的互動式網頁應用，不顯示程式碼，只展示輸出結果與互動元素。這讓你可以分享乾淨的儀表板給非技術人員。

## 與一般網頁的差異

| 特性 | Voilà | 傳統網頁 |
|------|-------|----------|
| 開發方式 | Jupyter Notebook | HTML/CSS/JS |
| 互動元素 | ipywidgets | JavaScript |
| 程式碼隱藏 | 自動 | N/A |
| 部署複雜度 | 簡單 | 複雜 |

## 安裝

```bash
pip install voila
```

## 基本使用

```bash
# 啟動 Voilà（針對特定 Notebook）
voila mynotebook.ipynb

# 透過 JupyterLab
# 1. 安裝Voilà extension
pip install voila
jupyter labextension install @jupyterlab/voila

# 2. 在 JupyterLab 中看到 "Voila" 按鈕
```

## 建立儀表板 Notebook

```python
# 1.ipynb
import ipywidgets as widgets
from IPython.display import display

# 建立 UI 元件
slider = widgets.IntSlider(
    value=50,
    min=0,
    max=100,
    description='選擇數值:'
)

output = widgets.Output()

def update(change):
    with output:
        output.clear_output()
        print(f"結果：{change['new'] ** 2}")

slider.observe(update, names='value')

display(slider, output)
```

執行 `voila 1.ipynb` 會得到一個只有滑桿與輸出的網頁。

## 部署 Voilà

### 本地部署

```bash
voila mynotebook.ipynb --port=8866
```

### JupyterHub 部署

Voilà 可以整合到 JupyterHub 中：

```bash
pip install voila
jupyter labextension install @jupyterlab/voila
```

### Binder 部署

可以將 Voilà 儀表板部署到 Binder：

```bash
# 在 Repository 中加入
# environment.yml:
# dependencies:
#   - voila
```

## Voilà 模板

```bash
# 指定模板（預設為 'default'）
voila mynotebook.ipynb --template=gridstack

# 可用模板
# - default：單欄佈局
# - gridstack：網格佈局
# - vuetify：使用 Vuetify UI 框架
```

## 參考資源

- https://www.google.com/search?q=Voilà+Jupyter+dashboard+interactive+2020+tutorial
- https://www.google.com/search?q=voila+ipywidgets+dashboard+Python+2020
- https://www.google.com/search?q=voila+deployment+binder+jupyterhub+2020