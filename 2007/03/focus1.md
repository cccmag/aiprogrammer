# 動態語言的復興：Python、Ruby 的崛起

## 前言

2007 年見證了動態語言的復興。Python 和 Ruby 從小眾語言成長為主流選擇。

## Python 的哲學

### 簡潔與優雅

Python 的設計強調可讀性和簡潔：

```python
# Pythonic 風格
# 傳統方式
result = []
for i in range(10):
    if i % 2 == 0:
        result.append(i * i)

# Python 方式
result = [i*i for i in range(10) if i % 2 == 0]
```

### Python 的應用領域

```
┌────────────────────────────────────────────────────────┐
│            Python 應用領域（2007 年）                   │
├────────────────────────────────────────────────────────┤
│                                                        │
│  網頁開發：                                           │
│  - Django, Pylons, Turbogears                        │
│                                                        │
│  科學計算：                                           │
│  - NumPy, SciPy, matplotlib                         │
│                                                        │
│  系統工具：                                           │
│  - Fabric, Buildout                                  │
│                                                        │
│  遊戲開發：                                           │
│  - Pygame                                            │
│                                                        │
│  文字處理：                                           │
│  - Natural Language Toolkit (NLTK)                  │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## Ruby 的優雅

### Ruby 的設計理念

```ruby
# Ruby 強調程式碼的優雅
# 區塊語法
[1, 2, 3].each { |i| puts i * 2 }

# 條件表達式
greeting = if name.empty?
             "Hello!"
           else
             "Hello, #{name}!"
           end
```

### Ruby on Rails 的影響

Ruby 的流行很大程度上歸功於 Rails 框架：

- Convention over Configuration
- DRY (Don't Repeat Yourself)
- RESTful 路由

## 比較

| 特性 | Python | Ruby |
|------|--------|------|
| 設計哲學 | 簡潔明確 | 優雅靈活 |
| 社群 | 科學計算強 | Web 開發強 |
| 學習曲線 | 較平緩 | 較陡 |
| 部署 | 廣泛採用 | 相對較少 |

---

## 延伸閱讀

- [Python 官方網站](https://www.google.com/search?q=Python+programming+language)
- [Ruby 官方網站](https://www.google.com/search?q=Ruby+programming+language)

*本篇文章為「AI 程式人雜誌 2007 年 3 月號」本期焦點系列文章。*