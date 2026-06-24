# WebAssembly 走出瀏覽器

## 前言

2019 年，WebAssembly 的應用場景正在擴展到瀏覽器之外。邊緣計算和無伺服器運算成為 WASM 的新舞台。

## WASM 的新應用

### Fastly + WASM

Fastly 宣佈在其邊緣計算平台上支援 WASM：

```javascript
// 在 Fastly Edge 運行的 WASM
addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request));
});
```

### Cloudflare Workers

Cloudflare Workers 支援 WASM 模組：

```javascript
export default {
    async fetch(request) {
        const { instance } = await WebAssembly.instantiate(wasmModule);
        return new Response(instance.exports.process(request));
    }
};
```

---

## WASM 的優勢

| 特性 | 說明 |
|------|------|
| 高效能 | 接近原生速度 |
| 跨平台 | 一次編譯，到處運行 |
| 安全 | 沙箱執行環境 |
| 小體積 | 載入速度快 |

---

## 結語

WebAssembly 正在從瀏覽器技術轉變為通用的跨平台運行時解決方案。

---

**延伸閱讀**

- [WebAssembly 2019](https://www.google.com/search?q=WebAssembly+edge+computing+2019)
- [WASM+serverless](https://www.google.com/search?q=WebAssembly+serverless+2019)