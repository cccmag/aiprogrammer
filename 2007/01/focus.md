# 本期焦點

## iPhone 與智慧型手機時代的來臨

### 引言

2007 年 1 月 9 日，在舊金山 Macworld Conference & Expo 的舞台上，Steve Jobs 從口袋中掏出了一台改變世界的裝置——iPhone。這一刻不僅是蘋果公司的重要里程碑，更是整個科技產業的轉捩點。

在接下來的章節中，我們將深入探討這場革命的各個層面。從 iPhone 的誕生背景，到智慧型手機的技術演進；從觸控介面的設計理念，到行動網路的基礎建設；從 App Store 商業模式的創新，到 Google Android 的崛起。我們將完整呈現這段改變人類數位生活的重要歷史。

---

## 大綱

* [程式：觸控介面與手勢辨識實作](focus_code.md)
   - iPhone 觸控技術解析
   - 手勢辨識原理
   - 多點觸控 Python 模擬

1. [蘋果的革命：iPhone 發表與 Macworld 2007](focus1.md)
   - Steve Jobs 的願景
   - iPhone 的設計理念
   - 三個產品的融合

2. [智慧型手機的崛起：從 PDA 到智慧型手機](focus2.md)
   - Palm 與 Windows Mobile
   - Nokia 的 Symbian 王朝
   - RIM 與 BlackBerry

3. [觸控介面的演進：多點觸控技術的歷史](focus3.md)
   - 多點觸控的發明
   - iPhone 的介面設計
   - 手勢操作革命

4. [行動網路的變革：3G 與行動上網時代](focus4.md)
   - EDGE、HSDPA、3G
   - WiFi 與行動網路
   - Mobile Web 的興起

5. [App Store 商業模式：軟體生態系的革命](focus5.md)
   - iPhone SDK 發布
   - App Store 誕生
   - 行動應用生態系

6. [Android 的誕生：Google 進軍手機市場](focus6.md)
   - Android 計畫啟動
   - Open Handset Alliance
   - 開放 vs 封閉之爭

7. [未來展望：智慧型手機的下一個十年](focus7.md)
   - 雲端與本機整合
   - AI 與語音助理
   - 物聯網的樞紐

---

## 濃縮回顧

### iPhone 的誕生

2007 年 1 月 9 日，Steve Jobs 在 Macworld 大會上發表了 iPhone：

```
"Today, we are introducing three revolutionary products."

1. A widescreen iPod with touch controls
2. A revolutionary mobile phone
3. A breakthrough internet communications device"

"Wait... there is ONE more thing... It's iPhone!"
```

iPhone 的四大創新：

1. **多點觸控介面**：完全顛覆傳統手機操作方式
2. **整合裝置**：手機 + iPod + 網路設備
3. **Mobile Safari**：完整網頁瀏覽體驗
4. **智慧型軟體**：OS X 核心的嵌入式系統

### 技術規格

```
┌─────────────────────────────────────────┐
│           iPhone 初代規格               │
├─────────────────────────────────────────┤
│  螢幕：3.5 吋 320x480 多點觸控          │
│  處理器：ARM 11 412MHz                  │
│  記憶體：128MB RAM                       │
│  儲存：4GB/8GB                           │
│  網路：EDGE + WiFi + Bluetooth          │
│  相機：200 萬像素（無影片）              │
│  系統：iPhone OS（後來稱 iOS）          │
│  發售日：2007 年 6 月 29 日             │
│  定價：$499/$599（綁約）                │
└─────────────────────────────────────────┘
```

### 市場影響

iPhone 的發表對整個產業造成巨大衝擊：

- **電信業**：AT&T 成為美國獨家合作夥伴
- **手機製造業**：Nokia、RIM、Samsung 股價下跌
- **軟體業**：預示著行動應用時代的來臨
- **網路業**：Mobile Web 使用量預期大增

---

## 觸控技術的革命

### 傳統 vs 觸控介面

```
傳統按鍵介面：
┌───────────────────┐
│  ┌─┐              │
│  │▲│  方向鍵     │
│  └─┘              │
│ ┌───┐             │
│ │ ○ │  確認鍵     │
│ └───┘             │
│                   │
│  1   2   3        │
│  4   5   6        │
│  7   8   9        │
│  *   0   #        │
└───────────────────┘

觸控介面：
┌───────────────────┐
│ ┌─────────────────┐│
│ │                 ││
│ │   全螢幕顯示    ││
│ │                 ││
│ │                 ││
│ │                 ││
│ └─────────────────┘│
│                   │
│  隱藏式按鍵區域   │
└───────────────────┘
```

### 多點觸控手勢

iPhone 引入的手勢操作：

| 手勢 | 動作 | 用途 |
|------|------|------|
| 點擊 | 輕觸一下 | 選擇/確認 |
| 滑動 | 水平/垂直滑動 | 捲動/換頁 |
| 雙擊 | 連續點擊兩下 | 縮放 |
| 捏合 | 兩指靠近/分開 | 縮放 |
| 長按 | 按住不放 | 選單/拖曳 |

---

## Mobile Web 的興起

### iPhone 對網路的影響

iPhone 的 Mobile Safari 是第一個完整支援桌面級網頁的行動瀏覽器：

- **完整 HTML 支援**：與桌面瀏覽器相同
- **CSS 支援**：完整的樣式表支援
- **JavaScript**：完整腳本支援
- **快取機制**：離線瀏覽支援

### WebKit 的崛起

iPhone 使用的 WebKit 渲染引擎後來成為行動瀏覽器的標準：

```
WebKit 家族：
├── Safari（macOS/iOS）
├── Chrome（Android/桌面）
├── Opera Mobile
└── 許多第三方瀏覽器
```

---

## 結論與展望

iPhone 的發表開啟了智慧型手機時代的序幕。這場革命不僅改變了我們使用手機的方式，更深刻影響了軟體開發、網路服務和數位媒體的發展方向。

從觸控介面到 App Store，從 Mobile Web 到雲端服務，iPhone 為未來十年的科技發展奠定了基礎。儘管當時批評者質疑其封閉性，但不可否認的是，這款產品為數百萬人帶來了前所未有的科技體驗。

在接下來的日子裡，智慧型手機將繼續演進，成為連接人與數位世界的最重要的裝置。

---

## 延伸閱讀

- [蘋果的革命：iPhone 發表](focus1.md)
- [智慧型手機的崛起](focus2.md)
- [觸控介面的演進](focus3.md)
- [行動網路的變革](focus4.md)
- [App Store 商業模式](focus5.md)
- [Android 的誕生](focus6.md)
- [未來展望](focus7.md)

---

*本期焦點到此結束。下期我們將探討 Web 2.0 與互聯網的發展，敬請期待。*