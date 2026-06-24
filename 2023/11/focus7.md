# 7. 率失真理論

## 從無失真到有損壓縮

前面的討論集中在無失真壓縮，但許多應用允許一定的失真。例如 JPEG 壓縮影像時，人眼無法察覺的細微差異是可接受的。率失真理論（Rate-Distortion Theory）就是在這種背景下應運而生。

## 率失真函數

率失真函數 $R(D)$ 定義為：在給定平均失真不超過 $D$ 的條件下，所能達到的最小傳輸速率。Shannon 的率失真定理指出，$R(D)$ 是這個問題的理論極限。

對於一個來源 $X$ 與重建 $Y$，其失真通常以均方誤差（MSE）或漢明距離度量。率失真函數為：

$$R(D) = \min_{p(y|x): E[d(X,Y)] \leq D} I(X; Y)$$

## 高斯來源的率失真

對於一個變異數為 $\sigma^2$ 的高斯來源且以 MSE 為失真度量，率失真函數為：

$$R(D) = \begin{cases}
\frac{1}{2} \log_2 \frac{\sigma^2}{D}, & 0 \leq D \leq \sigma^2 \\
0, & D > \sigma^2
\end{cases}$$

這說明：若容忍失真等於來源的變異數，那麼不需要任何位元；若要求無失真（$D = 0$），則需要無限大的速率。

## 應用：壓縮標準

| 標準 | 類型 | 失真度量 | 核心技術 |
|------|------|---------|---------|
| JPEG | 影像 | 視覺品質 | DCT + 量化 |
| MP3 | 音訊 | 聽覺模型 | 心理聲學編碼 |
| H.264 | 視訊 | SSIM/PSNR | 區塊運動補償 |
| VAE | 生成模型 | 重建損失 | 變分率失真 |

這些壓縮標準都在實務中實現了率失真的權衡：根據應用場景選擇可接受的失真水平來最大化壓縮比。

## 率失真與深度學習

近年來，率失真理論與深度學習產生了有趣的連結。變分自編碼器（VAE）的損失函數可以視為率失真函數的變分下界。而資訊瓶頸（Information Bottleneck）方法則利用互資訊來分析深度網路的表示學習。

## 參考資源

- https://www.google.com/search?q=rate+distortion+theory+Shannon+lossy+compression+function+definition
- https://www.google.com/search?q=Gaussian+source+rate+distortion+function+closed+form+formula+MSE
- https://www.google.com/search?q=VAE+rate+distortion+information+bottleneck+deep+learning+connection
