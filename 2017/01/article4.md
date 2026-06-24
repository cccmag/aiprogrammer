# Visual Studio Code 推出 Python 擴展

## 前言

微軟持續強化 VS Code 對 Python 的支援。2017 年 1 月，Python 擴展帶來了重大更新，包括更好的 IntelliSense、偵錯功能和程式碼導航。

## VS Code Python 擴展

VS Code 的 Python 擴展提供了完整的 Python 開發體驗：

```bash
# 安裝 Python 擴展
code --install-extension ms-python.python
```

### 核心功能

- **IntelliSense**：智慧代碼補全
- **語法高亮**：Python 特定語法
- **代碼導航**：跳轉到定義、查找引用
- **偵錯支援**：互動式偵錯
- **格式化和 Linting**：PEP 8 規範檢查

## IntelliSense 功能

```python
# 智慧代碼補全
import numpy as np
arr = np.array([1, 2, 3])
arr.  # 會顯示所有可用方法

# 跳轉到定義
# 右鍵點擊 → Go to Definition

# 查看文件
# 懸停顯示快速文檔
```

## 偵錯功能

```python
# launch.json 配置
{
    "name": "Python",
    "type": "python",
    "request": "launch",
    "program": "${file}",
    "console": "integratedTerminal"
}
```

```python
# 設定中斷點
def calculate_sum(numbers):
    total = 0  # 設定中斷點
    for n in numbers:
        total += n
    return total

# 使用偵錯器
# F5 開始偵錯
# F10 逐步執行
# F11 進入函式
# Shift+F11 跳出函式
```

## Jupyter Notebook 支援

VS Code 正在引入 Notebook 支援：

```javascript
// 未來版本將支援
{
    "cells": [
        {
            "cell_type": "code",
            "source": "import numpy as np"
        }
    ]
}
```

## 與其他 Python IDE 的比較

| 特性 | VS Code | PyCharm | Spyder |
|------|---------|---------|--------|
| 價格 | 免費開源 | 社群版免費/專業版付費 | 免費開源 |
| 擴展生態 | 豐富 | 豐富 | 一般 |
| 記憶體使用 | 低 | 高 | 中 |
| Jupyter 整合 | 進行中 | 一般 | 優秀 |

## 結語

VS Code 正在成為 Python 開發者的熱門選擇，特別是對於需要多種語言支援的開發團隊。微軟對 Python 工具的持續投資顯示了他們對 Python 社群承諾。

---

## 延伸閱讀

- [VS Code Python 擴展](https://www.google.com/search?q=Visual+Studio+Code+Python+extension)
- [VS Code Python 偵錯教程](https://www.google.com/search?q=VSCode+Python+debugging+tutorial)
- [Python+IDE+比較](https://www.google.com/search?q=Python+IDE+comparison+2017)
- [PyCharm+vs+VS+Code](https://www.google.com/search?q=PyCharm+vs+VS+Code+Python)

---

*本篇文章為「AI 程式人雜誌 2017 年 1 月號」文章系列之一。*