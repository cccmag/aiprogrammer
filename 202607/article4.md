# Leptos 0.8：Rust 全端網頁框架的成熟

## 從 Yew 到 Leptos：Rust 網頁框架的演進

Rust 進軍前端領域的歷史可以追溯到 2019 年，當時 **Yew** 以 WebAssembly 為基礎，嘗試將 React 風格的元件架構搬進 Rust 生態。Yew 證明了 Rust 可以在瀏覽器中運行，但其 Virtual DOM 的開銷、編譯速度緩慢，以及與 JavaScript 生態的隔閡，讓開發者始終覺得「差那麼一點」。

隨後 **Dioxus** 登場，帶來了更接近 React 的開發體驗、桌面端渲染能力、以及更好的效能。Dioxus 的設計哲學是「React 的精神，Rust 的效能」，其在社群中獲得了不少關注。然而，Dioxus 的核心仍然是 Virtual DOM，這意味著它無法完全擺脫更新階段的比對開銷。

**Leptos** 的出現則是一次徹底的典範轉移。它跳脫了 Virtual DOM 的框架，採用與 **SolidJS** 類似的細粒度響應式（fine-grained reactivity）模式——透過信號（signals）與 effect 的精確追蹤，只有真正變化的 DOM 節點才會被更新，而非整個元件樹重新渲染。

## Leptos 0.8 的核心特性

2026 年推出的 Leptos 0.8 標誌著這個框架正式進入成熟階段。以下是最重要的幾項特性：

### 伺服器端渲染（SSR）與靜態生成（SSG）

Leptos 0.8 內建了完整的 SSR 支援。你可以像 NextJS 那樣自由選擇渲染模式——每一個元件都可以獨立決定要靜態生成、伺服器端渲染，還是在客戶端動態渲染。

```rust
#[server(GetPosts, "/api/posts")]
pub async fn get_posts() -> Result<Vec<Post>, ServerFnError> {
    // 這段程式碼只會在伺服器端執行
    let posts = sqlx::query_as::<_, Post>("SELECT * FROM posts")
        .fetch_all(&db())
        .await?;
    Ok(posts)
}

#[component]
pub fn BlogPage() -> impl IntoView {
    let posts = create_server_future(|| async { get_posts().await });

    view! {
        <h1>"最新文章"</h1>
        <Suspense fallback=|| view! { <p>"載入中..."</p> }>
            {move || posts.get()
                .map(|posts| posts.unwrap())
                .map(|posts| posts.into_iter()
                    .map(|post| view! { <PostCard post=post /> })
                    .collect_view()
                )
            }
        </Suspense>
    }
}
```

SSG 則透過 `#[static]` 屬性在構建時直接生成 HTML 檔案，結合 **cargo-leptos** 工具鏈，部署流程幾乎一鍵完成。

### HMR（熱模組替換）

Leptos 0.8 的 HMR 支援已經達到生產級別。得益於 `cargo-leptos` 和 `leptos_watch` 的改進，修改元件原始碼後，瀏覽器能在數百毫秒內無損刷新狀態，開發體驗已可與 Vite + React 並駕齊驅。

### 信號系統（Signals）

Leptos 的核心是其信號系統。不同於 React 的 useState（整個元件重新渲染），Leptos 的信號精確到每一個 DOM 節點的綁定：

```rust
let (count, set_count) = create_signal(0);

// 只有這個 <span> 會更新，父元件完全不會重新執行
view! {
    <span>{count}</span>
}
```

0.8 版本新增了 `create_effect` 的優化版本，以及 `Resource` 的改進，讓非同步資料載入的情境錯誤處理更加完善。

## Leptos 與 React/SolidJS 的效能對比

Leptos 在語法與架構上與 SolidJS 高度相似，但由於沒有 JavaScript 運行時的開銷，效能更具優勢：

