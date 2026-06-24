# 影像合成與擴增技術（2017-2029）

## 從傳統擴增到擴散模型

影像合成與擴增從 2017 年的幾何變換發展到 2029 年的即時 3D 場景合成，技術迭代速度驚人。本節按時間線梳理關鍵技術突破。

### 2017-2020：傳統資料擴增

早期影像擴增依賴幾何變換：旋轉、翻轉、裁切、色彩抖動。Cutout、Mixup、CutMix 等方法引入區域遮罩與混合策略，顯著提升分類模型的泛化能力。

```python
# 合成表格資料並轉為影像特徵模擬
from _code.synthetic_data import SyntheticDataGenerator

gen = SyntheticDataGenerator()
rows = gen.generate_table(10)
features = [r["feature_a"] for r in rows]
bins = [0] * 5
for f in features:
    idx = min(int((f + 2) / 0.8), 4)
    bins[idx] += 1

print("合成資料分布:", bins)
print("類別分布:", {c: sum(1 for r in rows if r["category"] == c) for c in ["A", "B", "C"]})
```

### 2021-2023：擴散模型登場

DDPM、Stable Diffusion、DALL-E 2 讓影像合成進入新階段。文字到圖像（Text-to-Image）的成熟讓合成影像的品質達到照片級真實度。ControlNet、LoRA 等技術讓使用者可精準控制合成內容。

### 2024-2026：3D 與影片合成

Sora（2024）開啟影片合成時代。NeRF 與 3D Gaussian Splatting 讓 3D 場景合成成為可能。合成資料開始用於自動駕駛訓練——CARLA、SYNTHIA 等模擬器生成的合成街景已成為自駕車訓練的標準配備。

### 2027-2029：即時合成與領域適應

影像合成速度達即時（30fps），可用於線上資料擴增。Domain Adaptation 技術讓合成影像的特徵分布與真實影像無縫對齊，消除合成與真實之間的 Domain Gap。

### Face Swapping 與 Deepfake 防禦

合成人臉技術的進步也帶來了 Deepfake 檢測的軍備競賽。2024 年後合成人臉與真實人臉的差異縮小至人眼無法分辨。檢測方法從傳統 CNN 特徵進化到基於擴散模型指紋的溯源分析。合成人臉技術同時被用於隱私保護——以合成臉部替換真實人臉，在保留表情與姿態的前提下移除可識別身份資訊。

### 關鍵應用領域

- 醫學影像合成（罕見疾病資料擴增）
- 自動駕駛場景合成（邊緣案例生成）
- 衛星影像擴增（天氣、季節變換）
- 人臉隱私保護（替換真實人臉）
- 電子商務產品影像生成（虛擬試穿、場景合成）

## 延伸閱讀

- [Stable Diffusion image synthesis 2022](https://www.google.com/search?q=Stable+Diffusion+text+to+image+2022)
- [Sora video generation synthetic data 2024](https://www.google.com/search?q=Sora+OpenAI+video+generation+synthetic+data+2024)
- [Synthetic data autonomous driving CARLA](https://www.google.com/search?q=synthetic+data+autonomous+driving+simulator)
