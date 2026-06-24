# Bash 腳本程式設計

Bash (Bourne Again Shell) 是 Linux 最常用的 Shell，學會 Bash 腳本程式設計能大幅提升工作效率。

---

## 第一個腳本

```bash
#!/bin/bash
# 我的第一個腳本

echo "Hello, World!"
```

執行方式：

```bash
chmod +x script.sh
./script.sh

# 或直接執行
bash script.sh
```

---

## 變數

### 基本變數

```bash
name="John"
age=30

echo "Name: $name"
echo "Age: $age"
```

### 環境變數

```bash
echo "Home: $HOME"
echo "User: $USER"
echo "Path: $PATH"
```

### 只讀變數

```bash
readonly CONSTANT="固定值"
```

### 陣列

```bash
colors=("red" "green" "blue")

echo "第一個顏色: ${colors[0]}"
echo "所有顏色: ${colors[@]}"
```

---

## 條件判斷

### 基本語法

```bash
if [ condition ]; then
    # statements
elif [ condition ]; then
    # statements
else
    # statements
fi
```

### 比較運算子

```bash
# 數值比較
[ $a -eq $b ]  # 等於
[ $a -ne $b ]  # 不等於
[ $a -gt $b ]  # 大於
[ $a -lt $b ]  # 小於

# 字串比較
[ "$str1" = "$str2" ]  # 等於
[ "$str1" != "$str2" ]  # 不等於
[ -z "$str" ]          # 空字串
[ -n "$str" ]          # 非空字串

# 檔案比較
[ -e file ]   # 存在
[ -f file ]   # 普通檔案
[ -d dir ]    # 目錄
[ -r file ]   # 可讀
[ -w file ]   # 可寫
[ -x file ]   # 可執行
```

### 邏輯運算

```bash
if [ $a -gt 0 ] && [ $a -lt 10 ]; then
    echo "a 在 0 和 10 之間"
fi

if [ $a -lt 0 ] || [ $a -gt 100 ]; then
    echo "a 不在正常範圍內"
fi

if ! [ -f file ]; then
    echo "檔案不存在"
fi
```

---

## 迴圈

### for 迴圈

```bash
# 基本 for 迴圈
for i in 1 2 3 4 5; do
    echo "Number: $i"
done

# C 風格 for 迴圈
for ((i=0; i<10; i++)); do
    echo "i = $i"
done

# 遍歷陣列
for color in "${colors[@]}"; do
    echo "Color: $color"
done

# 遍歷檔案
for file in *.txt; do
    echo "Processing: $file"
done
```

### while 迴圈

```bash
count=0
while [ $count -lt 5 ]; do
    echo "Count: $count"
    count=$((count + 1))
done

# 讀取檔案
while read line; do
    echo "Line: $line"
done < file.txt
```

### until 迴圈

```bash
counter=0
until [ $counter -ge 5 ]; do
    echo "Counter: $counter"
    counter=$((counter + 1))
done
```

---

## 函數

```bash
# 定義函數
greet() {
    echo "Hello, $1!"
}

# 呼叫函數
greet "John"
greet "Mary"

# 带回傳值
add() {
    local result=$(( $1 + $2 ))
    echo $result
}

sum=$(add 3 5)
echo "Sum: $sum"
```

---

## 輸入輸出

### 讀取使用者輸入

```bash
echo "請輸入您的名字："
read name
echo "您好，$name！"

# 多個輸入
echo "輸入兩個數字："
read num1 num2
```

### 命令替換

```bash
# 使用反引號
current_date=`date`

# 使用 $()
files=$(ls -1)
```

---

## 錯誤處理

```bash
# 腳本錯誤時停止
set -e

# 追蹤錯誤
set -x

# 使用 trap
trap 'echo "Error on line $LINENO"' ERR

# 檢查命令是否成功
if ls /nonexistent; then
    echo "Success"
else
    echo "Failed"
fi
```

---

## 小結

Bash 腳本程式設計是 Linux 系統管理的基礎，熟練掌握這些概念能讓你更有效率地完成日常任務。

---

*作者：AI 程式人團隊*