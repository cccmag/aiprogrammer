# 樹與二元搜尋樹

## 樹的基本概念

樹（Tree）是一種階層式資料結構，由節點（Node）與邊（Edge）組成。每個樹只有一個根節點（Root），除了根節點之外，每個節點都只有一個父節點（Parent）。沒有子節點的節點稱為葉節點（Leaf）。樹的常見術語包括深度（depth，從根到節點的邊數）、高度（height，從節點到最遠葉節點的邊數）與層級（level）。樹在檔案系統、HTML DOM 樹、組織架構、編譯器語法樹等領域隨處可見。

二元樹（Binary Tree）是每個節點最多有兩個子節點（左子節點與右子節點）的樹。二元樹的類型包括：滿二元樹（每個節點有 0 或 2 個子節點）、完全二元樹（從左到右填滿節點）、完美二元樹（所有葉節點在同一層且每個內部節點都有兩個子節點）。

## 二元搜尋樹（BST）

二元搜尋樹是一種特殊的二元樹，滿足以下三個關鍵性質：

1. 左子樹的所有節點值都小於根節點的值。
2. 右子樹的所有節點值都大於根節點的值。
3. 左右子樹也必須分別是二元搜尋樹（遞迴定義）。

BST 的搜尋、插入與刪除操作在平均情況下為 O(log n)。但在最差情況（插入已排序資料）下，BST 會退化為鏈結串列，時間複雜度惡化為 O(n)，此時就需要使用平衡樹來解決問題。

## BST 的核心操作

**搜尋**：從根節點開始，比較目標值與當前節點值。目標值較小則往左，較大則往右，相等則找到。每一步排除一半子樹，效率極高。

**插入**：類似搜尋，找到適當空位後插入新節點，總是在葉節點位置發生。

**刪除**：三種情況。葉節點直接移除；有一個子節點則用子節點取代；有兩個子節點則找中序後繼者（inorder successor）取代。

## Python 實作

詳細的 BST 實作請參考 `_code/ds_theory.py`，包含節點類別 BSTNode 與 BST 類別的插入、搜尋與中序走訪方法。

## 延伸閱讀

- https://www.google.com/search?q=binary+search+tree+data+structure+definition+properties+traversal+應用
- https://www.google.com/search?q=二元搜尋樹+插入+刪除+中序走訪+範例+程式碼+Python+實作
- https://www.google.com/search?q=tree+data+structure+tutorial+beginners+applications+types+binary+tree
