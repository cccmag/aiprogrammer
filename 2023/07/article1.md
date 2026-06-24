# 凱薩密碼與維吉尼亞密碼

## 古典密碼的智慧

古典密碼學雖然在現代標準下已不安全，但它們所體現的加密思想至今仍影響著密碼設計。凱薩密碼和維吉尼亞密碼是其中最經典的兩個代表。

## 凱薩密碼的變體

凱薩密碼是移位密碼（Shift Cipher）的一種，其金鑰空間僅有 25 個有效值。除了 Caesar 使用的 3 位移位，還有其他知名的變體：

**ROT13**：移位量為 13 的凱薩密碼，在英文中有個有趣的特性——加密和解密是同一操作（因為 13 + 13 = 26）。ROT13 常用於線上論壇隱藏劇透內容，並非真正的加密。

**Atbash**：將字母表反轉（A ↔ Z, B ↔ Y, ...），這是一種特殊的移位密碼。Atbash 在聖經時代就有使用，在某些《聖經》經文中可以找到。

## 密碼分析入門

凱薩密碼的破解可以通過暴力搜尋完成——嘗試所有 25 種移位，找到其中有意義的明文。這在 Python 中可以輕鬆實現：

```python
def caesar_bruteforce(ciphertext):
    for shift in range(26):
        plain = caesar_decrypt(ciphertext, shift)
        print(f"shift {shift}: {plain}")
```

對於維吉尼亞密碼，破解需要兩個步驟：首先確定金鑰長度（使用 Kasiski 測試或重合指數法），然後對每個分組獨立進行頻率分析。

**重合指數（Index of Coincidence, IC）** 是一種統計度量，用於判斷密文是否源自單表替代或多表替代。英文隨機文字的 IC 約為 0.038，而英文自然語言的 IC 約為 0.065。通過分析密文的 IC 值，可以推測金鑰長度。

## 自動化破解維吉尼亞密碼

以下是一個簡化的 Kasiski 測試 Python 實作：

```python
def kasiski_examination(ciphertext, max_key_length=20):
    from math import gcd
    from functools import reduce
    distances = []
    for seq_len in range(3, 6):
        seq_positions = {}
        for i in range(len(ciphertext) - seq_len):
            seq = ciphertext[i:i+seq_len]
            if seq in seq_positions:
                for pos in seq_positions[seq]:
                    distances.append(i - pos)
            else:
                seq_positions[seq] = []
            seq_positions[seq].append(i)
    if not distances:
        return None
    return reduce(gcd, distances)
```

## 維吉尼亞密碼的現代意義

雖然維吉尼亞密碼已不再安全，但它引入了兩個重要的現代密碼學概念：

**多表替代（Polyalphabetic Substitution）**：使用多個替代表來抵抗頻率分析。現代區塊密碼雖然使用更複雜的結構，但這一思想仍然核心。

**金鑰擴展（Key Expansion）**：將短金鑰擴展為長的金鑰流。維吉尼亞密碼通過重複金鑰來實現，現代密碼則使用更複雜的金鑰排程算法。

## 延伸閱讀

- [ROT13](https://www.google.com/search?q=ROT13+cipher)
- [Kasiski 測試詳解](https://www.google.com/search?q=Kasiski+examination+polyalphabetic)
- [重合指數](https://www.google.com/search?q=index+of+coincidence+cryptography)
- [Atbash 密碼](https://www.google.com/search?q=Atbash+cipher)

---

*本篇文章為「AI 程式人雜誌 2023 年 7 月號」精選文章。*
