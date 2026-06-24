# 注意力蒸餾

## 知識蒸餾簡介

知識蒸餾（Knowledge Distillation）是一種模型壓縮技術，讓一個小型模型（學生）去模仿一個大型模型（教師）的行為。傳統的知識蒸餾專注於模仿教師模型的最終輸出機率分佈（logits）。

但在注意力機制普及後，研究人員發現：不僅最終輸出可以蒸餾，教師模型內部的注意力權重也可以被蒸餾——這就是「注意力蒸餾」（Attention Distillation）。

## 為什麼蒸餾注意力？

### 注意力權重攜帶語法知識

研究發現，大型語言模型的注意力頭學到了豐富的語言學知識，包括：
- 依存句法關係（動詞-賓語、名詞-修飾語）
- 共指解析（代詞與先行詞的對應關係）
- 語義角色（主語、謂語、賓語的區分）

這些知識不是顯式訓練出來的，而是模型在語言建模過程中自發學到的。透過注意力蒸餾，我們可以將這些隱含的語言知識從大型教師模型轉移給小型學生模型。

### 注意力權重的重要性

對於大型教師模型，注意力權重提供了比 logits 更豐富的資訊。logits 只包含模型對最終輸出的偏好，而注意力權重揭示了模型在處理每個 token 時的「內部決策過程」。

## 注意力蒸餾的方法

### Logit 蒸餾 + 注意力蒸餾

最常見的方法是將 logit 蒸餾和注意力蒸餾結合：

```
L = α × L_logit + β × L_attention

L_logit = KL(教師 logits || 學生 logits)
L_attention = MSE(教師注意力權重, 學生注意力權重) / 層數
```

### 跨層注意力對齊

教師模型通常比學生模型更深。跨層注意力對齊需要決定：
- 學生第 i 層應該模仿教師的第幾層？
- 如何處理層數不匹配的問題？

常用的策略：
- **均勻映射**：學生每層對應教師的 ceil(i × N/M) 層
- **自適應映射**：透過一個可學習的層選擇網路
- **平均映射**：學生模仿教師多層注意力的平均值

### Multi-Head 注意力的蒸餾

多頭注意力的蒸餾需要考慮：

**頭對齊問題**：
教師和學生的注意力頭可能具有不同的功能。單純的逐頭匹配可能不是最優的。

解決方法：
- 對所有頭的注意力權重求平均後進行蒸餾
- 使用匈牙利演算法匹配最相似的頭對
- 在注意力權重上使用對抗性損失來對齊頭的分佈

## 注意力蒸餾的變體

### 基於關係的注意力蒸餾

不僅模仿注意力權重本身，還模仿注意力權重之間的關係：

```
L_relation = ||G_T - G_S||²

G_T[i,j] = cosine_sim(attn_T[i], attn_T[j])
G_S[i,j] = cosine_sim(attn_S[i], attn_S[j])
```

這種方法保留了注意力頭之間的相關性結構。

### 上下文蒸餾

將注意力蒸餾擴展到注意力所攜帶的語境資訊：

```
L_context = MSE(Attention_T @ V_T, Attention_S @ V_S)
```

這等價於蒸餾注意力層的輸出，而不是注意力權重本身。

### 模態感知的注意力蒸餾

在多模態模型中，不同模態的注意力模式可能不同。模態感知的注意力蒸餾為不同模態使用不同的蒸餾權重：

```
L = Σ_m λ_m × MSE(Attn_Teacher^m, Attn_Student^m)
```

其中 m 代表不同的模態（文字、圖像、語音等）。

## 實際應用案例

### BERT 蒸餾

DistilBERT 是注意力蒸餾的經典案例。相比於教師 BERT-Base：
- 保留 97% 的性能
- 減少 40% 的參數
- 提速 60%

後續的 TinyBERT 更進一步，使用注意力蒸餾將 BERT 壓縮到原始大小的 1/7，同時保留了 96% 的性能。

### ViT 蒸餾

DeiT（Data-efficient Image Transformers）使用注意力蒸餾訓練 Vision Transformer：

```
L = λ_CE × L_CE + λ_attn × L_attn + λ_logit × L_logit

L_attn = Σ_h ||A_teacher_h - A_student_h||²
```

DeiT 將 ViT 的訓練資料效率提升了 3-5 倍。

## 注意事項與挑戰

### 注意力不等於重要

如前所述（焦點七），注意力權重並不等於特徵重要性。如果教師模型的注意力權重包含了某些偏差或冗餘模式，直接蒸餾可能會將這些問題傳遞給學生。

### 過度模仿的風險

學生模型可能過度模仿教師的注意力模式，無法發揮自身架構的優勢。為了解決這個問題，可以：
- 在訓練後期減少注意力蒸餾的權重
- 僅在部分層上進行注意力蒸餾
- 使用自適應的蒸餾門檻

## 結論

注意力蒸餾是知識蒸餾領域的重要進展。它不僅能夠有效地進行模型壓縮，還提供了理解教師模型內部知識的新視角。隨著大型語言模型的普及，注意力蒸餾在模型部署和資源受限場景中將發揮越來越重要的作用。

---

**延伸閱讀**
- [TinyBERT: Distilling BERT for Natural Language Understanding](https://www.google.com/search?q=TinyBERT+attention+distillation)
- [DeiT: Data-efficient Image Transformers with Attention Distillation](https://www.google.com/search?q=DeiT+attention+distillation)
- [DistilBERT: A Distilled Version of BERT](https://www.google.com/search?q=DistilBERT+knowledge+distillation)
