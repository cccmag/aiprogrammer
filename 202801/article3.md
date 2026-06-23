# 測試自動生成策略

## 1. 引言

軟體測試是確保程式碼品質的關鍵，卻也是開發者最不願意花時間的環節。AI 輔助的測試自動生成技術正在改變這個局面——從單元測試到整合測試，從邊界條件到回歸測試，AI 可以在幾秒鐘內生成人類需要數小時才能完成的測試覆蓋。

## 2. 測試生成的三大策略

### 2.1 基於程式碼分析的生成

最直接的方法：給定原始碼，讓模型生成對應的測試案例。這種方法適合單元測試，模型可以分析函式的輸入輸出、邊界條件、異常路徑。

```python
# 給定函式
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# AI 生成的測試
def test_divide():
    assert divide(10, 2) == 5.0
    assert divide(0, 5) == 0.0
    assert divide(-6, 3) == -2.0
    import pytest
    with pytest.raises(ValueError):
        divide(1, 0)
```

### 2.2 基於規格的生成

從型別簽名、docstring、介面定義生成測試。這種方法在 TDD（測試驅動開發）場景特別有用——先定義介面，讓 AI 生成測試，再實現功能。

```python
def sort_list(items: list[int]) -> list[int]:
    """將整數列表由小到大排序，不回傳新的列表。"""
    # AI 先從規格生成測試
```

### 2.3 基於執行的增強

傳統模糊測試（fuzzing）與 AI 的結合。AI 分析程式碼的執行路徑，生成能觸發特定分支的輸入值，搭配 coverage-guided 策略最大化測試覆蓋率。

## 3. 實戰工具

| 工具 | 策略 | 語言支援 |
|------|------|---------|
| CodiumAI | 程式碼分析+生成 | Python、JS、Java |
| Diffblue Cover | 深度學習模型 | Java |
| EvoSuite | 演化演算法 | Java |
| pytest-copilot | Copilot 整合 | Python |

## 4. 品質評估

自動生成的測試需要評估三個維度：

1. **覆蓋率**：行覆蓋、分支覆蓋、突變覆蓋
2. **正確性**：測試是否真的通過（false positive 與 false negative）
3. **可讀性**：測試名稱是否清晰，斷言是否合理

研究顯示，AI 生成的測試在覆蓋率上通常優於人工撰寫的測試，但在邊界條件和異常處理的完整性上仍有差距。

## 5. 挑戰與未來

測試自動生成面臨的主要挑戰包括：

- **斷言品質**：生成「總是通過」的無效測試
- **環境依賴**：需要資料庫、網路服務的整合測試
- **假陽性**：測試依賴實作細節，重構時誤報

未來的方向是「自我修復測試」——當程式碼變更導致測試失敗時，AI 判斷是測試需要更新還是程式碼有 bug。

---

## 延伸閱讀

- [CodiumAI 測試生成](https://www.google.com/search?q=CodiumAI+automated+test+generation)
- [Diffblue Cover 介紹](https://www.google.com/search?q=Diffblue+Cover+AI+testing)
- [EvoSuite 演化測試](https://www.google.com/search?q=EvoSuite+evolutionary+testing)
- [Test Generation with LLMs 論文](https://www.google.com/search?q=LLM+test+generation+survey+paper)
