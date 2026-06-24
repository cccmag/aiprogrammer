# 高效 Transformers：Linformer、FlashAttention

## O(n²) 的問題根源

標準注意力機制的時間與記憶體複雜度均為 O(n²)，其中 n 為序列長度。當序列長度達到數千甚至數萬時，計算和記憶體成本急劇膨脹。例如處理一份 10 萬字的文件，注意力矩陣需要儲存 10^10 個權重，約需 80 GB 的記憶體（float32），這在實務上完全不可行。這個瓶頸推動了高效 Transformer 研究的蓬勃發展。

## Linformer — 低秩注意力

Linformer（Wang et al., 2020）基於一個關鍵假設：注意力矩陣是低秩的，這意味著它可以被壓縮到更低維度的空間。具體方法是將 K 和 V 分別透過線性投影壓縮到 k 維空間（k ≪ n），然後在 k 維空間中計算注意力。這樣複雜度從 O(n²) 降至 O(nk)，大幅減少了計算和記憶體開銷。

## FlashAttention — IO 感知演算法

FlashAttention（Dao et al., 2022）是 2022 年最重要的高效 Transformer 進展之一。它的核心創新在於不改變注意力機制的數學結果，而是重新組織計算流程以充分利用 GPU 的記憶體層級結構。FlashAttention 將 Q、K、V 分塊載入到快速的 SRAM 中，在 SRAM 內完成注意力計算後再將結果寫回 HBM。這種 tiling 策略減少了慢速 HBM 的讀寫次數，實現 2 到 4 倍的實際速度提升，同時將記憶體用量從 O(n²) 降至 O(n)。

## Reformer — LSH 注意力

Reformer（Kitaev et al., 2020）使用局部敏感哈希將 Query 和 Key 分桶。每個 Query 只與同桶內的 Key 計算注意力，將複雜度降至 O(n log n)。這種近似方法在序列長度非常長時效果顯著，但需要仔細調整哈希函數以保持良好的近似品質。

## Longformer 與 Big Bird

Longformer 採用滑動視窗注意力搭配全局 token，每個 token 僅關注附近 w 個 token，同時讓特定位置（如 [CLS]）擁有全局視野。Big Bird 進一步結合滑動視窗、隨機注意力和全局注意力三種模式，理論上可證明能逼近完整注意力的表現。兩者在長文本處理上都有不錯的表現。

## 方法選擇建議

序列長度小於 512 時直接使用標準注意力最簡單。中等長度（512 到 4096）推薦 FlashAttention 兼顧速度與準確性。超長序列（大於 4096）則建議使用 Linformer 或 Longformer 等近似方法。選擇時還需要考慮硬體支援和實作複雜度。

## 參考資源

- FlashAttention 論文：https://www.google.com/search?q=FlashAttention+fast+efficient+attention
- Linformer 論文：https://www.google.com/search?q=Linformer+linear+attention
- Longformer：https://www.google.com/search?q=Longformer+attention+sliding+window
