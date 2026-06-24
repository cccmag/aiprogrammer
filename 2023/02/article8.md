# 頁面置換演算法

## 問題背景

在虛擬記憶體系統中，當一個行程試圖存取不在實體記憶體中的頁面時，發生頁錯誤（page fault）。作業系統需要將所需的頁面從磁碟載入到記憶體。如果實體記憶體已滿，則需要選擇一個現有頁面「犧牲」——將它換出到磁碟，騰出空間給新頁面。

頁面置換演算法就是決定「哪個頁面應該被換出」的策略。

## 演算法評估指標

- **頁錯誤率**：頁錯誤次數 / 記憶體存取次數（越低越好）
- **時間開銷**：演算法本身的執行時間（應盡可能低）
- **空間開銷**：需要的額外資料結構

## 經典演算法

### FIFO（先進先出）

最簡單的演算法：選擇在記憶體中停留時間最久的頁面置換。

```python
def fifo(ref_string, frames):
    memory = []
    faults = 0
    for page in ref_string:
        if page not in memory:
            if len(memory) >= frames:
                memory.pop(0)  # 移除最先進入的頁面
            memory.append(page)
            faults += 1
    return faults
```

**Belady 異常**：FIFO 違反直覺——增加框架數量有時反而增加頁錯誤率！

### LRU（最近最少使用）

選擇最久未使用的頁面置換。基於時間局部性原理——最近使用的頁面很可能近期再次使用。

```python
def lru(ref_string, frames):
    memory = []
    faults = 0
    for page in ref_string:
        if page in memory:
            memory.remove(page)  # 重新排序
        else:
            if len(memory) >= frames:
                memory.pop(0)  # 移除最久未使用的
            faults += 1
        memory.append(page)     # 移到最近使用位置
    return faults
```

**實作挑戰**：精確的 LRU 需要記錄每次存取的時間戳或維護堆疊，開銷較大。

### OPT（最優置換）

選擇未來最晚才會被存取的頁面置換。這是理論最優解——頁錯誤率最低。

```python
def opt(ref_string, frames):
    memory = []
    faults = 0
    for i, page in enumerate(ref_string):
        if page not in memory:
            if len(memory) >= frames:
                farthest = -1; victim = None
                for m in memory:
                    try:
                        pos = ref_string.index(m, i+1)
                    except ValueError:
                        pos = len(ref_string)
                    if pos > farthest:
                        farthest = pos; victim = m
                memory.remove(victim)
            memory.append(page)
            faults += 1
    return faults
```

**限制**：無法在實際系統中使用——需要預知未來的記憶體存取模式。

### Clock（NRU, 時鐘演算法）

Clock 演算法是 LRU 的近似實作，也稱為「二次機會演算法」：

1. 維護一個循環鏈表和一個參考位元（referenced bit）
2. 當需要置換時，週圍巡視頁面
3. 如果參考位元為 0：選擇該頁面置換
4. 如果參考位元為 1：清除為 0，繼續巡視

```
初始： [P7(1)] → [P0(1)] → [P1(1)] → [P2(1)]
                        ↑ (時針)
頁錯誤時巡視：
[P7(0)] → [P0(0)] → [P1(0)] → [P2(1)] → 選擇 P7
```

### LFU（最少使用）

選擇被存取次數最少的頁面置換。需要維護每個頁面的存取計數器。

**問題**：早期頻繁使用但後期不再使用的頁面會長期滯留。

## 演算法比較

以經典參照序列 `[7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7]` 測試（3 個框架）：

| 演算法 | 頁錯誤次數 | 優點 | 缺點 |
|--------|-----------|------|------|
| FIFO | 15 | 最簡單 | Belady 異常 |
| LRU | 12 | 效能好 | 實作開銷大 |
| OPT | 9 | 理論最優 | 無法實作 |
| Clock | ~12-13 | 接近 LRU | 依賴參考位元精度 |

## 框架分配

除了置換演算法，框架分配策略也影響效能：

- **固定分配**：每個行程獲得固定數量的框架
- **可變分配**：根據行程行為調整框架數量
- **全域置換**：從所有行程中選擇頁面置換
- **局部置換**：只從觸發頁錯誤的行程中選擇

現代系統通常使用可變分配 + 全域置換 + Clock 近似。

## 延伸閱讀

- [頁面置換演算法視覺化](https://www.google.com/search?q=page+replacement+algorithm+visualization+simulation)
- [Belady 異常](https://www.google.com/search?q=Belady%27s+anomaly+FIFO+page+replacement)
- [Linux 頁面置換](https://www.google.com/search?q=Linux+kernel+page+replacement+algorithm+LRU+Clock)
