# 終端機與 Shell 入門

## 什麼是終端機？

終端機 (Terminal) 是與電腦互動的文字介面。在圖形化介面普及之前，終端機是使用電腦的唯一方式。今天，終端機仍然是開發者最高效的工作環境。

### 歷史演進

```
1870s: 電傳打字機 (Teletype) ── 機械式文字輸入輸出
1960s: 終端機 (VT100) ── 電子式顯示器 + 鍵盤
1970s: Unix Shell ── 命令列直譯器
1980s: xterm ── 圖形環境中的終端機模擬器
2000s: iTerm2 / GNOME Terminal ── 現代終端機
2010s: Alacritty / kitty ── GPU 加速終端機
2020s: Warp / Hyper ── AI 增強的終端機
```

### 終端機 vs Shell

很多人混淆這兩個概念：

- **終端機**: 提供文字輸入/輸出的視窗程式 (如 GNOME Terminal、iTerm2)
- **Shell**: 命令列直譯器，解譯並執行你輸入的命令 (如 Bash、Zsh、Fish)

```
你輸入命令 ──► 終端機 ──► Shell ──► 作業系統 ──► 執行結果
```

## 常見的 Shell

### Bash (Bourne Again Shell)

最廣泛使用的 Shell，是大多數 Linux 發行版的預設 Shell。Bash 是 GNU 專案的一部分，支援腳本程式設計、命令補全和歷史記錄。

### Zsh (Z Shell)

macOS 的預設 Shell (自 Catalina 起)，提供更強的主題自訂和自動補全功能。oh-my-zsh 是 Zsh 最受歡迎的設定框架。

### Fish (Friendly Interactive Shell)

以使用者友善著稱的 Shell，提供開箱即用的語法高亮和自動建議。

```bash
# 查看當前 Shell
echo $SHELL

# 切換 Shell
chsh -s /bin/zsh

# Shell 版本
bash --version
zsh --version
```

## 基本 Shell 操作

### 快捷鍵

| 快捷鍵 | 功能 |
|--------|------|
| Ctrl+C | 終止當前命令 |
| Ctrl+D | 結束輸入/登出 |
| Ctrl+Z | 暫停命令 (可恢復) |
| Ctrl+R | 反向搜尋歷史 |
| Ctrl+L | 清屏 |
| Tab | 命令/檔案名自動補全 |
| ↑/↓ | 瀏覽命令歷史 |

### 歷史記錄

```bash
history              # 顯示命令歷史
!!                   # 執行上一條命令
!100                 # 執行歷史中第 100 條命令
!$                   # 上一條命令的最後一個參數
!grep                # 執行最近的 grep 命令
```

### Python 中的 Shell 呼叫

```python
import subprocess
import shlex

# 執行 Shell 命令
result = subprocess.run(["ls", "-la"], capture_output=True, text=True)
print(result.stdout)

# 使用 Shell 管線
cmd = "ps aux | grep python | head -5"
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
print(result.stdout)

# 安全處理使用者輸入
user_input = "somefile.txt"
safe_cmd = shlex.quote(user_input)
subprocess.run(f"cat {safe_cmd}", shell=True, check=True)
```

## 選擇你的終端機

### Linux 推薦

- **GNOME Terminal**: 功能完整，整合 GNOME 桌面
- **Konsole**: KDE 桌面的終端機
- **Alacritty**: GPU 加速，設定檔驅動
- **Terminator**: 支援分割視窗

### macOS 推薦

- **iTerm2**: 功能最豐富的 macOS 終端機
- **Warp**: AI 增強的現代終端機
- **Kitty**: GPU 加速，高度可自訂

---

## 延伸閱讀

- [Unix Shell 歷史](https://www.google.com/search?q=Unix+shell+history+Bash+Zsh+Fish)
- [Bash 快捷鍵大全](https://www.google.com/search?q=Bash+keyboard+shortcuts+cheat+sheet)
- [Python subprocess 教學](https://www.google.com/search?q=Python+subprocess+module+tutorial)
