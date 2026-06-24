# 程式實作：合成資料生成器

## 簡介

本實作建構一個多功能合成資料生成器，支援文字、表格與程式碼三種資料類型的合成生成。完整程式碼在 `_code/synthetic_data.py`。

## 核心元件

### 1. 文字合成

```python
gen = SyntheticDataGenerator()
records = gen.generate_text(5)
for r in records:
    print(f"[{r.label}] {r.text}")
```

### 2. 表格合成

```python
rows = gen.generate_table(3)
# 返回結構化 dict 列表，含特徵與標籤
```

### 3. 程式碼合成

```python
code = gen.generate_code("class")
# 支援 function / class / test 三種模式
```

## 執行方式

```bash
cd _code
python3 synthetic_data.py
```

## 延伸練習

1. **自訂模板**：擴展 `TEMPLATES` 列表，加入特定領域的文字模板
2. **條件生成**：根據指定標籤比例生成平衡資料集
3. **對抗品質評估**：實作分類器來區分合成資料與真實資料
4. **差分隱私合成**：為表格資料加入拉普拉斯雜訊
5. **多語言擴展**：加入中文模板與詞彙生成中文合成資料
