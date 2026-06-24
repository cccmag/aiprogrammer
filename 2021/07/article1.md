# Python 文字處理技巧

Python 提供了豐富的文字處理功能，從基本的字串操作到正規表達式，無所不包。本文介紹實用的文字處理技巧，幫助讀者更高效地處理文字資料。

## 1. 基本字串操作

Python 的字串是不可變物件，但提供了大量有用的方法：

```python
text = "  Hello, World!  "

print(text.lower())           # 小寫
print(text.upper())           # 大寫
print(text.strip())          # 去除空白
print(text.replace("World", "Python"))  # 取代
print(text.split(","))       # 分割
print(",".join(["a", "b", "c"]))  # 連接
```

## 2. 字串格式化

Python 提供了多種字串格式化方法：

```python
name = "Alice"
age = 30

print(f"My name is {name} and I'm {age} years old.")
print("My name is {} and I'm {} years old.".format(name, age))
print("My name is %s and I'm %d years old." % (name, age))
```

f-string 是 Python 3.6+ 引入的最簡潔格式。

## 3. 正規表達式基礎

正規表達式是處理複雜文字模式的有力工具：

```python
import re

text = "My email is test@example.com and phone is 123-456-7890"

emails = re.findall(r'\b[\w.-]+@[\w.-]+\.\w+\b', text)
phones = re.findall(r'\d{3}-\d{3}-\d{4}', text)

print("Emails:", emails)
print("Phones:", phones)
```

## 4. Unicode 與編碼

處理多語言文字時需要注意編碼問題：

```python
text = "你好，世界！ Hello, World!"

encoded = text.encode('utf-8')
decoded = encoded.decode('utf-8')

print(f"原始文字: {text}")
print(f"編碼後位元組數: {len(encoded)}")
print(f"解碼後: {decoded}")
```

## 5. 文字檔案處理

讀取和寫入文字檔案：

```python
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()

with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(content)
```

使用 `with` 語句確保檔案正確關閉。

## 6. 結論

掌握這些文字處理技巧，能讓你在處理 NLP 任務時更加得心應手。

---

## 延伸閱讀

- [Python 官方文檔：文字序列類型](https://www.google.com/search?q=Python+string+methods+official+documentation)
- [正規表達式 HOWTO](https://www.google.com/search?q=Python+regular+expression+HOWTO)