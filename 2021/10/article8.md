# (property-based testing) 屬性測試

## 屬性測試 vs 範例測試

傳統的範例測試（example-based testing）用特定輸入驗證輸出：

```python
def test_add_two_numbers():
    assert add(2, 3) == 5
```

屬性測試（property-based testing）驗證的是輸入輸出間的通用屬性：

```python
from hypothesis import given, strategies as st

@given(st.integers(), st.integers())
def test_add_commutative(a, b):
    assert add(a, b) == add(b, a)
```

這個測試會自動產生數百種輸入組合。

## Hypothesis 快速入門

```bash
pip install hypothesis
```

```python
from hypothesis import given, strategies as st

@given(st.integers())
def test_double_is_not_identity(n):
    assert 2 * n != n or n == 0
```

Hypothesis 會嘗試各種整數，包括邊界情況如 0、負數、超大數。

## 通用屬性

常見的屬性包括：

- **交換律**：`f(a, b) == f(b, a)`
- **結合律**：`f(f(a, b), c) == f(a, f(b, c))`
- **同一性**：`f(a, identity) == a`
- **反向性**：`f(a) == inverse(inverse(a))`

## 複合策略

```python
from hypothesis import given, strategies as st

# 複合多個策略
@given(st.lists(st.integers(min_value=1, max_value=100), min_size=1))
def test_list_sorting(lst):
    sorted_lst = sorted(lst)
    assert all(sorted_lst[i] <= sorted_lst[i+1] for i in range(len(sorted_lst)-1))

# 生成更複雜的資料
@given(st.dictionaries(
    keys=st.text(min_size=1),
    values=st.integers(),
    min_size=1
))
def test_dict_keys_not_none(d):
    assert None not in d.keys()
```

## 假設（Assumptions）

只測試有效的輸入：

```python
@given(st.integers(), st.integers())
def test_division(a, b):
    assume(b != 0)  # 只測試非零除數
    assert a / b is not None
```

## 尋找反例

當 Hypothesis 找到失敗的輸入，會嘗試簡化它並給出最小反例：

```
Falsifying example: test_division(a=0, b=0)
```

這極大地幫助偵錯。

## 應用場景

屬性測試特別適合：
- 數學計算函式
- 序列化和反序列化
- 資料結構操作
- 加密/壓縮等有確定性屬性的演算法

## 結論

屬性測試能發現範例測試難以捕捉的邊界問題和隱藏假設。配合 Hypothesis，讓這種強大的測試方法變得簡單。