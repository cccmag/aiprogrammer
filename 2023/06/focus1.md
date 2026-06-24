# 可計算性與 Entscheidungsproblem

## 判定問題的起源

1900 年，David Hilbert 在巴黎國際數學家大會上提出了 23 個有待解決的數學問題。其中第十個問題是：是否存在一個通用的演算法，可以用來判定任意多項式方程式是否有整數解？這個問題後來被稱為 Hilbert 的 Entscheidungsproblem（判定問題），字面意思是「決策問題」。

Hilbert 當時樂觀地相信：所有數學問題最終都可以透過機械化的計算步驟來解決。他認為存在一個「萬能演算法」，可以回答任何良定義的數學問題。這種信念被稱為 Hilbert 的「形式主義」哲學。

## Gödel 不完全性定理的衝擊

1931 年，Kurt Gödel 發表了不完全性定理，徹底撼動了 Hilbert 的信念。Gödel 證明：

1. **第一不完全性定理**：任何足夠強大的形式系統，都存在無法在該系統內被證明或否定的命題。
2. **第二不完全性定理**：任何足夠強大的形式系統，都無法在自身內部證明自身的一致性。

Gödel 的證明技巧非常巧妙——他發明了一種編碼方式（現在稱為 Gödel 編號），將數學陳述式對應到自然數。這樣一來，一個關於數學陳述式的命題就變成了一個算術命題。

## Church 的回答

1936 年，Alonzo Church 在普林斯頓發表論文《An Unsolvable Problem of Elementary Number Theory》，首次給出了 Entscheidungsproblem 的否定答案。Church 使用他提出的 λ 演算作為計算的形式模型，證明了不存在一個通用的 λ 可定義函式可以判定任意 λ 項是否具有正規形式。

Church 的證明依賴於他對「可計算性」的精確定義：一個函式是可計算的，當且僅當它是 λ 可定義的。這個定義後來被稱為 Church 論題。

## Turing 的回答

幾乎在同一時間，Alan Turing 在劍橋大學獨立完成了相似的證明。Turing 在 1936 年發表的論文《On Computable Numbers, with an Application to the Entscheidungsproblem》中，提出了圖靈機的概念，並使用圖靈機證明了 Entscheidungsproblem 是不可解的。

Turing 的證明更為直觀：他首先證明了停機問題的不可判定性，然後將 Entscheidungsproblem 歸約到停機問題。

## 方法論的差異

Church 與 Turing 雖然得出了相同的結論，但方法卻大不相同：

| Church | Turing |
|--------|--------|
| 使用 λ 演算 | 使用圖靈機 |
| 代數與函式視角 | 機械與狀態視角 |
| 證明較抽象 | 證明較直觀 |
| 基於 λ 可定義性 | 基於機械可計算性 |

有趣的是，Turing 的證明後來被認為更容易理解，這也是為什麼計算理論課程通常從圖靈機開始。

## Entscheidungsproblem 的深遠意義

Entscheidungsproblem 的不可解性告訴我們：

1. **電腦能力的根本限制**：有些數學問題是任何演算法都無法解決的
2. **自動化證明有極限**：我們無法建立一個萬能定理證明器
3. **可計算性的精確定義**：我們需要像圖靈機這樣的模型來嚴謹討論「什麼可以被計算」

這個結論對今天的 AI 研究也有啟示：即使是最強大的 AI 系統，也無法超越計算理論所設下的根本限制。

## 延伸閱讀

- [Hilbert's Entscheidungsproblem](https://www.google.com/search?q=Entscheidungsproblem+Hilbert)
- [Gödel Incompleteness Theorems](https://www.google.com/search?q=G%C3%B6del+incompleteness+theorems)
- [Church 1936 Unsolvable Problem](https://www.google.com/search?q=Church+unsolvable+problem+1936)
