# Vision Transformer（ViT）

## Transformer 進入視覺領域

長期以來，卷積神經網路（CNN）是電腦視覺的主流架構。從 AlexNet、VGG 到 ResNet、EfficientNet，CNN 的進化推動了電腦視覺的快速發展。2020 年，Dosovitskiy et al. 發表 Vision Transformer（ViT），證明無需卷積，純 Transformer 在大型資料集上可以超越最先進的 CNN。這是視覺領域的一次重要典範轉移。

## ViT 的設計

ViT 的設計優雅而直接。首先將圖片分割為固定大小的 patch，通常為 16×16 畫素。每個 patch 展平後透過線性投影映射為一維嵌入向量。然後加上可學習的位置編碼，保持 patch 的空間順序資訊。此外還插入一個特殊的 [CLS] token 用於分類任務。最後將這個 token 序列送入標準的 Transformer 編碼器，[CLS] 的輸出通過一個分類頭得到預測結果。

## 為什麼 ViT 有效？

CNN 受限於局部感受野，每一層只能看到局部區域，需要堆疊多層才能逐步擴大視野。深層 CNN 雖然理論上能建立長距離依賴，但實際的梯度傳播路徑使得這種依賴仍然受限。ViT 的自注意力機制在第一層就能直接建立任意兩個 patch 之間的聯繫，實現真正的全局建模。這種全局視野在處理需要理解整體結構的任務時具有明顯優勢。

## 資料量要求

ViT 最重要的發現之一是它需要大量訓練資料才能發揮潛力。在 ImageNet（130 萬張圖片）上，ViT 的表現不如同等參數量的 EfficientNet。但在 JFT-300M（3 億張圖片）上，ViT 大幅超越所有 CNN。這說明 Transformer 需要足夠的資料量來啟動其全局建模優勢，而 CNN 的歸納偏誤（locality、translation equivariance）在小資料集上更具優勢。

## Swin Transformer

Swin Transformer 引入分層特徵圖與移位視窗機制。它先在局部視窗內計算注意力，然後在相鄰層間移動視窗實現跨視窗資訊交流。這種設計讓 Swin Transformer 擁有類似 CNN 的尺度不變性和線性計算複雜度，成為檢測和分割任務的新基準。

## 影響與未來

ViT 的出現證明了卷積運算並非視覺處理的唯一方式，開啟了視覺基礎模型的新方向。後續的 DINO、MAE、CLIP 等劃時代模型都建立在 ViT 之上。ViT 的成功也推動了視覺與語言模型的統一，為多模態 AI 的發展奠定了重要基礎。

## 參考資源

- ViT 論文：https://www.google.com/search?q=vision+transformer+ViT+paper
- Swin Transformer：https://www.google.com/search?q=Swin+Transformer+hierarchical+vision
- ViT 實作：https://www.google.com/search?q=ViT+implementation+from+scratch+pytorch
