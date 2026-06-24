# 程式碼文件 — Flutter 核心機制模擬

## 概述

`_code/flutter_demo.js` 是一個使用 Node.js 撰寫的模擬程式，旨在展示 Flutter 框架的核心設計理念，包含：

- Widget 樹的建置與組合
- StatefulWidget 的生命週期管理
- Provider 狀態管理模式
- Navigator 路由導航機制

## 執行方式

```bash
cd _code
bash test.sh
```

或直接執行：

```bash
node _code/flutter_demo.js
```

## 架構說明

### Widget 系統

`Widget` 為基底類別，所有 Widget 須實作 `build()` 方法。支援的 Widget 包括：

| Widget | 說明 |
|--------|------|
| Text | 文字顯示 |
| Column | 垂直排列 |
| Row | 水平排列 |
| Center | 居中佈局 |
| Padding | 內邊距 |
| ElevatedButton | 按鈕 |
| Scaffold | 頁面骨架 |

### 狀態管理

`Provider` 使用全域容器儲存共享狀態，搭配 `ChangeNotifier` 實作觀察者模式。`TodoModel` 示範了待辦事項的增刪與狀態變更通知。

### 路由導航

`Navigator` 模擬 Flutter 的導航棧，支援 `push()`、`pop()`、`current()` 等操作。

## 輸出範例

執行程式後會依序輸出：

1. Provider 狀態變更日誌
2. Widget 樹的 JSON 結構
3. 路由導航過程
4. 複雜佈局的組合結果

## 原始碼位置

https://github.com/ccc112a/aiprogrammer/tree/main/202408/_code/flutter_demo.js
