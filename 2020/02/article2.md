# Markdown 與 Latex

## Jupyter 中的 Markdown

Jupyter Notebook 使用 Markdown 作為文件格式，支援標準語法與擴充功能。

## 基本語法

### 標題

```markdown
# H1 標題
## H2 標題
### H3 標題
```

### 格式化

```markdown
**粗體文字**
*斜體文字*
~~刪除線~~
`行內代碼`
```

### 列表

```markdown
- 項目一
- 項目二
  - 巢狀項目

1. 編號一
2. 編號二
```

### 連結與圖片

```markdown
[連結文字](https://example.com)
![替代文字](image.png)
```

## 程式碼區塊

三個反引號包圍，並可指定語言：

````markdown
```python
print("Hello")
```
````

## Latex 數學公式

Jupyter 使用 MathJax 渲染數學公式。

### 行內公式

```markdown
質能轉換公式：$E = mc^2$
```

### 區塊公式

```markdown
$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$
```

### 常見範例

```latex
$$
\hat{y} = \beta_0 + \beta_1 x + \epsilon
$$

$$
\mathbf{X} = \begin{pmatrix}
x_{11} & x_{12} \\
x_{21} & x_{22}
\end{pmatrix}
$$

$$
\frac{\partial L}{\partial \theta} = \sum_{i=1}^{n} (y_i - \hat{y}_i)x_i
$$
```

## 表格

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| A1       | B1       | C1       |
| A2       | B2       | C2       |
```

## 標題層級與文件結構

建議使用明確的標題層級（H1 > H2 > H3），方便生成目錄。

## 參考資源

- https://www.google.com/search?q=Jupyter+Markdown+Latex+tutorial+2020
- https://www.google.com/search?q=Markdown+math+Latex+mathjax+formula+Python+notebook
- https://www.google.com/search?q=Jupyter+Markdown+table+formatting+guide