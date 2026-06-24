# 觸控介面的演進：多點觸控技術的歷史

## 前言

iPhone 最令人驚艷的特性之一就是多點觸控螢幕。但這項技術並非蘋果發明，而是數十年研究的結晶。讓我們回顧多點觸控技術的發展歷程。

## 觸控技術的早期歷史

### 1960 年代：觸控技術的發明

觸控螢幕的概念可以追溯到 1960 年代：

```
┌────────────────────────────────────────────────────────┐
│              觸控技術發展時間線                          │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1965：E.A. Johnson 發明第一個觸控螢幕                   │
│  └─ 用途：英國航空交通管制系統                          │
│                                                        │
│  1970：IBM 開發了觸控式資料輸入系統                     │
│                                                        │
│  1972：PLATO IV 系統使用電阻式觸控                      │
│  └─ 最早的電腦輔助教學系統                              │
│                                                        │
│  1982：多點觸控專利首次出現                             │
│                                                        │
│  1984：Casio 發表觸控式計算器                           │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### 電阻式觸控技術

最早的消費級觸控技術是電阻式：

```python
# 電阻式觸控原理
"""
原理：兩層導電膜之間有空隙，觸控時導電膜接觸

結構：
┌─────────────────┐
│ 上層導電膜      │ ─── ITO（氧化銦錫）
├─────────────────┤
│ 空隙            │ ─── 2-5 微米
├─────────────────┤
│ 下層導電膜      │ ─── ITO
└─────────────────┘

電壓分壓原理：
Vout = Vref × (R1 / (R1 + R2))
"""
```

**電阻式的特點：**
- 結構簡單，成本低廉
- 可以用任何物體觸控（手指、觸控筆、手套）
- 無法實現真正的多點觸控
- 螢幕透光度較低（約 75%）

## 多點觸控的發明

### 1982 年的突破

1982 年，位於多倫多的 University of Toronto 的 Nimish Mehta 展示了第一個多點觸控系統：

```
┌────────────────────────────────────────────────────────┐
│     早期多點觸控實驗                                    │
├────────────────────────────────────────────────────────┤
│                                                        │
│  發明者：Nimish Mehta                                  │
│  地點：University of Toronto                          │
│  技術：紅外線矩陣觸控                                   │
│  應用：電容式表面觸控                                   │
│                                                        │
│  這是一個「觸控面積追蹤」系統                           │
│  可以追蹤多個觸控點的位置                               │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### 1990 年代：室內追蹤系統

1990 年代，觸控牆和互動桌面開始出現：

- **FTIR（Frustrated Total Internal Reflection）**
  - 光纖技術檢測手指接觸
  - 可以追蹤大量觸控點
  - 典型應用：互動式桌子

- **DiamondTouch**
  - Mitsubishi Electric Research Laboratories (MERL)
  - 座椅墊感應多人觸控
  - 支援多人同時使用

### 2000 年代：觸控介面的成熟

```
┌────────────────────────────────────────────────────────┐
│           多點觸控技術成熟期                            │
├────────────────────────────────────────────────────────┤
│                                                        │
│  2001：Buxton 發表白板互動系統                         │
│                                                        │
│  2005：Apple 秘密收購 FingerWorks                      │
│  └─ 取得多點觸控技術專利                               │
│  └─ 將技術整合到 iPhone                               │
│                                                        │
│  2006：Microsoft Surface 原型展示                      │
│  └─ 互動式觸控桌面                                     │
│                                                        │
│  2007：iPhone 發表                                    │
│  └─ 多點觸控進入消費市場                               │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## Apple 與 FingerWorks

### 收購背景

2005 年，Apple 收購了 FingerWorks，這是一家由 Wayne Westerman 和 John Elias 創辦的公司，專注於多點觸控技術。

### FingerWorks 的技術

FingerWorks 開發了多種創新的觸控手勢：

```python
# FingerWorks 的手勢專利技術
"""
1. 手指姿態識別
   - 單指、雙指、三指姿勢
   - 手指方向判斷

2. 多指手勢
   - 旋轉（雙指旋轉）
   - 縮放（雙指捏合）
   - 滾動（邊緣滑動）

3. 模擬鍵盤
   - 虛擬qwerty鍵盤
   - 動態調整按鍵大小
"""
```

這些技術後來成為 iPhone 介面的核心。

## iPhone 的觸控介面設計

### 觸控螢幕硬體

iPhone 使用投射式電容觸控（Projected Capacitive Touch）：

```
┌────────────────────────────────────────────────────────┐
│         投射式電容觸控結構                              │
├────────────────────────────────────────────────────────┤
│                                                        │
│  保護層（康寧大金猩猩玻璃）                             │
│       ↓                                               │
│  發送電極（透明導電層 Tx）                             │
│       ↓                                               │
│  絕緣層                                               │
│       ↓                                               │
│  接收電極（透明導電層 Rx）                             │
│       ↓                                               │
│  LCD 顯示層                                           │
│                                                        │
│  感測原理：測量 Rx 接收到的電荷變化                     │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### 手勢操作矩陣

