# AI 輔助 GPU 除錯與效能分析

## 前言

GPU 程式設計的除錯向來是開發者的一大痛點。與 CPU 程式不同，GPU 的平行執行模型讓中斷點除錯幾乎不可行——數千個執行緒同時運行，傳統的 step-by-step 除錯模式完全失效。著色器編譯錯誤訊息往往語焉不詳，GPU 驅動崩潰（device lost）的錯誤訊息只給你一個通用代碼，而效能瓶頸分析需要對 GPU 架構有深層理解。2024 年以來，大型語言模型（LLM）開始從根本上改變這個困境——從自動解釋 Vulkan 驗證層的錯誤訊息，到分析 GPU 追蹤檔案並提出最佳化建議，AI 正在成為 GPU 開發者工具箱中不可或缺的夥伴。

## LLM 輔助著色器除錯

### 錯誤訊息解讀

WGSL 編譯器（naga）的錯誤訊息對新手來說相當難以理解。LLM 可以將原始錯誤轉換為可操作的分析和修復建議：

```
使用者輸入的錯誤：

error: '=' operator cannot be used with 'array<vec2<f32>, 3>' on left-hand side
  --> shader.wgsl:12:5
   |
12 |     positions = array<vec2<f32>, 3>(vec2(0.0, 0.5), ...);

LLM 分析：
此錯誤是因為 WGSL 中陣列預設為不可變綁定。
'positions' 如果在函數內宣告，需要用 'var' 關鍵字；
如果是 storage buffer，需要在綁定宣告中使用 'read_write'。
修正：將 'let positions' 改為 'var positions'。
```

### 自動修復工作流程

結合 Rust 工具鏈與 LLM API 可以建立自動化著色器修復管線：

```rust
fn ai_debug_shader(wgsl_source: &str) -> String {
    // 1. 嘗試使用 naga 編譯
    let output = Command::new("naga")
        .arg("--stdin-fmt")
        .arg("wgsl")
        .stdin(std::process::Stdio::piped())
        .output()
        .unwrap();

    if output.status.success() {
        return wgsl_source.to_string();
    }

    let error_msg = String::from_utf8_lossy(&output.stderr);

    // 2. 將錯誤上下文發送給 LLM 請求修復
    let prompt = format!(
        "你是一個 WGSL 著色器專家。以下著色器程式碼編譯失敗。\n\n\
        錯誤訊息：\n{}\n\n\
        程式碼：\n```wgsl\n{}\n```\n\n\
        請僅輸出修正後的完整程式碼，不要外加說明。",
        error_msg, wgsl_source
    );

    call_llm(&prompt)
}
```

### GPU 崩潰分析

GPU 驅動程式崩潰（device lost、driver hang）是最難除錯的問題類型。LLM 可以基於已知的症狀模式推測根因：

```
症狀：wgpu 回報 'GPU device lost'，無其他錯誤資訊

LLM 建議的檢查清單：
1. 著色器中的 for 迴圈是否有明確的邊界條件？GPU 不允許動態迴圈。
2. 除法運算是否可能出現除數為零的情況？例如 a / (1.0 - t)。
3. textureSample 是否可能超出紋理邊界？採樣座標是否在 [0, 1] 範圍內？
4. 計算著色器的 workgroup 大小是否超過裝置的 maxComputeWorkgroupSize 限制？
5. storage buffer 的寫入操作是否可能超出陣列範圍？
```

## 自動化 GPU 追蹤分析

### wgpu-profiler 整合 Tracy

Tracy 是一款高效的幀級效能分析工具，支援 GPU 時間戳查詢。透過 `wgpu-profiler` crate 可以在 Rust 中插入 GPU 標記：

```rust
use wgpu_profiler::GpuProfiler;

fn render_frame(
    encoder: &mut wgpu::CommandEncoder,
    profiler: &mut GpuProfiler,
    scene: &Scene,
) {
    // 標記陰影貼圖階段
    let _shadow_query = profiler.begin_query(encoder, "shadow_map");
    {
        let mut rpass = encoder.begin_render_pass(&shadow_pass_desc);
        scene.render_shadow_map(&mut rpass);
    }

    // 標記主渲染階段
    let _main_query = profiler.begin_query(encoder, "main_pass");
    {
        let mut rpass = encoder.begin_render_pass(&main_pass_desc);
        scene.render(&mut rpass);
    }

    // 標記後處理階段
    let _post_query = profiler.begin_query(encoder, "post_process");
    {
        let mut cpass = encoder.begin_compute_pass(&Default::default());
        cpass.set_pipeline(&post_process_pipeline);
        cpass.dispatch_workgroups(width / 8, height / 8, 1);
    }
}
```

