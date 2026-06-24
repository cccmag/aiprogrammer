# MVC vs MVP vs MVVM 比較

## 前言

UI 架構模式經歷了多年的演化。讓我們比較三種最常見的模式。

## MVC（Model-View-Controller）

**特點**：
- Model：商業邏輯和資料
- View：呈現和使用者介面
- Controller：協調者和請求處理

**優點**：
- 簡單直觀
- 職責分離清楚

**缺點**：
- Controller 可能變得肥大
- View 和 Model 有時會有耦合

## MVP（Model-View-Presenter）

**特點**：
- View 是被動的，只執行 Presenter 的指令
- Presenter 負責所有 UI 邏輯
- View 和 Model 完全隔離

**優點**：
- View 和 Model 完全解耦
- 易於單元測試

**缺點**：
- Presenter 可能變得複雜
- 需要雙向同步

## MVVM（Model-View-ViewModel）

**特點**：
- ViewModel 是 View 的抽象
- 雙向資料綁定
- 主要用於 WPF、XAML 技術

**優點**：
- 大幅減少 UI 程式碼
- 資料綁定自動化

**缺點**：
- 學習曲線較陡
- 資料綁定可能隱藏過多細節

## 比較表

| 特性 | MVC | MVP | MVVM |
|------|-----|-----|------|
| 複雜度 | 中 | 中 | 高 |
| 測試性 | 中 | 高 | 高 |
| 適用場景 | Web | 桌面/行動 | 響應式 UI |
| 資料綁定 | 無 | 需手動 | 自動 |

## 小結

選擇哪種模式取決於你的技術棧和團隊經驗。沒有最好的模式，只有最適合的選擇。

---

## 延伸閱讀

- [MVC vs MVP vs MVVM](https://www.google.com/search?q=MVC+vs+MVP+vs+MVVM)
- [UI Architecture Patterns](https://www.google.com/search?q=UI+architecture+patterns+comparison)