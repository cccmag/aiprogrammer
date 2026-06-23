# 2027 年 3 月 — GPU 與 WebGPU 新聞

## WebGPU 在所有主流瀏覽器達成穩定

2027 年 2 月，Safari 18 正式啟用 WebGPU 支援，標誌著 WebGPU 在 Chrome、Firefox、Safari 三大瀏覽器引擎中全面穩定。開發者現在可以放心地在生產環境中使用 WebGPU。

- Chrome：自 113 版支援（2023）
- Firefox：自 127 版支援（2024）
- Safari：自 18 版支援（2027）

參考：[WebGPU browser support](https://www.google.com/search?q=WebGPU+browser+support+2027)

## wgpu 22 發布：DX12 光追與效能改進

wgpu 22 是重要的功能更新，包含：

- **DirectX 12 光線追蹤支援**（實驗性）
- **GPU 驅動 ECS**：在 GPU 上直接排程 System 執行
- **非同步著色器編譯**：不再阻塞主執行緒
- **記憶體使用減少 30%**：更智慧的資源分配

## Rust GPU 專案達到里程碑

Embark Studios 的 rust-gpu 專案現在可以將 Rust 原始碼直接編譯為 SPIR-V 著色器，在 Unreal Engine 5 中實際使用。這意味著開發者可以用同一種語言編寫 CPU 和 GPU 程式碼。

參考：[rust-gpu project](https://www.google.com/search?q=rust-gpu+Embark+Studios)

## NVIDIA 與 AMD 發布 WebGPU 驅動更新

NVIDIA 在 572.xx 驅動中大幅改進了 Vulkan 後端上的 WebGPU 效能。AMD 則在最新的 Adrenalin 驅動中加入了對 WebGPU 計算著色器的硬體加速支援。

## Khronos 發布 SYCL 2027

雖然 WebGPU 持續成長，Khronos Group 也發布了 SYCL 2027，專注於異質運算的標準化。與 WebGPU 不同的是，SYCL 更偏向 HPC 而非即時渲染。

參考：[SYCL 2027](https://www.google.com/search?q=SYCL+2027+Khronos)
