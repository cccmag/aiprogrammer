# 微軟 Windows 7 觸控優化

## Windows 7 觸控功能

Windows 7 在 2009 年 10 月發布，2010 年 1 月已獲得廣泛採用。它是微軟首次大幅強化觸控支援的作業系統。

```
Windows 7 觸控功能：
──────────────────
多點觸控：   支援多指操作
手勢支援：   捏合縮放、滑動翻頁
虛擬鍵盤：   螢幕點字鍵盤
觸控優化：   常用功能觸控化
API 支援：   WinRT 觸控 API
```

## 觸控 API

### 基本觸控訊息

```cpp
// Windows 觸控訊息處理
case WM_TOUCH:
{
    UINT cInputs = LOWORD(wParam);
    TOUCHINPUT* pTouchInput = (TOUCHINPUT*)lParam;

    for (UINT i = 0; i < cInputs; i++) {
        TOUCHINPUT ti = pTouchInput[i];

        if (ti.dwFlags & TOUCHEVENTF_DOWN) {
            // 觸控按下
            int x = GET_X_LPARAM(ti.dwLocation);
            int y = GET_Y_LPARAM(ti.dwLocation);
        }

        if (ti.dwFlags & TOUCHEVENTF_MOVE) {
            // 觸控移動
        }

        if (ti.dwFlags & TOUCHEVENTF_UP) {
            // 觸控釋放
        }
    }
}
```

### 啟用觸控

```cpp
// 啟用視窗觸控
BOOL EnableTouchWindow(HWND hwnd, ULONG ulFlags);

// 註冊 Touch Window
RegisterTouchWindow(hwnd, 0);
```

## 觸控手勢支援

### 手勢訊息

```cpp
// WM_GESTURE 訊息處理
case WM_GESTURE:
{
    GESTUREINFO gi;
    gi.cbSize = sizeof(GESTUREINFO);

    if (GetGestureInfo((HGESTUREINFO)lParam, &gi)) {
        switch (gi.dwID) {
            case GID_ZOOM:
                // 縮放
                double scale = (double)gi.ullArguments / 100.0;
                break;

            case GID_PAN:
                // 拖曳
                break;

            case GID_ROTATE:
                // 旋轉
                break;

            case GID_TWOFINGERTAP:
                // 雙擊
                break;

            case GID_PRESSANDTAP:
                // 按住後點擊
                break;
        }
    }
}
```

### 手勢識別

```
Windows 7 支援的手勢：
──────────────────────
GID_PAN：          單指拖曳
GID_ZOOM：         雙指縮放
GID_ROTATE：       雙指旋轉
GID_TWOFINGERTAP： 雙擊
GID_PRESSANDTAP：  按住+點擊
GID_PRESSANDDRAG： 按住+拖曳
GID_LONGPRESS：    長按
```

## UI 觸控優化

### Windows Touch 觸控 API

```cpp
// 手指追蹤
typedef struct tagTOUCHINPUT {
    DWORD dwID;
    DWORD dwTarget;
    DWORD dwFlags;
    DWORD dwMask;
    DWORD dwTime;
    ULONG_PTR dwExtraInfo;
    POINT ptLocation;
} TOUCHINPUT, *PTOUCHINPUT;

// 觸控筆支援
typedef struct tagPEN_DATA {
    DWORD dwPenID;
    DWORD dwPenFlags;
    DWORD dwPenMask;
    POINT ptLocation;
    LONG pressure;
} PEN_DATA, *PPEN_DATA;
```

### Touch-Friendly UI 設計

```
觸控 UI 設計原則：
──────────────────
按鈕大小：     至少 40x40 像素
間距：        足夠的點擊間距
圖示：        夠大且易識別
文字：        足夠大小（14pt 以上）
滾動：        支援觸控滑動
```

## 應用程式觸控化

### 範例：圖片檢視器

```cpp
// 圖片檢視器觸控支援
void CImageViewer::OnZoomGesture(double scale) {
    m_scale *= scale;
    InvalidateRect(NULL, TRUE);
}

void CImageViewer::OnPanGesture(int dx, int dy) {
    m_offsetX += dx;
    m_offsetY += dy;
    InvalidateRect(NULL, TRUE);
}
```

### 觸控相容層

```
Windows 7 觸控相容性：
───────────────────
單點觸控：     完全支援
多點觸控：     部分支援
舊應用程式：   自動相容（單點）
需要更新：     充分利用多點觸控
```

## Windows Touch 硬體

### 支援的觸控螢幕

```
Windows 7 觸控硬體（2010年）：
───────────────────────────────
觸控一體機：   HP TouchSmart、Dell XPS One
觸控螢幕：     華碩、三星、星評
平板電腦：     支援 Windows 7 的 Tablet PC
多點觸控：     大多數新觸控螢幕
```

### 驅動程式支援

```
觸控驅動支援：
──────────────────
MTouch：       單點觸控（傳統）
TouchPack：    多點觸控
WM_TOUCH：     新的統一 API
WM_GESTURE：   手勢識別
```

## .NET 中的觸控支援

### WPF 觸控

```csharp
// WPF 觸控支援
public class TouchCanvas : Canvas
{
    public TouchCanvas() {
        // 啟用觸控
        this.TouchDown += OnTouchDown;
        this.TouchMove += OnTouchMove;
        this.TouchUp += OnTouchUp;
    }

    private void OnTouchDown(object sender, TouchEventArgs e) {
        TouchPoint tp = e.GetTouchPoint(this);
        // 處理觸控按下
    }

    private void OnTouchMove(object sender, TouchEventArgs e) {
        // 處理觸控移動
    }

    private void OnTouchUp(object sender, TouchEventArgs e) {
        // 處理觸控釋放
    }
}
```

### Silverlight 觸控

```csharp
// Silverlight 觸控
public partial class MainPage : UserControl
{
    public MainPage() {
        InitializeComponent();
        this.Touch.FrameReported += OnTouchFrameReported;
    }

    private void OnTouchFrameReported(object sender, TouchFrameEventArgs e) {
        TouchPoint primary = e.GetPrimaryTouchPoint(this);

        if (primary.Action == TouchAction.Down) {
            // 開始拖曳
        }
        else if (primary.Action == TouchAction.Move) {
            // 拖曳中
        }
        else if (primary.Action == TouchAction.Up) {
            // 結束拖曳
        }
    }
}
```

## 觸控與傳統輸入的共存

### 輸入管理

```
多輸入方式共存：
──────────────────
觸控：         直覺但粗略
滑鼠：         精確
觸控筆：       中間值
鍵盤：         文字輸入
```

### 自動偵測

```cpp
// 偵測輸入類型
BOOL IsTouchDevice() {
    return GetSystemMetrics(SM_DIGITIZER) & NID_INTEGRATED_TOUCH;
}
```

---

## 結論

Windows 7 是微軟對觸控時代的重要回應。雖然當時平板電腦尚未普及，但 Windows 7 為日後的觸控應用奠定了基礎。

Windows 7 的觸控 API 讓開發者能夠建立支援多點觸控的應用程式，也為後續 Windows 8/10 的全面觸控化做好了準備。

---

*本期文章到此結束。*