iPhone 的手勢識別可以總結為：

| 手指數 | 手勢類型 | 操作效果 |
|--------|----------|----------|
| 1 | 點擊 | 選擇/確認 |
| 1 | 滑動 | 捲動/導航 |
| 1 | 長按 | 選單/預覽 |
| 2 | 滑動 | 頁面切換 |
| 2 | 捏合 | 縮放 |
| 2 | 旋轉 | 旋轉圖片 |
| 3 | 滑動 | 自定義動作 |

### 手勢辨識流程

```python
# iPhone 手勢辨識流程
class iPhoneGestureRecognizer:
    def __init__(self):
        self.touch_tracker = TouchTracker()
        self.gesture_patterns = {
            'tap': self._is_tap,
            'double_tap': self._is_double_tap,
            'swipe': self._is_swipe,
            'pinch': self._is_pinch,
            'rotation': self._is_rotation
        }

    def process_touches(self, touch_events):
        """處理觸控事件序列"""
        tracked_touches = self.touch_tracker.update(touch_events)

        for pattern_name, pattern_func in self.gesture_patterns.items():
            if pattern_func(tracked_touches):
                return pattern_name

        return None

    def _is_tap(self, touches):
        """點擊：一個觸控點，時間短，距離小"""
        if len(touches) != 1:
            return False
        touch = touches[0]
        duration = touch.end_time - touch.start_time
        distance = touch.total_movement
        return duration < 0.2 and distance < 10

    def _is_pinch(self, touches):
        """捏合：兩個觸控點，距離變化顯著"""
        if len(touches) != 2:
            return False
        initial_dist = touches[0].initial_distance_to(touches[1])
        current_dist = touches[0].current_distance_to(touches[1])
        return abs(current_dist - initial_dist) > 30
```

## 多點觸控的影響

### UI 設計革命

多點觸控徹底改變了 UI 設計：

```
傳統 UI ─────────────────────────────────────────────→ 觸控 UI
─────────────────────────────────────────────────────────────
│                                                       │
│  滑鼠指標                                              │
│  精確點擊                                              │
│  右鍵選單                                              │
│  拖放操作                                              │
│                                                       │
│          →                     →                      │
│                                                       │
│  手指觸控                                              │
│  手勢操作                                              │
│  直接操作                                              │
│  多點互動                                              │
│                                                       │
└─────────────────────────────────────────────────────────────
```

### 新型態應用

多點觸控催生了新型態的應用：

- **影像處理** —— 直接用手指旋轉、縮放照片
- **地圖應用** —— 雙指縮放、旋轉地圖
- **音樂應用** —— 用手勢控制播放
- **遊戲** —— 體感遊戲、派對遊戲

## 結論

觸控技術經歷了半個世紀的發展。從實驗室的原型到消費級產品，多點觸控的普及改變了我們與數位裝置的互動方式。

iPhone 的成功不僅是因為蘋果的設計能力，更是站在巨人肩膀上的結果。從 1960 年代的發明，到 1980 年代的實驗，再到 2000 年代的成熟，每一次進步都為這場觸控革命貢獻了力量。

---

## 延伸閱讀

- [多點觸控歷史](https://www.google.com/search?q=history+of+multitouch+touchscreen)
- [FingerWorks 收購](https://www.google.com/search?q=Apple+FingerWorks+acquisition)
- [投射式電容觸控原理](https://www.google.com/search?q=projected+capacitive+touch+technology)
- [Nimish Mehta 多點觸控](https://www.google.com/search?q=Nimish+Mehta+multitouch+University+Toronto)

---

*本篇文章為「AI 程式人雜誌 2007 年 1 月號」本期焦點系列文章。*