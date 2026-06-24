# 函數式語言在區塊鏈的應用

## 區塊鏈與智慧合約

區塊鏈技術的核心是去中心化的信任機器，而智慧合約是區塊鏈程式的核心。以太坊的智慧合約某種程度上就是「區塊鏈上的函式」。

## Haskell 在區塊鏈的應用

### Cardano 與 Plutus

Cardano 區塊鏈平臺採用 Haskell 作為其智慧合約語言。Plutus 是 Haskell 的一個子集，用於編寫智慧合約。

```haskell
-- Plutus 範例：簡單的鎖定合約
module Plutus where

-- 合約狀態
data ContractState = ContractState
    { owner    :: PubKeyHash
    , deadline :: Slot
    , amount   :: Value
    }

-- 驗證函式
validate :: ContractState -> PendingTx -> Bool
validate state ptx =
    -- 檢查是否已超過截止日期
    (slotToGT (deadline state) `contains` pendingTxSlot ptx)
    -- 或者擁有者才能解鎖
    || (txSignedBy ptx (owner state))
```

### Marlowe：金融合約專用語言

Marlowe 是 Cardano 團隊為金融合約設計的領域特定語言，基於 Haskell：

```haskell
-- Marlowe 合約範例
escrow :: Party -> Party -> Value -> Contract
escrow buyer seller price =
    Commit 1 (pay buyer (Value price) (-seller-) (When
        (Case (Deposit buyer seller price)
            (Both
                (Pay buyer (Value price) (-seller-) (Notify
                    (Both
                        (When
                            (Case (Choice buyer (ChoiceId "ok" buyer) [Bound 0 0])
                                Pay buyer (Value price) (-seller-) Close)
                            (Slot 100)
                            Close))
                        Close)))
                Close))
        (Slot 0) Close)))
```

## Rust 與區塊鏈

Rust 以其記憶體安全和效能，成為區塊鏈開發的熱門選擇：

### 以太坊客戶端：Parity

Parity Technologies 使用 Rust 開發了高效能以太坊客戶端：

```rust
// Rust 區塊鏈範例結構
struct Block {
    header: BlockHeader,
    transactions: Vec<Transaction>,
}

impl Block {
    // 區塊驗證
    fn validate(&self, state: &State) -> Result<(), BlockchainError> {
        // 驗證工作量證明
        self.header.validate_pow()?;

        // 驗證交易
        for tx in &self.transactions {
            tx.validate(state)?;
        }

        Ok(())
    }
}
```

### Solana 區塊鏈

Solana 使用 Rust 作為智慧合約語言，以其高效能共識機制聞名。

## Clojure 與區塊鏈

Clojure 的不可變性使其適合區塊鏈開發：

```clojure
;; 簡化區塊結構
(defrecord Block [index timestamp data prev-hash hash])

;; 創建新區塊
(defn create-block [index data prev-hash]
  (let [timestamp (System/currentTimeMillis)
        hash (calculate-hash index timestamp data prev-hash)]
    (->Block index timestamp data prev-hash hash)))

;; 創建創世塊
(def genesis-block
  (create-block 0 "Genesis Block" "0"))
```

## 為何區塊鏈偏好函數式語言？

### 不可變性

區塊鏈的本质是不可變的——歷史記錄不可更改。函數式語言的不可變資料結構完美契合這一特性。

### 可推斷性

純函式易於形式化驗證，對於金融合約至關重要。

### 並發安全

函數式語言的並發特性適合區塊鏈的分散式環境。

## 未來展望

2016 年區塊鏈技術剛開始發展，但函數式語言在這個領域的潛力已經顯現：

- Cardano 持續發展 Haskell 生態
- Rust 在區塊鏈開發中的採用率不斷上升
- 更多函數式區塊鏈框架出現

延伸閱讀：
- [Google 搜尋：Haskell blockchain smart contracts](https://www.google.com/search?q=Haskell+blockchain+smart+contracts)
- [Google 搜尋：Rust blockchain development](https://www.google.com/search?q=Rust+blockchain+development)