# 智慧型手機的崛起：從 PDA 到智慧型手機

## 前言

在 iPhone 橫空出世之前，智慧型手機的概念已經醞釀了十多年。從早期的 PDA 到具備電話功能的智慧型裝置，這條發展脈絡為 iPhone 的革命奠定了基礎。

## PDA 的黃金時代

### Palm Pilot 的崛起

1996 年，Palm Computing 推出了 Palm Pilot，這款裝置徹底改變了個人數位助理的概念：

```
┌────────────────────────────────────────────────────────┐
│                    Palm Pilot  Timeline                │
├────────────────────────────────────────────────────────┤
│  1996：Palm Pilot 1000/5000 —— 入門級 PDA             │
│  1999：Palm IIIx —— 加入紅外線、RAM 擴充               │
│  1999：Palm V —— 金屬機身，設計典範                     │
│  2000：Palm m500 —— SD 卡支援                         │
│  2001：Palm Tungsten T —— 彩色螢幕、手寫辨識           │
│  2002：Palm OS 5 —— ARM 處理器、多工支援               │
│                                                        │
│  市場定位：                                           │
│  - 專業人士的首選                                      │
│  - 手寫辨識（Graffiti）                                │
│  - HotSync 同步技術                                    │
└────────────────────────────────────────────────────────┘
```

### Windows Mobile 的興起

Microsoft 在 2000 年推出了 Pocket PC 作業系統，後來更名為 Windows Mobile：

```csharp
// Windows Mobile 典型應用結構
public class SmartDeviceExample
{
    // 行事曆整合
    public void SyncCalendar()
    {
        // Exchange Server 同步
    }

    // 電話功能
    public void MakeCall(string number)
    {
        // TAPI 整合
    }

    // GPS 定位
    public void GetLocation()
    {
        // GPS Intermediate Driver
    }
}
```

Windows Mobile 的特色：

- **完整 Office 支援** —— Word、Excel、Outlook
- **觸控筆操作** —— 螢幕觸控與手寫
- **桌面同步** —— 與 Windows 無縫整合

## 智慧型手機的誕生

### Nokia 與 Symbian

Nokia 在 1996 年推出了 Nokia 9000 Communicator，這是第一批具備完整網頁瀏覽和電子郵件功能的行動裝置：

```
┌────────────────────────────────────────────────────────┐
│              Nokia Communicator 系列                    │
├────────────────────────────────────────────────────────┤
│  1996：9000 —— 喱妹姊妹、QWERTY 鍵盤                    │
│  1999：9110 —— 更輕薄、無線網卡支援                     │
│  2001：9210 —— 彩色螢幕、HTML 郵件                     │
│  2005：N80 —— 320萬像素、WiFi                         │
│  2007：N95 —— GPS、智慧型功能                         │
└────────────────────────────────────────────────────────┘
```

Symbian 作業系統的特點：

- **多工支援** —— 早期智慧型手機的多工能力
- **豐富的 API** —— 電話、訊息、檔案系統
- **Java ME 支援** —— 第三方應用開發

### BlackBerry 與 RIM

Research In Motion（RIM）公司的 BlackBerry 系列在企業市場佔據統治地位：

```
BlackBerry 的核心賣點：
┌────────────────────────────────────────────────────────┐
│                                                        │
│  1. Push Email —— 即時郵件推送，業界領先              │
│                                                        │
│  2. QWERTY 鍵盤 —— 快速輸入，專業形象                   │
│                                                        │
│  3. 安全性 —— 軍事級加密，企業青睞                    │
│                                                        │
│  4. BBM —— 免費的裝置間訊息                            │
│                                                        │
│  5. Enterprise Server —— 完整的企業管理解決方案        │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 智慧型手機的技術規格比較

### 2007 年主要智慧型手機

| 型號 | 系統 | 處理器 | 記憶體 | 螢幕 | 特點 |
|------|------|--------|--------|------|------|
| Nokia N95 | Symbian | 332MHz | 64MB | 2.6" QVGA | GPS、500萬像素 |
| BlackBerry 8800 | BlackBerry OS | 312MHz | 64MB | 2.5" QVGA | QWERTY、軌跡球 |
| Palm Treo 750 | Windows Mobile | 400MHz | 64MB | 2.5" QVGA | 觸控筆、QWERTY |
| HTC TyTN II | Windows Mobile | 400MHz | 128MB | 2.8" QVGA | 側滑鍵盤、3G |
| iPhone | iPhone OS | 412MHz | 128MB | 3.5" 320x480 | 多點觸控、WiFi |

## 智慧型手機的軟體生態

### Java ME 平台

大多數非 iPhone 智慧型手機都支援 Java ME：

```java
// Java ME 應用程式範例
import javax.microedition.lcdui.*;
import javax.microedition.midlet.*;

