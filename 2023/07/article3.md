# AES 結構詳解

## Rijndael 的設計哲學

AES（Advanced Encryption Standard）的核心演算法 Rijndael 由比利時密碼學家 Joan Daemen 和 Vincent Rijmen 設計。其設計哲學可以概括為三個關鍵詞：簡潔、效率與安全。

Daemen 和 Rijmen 在設計時遵循了以下原則：
- 使用寬軌策略（Wide Trail Strategy）抵抗差分和線性密碼分析
- 所有操作在有限域 GF(2^8) 中定義，確保數學上的清晰性
- 設計適合在現代 CPU 上高效實作的結構

## 狀態矩陣

AES 將 128 位元（16 位元組）的資料組織成 4×4 的位元組矩陣（State）：

```
輸入 [a0, a1, ..., a15]
      ┌────┬────┬────┬────┐
      │ a0 │ a4 │ a8 │ a12│
      ├────┼────┼────┼────┤
      │ a1 │ a5 │ a9 │ a13│
      ├────┼────┼────┼────┤
      │ a2 │ a6 │ a10│ a14│
      ├────┼────┼────┼────┤
      │ a3 │ a7 │ a11│ a15│
      └────┴────┴────┴────┘
```

AES 的所有操作都是在這個 4×4 位元組矩陣上進行的。

## 金鑰擴展

AES 的金鑰擴展（Key Expansion）從初始金鑰生成所有輪金鑰（Round Key）。對於 AES-128（10 輪），需要 11 個 128 位元的輪金鑰。

輪金鑰的生成使用 XOR 和 S-box 操作，確保不同的輪使用不同的金鑰，防止金鑰相關攻擊。

```python
def key_expansion(key, rounds=10):
    # key: 16 bytes
    w = [list(key[i:i+4]) for i in range(0, 16, 4)]
    for i in range(4, 4 * (rounds + 1)):
        temp = w[i-1].copy()
        if i % 4 == 0:
            # RotWord
            temp = temp[1:] + temp[:1]
            # SubWord
            temp = [SBOX[b] for b in temp]
            # XOR with RCON
            temp[0] ^= RCON[i // 4]
        w.append([w[i-4][j] ^ temp[j] for j in range(4)])
    return w
```

## 四步驟詳解

### 1. SubBytes

SubBytes 對狀態矩陣中的每個位元組應用 S-box 進行非線性替代。S-box 是 AES 中唯一的非線性操作，是抵抗線性密碼分析的關鍵。

S-box 在 GF(2^8) 中計算乘法逆元後進行仿射變換，確保了良好的非線性特性。

### 2. ShiftRows

ShiftRows 對狀態矩陣的行進行循環左移位。這一操作確保了列的混合——經過 ShiftRows 後，一列的資料被分散到多列中。

### 3. MixColumns

MixColumns 將狀態矩陣的每列視為 GF(2^8) 上的 4 項多項式，與固定多項式 c(x) = 03x³ + 01x² + 01x + 02 進行乘法運算。

這一操作確保了擴散效果：改變一個位元組會影響所在列的全部 4 個位元組。

```python
def mix_columns(state):
    def galois_mul(a, b):
        # GF(2^8) multiplication
        r = 0
        for _ in range(8):
            if b & 1:
                r ^= a
            a = (a << 1) ^ (0x11B if a & 0x80 else 0)
            b >>= 1
        return r
    for c in range(4):
        a = [state[r][c] for r in range(4)]
        state[0][c] = galois_mul(2, a[0]) ^ galois_mul(3, a[1]) ^ a[2] ^ a[3]
        state[1][c] = a[0] ^ galois_mul(2, a[1]) ^ galois_mul(3, a[2]) ^ a[3]
        state[2][c] = a[0] ^ a[1] ^ galois_mul(2, a[2]) ^ galois_mul(3, a[3])
        state[3][c] = galois_mul(3, a[0]) ^ a[1] ^ a[2] ^ galois_mul(2, a[3])
```

### 4. AddRoundKey

AddRoundKey 將當前輪的輪金鑰與狀態矩陣進行 XOR。這是唯一直接使用金鑰的步驟。

## 解密流程

AES 的解密需要執行逆向操作：

```
InvShiftRows → InvSubBytes → AddRoundKey → InvMixColumns
```

注意 AddRoundKey 是其自身的反操作（XOR 的性質）。

## 效能優化

在現代 CPU 上，AES 通常使用查表法（T-table）進行優化，將 SubBytes、ShiftRows 和 MixColumns 合併為 4 個 8KB 的查詢表。支援 AES-NI 指令集的 CPU 可以在硬體層級直接執行 AES 操作，達到極高的吞吐量。

## 延伸閱讀

- [AES FIPS-197 標準](https://www.google.com/search?q=AES+FIPS+197+official+standard)
- [Rijndael 設計文件](https://www.google.com/search?q=Rijndael+AES+design+Daemen+Rijmen)
- [AES-NI 指令集](https://www.google.com/search?q=AES-NI+hardware+acceleration)
- [寬軌策略](https://www.google.com/search?q=wide+trail+strategy+AES)

---

*本篇文章為「AI 程式人雜誌 2023 年 7 月號」精選文章。*
