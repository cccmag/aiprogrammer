# 微軟 Silverlight 1.0：RIA 市場新競爭者

## 概述

2007 年 9 月，微軟正式發布 Silverlight 1.0，這是一個跨平台、跨瀏覽器的 Web 插件，旨在為 Web 應用提供豐富的多媒體體驗和互動功能。Silverlight 的出現，使RIA（Rich Internet Application）市場形成了 Flash/Flex、Adobe AIR 和 Silverlight 三足鼎立的局面。

## Silverlight 的設計目標

Silverlight 的核心設計目標是：

1. **豐富的視覺效果** -- 向量圖形、動畫、視訊
2. **跨平台支援** -- Windows、Mac（Linux 部分支援）
3. **開發彈性** -- XAML + .NET 程式碼
4. **與 Expression 工具整合** -- 設計師和開發者協作

## Silverlight 架構

### XAML 標記語言

XAML 是 Silverlight UI 的宣告式標記語言：

```xml
<Canvas xmlns="http://schemas.microsoft.com/client/2007"
         xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">

    <!-- 形狀和圖形 -->
    <Rectangle Width="200" Height="100"
               Fill="Blue" Stroke="Black" StrokeThickness="2"
               RadiusX="10" RadiusY="10"/>

    <Ellipse Width="150" Height="150"
             Fill="Red" Opacity="0.7"/>

    <!-- 文字 -->
    <TextBlock Text="Hello, Silverlight!"
               FontSize="24" FontFamily="Arial"
               Foreground="White"
               Canvas.Left="50" Canvas.Top="50"/>

    <!-- 按鈕 -->
    <Button Content="點擊我"
            Width="100" Height="30"
            Canvas.Left="100" Canvas.Top="200"/>
</Canvas>
```

### 事件處理

```csharp
// Silverlight 1.0 事件處理（JavaScript）
function onMouseEnter(sender, eventArgs) {
    sender.fill = new SolidColorBrush(Colors.Red);
}

function onMouseLeave(sender, eventArgs) {
    sender.fill = new SolidColorBrush(Colors.Blue);
}

// 連接事件
function onLoaded(sender, eventArgs) {
    var rect = sender.findName("myRectangle");
    rect.addEventListener("mouseenter", onMouseEnter);
    rect.addEventListener("mouseleave", onMouseLeave);
}
```

## Silverlight 的核心功能

### 向量圖形

```xml
<!-- 複雜的向量圖形 -->
<Canvas>
    <!-- 路徑 -->
    <Path Stroke="Black" StrokeThickness="2" Fill="Yellow">
        <Path.Data>
            <PathGeometry>
                <PathFigure StartPoint="0,50">
                    <BezierSegment Point1="25,0" Point2="75,100" Point3="100,50"/>
                </PathFigure>
            </PathGeometry>
        </Path.Data>
    </Path>

    <!-- 漸層 -->
    <Rectangle Width="200" Height="100" Canvas.Left="50">
        <Rectangle.Fill>
            <LinearGradientBrush StartPoint="0,0" EndPoint="1,1">
                <GradientStop Color="Blue" Offset="0"/>
                <GradientStop Color="White" Offset="1"/>
            </LinearGradientBrush>
        </Rectangle.Fill>
    </Rectangle>
</Canvas>
```

### 動畫系統

```xml
<!-- 使用 Storyboard 動畫 -->
<Canvas x:Name="layoutRoot">
    <Rectangle x:Name="animatedRect"
              Width="100" Height="100" Fill="Blue"/>

    <Canvas.Triggers>
        <EventTrigger RoutedEvent="Canvas.Loaded">
            <BeginStoryboard>
                <Storyboard>
                    <DoubleAnimation
                        Storyboard.TargetName="animatedRect"
                        Storyboard.TargetProperty="Opacity"
                        From="1.0" To="0.0" Duration="0:0:2"
                        AutoReverse="True" RepeatBehavior="Forever"/>

                    <DoubleAnimation
                        Storyboard.TargetName="animatedRect"
                        Storyboard.TargetProperty="(Canvas.Left)"
                        From="0" To="300" Duration="0:0:3"/>
                </Storyboard>
            </BeginStoryboard>
        </EventTrigger>
    </Canvas.Triggers>
</Canvas>
```

### 視訊播放

