# LZW 壓縮演算法

## 字典式壓縮

LZW（Lempel-Ziv-Welch）是一種字典式壓縮演算法，由 Abraham Lempel、Jacob Ziv 與 Terry Welch 發展而成。與 Huffman 和算術編碼不同，LZW 不需要事先知道符號的機率分布，而是動態建構一個字典來編碼重複出現的序列。

LZW 被廣泛應用於：
- GIF 影像格式
- Unix compress 指令
- 早期的 ZIP 實作

## 演算法原理

LZW 的核心思想是將重複出現的字串替換為一個字典索引。

### 編碼流程

1. 初始化字典包含所有單一字元
2. 從輸入讀取最長的字串 $W$ 存在於字典中
3. 輸出 $W$ 的索引
4. 將 $W$ 加上下一個字元加入字典
5. 回到步驟 2

### 解碼流程

解碼器維護相同的字典，將每個索引還原為字串。需要注意「KW」問題：當編碼器遇到一個尚未加入字典的序列時，解碼器需要特殊處理。

## Python 實作

```python
def lzw_encode(data):
    dictionary = {chr(i): i for i in range(256)}
    next_code = 256
    w = ""
    result = []
    for ch in data:
        wc = w + ch
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = next_code
            next_code += 1
            w = ch
    if w:
        result.append(dictionary[w])
    return result

def lzw_decode(codes):
    dictionary = {i: chr(i) for i in range(256)}
    next_code = 256
    w = chr(codes[0])
    result = [w]
    for code in codes[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = w + w[0]
        else:
            raise ValueError("Invalid code")
        result.append(entry)
        dictionary[next_code] = w + entry[0]
        next_code += 1
        w = entry
    return "".join(result)
```

## 範例

```python
text = "ABABABA"
encoded = lzw_encode(text)   # [65, 66, 256, 258]
decoded = lzw_decode(encoded) # "ABABABA"
```

在 "ABABABA" 中，"AB" 與 "ABA" 被分別編碼為 256 與 258，達到了壓縮效果。

## LZW 的優缺點

優點：
- 不需要事前統計，適合串流資料
- 解碼器簡單且效率高
- 對重複模式豐富的資料壓縮效果極佳

缺點：
- 字典大小有限，需處理溢出（GIF 使用 12-bit 索引）
- 對小檔案壓縮效果不佳（字典本身有開銷）
- 部分專利問題（已過期）

## 參考資源

- https://www.google.com/search?q=LZW+compression+algorithm+Lempel+Ziv+Welch+dictionary+encoding+working
- https://www.google.com/search?q=LZW+Python+implementation+encode+decode+tutorial+example
- https://www.google.com/search?q=LZW+GIF+format+compress+application+patent+history