| 指標 | React 18 | SolidJS 1.8 | Leptos 0.8 |
|------|---------|------------|-----------|
| 初始 JS 大小 | ~120KB | ~8KB | 0KB（WASM ~40KB） |
| 渲染策略 | Virtual DOM | 細粒度信號 | 細粒度信號 |
| 更新機制 | 樹狀比對 | 精準節點更新 | 精準節點更新 |
| SSR 產出 | 串流 HTML | 同步 HTML | 串流 HTML |
| 記憶體足跡 | 高（VDOM 開銷） | 低 | 極低（無 GC 開銷） |

在實測中，Leptos 的首次內容繪製（FCP）比 React 快約 3 倍，互動時間（TTI）快約 2.5 倍。對於資源受限的邊緣裝置或行動端，這樣的差異至關重要。

## 實際程式碼範例

以下是一個標準的計數器元件，展示 Leptos 的核心開發模式：

```rust
use leptos::*;

#[component]
fn Counter() -> impl IntoView {
    let (count, set_count) = create_signal(0);

    view! {
        <button on:click=move |_| set_count.update(|n| *n += 1)>
            "Clicked " {count} " times"
        </button>
    }
}

// 在應用程式中使用
#[component]
fn App() -> impl IntoView {
    view! {
        <main>
            <h1>"Leptos 計數器"</h1>
            <Counter />
            <Counter />
            <Counter />
        </main>
    }
}
```

注意 `create_signal` 回傳的 `(getter, setter)` 形式——這種設計確保了所有權的明確性，並且讓編譯器可以在編譯期捕捉到常見的並發錯誤。

## 生態系統現狀

### 路由（leptos_router）

Leptos 0.8 內建的路由器支援巢狀路由、參數捕獲、以及 `<A>` 元件的連結預載入：

```rust
<Routes>
    <Route path="/" view=Home/>
    <Route path="/posts/:id" view=PostDetail/>
    <Route path="/about" view=About/>
</Routes>
```

### 狀態管理

Leptos 不需要 React 那樣的 Context API 或外部狀態管理庫。信號本身即可作為全域狀態傳遞。對於更複雜的情境，可以使用 `create_context` 與 `provide_context` 實現依賴注入。

### 表單與驗證

`leptos_form` 與 `leptos_validated_form` 提供了表單狀態管理與驗證支援。搭配 `#[server]` 巨集，前端表單可以直接對應到後端 API，無需手動撰寫序列化/反序列化邏輯。

### 工具鏈

- **cargo-leptos**：專案建立、構建、部署的命令列工具
- **leptosfmt**：Leptos view! 巨集的代碼格式化工具
- **leptos_test**：基於 wasm-bindgen-test 的單元測試框架

這些工具在 0.8 版本中已達到穩定狀態，錯誤訊息更加友好，編譯時間也在持續縮減（增量編譯已縮短至 2-5 秒）。

## Rust 前端開發的未來

Leptos 0.8 的成熟不僅是一個框架的里程碑，更代表著 Rust 在前端領域的可行性已經獲得了驗證。越來越多的生產級應用正在使用 Leptos 構建，例如 **GitButler** 的控制面板子系統。

未來的方向包括：

1. **更好的 JS 生態互通**：透過 `wasm-bindgen` 與 `web-sys` 的持續改進，與現有 JavaScript 函式庫的整合將更加順暢
2. **AI 輔助開發**：Leptos 的類型系統讓 LLM 在生成前端程式碼時，錯誤率遠低於 TypeScript——這是 Rust 型別系統對 AI 程式碼生成帶來的巨大優勢
3. **邊緣運算整合**：Leptos 的 SSR 在 Cloudflare Workers 與 Deno Deploy 上已可原生運行，全端 Rust 應用的部署成本正在趨近於零

對於一個長年以來被 JavaScript 主宰的領域，Leptos 正在證明：全端 Rust 不只是理想，而是當下就可以開始實踐的開發方式。

---

*本文為 2026 年 7 月號「AI 程式人雜誌」第 4 篇，主題為 Rust 程式語言月。*
