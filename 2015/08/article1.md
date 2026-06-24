# Shell 腳本的最佳實踐

## 前言

編寫高質量的 Shell 腳本能大幅提升工作效率並減少錯誤。

---

## 基本的最佳實踐

### 1. Shebang 與錯誤處理

```bash
#!/bin/bash
# 開頭設定
set -euo pipefail
IFS=$'\n\t'
```

為什麼要這樣設定：
- `set -e`：命令失敗時立即退出
- `set -u`：使用未定義變數時退出
- `set -o pipefail`：管線中任何命令失敗都退出
- `IFS`：正確處理檔名中的空格

### 2. 使用變數

```bash
# 好的命名
readonly CONFIG_FILE="/etc/myapp/config.yml"
readonly LOG_FILE="/var/log/myapp.log"

# 壞的命名
CF="/etc/1"
LF="/var/2"
```

### 3. 函數結構

```bash
log_info() {
    echo "[INFO] $*"
}

log_error() {
    echo "[ERROR] $*" >&2
}

cleanup() {
    log_info "清理資源..."
    # 清理邏輯
}
trap cleanup EXIT
```

---

## 錯誤處理

### 自訂錯誤函數

```bash
error_exit() {
    local line="$1"
    local message="${2:-未知錯誤}"
    echo "[行 $line] 錯誤: $message" >&2
    exit 1
}

# 使用方式
command_that_might_fail || error_exit $LINENO "命令失敗"
```

### 驗證輸入

```bash
validate_input() {
    if [[ ! "$1" =~ ^[a-zA-Z]+$ ]]; then
        echo "錯誤: 只需要字母"
        return 1
    fi
}
```

---

## 效能優化

### 字串操作

```bash
# 慢
for line in $(cat file.txt); do
    echo "$line"
done

# 快
while IFS= read -r line; do
    echo "$line"
done < file.txt
```

### 並行處理

```bash
#!/bin/bash
# 使用 & 和 wait 實現並行

for url in "${URLS[@]}"; do
    curl -s "$url" &  # 後台執行
done
wait  # 等待所有完成
```

---

## 測試

### ShellCheck

```bash
# 安裝
apt-get install shellcheck

# 使用
shellcheck myscript.sh
```

### 單元測試

```bash
#!/bin/bash
# bats (Bash Automated Testing System)

@test "加法測試" {
    result=$(add 2 3)
    [ "$result" -eq 5 ]
}
```

[搜尋 ShellScript testing best practices](https://www.google.com/search?q=ShellScript+testing+best+practices)

---

## Debug 技巧

```bash
# 方法 1: -x 追蹤執行
bash -x script.sh

# 方法 2: 在腳本中加入
set -x
# ... code ...
set +x

# 方法 3: 使用 DEBUG trap
trap 'echo "執行: $BASH_COMMAND"' DEBUG
```

---

## 常用模板

```bash
#!/bin/bash
#
# 腳本名稱: myapp.sh
# 描述: 用途描述
# 作者: 作者名稱
# 日期: 2025-01-01
#

set -euo pipefail
IFS=$'\n\t'

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*"
}

main() {
    log "開始執行"
    # 主邏輯
    log "執行完成"
}

main "$@"
```

---

## 小結

遵循這些最佳實踐能讓你的 Shell 腳本更加健壯、可維護和易於測試。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [ShellCheck 官方網站](https://www.google.com/search?q=ShellCheck+official)
- [Advanced Bash-Scripting Guide](https://www.google.com/search?q=Advanced+Bash-Scripting+Guide)