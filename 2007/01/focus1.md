# 蘋果的革命：iPhone 發表與 Macworld 2007

## 前言

2007 年 1 月 9 日，這一天在科技史上佔據了特殊的位置。在舊金山 Moscone Center 舉行的 Macworld Conference & Expo 上，Steve Jobs 向全世界展示了 iPhone——一款他稱之為「領先業界五年」的產品。

## Steve Jobs 的願景

### 三個產品的融合

在演講開始時，Jobs 先介紹了蘋果當時的三大產品線：

1. **iPod** —— 市場領導的音樂播放器
2. **手機** —— 當時市面上令人不滿意的產品
3. **網路設備** —— 筆記型電腦與網路瀏覽體驗

然後他說出了那段著名的話：

> 「Today, we are introducing three revolutionary products.」
> 「A widescreen iPod with touch controls.」
> 「A revolutionary mobile phone.」
> 「A breakthrough internet communications device.」
> 「Wait... there is ONE more thing... It's iPhone!」

這不是三個產品，而是一個完全整合的設備。

### 當時的市場背景

2007 年的手機市場：

```
┌────────────────────────────────────────────────────────┐
│              2007 年手機市場概況                        │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Nokia：全球市佔率 40%，以功能手機為主                  │
│  RIM：BlackBerry 專注企業用戶，商務市場領導者           │
│  Palm：Treo 系列，智慧型手機先驅                        │
│  Windows Mobile：Microsoft 的手機作業系統               │
│  Motorola：RAZR 薄型手機，時尚代表                     │
│                                                        │
│  特點：                                                │
│  - 物理鍵盤/按鍵                                       │
│  - 有限的功能擴展                                       │
│  - 糟糕的網頁瀏覽體驗                                   │
│  - 各自為政的應用生態                                   │
│                                                        │
└────────────────────────────────────────────────────────┘
```

Jobs 認為市面上的手機都有嚴重問題：

1. **糟糕的電話功能** —— 訊號問題、語音品質差
2. **糟糕的網頁瀏覽** —— 不是真正的網路體驗
3. **各自為政的應用** —— 沒有好的應用生態

## iPhone 的設計理念

### 硬體設計

iPhone 的硬體設計體現了蘋果的設計哲學：

```c
// iPhone 初代硬體規格
typedef struct {
    char* name = "iPhone";
    float screen_size = 3.5;  // 英吋
    int resolution_x = 320;
    int resolution_y = 480;
    char* processor = "ARM 11";
    int clock_speed = 412;  // MHz
    int ram = 128;  // MB
    int storage_choices[] = {4, 8};  // GB
    char* network = "EDGE + WiFi + Bluetooth";
    int camera = 2;  // 百萬像素
} iPhone_spec;
```

### 軟體設計

iPhone 採用了修改過的 Mac OS X 作為核心：

- **完整的 Safari 瀏覽器** —— 不是 WAP，不是修剪過的版本
- **桌面級網頁渲染** —— 與 Mac/PC 相同的瀏覽體驗
- **OS X 核心** —— 穩定可靠的Unix基礎
- **優雅的觸控介面** —— 革命性的用戶體驗

### 五個核心應用

發表會上展示的五個「殺手級應用」：

1. **電話** —— 整合的語音通訊
2. **郵件** —— 支援 Yahoo! Mail、Microsoft Exchange、Gmail
3. **Safari** —— 真正的網路瀏覽
4. **iPod** —— 觸控式的音樂體驗
5. **Widgets** —— 天氣、股票、時鐘

## 革命性的用戶介面

### 多點觸控的突破

iPhone 的介面設計徹底顛覆了傳統：

```
傳統智慧型手機：
┌─────────────────┐
│  ┌───┐ ┌───┐   │ ← 實體按鍵
│  │目錄│ │返回│   │
│  └───┘ └───┘   │
│                 │
│  ┌─────────────┐│
│  │             ││
│  │   有限螢幕   ││
│  │             ││
│  └─────────────┘│
│  123 456 789* 0#│ ← 數字鍵盤
└─────────────────┘

iPhone：
┌─────────────────┐
│                 │
│  ┌─────────────┐│
│  │             ││
│  │   全螢幕    ││
│  │   應用      ││
│  │             ││
│  └─────────────┘│
│                 │
│  隱藏式 Home 鍵  │
└─────────────────┘
```

### 滾動與操作

iPhone 引入了革命性的滾動機制：

- **手指滑動** —— 直接在內容上滑動
- **慣性捲動** —— 物理感官的延續
- **彈簧效果** —— 邊界時的自然回彈
- **下拉刷新** —— 拉下更新內容

## 發表會的深遠影響

### 業界反應

iPhone 發表後的業界反應：

| 公司 | 反應 |
|------|------|
| Apple 員工 | 興奮但保密嚴格 |
| AT&T | 成為獨家合作夥伴 |
| Nokia | 市值短暫下跌 |
| RIM | 急忙評估應對策略 |
| Google | 加速 Android 開發 |
| Microsoft | 重新評估 Windows Mobile |

### 批評與質疑

並非所有人都看好 iPhone：

> 「iPhone 沒有實體鍵盤，會有很多人不習慣。」
> 「封閉的系統會限制其發展。」
> 「$499 的價格太高了。」
> 「Steve Jobs 又在誇大其詞了。」

這些質疑在後來證明是多餘的，iPhone 掀起了行動運算的革命。

## Macworld 的歷史意義

### 最後一次 Keynote

2007 年的 Macworld 有特殊意義——這是 Steve Jobs 最後一次在 Macworld 上發表主題演講。此後蘋果決定不再參加這個展覽。

### 蘋果的轉型

Macworld 2007 標誌著蘋果公司的重大轉型：

- 從電腦公司轉型為消費電子公司
- 從軟體/硬體整合轉向更廣泛的生態系
- 從專業市場轉向大眾市場

---

## 結論

iPhone 的發表不僅是一款產品的誕生，更是整個科技產業轉捩點。它開創了智慧型手機的新時代，樹立了用戶體驗的新標準，並為後續的行動運算革命奠定了基礎。

回顧這段歷史，我們看到的不只是一款產品的成功，更是一位創辦人對未來的遠見，以及一家公司敢於顛覆自己的勇氣。

---

## 延伸閱讀

- [Steve Jobs iPhone 發表會](https://www.google.com/search?q=Steve+Jobs+iPhone+Macworld+2007)
- [iPhone 發表歷史](https://www.google.com/search?q=iPhone+announced+January+2007)
- [2007 Macworld Conference](https://www.google.com/search?q=Macworld+2007+Steve+Jobs+keynote)

---

*本篇文章為「AI 程式人雜誌 2007 年 1 月號」本期焦點系列文章。*