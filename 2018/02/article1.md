# 程式設計基本概念

## 簡介

程式設計是告訴電腦要做什麼的過程。本篇介紹程式設計的基本概念、思維方式，以及如何開始學習寫程式。

## 什麼是程式

程式（Program）是一連串讓電腦執行的指令。就像食譜告訴廚師如何做菜一樣，程式告訴電腦如何完成任務。

### 範例：偽程式碼

```
1. 開始
2. 讀取使用者輸入的數字
3. 將數字乘以 2
4. 輸出結果
5. 結束
```

### Python 實作

```python
number = int(input("請輸入數字: "))
result = number * 2
print(f"結果是: {result}")
```

## 演算法

### 什麼是演算法

演算法是解決問題的步驟和方法。它是與程式語言無關的問題解決描述。

### 演算法特性

1. **輸入** - 可以有零或多個輸入
2. **輸出** - 至少有一個輸出
3. **明確性** - 每個步驟都清楚無歧義
4. **有限性** - 在有限步驟後一定會結束
5. **可行性** - 每個步驟都能被執行

### 範例：找出最大值

```python
def find_maximum(numbers):
    if not numbers:
        return None

    max_value = numbers[0]
    for num in numbers:
        if num > max_value:
            max_value = num

    return max_value

# 測試
data = [3, 7, 2, 9, 5]
print(find_maximum(data))  # 9
```

### 範例：泡泡排序

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# 測試
numbers = [64, 34, 25, 12, 22, 11, 90]
print(bubble_sort(numbers))
```

## 程式設計思維

### 分解（Decomposition）

將大問題拆分成小問題：

```
建立網站
├── 前端設計
│   ├── 頁面布局
│   ├── 樣式設計
│   └── 互動功能
├── 後端開發
│   ├── API 設計
│   ├── 資料庫
│   └── 業務邏輯
└── 部署上線
```

### 模式識別（Pattern Recognition）

找出問題中的相似模式：

```python
# 計算陣列總和
def sum_array(arr):
    total = 0
    for num in arr:
        total += num
    return total

# 計算陣列乘積
def product_array(arr):
    total = 1
    for num in arr:
        total *= num
    return total
```

### 抽象化（Abstraction）

忽略細節，專注目要部分：

```python
# 不需要知道是如何排序的，調用 sort() 即可
def process_data(data):
    data.sort()
    return data
```

## 程式結構

### 順序執行

```python
print("第一步")
print("第二步")
print("第三步")
```

### 條件判斷

```python
x = 10
if x > 5:
    print("x 大於 5")
else:
    print("x 不大於 5")
```

### 迴圈

```python
for i in range(5):
    print(f"第 {i} 次")
```

## 錯誤處理

### 語法錯誤

```python
# 錯誤：缺少冒號
if x > 5
    print("x 大於 5")

# 修正
if x > 5:
    print("x 大於 5")
```

### 邏輯錯誤

```python
# 意圖：計算平均
# 錯誤：沒有除以數量
def calculate_average(numbers):
    return sum(numbers)  # 缺少 / len(numbers)

# 修正
def calculate_average(numbers):
    return sum(numbers) / len(numbers)
```

### 例外處理

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("不能除以零")
```

## 學習資源

### 推薦的學習路徑

1. 選擇一門程式語言（推薦 Python）
2. 學習基本語法
3. 練習解題
4. 學習資料結構與演算法
5. 參與專案實作

### 練習平台

- LeetCode - 演算法練習
- HackerRank - 程式技能
- Project Euler - 數學與程式

## 練習題

1. 寫一個判斷是否為質數的程式
2. 寫一個計算費氏數列第 N 項的程式
3. 寫一個反轉字串的程式
4. 寫一個判斷是否為迴文的程式