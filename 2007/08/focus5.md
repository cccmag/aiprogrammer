# 主題五：桌面 Linux 的掙扎

## 向主流邁進

儘管 Linux 在伺服器領域取得了巨大成功，但桌面 Linux 的普及率仍然偏低。2007 年，桌面 Linux 社群正在努力縮小這個差距，Ubuntu 的崛起帶來了新的希望。

## 桌面 Linux 的現況

### 2007 年的市場佔有率

```bash
# 桌面作業系統市場（估計）
Windows XP:        ~60%
Windows Vista:     ~10%
Mac OS X:          ~5%
Linux (桌面):      ~1%
其他:              ~24%

# 調查結果
- 普通消費者使用 Linux: < 1%
- 開發者使用 Linux: ~15%
- 學生使用 Linux: ~10%
```

### 主要障礙

```markdown
1. 軟體相容性
   - Microsoft Office 檔案格式差異
   - Adobe Photoshop 等專業軟體缺失
   - Windows 遊戲無法執行

2. 硬體支援
   - 顯示卡 3D 加速支援不完整
   - 指紋識別、TV 卡等特殊硬體
   - 專有驅動程式

3. 學習曲線
   - 與 Windows 不同的操作習慣
   - 命令列恐懼症
   - 疑難排解需要更多技術知識

4. 軟體生態
   - 專業軟體替代品不足
   - 遊戲選擇有限
   - iTunes 支援問題
```

## Ubuntu 的突破

### 為什麼 Ubuntu 有希望

```bash
# Ubuntu 的優勢

1. 易用性
   - 自動硬體偵測
   - 圖形化安裝程式
   - 預設軟體完整

2. 社群支援
   - 活跃的中文論壇
   - 豐富的文件
   - 免費技術支援

3. 硬體相容
   - 對新硬體支援較好
   - 簡化的驅動安裝（附加驅動程式工具）
```

### 附加驅動程式工具

```bash
# Ubuntu 附加驅動程式
System → Administration → Hardware Drivers

# 自動偵測需要專有驅動的硬體
# 常見需要驅動的硬體：
# - NVIDIA 顯示卡
# - ATI 顯示卡
# - 某些 WiFi 網卡
# - 某些印表機
```

## Wine：執行 Windows 程式

### Wine 的能力

```bash
# Wine - Wine Is Not an Emulator
# 在 Linux 上執行 Windows 程式

# 安裝
sudo apt-get install wine

# 使用
wine notepad.exe        # 執行 Windows 記事本
winecfg                 # Wine 設定
wine uninstaller        # 解除安裝程式

# CrossOver Office
# 商業化的 Wine
# 支援 Microsoft Office、Photoshop 等
```

### 可執行的軟體

```bash
# 2007 年 Wine 支援的軟體
Microsoft Office 2000/XP/2003  # 可用
Internet Explorer 6           # 可用
Photoshop CS2                 # 部分可用
Winamp                        # 良好支援
# 不支援：DirectX 遊戲（需要額外設定）
```

## 虛擬機器方案

### 執行完整的 Windows

```bash
# VMware Player
# 免費的桌面虛擬化
# 需要預先存在的 VM 映像

# VirtualBox (OSS 版本)
# Sun 的虛擬化解決方案
sudo apt-get install virtualbox-ose

# QEMU
# 開源模擬器
sudo apt-get install qemu
qemu -m 512 -cdrom windows.iso
```

## 替代軟體生態

### 辦公軟體

```bash
# OpenOffice.org 2.3
# 替代 Microsoft Office
# 完全支援 Office 格式

# 包含：
Writer      # 取代 Word
Calc        # 取代 Excel
Impress     # 取代 PowerPoint
Draw        # 取代 Visio
Base        # 取代 Access
```

### 網頁瀏覽

```bash
# Firefox 2.0
# Ubuntu 預設瀏覽器
# 與 Windows 版本相同

# Opera
# 另一選擇

# Konqueror
# KDE 內建瀏覽器
```

### 圖形處理

```bash
# GIMP 2.4
# 替代 Photoshop
# 專業級影像編輯

# Inkscape
# 替代 Illustrator
# 向量圖形編輯

# Blender
# 3D 建模和動畫
```

### 音訊和視訊

```bash
# 音訊
Rhythmbox        # 音樂播放
Audacity         # 音訊編輯
 Ardour          # DAW 數位音訊工作站

# 視訊
Totem            # 影片播放
 mencoder/ffmpeg # 影片轉檔
PiTiVi           # 視訊編輯
```

## 遊戲支援

### 開放 Source 遊戲

```bash
# Nexuiz
# 開源 FPS 遊戲

# Tremulous
# 團隊 FPS

# Wesnoth
# 回合制策略

# Planeshift
# MMORPG

# Frozen Bubble
# 彈珠射擊
```

### 遊戲平台

```bash
# Cedega
# 商業 Wine 分支
# 專注於 Windows 遊戲

# Linux Games
# Tux Games
# 預裝 Linux 遊戲的 DVD
```

## 未來希望

### 2007 年的進展

```markdown
# 正面發展：

1. Ubuntu 用戶快速增長
2. 顯示卡 3D 驅動改善
3. OpenOffice.org 格式相容性提升
4. Firefox 市佔率上升
5. 越來越多廠商提供 Linux 版軟體

# 硬體廠商開始關注：
- HP 開始銷售預裝 Ubuntu 的電腦
- Dell 提供 Ubuntu 選項
- NVIDIA 改善 Linux 驅動
```

### Linux 桌面份額變化趨勢

```
1998: ~0.1%
2000: ~0.3%
2003: ~0.5%
2005: ~0.7%
2007: ~1.0%
2009: ~1.5% (預測)
```

## 結語

桌面 Linux 的普及是一個漫長的過程。2007 年是一個重要的轉捩點，Ubuntu 的出現讓更多人開始嘗試 Linux。雖然距離主流應用還有距離，但進步是實實在在的。隨著雲端運算和 Web 應用的興起，傳統桌面作業系統的重要性可能會發生變化，這為 Linux 桌面帶來了新的機會。

---

*延伸閱讀：*
- [Ubuntu 桌面版](https://developers.google.com/search/?q=ubuntu+desktop)
- [Linux 桌面環境](https://developers.google.com/search/?q=linux+desktop+environment)