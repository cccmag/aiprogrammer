# awk 資料處理

## awk 是什麼？

awk 不僅僅是一個命令列工具——它是一門完整的程式語言。awk 由 Alfred Aho、Peter Weinberger 和 Brian Kernighan 於 1977 年創建，名字取自他們的姓氏首字母。

awk 自動將每行輸入分割成欄位 (`$1`, `$2`, …, `$NF`)，並針對符合條件的行執行操作。

### 基本結構

```bash
awk 'pattern { action }' file.txt
```

- **pattern**: 何時執行 (可省略，省略則對所有行執行)
- **action**: 要做什麼 (可省略，省略則列印整行)

## 欄位與記錄

```bash
# 預設以空白分隔欄位
awk '{print $1, $3}' data.txt

# 自訂分隔符
awk -F: '{print $1}' /etc/passwd
awk -F',' '{print $2, $3}' data.csv

# NF：欄位數量
awk '{print "欄位數:", NF, "最後一欄:", $NF}' file

# NR：行號
awk '{print NR":", $0}' file

# FS / OFS：輸入/輸出分隔符
awk 'BEGIN {FS=","; OFS=" | "} {print $1, $2}'
```

### 內建變數

| 變數 | 說明 |
|------|------|
| `NR` | 已處理的記錄數 (行號) |
| `NF` | 當前行的欄位數 |
| `$0` | 整行內容 |
| `$1..$NF` | 各欄位 |
| `FS` | 輸入欄位分隔符 (預設空白) |
| `OFS` | 輸出欄位分隔符 (預設空白) |
| `RS` | 記錄分隔符 (預設換行) |
| `ORS` | 輸出記錄分隔符 |
| `FILENAME` | 當前檔案名 |

## 模式匹配

```bash
# 行號範圍
awk 'NR >= 10 && NR <= 20' file

# 正則匹配
awk '/error/' log.txt
awk '/^[0-9]/' data.txt

# 欄位條件
awk '$3 > 1000' data.txt
awk '$2 == "Alice"' data.txt
awk '$NF ~ /@/' contacts.csv   # 正則比對
```

## 動作 (Action)

### 列印

```bash
awk '{print}' file                    # 列印整行
awk '{print $1, $3}' file             # 特定欄位
awk '{printf "%-10s %5d\n", $1, $3}'  # 格式化輸出
```

### 內建函式

```bash
# 字串函式
awk '{print length($0), toupper($1)}' file
awk '{print substr($1, 1, 3)}' file

# 數學函式
awk '{print int($1), sqrt($2)}' file
awk '{sum += $3} END {print "總和:", sum}'

# 時間函式
awk 'BEGIN {print strftime("%Y-%m-%d")}'
```

### 條件與迴圈

```awk
{
    if ($3 > 1000) {
        print $1, "高薪"
    } else if ($3 > 500) {
        print $1, "中薪"
    } else {
        print $1, "低薪"
    }
}
```

## BEGIN 與 END 區塊

- **BEGIN**: 在處理任何輸入之前執行 (用於初始化)
- **END**: 在處理所有輸入之後執行 (用於彙總)

```bash
# 計算總和與平均
awk 'BEGIN {print "報告"}
     {sum += $3; count++}
     END {print "總和:", sum; print "平均:", sum/count}' data.txt

# 群組統計
awk '{dept[$2] += $3} END {for (d in dept) print d, dept[d]}' employees.txt
```

## 實戰案例

### CSV 資料處理

```bash
# 計算各部門平均薪資
cat << 'EOF' | awk -F, 'NR>1 {dept[$2]+=$3; count[$2]++} END {for (d in dept) print d, dept[d]/count[d]}'
Name,Dept,Salary
Alice,Engineering,75000
Bob,Sales,65000
Charlie,Engineering,82000
Diana,Sales,70000
EOF
```

### 日誌分析

```bash
# 每小時請求數
awk '{print substr($4, 2, 3)}' access.log | sort | uniq -c | sort -rn

# HTTP 狀態碼分布
awk '{print $9}' access.log | sort | uniq -c | sort -rn
```

### Python 實作 awk 風格處理

```python
import csv

def pyawk(text, field_sep=None, select_cols=None, conditions=None, aggregate=None):
    """Python 版 awk 風格資料處理"""
    lines = text.strip().split("\n")
    reader = csv.reader(lines, delimiter=field_sep or " ")
    results = []
    grouped = {}

    for row in reader:
        # 條件過濾
        if conditions:
            if not all(cond(row) for cond in conditions):
                continue

        # 欄位選取
        if select_cols:
            out = [row[i-1] for i in select_cols]
        else:
            out = row

        # 彙總
        if aggregate:
            key = row[aggregate["key_col"] - 1]
            val = float(row[aggregate["val_col"] - 1])
            if key not in grouped:
                grouped[key] = 0
            grouped[key] += val
        else:
            results.append(out)

    if aggregate:
        return grouped
    return results

# 使用範例
data = "A,100\nB,200\nA,150"
result = pyawk(data, field_sep=",", aggregate={"key_col": 1, "val_col": 2})
print(result)  # {'A': 250.0, 'B': 200.0}
```

---

## 延伸閱讀

- [awk 程式設計教學](https://www.google.com/search?q=awk+programming+tutorial+Linux)
- [awk 內建變數與函式](https://www.google.com/search?q=awk+builtin+variables+functions)
- [awk 資料處理實戰](https://www.google.com/search?q=awk+data+processing+examples+log+analysis)
