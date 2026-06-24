# 抽象資料型別 ADT

## 什麼是 ADT？

抽象資料型別（Abstract Data Type, ADT）是一種將資料與操作封裝在一起的思考方式。ADT 只定義行為（what），不限定實作方式（how）。例如，「堆疊」這個 ADT 定義了 push、pop、peek、isEmpty 等操作，但你可以用陣列實作，也可以用鏈結串列實作。這種分離介面與實作的概念是軟體工程的核心原則之一，也是模組化設計與測試的基礎。

## ADT 與物件導向的關係

ADT 的概念與物件導向程式設計（OOP）中的「類別」非常相似。事實上，ADT 正是 OOP 的理論基礎。當你定義一個 class 並將資料設為 private、只透過 public method 來操作資料時，你就在實踐 ADT 的精神。封裝（Encapsulation）讓我們可以隱藏內部實作細節，只暴露必要的操作介面，降低元件間的耦合度，提高程式的可維護性。

## 常見的 ADT 範例

**堆疊（Stack）**：後進先出（LIFO），操作有 push、pop、top、isEmpty。應用於函式呼叫堆疊、undo/redo 功能、括號配對檢查、表示式求值。

**佇列（Queue）**：先進先出（FIFO），操作有 enqueue、dequeue、front、isEmpty。應用於工作排程、BFS 演算法、訊息佇列、印表機任務管理。

**列表（List）**：有序資料集合，支援插入、刪除、存取等操作。陣列（ArrayList）與鏈結串列（LinkedList）都是列表的實作方式，各有不同的優缺點。

**字典（Dictionary / Map）**：鍵值對集合，支援 put、get、delete、containsKey。可用雜湊表（平均 O(1)）或二元搜尋樹（O(log n)）實作。

## 為什麼要用 ADT 思考？

1. **抽離實作細節**：不需要知道內部如何儲存，只需知道操作介面。
2. **易於替換實作**：只要介面不變，可隨時最佳化底層實作。
3. **提高可讀性**：程式碼意圖更清楚，操作名稱說明用途。
4. **促進模組化**：元件耦合度降低，易於測試與維護。

## 延伸閱讀

- https://www.google.com/search?q=Abstract+Data+Type+ADT+定義+範例+程式碼+OOP
- https://www.google.com/search?q=ADT+vs+OOP+封裝+資訊隱藏+差異+說明
- https://www.google.com/search?q=data+abstraction+程式設計+原則+優點+模組化
