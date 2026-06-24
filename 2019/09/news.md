# 本月新知

## 2019 年 9 月程式與 AI 技術動態

### 程式語言與框架

**Python 3.8 正式發布**

Python 3.8 於 2019 年 10 月正式發布。本月我們迎來了這個重要版本的功能預覽，包括海象運算子（`:=`）、位置-only 參數（`/`）、改進的 `typing` 模組等特性。Python 3.8 將於下月正式成為穩定版本，為 Python 開發者帶來更現代的語法支持。

**Rust 1.38 發布**

Rust 團隊於本月發布 Rust 1.38，這個版本引入了 pipeline 運算子（`|`）的穩定化，允許更直觀的函式鏈式調用。同時，編譯器優化和更好的錯誤消息也提升了開發體驗。

Rust 的安全性保證和現代化設計使其在系統程式領域持續獲得青睞。

**TypeScript 3.7 進入 RC**

TypeScript 3.7 的候選版本於本月發布，帶來了兩個重要特性：可選鏈（`?.`）和空位合併運算子（`??`）。這些特性借鑒自其他語言（如 C#、Kotlin），大大簡化了空值處理和鏈式調用的程式碼。

**Node.js 13 發布**

Node.js 13 於本月發布，提供了對 ES Module 的更好支援。`--experimental-modules` 標誌不再是必須，許多 ES Module 功能開始默認啟用。這是 Node.js 向全面 ES Module 支持邁進的重要一步。

### AI 與機器學習

**TensorFlow 2.0 正式發布**

本月的最大新聞！Google 於 2019 年 9 月正式發布 TensorFlow 2.0。這是 TensorFlow 自 2015 年發布以來最重要的版本更新。

TensorFlow 2.0 的核心變化：
- Eager Execution 默認開啟，告別麻煩的 `tf.Session`
- `tf.keras` 作為官方高階 API，統一了模型構建
- API 清理，移除了許多過時的 API
- 更好的向後兼容性（`tf.compat.v1`）
- TensorFlow Extended（TFX）整合

TensorFlow 2.0 的發布標誌著深度學習框架進入了一個更易用、更高效的新時代。

**PyTorch 1.3 發布**

Facebook AI 發布了 PyTorch 1.3，這個版本帶來了多項重要功能：量化支持（8 位元模型）、張量處理優化、以及更好的行動裝置部署支持。PyTorch 繼續保持著與 TensorFlow 競爭的態勢。

**JAX 獲得關注**

Google 的 JAX 框架本月獲得更多關注。JAX 是一個函式式的深度學習框架，結合了 Autograd 和 XLA，提供了高效且可組合的梯度計算。JAX 的函式編程範式吸引了對函式式編程感興趣的開發者。

### 雲端與開發工具

**Kubernetes 1.17 發布**

CNCF 發布了 Kubernetes 1.17，這個版本包含多項重要更新：

- Custom Resources Definition (CRD) v1 正式穩定
- 更好的 CSI 支援
- 改善的節點資源管理

**雲端 AI 服務升級**

主要雲端廠商升級了他們的 AI 服務：
- AWS SageMaker 增加了更多內建演算法
- Google Cloud AI Platform 提升了 Training/Prediction 效能
- Azure ML 增強了自動化機器學習功能

### 業界動態

- **華為發布 Atlas 200**：華為的 AI 加速器，瞄準邊緣運算
- **騰訊開源 Megvii**：面部識別技術開源
- **IBM 推出 AI Ethics**：AI 倫理框架
- **Adobe 發布 Sensei 更新**：創意 AI 新功能

### 標準與規範

- **W3C 發布 WebGPU 初始草案**：新一代 Web 圖形 API
- **IETF 標準化 HTTP/3**：QUIC 協議接近完成
- **Unicode 12.1**：新增 5 個表情符號

---

*本頁內容依照 [Google 新聞搜尋](https://www.google.com/search?q=2019+September+tech+news+programming+AI) 整理，相關連結僅供參考。*