收集到的追蹤數據可以餵給 LLM 進行自動分析：

```rust
fn analyze_perf_trace(trace_json: &str) -> String {
    let prompt = format!(
        "你是 GPU 效能分析專家。以下是 wgpu 應用程式的 Tracy 效能追蹤數據。\n\n\
        追蹤數據：\n{}\n\n\
        請分析：1) 哪個渲染階段耗時最長？2) 是否存在 CPU-GPU 同步瓶頸？\
        3) 具體的最佳化建議。",
        trace_json
    );
    call_llm(&prompt)
}
```

### 著色器瓶頸分類

LLM 可以透過靜態分析對著色器瓶頸進行分類和建議：

| 瓶頸類型 | 典型特徵 | AI 建議的最佳化策略 |
|---------|---------|-------------------|
| ALU-bound | 大量的數學運算（sin/cos/pow） | 使用低精度 `f16`，預先計算常數，用查表代替運算 |
| Memory-bound | 大量紋理讀取和取樣操作 | 使用紋理壓縮（BC7/ASTC），合併紋理為 texture array |
| Divergence-bound | Warp 內大量 if-else 分支 | 重構為 lerp/mix 平滑過渡，將條件移到 uniform |
| Output-bound | 過多的渲染目標（MRT） | 合併渲染目標，使用合併著色器（uber-shader） |

## AI 建議的 GPU 最佳化策略

### 減少 Draw Call

LLM 可以分析場景結構並建議合併策略。假設你的場景有 1000 個獨立物體：

```
原始方案：每個物體呼叫一次 draw() → 1000 次 draw call

AI 建議的合併方案：
1. 使用 texture array 合併使用相同材質的所有物體
2. 對靜態物體使用 indirect draw + GPU-driven culling
3. 對相同 mesh 的物體使用 instancing 渲染

預期效果：draw call 從 1000 降到 50，CPU 端的命令緩衝開銷減少 90%
```

### 著色器合併

將多功能整合到單一著色器中，減少管線切換的開銷：

```wgsl
// AI 生成的合併著色器：根據 material_type 選擇渲染路徑
fn fragment_main(
    @location(0) uv: vec2<f32>,
    @builtin(front_facing) is_front: bool,
) -> @location(0) vec4<f32> {
    let material = get_material_type();
    let base = textureSample(base_map, base_sampler, uv);

    // 統一的光照計算
    let lighting = compute_lighting(base.rgb);

    var final_color: vec3<f32>;
    switch material {
        case 0u: { final_color = lambertian(base.rgb, lighting); }
        case 1u: { final_color = cook_torrance(base.rgb, lighting, roughness, metallic); }
        case 2u: { final_color = toon_shading(base.rgb, lighting); }
        case 3u: { final_color = unlit(base.rgb); }
        default: { final_color = base.rgb * lighting; }
    }
    return vec4<f32>(final_color, base.a);
}
```

### 記憶體頻寬最佳化

GPU 的記憶體頻寬是珍貴資源。AI 分析紋理存取模式後常見的建議：

- 將最常存取的紋理綁定到 bind group 0（效能最快的綁定槽位）
- 使用 `textureGather` 指令一次取得四個紋素，代替四次獨立的 `textureSample`
- 對固定紋理使用不可變取樣器（immutable sampler），減少取樣器狀態切換
- 將多個小型 uniform buffer 合併為一個，批次上傳減少 staging 次數

## 整合開發環境

2026 年出現了專門的 AI GPU 除錯助手，常見的功能包括：

- **即時著色器分析**：在編輯器中輸入 WGSL 即獲得 AI 的最佳化建議和安全檢查
- **追蹤可視化**：AI 自動標註效能瓶頸位置，並顯示與前一次運行的比較
- **自動修復**：一鍵套用 LLM 建議的修改，並自動驗證編譯結果
- **知識庫整合**：結合 wgpu GitHub issue、GPU 廠商論壇和官方文件的知識問答

## 參考資料

- [wgpu-profiler crate](https://www.google.com/search?q=wgpu+profiler+rust+GPU+profiling)
- [Tracy Profiler](https://www.google.com/search?q=Tracy+profiler+GPU+frame+analysis)
- [NVIDIA Nsight Graphics](https://www.google.com/search?q=NVIDIA+Nsight+Graphics+debugging+profiling)
- [LLM 輔助 Vulkan 除錯](https://www.google.com/search?q=LLM+Vulkan+validation+layer+debugging)
- [著色器最佳化指南](https://www.google.com/search?q=GPU+shader+optimization+techniques+best+practices)