```xml
<!-- MediaElement 視訊播放 -->
<MediaElement x:Name="videoPlayer"
              Source="video.wmv"
              Width="400" Height="300"
              AutoPlay="False"
              MediaOpened="onMediaOpened"
              MediaEnded="onMediaEnded"/>

<Canvas>
    <!-- 播放控制按鈕 -->
    <Button Content="播放" Canvas.Left="10" Canvas.Top="310"
            Click="playVideo"/>
    <Button Content="暫停" Canvas.Left="60" Canvas.Top="310"
            Click="pauseVideo"/>
    <Button Content="停止" Canvas.Left="110" Canvas.Top="310"
            Click="stopVideo"/>
</Canvas>
```

```javascript
// 視訊控制 JavaScript
var media = sender.findName("videoPlayer");

function playVideo(sender, eventArgs) {
    media.play();
}

function pauseVideo(sender, eventArgs) {
    media.pause();
}

function stopVideo(sender, eventArgs) {
    media.stop();
}

function onMediaOpened(sender, eventArgs) {
    var duration = sender.findName("videoPlayer").duration;
    alert("視訊時長: " + duration + " 秒");
}
```

### 圖像和效果

```xml
<!-- 圖像和變換效果 -->
<Canvas>
    <Image Source="photo.jpg" Width="300" Height="200">
        <Image.RenderTransform>
            <TransformGroup>
                <RotateTransform Angle="15"/>
                <ScaleTransform ScaleX="1.1" ScaleY="1.1"/>
            </TransformGroup>
        </Image.RenderTransform>
        <Image.Effect>
            <DropShadowEffect Color="Black" BlurRadius="10" ShadowDepth="5"/>
        </Image.Effect>
    </Image>
</Canvas>
```

## Silverlight 與 .NET

Silverlight 使用 .NET 子集作為程式碼後端：

```csharp
// Silverlight 1.0 中的 JavaScript 互動
// 在 JavaScript 中呼叫 Silverlight 物件
var control = sender.findName("myControl");
control.MyMethod();

// C# 後端程式碼（需要 1.1 或更高版本）
public partial class Page : UserControl
{
    public Page() {
        InitializeComponent();
    }

    public void MyMethod() {
        // 處理業務邏輯
    }

    private void OnClick(object sender, EventArgs e) {
        MessageBox.Show("按鈕被點擊！");
    }
}
```

## 與 ASP.NET AJAX 整合

```html
<!-- Silverlight 和 ASP.NET AJAX 整合 -->
<asp:ScriptManager ID="ScriptManager1" runat="server"/>

<asp:UpdatePanel ID="UpdatePanel1" runat="server">
    <ContentTemplate>
        <asp:Label ID="lblStatus" runat="server" Text="等待更新..."/>
        <asp:Button ID="btnUpdate" runat="server"
                    Text="更新 Silverlight"
                    OnClick="btnUpdate_Click"/>
    </ContentTemplate>
</asp:UpdatePanel>

<!-- Silverlight 物件 -->
<object data="data:application/x-silverlight-2,"
        type="application/x-silverlight-2"
        width="400" height="300">
    <param name="source" value="MyApp.xap"/>
    <param name="onError" value="onSilverlightError"/>
</object>
```

## Silverlight 的市場定位

| 特性 | Silverlight | Flash/Flex |
|------|-------------|------------|
| 開發語言 | XAML + C#/VB | ActionScript |
| 設計工具 | Expression Blend | Flash Builder |
| 視訊支援 | WMv, VC-1 | H.264, FLV |
| .NET 整合 | 深度整合 | 有限支援 |
| 跨平台 | Windows, Mac | 全平台 |

## 應用場景

Silverlight 特別適合：
1. **企業內部應用** -- .NET 開發者友好
2. **視訊串流** -- Windows Media 支援
3. **金融應用** -- 即時資料視覺化
4. **線上遊戲** -- 豐富的圖形能力

## 結語

Silverlight 1.0 的發布，標誌著微軟正式進軍 RIA 市場。雖然 Silverlight 後來因為策略調整而停止開發，但其對視訊串流、豐富互動應用的推動，以及與 .NET 生態的深度整合，對後續 Web 技術的發展產生了深遠影響。

---

*延伸閱讀：*
- [Silverlight 官方網站](https://developers.google.com/search/?q=microsoft+silverlight+official)
- [Silverlight 文件](https://developers.google.com/search/?q=silverlight+documentation)