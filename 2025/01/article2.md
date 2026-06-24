# 你的第一個 Python 程式

## 經典起點：Hello, World!

幾乎每一位程式設計師的第一行程式碼都是「Hello, World!」。這個傳統可以追溯到 1978 年的《The C Programming Language》教科書。

### 建立你的第一個檔案

建立一個名為 `hello.py` 的檔案，輸入以下內容：

```python
print("Hello, World!")
```

然後在終端機執行：

```bash
python hello.py
```

輸出：
```
Hello, World!
```

恭喜！你已經寫出了第一個 Python 程式！

## print() 函數深入

`print()` 是 Python 中最常用的內建函數，用於將輸出顯示在螢幕上。

### 多個參數

```python
# 自動在參數間加入空格
print("Hello", "Python", "World")
# Hello Python World

# 自訂分隔符號
print("apple", "banana", "orange", sep=", ")
# apple, banana, orange

# 自訂結尾
print("Loading", end="")
print("...完成")
# Loading...完成
```

## 程式的執行流程

### 互動式模式

直接在終端機輸入 `python` 進入互動式模式：

```python
>>> 1 + 1
2
>>> print("hello")
hello
>>>
```

使用 `exit()` 或 Ctrl+D 離開。

### 腳本模式

將程式碼寫在 `.py` 檔案中，然後用 `python filename.py` 執行。

## 從使用者獲取輸入

```python
name = input("請輸入你的名字：")
print(f"你好，{name}！歡迎來到 Python 的世界！")

age = input("請輸入你的年齡：")
# input 回傳的是字串，需要轉換
age = int(age)
print(f"明年你將 {age + 1} 歲")
```

## 你的第一個計算程式

```python
# 簡單計算機
print("=== 簡單計算機 ===")
a = float(input("請輸入第一個數字："))
b = float(input("請輸入第二個數字："))

print(f"{a} + {b} = {a + b}")
print(f"{a} - {b} = {a - b}")
print(f"{a} * {b} = {a * b}")
print(f"{a} / {b} = {a / b}")
```

## 註解的力量

註解是寫給人看的，不是給電腦執行的：

```python
# 這是單行註解

"""
這是多行註解
可以寫多行說明文字
"""

# 好的註解解釋「為什麼」，而不是「做什麼」
# 壞的註解：將華氏溫度轉換為攝氏溫度  ← 明顯的事實
# 好的註解：使用近似公式以提升計算速度
```

## 第一個實用程式

讓我們寫一個實用的溫度轉換程式：

```python
def celsius_to_fahrenheit(c):
    """攝氏轉華氏"""
    return c * 9 / 5 + 32

def fahrenheit_to_celsius(f):
    """華氏轉攝氏"""
    return (f - 32) * 5 / 9

print("=== 溫度轉換工具 ===")
print("1. 攝氏 → 華氏")
print("2. 華氏 → 攝氏")

choice = input("請選擇轉換方向 (1/2): ")

if choice == "1":
    c = float(input("請輸入攝氏溫度："))
    f = celsius_to_fahrenheit(c)
    print(f"{c}°C = {f:.1f}°F")
elif choice == "2":
    f = float(input("請輸入華氏溫度："))
    c = fahrenheit_to_celsius(f)
    print(f"{f}°F = {c:.1f}°C")
else:
    print("無效的選擇")
```

## 程式除錯的基本觀念

當程式出現錯誤時，不要驚慌。錯誤訊息是你的好朋友：

```python
# 常見錯誤類型
print(undefined_var)  # NameError: 未定義的變數
"2" + 2               # TypeError: 不能串接字串和數字
int("abc")            # ValueError: 無法轉換
```

### 使用 print 除錯法

最簡單有效的除錯方式：

```python
def divide(a, b):
    print(f"除錯：a={a}, b={b}")  # 印出變數值
    result = a / b
    print(f"除錯：result={result}")
    return result
```

## 小結

你的第一個 Python 程式不僅僅是「Hello, World!」，而是理解程式與使用者互動的開始。從簡單的輸出輸入開始，逐步加入計算邏輯，你已經掌握了程式設計的基本模式：輸入 → 處理 → 輸出。

---

**延伸閱讀**

- [Python print() 函數文件](https://www.google.com/search?q=Python+print+function+documentation)
- [Python input() 函數文件](https://www.google.com/search?q=Python+input+function)
