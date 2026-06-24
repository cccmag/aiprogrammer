# Unity 5.4 新特性

## Unity 5.4 概述

Unity 5.4 是 2016 年 7 月發布的重大更新，帶來了多項 VR 支援改進和圖形增強。

## 主要新功能

### VR 支援優化

- 原生支援 Oculus Rift 和 HTC Vive
- 減少 VR 渲染延遲
- 支援立體視圖渲染優化

### 光照系統改進

```csharp
// 新的光照模式
Light light = GetComponent<Light>();
light.mode = LightMode.Realtime;
light.intensity = 2.0f;
```

### 多執行緒渲染

```csharp
// 開啟多執行緒渲染
PlayerSettings.multiThreadedRendering = true;
```

## 圖形增強

### 即時陰影改進

- 新增陰影層級設定
- 支援軟陰影陰影級聯

### 著色器改進

- 支援著色器變體裁剪
- 改善著色器編譯時間

## 性能提升

- GPU 實例化支援
- 優化批次處理
- 減少 draw call

## 參考資料

- [Unity 5.4 發布說明](https://www.google.com/search?q=Unity+5.4+release+notes)