# 本月新知

## 2024 年 2 月程式與 AI 技術動態

### Node.js 生態

**Node.js 21.7 發布**

Node.js 團隊於本月發布 v21.7 版本，引入實驗性的 `node:sqlite` 內建模組，允許開發者直接在 Node.js 中操作 SQLite 資料庫，無需第三方套件。此外，`--experimental-strip-types` 標誌允許直接執行 TypeScript 檔案，標誌著 Node.js 原生 TypeScript 支援的重要一步。

**Express 5.0 正式候選**

Express.js 團隊宣布 Express 5.0 進入 RC 階段，這是自 2015 年以來的首次大版本更新。5.0 版捨棄了對 Node.js 0.10 的向後相容支援，改進了 async error handling，讓開發者可以在路由處理器中直接使用 `async/await` 而無需額外的 try-catch 包裝。

**npm 10.5 引入 Audit Signatures**

npm 10.5 版本新增了 `audit signatures` 功能，允許套件發布者使用簽章機制驗證套件的完整性，大幅提升供應鏈安全性。同時，npm 團隊宣布將逐步淘汰對不安全的 TLS 1.0/1.1 的支援。

### JavaScript 與 TypeScript

**TypeScript 5.4 進入 Beta**

微軟發布 TypeScript 5.4 Beta，主要改進包括：`NoInfer` 工具型別、在 `switch` 與 `if` 條件收束的增強、以及更精確的型別縮小。這些改進讓開發者能更精確地控制型別推斷行為。

**WinterCG 成立**

WinterCG (Web-interoperable Runtimes Community Group) 正式成立，旨在制定跨執行期的 Web API 標準。Deno、Bun、Node.js 等執行期團隊共同參與，目標是讓 JavaScript 生態在不同執行期之間更具互通性。

### AI 與開發工具

**GitHub Copilot 全面升級**

GitHub 宣布 Copilot 採用 GPT-4 Turbo 模型，程式碼生成速度與準確度大幅提升。新功能包括 copilot-chat 的 `/explain` 和 `/tests` 指令，以及對 Jupyter Notebook 的完整支援。

**Llama 3 傳聞**

業界傳聞 Meta 正在訓練 Llama 3，預計參數量將達到 140B 以上。開源社群對此高度期待，認為這將進一步推動開源 LLM 的發展。

### 資料庫與後端

**MongoDB 8.0 預覽**

MongoDB 發布 8.0 預覽版，引入了新的查詢引擎「Juggler」，號稱在聚合管線和複雜查詢上有 3-5 倍效能提升。此外，新的 `live resharding` 功能允許在不停機的情況下重新分片。

**SQLite 3.45 發布**

SQLite 3.45 新增了 JSON 處理的最佳化，大幅提升 JSON 操作的效能。加上成為 Node.js 內建模組的消息，SQLite 在輕量級後端應用中的地位更加穩固。

### 業界動態

- **Express 團隊重組**：OpenJS Foundation 宣布 Express 專案的新維護團隊，加速框架現代化
- **Deno 與 Node.js 相容性提升**：Deno 1.40 大幅提升對 Node.js 內建模組的相容性
- **Vercel 推出 Edge Runtime 2.0**：支援更完整的 Web API 和中間件

### 延伸閱讀

- [Node.js 21.7 發佈說明](https://www.google.com/search?q=Node.js+21.7+release)
- [Express 5.0 RC](https://www.google.com/search?q=Express+5.0+release+candidate)
- [WinterCG 標準](https://www.google.com/search?q=WinterCG+web+interoperable+runtimes)
