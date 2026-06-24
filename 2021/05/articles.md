# 文章總覽

本期共十篇技術文章，深入探討深度學習的核心理論基礎。

## 第一期：從微分到反向傳播

從微積分的鏈式法則出發，逐步推導反向傳播的數學過程。解釋計算圖的概念，以及自動微分如何實現。幫助讀者建立從數學到程式的完整映射。[閱讀全文](article1.md)

## 第二期：Adam vs SGD：何時用哪個？

詳細比較 Adam 和 SGD 的理論特性、收斂速度和泛化表現。討論在 CNN、Transformer、不同任務場景下的適用性。提供決策樹幫助讀者做出選擇。[閱讀全文](article2.md)

## 第三期：Dropout 的理論解釋

從生物學靈感到數學推導，全面理解 Dropout。解釋訓練時的隨機 dropout 和推斷時的 weight scaling 為何等價。討論 Variational Dropout、Concrete Dropout 等變體。[閱讀全文](article3.md)

## 第四期：Layer Normalization 詳解

對比 Layer Normalization 與 Batch Normalization 的差異。解釋 LN 在 RNN 和 Transformer 中的應用。討論 Pre-LN vs Post-LN Transformer 的訓練差异。[閱讀全文](article4.md)

## 第五期：權重衰減與L2正則化

從貝葉斯視角解釋 L2 正則化：假設權重服從高斯先驗，最大化後驗概率等同於最小化 L2 損失。討論權重衰減與 L2 正則化的細微區別，以及在實務中的選擇。[閱讀全文](article5.md)

## 第六期：梯度消失與爆炸解決方案

回顧深度網路訓練中的梯度問題。介紹 Xavier/He 初始化、Batch Normalization、殘差連接、梯度裁剪等解決方案。解釋為何這些技術有效以及何時該用它們。[閱讀全文](article6.md)

## 第七期：動量法的物理直覺

從物理學角度理解動量法：想像一個小球在損失曲面上滾動，動量幫助它越过小坑、冲出局部極小值。介紹 Nesterov 加速梯度如何改進傳統動量法。[閱讀全文](article7.md)

## 第八期：學習率探尋與自適應調整

介紹 learning rate range test 等系統性學習率探尋方法。討論如何根據訓練階段動態調整學習率。比較 warmup、decay、cycle 等策略的優劣。[閱讀全文](article8.md)

## 第九期：標籤平滑的理論基礎

標籤平滑將硬標籤轉為軟標籤，避免模型過度自信。從標籤平滑的物理含義、對損失函數的影響、以及對泛化的作用三個維度解釋這一技術。[閱讀全文](article9.md)

## 第十期：未來理論研究方向

回顧深度學習理論的現狀，展望未來可能的突破方向。討論超大規模預訓練、Transformer 理論、可解釋性等前沿問題的理論重要性。[閱讀全文](article10.md)