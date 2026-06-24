# 取代與置換網路

## SPN 結構概論

取代與置換網路（Substitution-Permutation Network, SPN）是現代區塊密碼的核心設計範式。它由 Claude Shannon 提出的混淆與擴散原則衍生而來，是 AES 等加密標準的基礎。

SPN 的核心思想是將多個較小的、可管理的密碼操作——即 S-box（取代盒）和 P-box（置換盒）——組合在一起，經過多輪疊代，產生強大的整體加密效果。

## S-box：取代操作

S-box 是一個查詢表，將固定大小的輸入位元組映射到輸出位元組。例如，AES 的 S-box 是一個 16×16 的表，輸入 8 位元，輸出 8 位元。

S-box 的設計至關重要，需要滿足以下標準：

- **非線性**：S-box 必須是非線性的，即其輸出不能表示為輸入的線性組合。這對抵抗線性密碼分析至關重要。
- **差分均勻性**：良好的 S-box 能抵抗差分密碼分析
- **代數複雜度**：S-box 的代數表達式應盡可能複雜
- **雪崩效應**：輸入的微小變化應導致輸出的顯著變化

AES 的 S-box 基於有限域 GF(2^8) 中的乘法逆元和仿射變換。其代數表達式為：

```
S(x) = A × x^(-1) + b
```

其中 A 是可逆的仿射矩陣，b 是常數向量，x^(-1) 是 x 在 GF(2^8) 中的乘法逆元。

S-box 的查表實作非常高效：

```python
AES_SBOX = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5,
    0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    # ... 共 256 個值
]
def sub_bytes(state):
    return [[AES_SBOX[b] for b in row] for row in state]
```

## P-box：置換操作

P-box 負責對資料位元進行重新排列，以實現擴散效果。在 AES 中，ShiftRows 和 MixColumns 兩個步驟共同完成了置換的功能。

**ShiftRows**：將狀態矩陣的每一行向左循環移位不同的位元組數：
- 第 0 行不移位
- 第 1 行移位 1 位元組
- 第 2 行移位 2 位元組
- 第 3 行移位 3 位元組

**MixColumns**：將狀態矩陣的每一列視為 GF(2^8) 上的多項式，與固定多項式進行乘法運算。這確保了在一列中的任何修改都會擴散到整列。

## 輪函數的組合

在 SPN 中，一輪加密的標準流程為：

```
SubBytes → ShiftRows → MixColumns → AddRoundKey
```

最後一輪省略 MixColumns。這個流程經過多次迭代（AES-128 為 10 次），使得明文與密文之間的關係極其複雜。

## SPN 與 Feistel 的比較

| 特性 | SPN | Feistel |
|:---|:---|:---|
| 結構 | 平行取代+置換 | 左右交替處理 |
| 加密逆操作 | 需要反向 S-box | 相同結構（反向金鑰） |
| 擴散速度 | 更快 | 較慢 |
| 硬體占用 | 較大（同時需要加密/解密電路） | 較小 |
| 代表演算法 | AES, PRESENT | DES, Blowfish, Twofish |

SPN 的擴散比 Feistel 網路更快，通常需要更少的輪數。但 Feistel 網路的優勢在於加密和解密可以使用相同的硬體電路。

## 延伸閱讀

- [SPN 結構介紹](https://www.google.com/search?q=substitution+permutation+network)
- [AES S-box 設計](https://www.google.com/search?q=AES+S-box+design+principles)
- [差分密碼分析](https://www.google.com/search?q=differential+cryptanalysis)
- [線性密碼分析](https://www.google.com/search?q=linear+cryptanalysis)

---

*本篇文章為「AI 程式人雜誌 2023 年 7 月號」精選文章。*