public class SmartPhoneApp extends MIDlet {
    private Display display;

    public void startApp() {
        display = Display.getDisplay(this);
        Form mainForm = new Form("智慧型手機");
        mainForm.append(new StringItem("版本:", "Java ME"));
        display.setCurrent(mainForm);
    }

    public void pauseApp() {}

    public void destroyApp(boolean unconditional) {}
}
```

### 應用商店的先驅

在 App Store 之前，已有一些行動應用下載服務：

- **Palm Software Store** —— Palm 應用市集
- **BlackBerry App World**（2009年上線）
- **Handango** —— 第三方應用市集
- **GetJar** —— 跨平台應用下載

## 市場與使用者

### 智慧型手機的目標用戶

2007 年初的智慧型手機用戶特徵：

```
┌────────────────────────────────────────────────────────┐
│            智慧型手機用戶分布（2007年初）                │
├────────────────────────────────────────────────────────┤
│                                                        │
│  商務人士 ─────────────────────────────────── 45%     │
│  └─ BlackBerry、Nokia E 系列                       │
│                                                        │
│  科技愛好者 ────────────────────────────────── 25%     │
│  └─ 早期採用者、程式設計師                        │
│                                                        │
│  專業人士 ─────────────────────────────────── 20%     │
│  └─ 醫生、律師、會計師                            │
│                                                        │
│  學生族群 ─────────────────────────────────── 10%     │
│  └─ Pocket PC、Windows Mobile                    │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### 智慧型手機的局限性

iPhone 發表前，智慧型手機面臨的問題：

1. **複雜的使用者介面** —— 需要觸控筆和學習
2. **有限的網頁體驗** —— 不是真正的網頁瀏覽
3. **分散的應用生態** —— 缺乏統一平台
4. **昂貴的價格** —— 企業採購為主
5. **糟糕的多媒體體驗** —— 音樂、影片功能有限

## 過渡時期的掙扎

### Palm 的衰落

Palm 在 2000 年代中期開始衰落：

- 作業系統過時
- 硬體創新不足
- 開發者生態薄弱
- 最終被 HP 收購

### Microsoft 的困境

Windows Mobile 在智慧型手機市場一直處於尷尬位置：

- 過於複雜的介面
- 缺乏消費者吸引力
- 對硬體廠商的控制不足
- 最終被 Windows Phone 取代

### Nokia 的傲慢

Nokia 作為市場領導者，面臨創新者的困境：

- 過度依賴 Symbian
- 對觸控趨勢反應遲緩
- 軟體生態建設不足
- 最終失去市場地位

---

## 結論

智慧型手機的崛起是一個漫長的演進過程。從 Palm 的 PDA 技術，到 Nokia 的Communicator，再到 BlackBerry 的企業市場，每個先驅都為這個市場的成熟做出了貢獻。

然而，這些先驅者都有共同的局限性：複雜的介面、有限的網頁體驗、和分散的應用生態。正是這些問題，為 iPhone 的革命性突破提供了舞台。

---

## 延伸閱讀

- [Palm Pilot 歷史](https://www.google.com/search?q=Palm+Pilot+history+PDA)
- [BlackBerry 發展歷史](https://www.google.com/search?q=BlackBerry+history+RIM)
- [Nokia Communicator 系列](https://www.google.com/search?q=Nokia+Communicator+history)
- [Windows Mobile 發展](https://www.google.com/search?q=Windows+Mobile+history)

---

*本篇文章為「AI 程式人雜誌 2007 年 1 月號」本期焦點系列文章。*