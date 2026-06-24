# 主題一：Ubuntu 7.10 發布

## 最友善的 Linux 發行版

2007 年 10 月，Canonical 正式發布 Ubuntu 7.10，代號「Gutsy Gibbon」。這個版本延續了 Ubuntu「讓 Linux 對每個人都可用」的理念，在易用性、功能性和效能方面都有顯著提升。

## Ubuntu 的起源

### 從 Debian 到 Ubuntu

Ubuntu 基於 Debian 發行版，但更注重使用者的即時體驗：

| 特性 | Debian | Ubuntu |
|------|--------|--------|
| 發布週期 | 不固定 | 每 6 個月 |
| 核心版本 | 保守 | 較新 |
| 預設軟體 | 精簡 | 完整 |
| 社群支援 | 論壇 | 論壇 + 商業支援 |

### Ubuntu 的設計理念

1. **每 6 個月發布新版本** -- 可預測的更新週期
2. **GNOME 桌面環境** -- 現代化的使用者介面
3. **單一使用者體驗** -- 預設配置最佳化
4. **社群和商業結合** -- Canonical 提供企業支援

## Ubuntu 7.10 的新特性

### Compiz Fusion 桌面特效

Ubuntu 7.10 預設啟用了 Compiz Fusion，帶來華麗的 3D 桌面效果：

```bash
# 啟動 Compiz Fusion
System → Preferences → Appearance → Visual Effects

# 手動啟動
compiz --replace &
```

特效包括：
- 立方體旋轉桌面
- 視窗燃燒效果
- 縮放視圖
- 半透明視窗
- 晃動以聚焦

### 簡化的網路設定

Ubuntu 7.10 簡化了網路設定流程：

```bash
# 圖形化網路管理
System → Administration → Network

# 有線網路自動偵測
# 支援 DHCP 自動設定
# VPN 支援更簡單
```

### 快速使用者切換

```bash
# 使用 GDM 快速切換使用者
# System → Log Out → Switch User
# 或使用快速鍵：Ctrl + Alt + F7-F8
```

## Ubuntu 的軟體生態

### 預設軟體

Ubuntu 7.10 預設安裝了完整的辦公和娛樂軟體：

| 類別 | 軟體 |
|------|------|
| 辦公室 | OpenOffice.org 2.3 |
| 網頁瀏覽 | Firefox 2.0 |
| 電子郵件 | Evolution |
| 即時通訊 | Pidgin |
| 影像處理 | F-Spot |
| 音樂 | Rhythmbox |
| 影片 | Totem |
| 圖形處理 | GIMP 2.4 |

### 軟體安裝

```bash
# 使用 Synaptic 套件管理員
sudo synaptic

# 命令列安裝
sudo apt-get install package-name

# 新立得搜尋和安裝
# 1. 搜尋關鍵字
# 2. 標記安裝
# 3. 套用變更
```

### Add/Remove Applications

Ubuntu 7.10 提供了圖形化的軟體安裝工具：

```
Applications → Add/Remove...
# 類別瀏覽
# 熱門軟體
# 最近使用
# 軟體更新
```

## Ubuntu 的社群

### 文件和支援

```bash
# 內建說明系統
System → Help and Support

# 社群文件
https://help.ubuntu.com/

# 論壇
https://ubuntuforums.org/
```

### 翻譯和在地化

Ubuntu 支援 40+ 種語言，包括正體中文：

```bash
# 系統語言設定
System → Administration → Language Support

# 安裝語言包
sudo apt-get install language-pack-gnome-zh
```

## Ubuntu 的變種

Ubuntu 社群衍生出多個官方認可的變種：

| 版本 | 桌面環境 | 特色 |
|------|----------|------|
| Kubuntu | KDE | KDE 桌面 |
| Xubuntu | XFCE | 輕量級 |
| Edubuntu | 教育軟體 | 教育用途 |
| Ubuntu Server | 無桌面 | 伺服器最佳化 |
| Ubuntu Studio | 音訊/視訊 | 多媒體創作 |

## 技術規格

### 系統需求

```
最低需求：
- 700 MHz x86 處理器
- 384 MB 記憶體
- 8 GB 硬碟空間
- 繪圖卡支援 800x600

建議需求：
- 1 GHz x86 處理器
- 512 MB 記憶體
- 15 GB 硬碟空間
- 繪圖卡支援 1024x768
```

### 預設核心

Ubuntu 7.10 使用 Linux 核心 2.6.22，支援：
- Ext4 檔案系統（可選）
- UUID 開機
- 最新硬體支援

## 結語

Ubuntu 7.10 代表了桌面 Linux 的一個重要里程碑。透過 Compiz Fusion 的華麗視覺效果、直覺的軟體管理和持續改善的硬體支援，Ubuntu 正在一步步實現「讓 Linux 走進千家萬戶」的願景。

---

*延伸閱讀：*
- [Ubuntu 官方網站](https://developers.google.com/search/?q=ubuntu+official+website)
- [Ubuntu 文件](https://developers.google.com/search/?q=ubuntu+documentation)