# 4. Attention 機制的革命

## Attention 的起源

Attention 機制在 2015 年被引入神經機器翻譯：
- 讓 Decoder 在生成每個詞時「注意」 Encoder 的不同位置
- 解決了 Seq2Seq 模型中固定 context 向量的瓶頸
- 顯著提升了翻譯品質

## Self-Attention 的提出

Self-Attention（自注意力）將注意力應用於同一序列：
- 每個位置可以注意序列中的所有其他位置
- 直接捕捉任意距離的依賴關係
- 是 Transformer 的核心組件

## Scaled Dot-Product Attention

Transformer採用的注意力計算：
1. 輸入向量透過線性變換生成 Q、K、V
2. 計算 Q 與 K 的點積，除以 √d_k
3. 通過 Softmax 獲得注意力權重
4. 加權 V 得到輸出

除以 √d_k 是為了避免點積過大導致 Softmax 梯度消失。

## Multi-Head Attention

多頭注意力讓模型同時關注多個子空間：
- 將 Q、K、V 投影到 h 個不同空間
- 每個頭獨立計算注意力
- 拼接所有頭的輸出

不同頭可能專注於不同的語言特性：
- 語法結構
- 語義關聯
- 共指標關係

## Attention 的優勢

相較於 RNN，Attention 具有：
- **平行計算**：所有位置同時處理
- **路徑長度**：O(1) 的路徑長度（任意位置直接可達）
- **可解釋性**：注意力權重可視化
- **靈活性**：可應用於各種任務

## 參考資源

- https://www.google.com/search?q=Attention+机制+革命+self-attention+Transformer+原理+2018
- https://www.google.com/search?q=scaled+dot-product+attention+multi-head+Transformer+详解
- https://www.google.com/search?q=attention+vs+RNN+優勢+為何+注意力機制+重要