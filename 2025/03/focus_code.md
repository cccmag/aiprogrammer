# OOP 完整實作展示

## 前言

本篇文章展示了物件導向程式設計的核心概念在 Python 中的完整實作。完整的程式碼請參考 [_code/oop_basics.py](_code/oop_basics.py)，你可以直接執行它來觀察 OOP 的各項特性。

## 原始碼結構

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, name: str):
        self._name = name

    @abstractmethod
    def speak(self) -> str:
        pass

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value
```

### 類別層次結構

```
Animal (ABC)          Vector          AnimalFactory
  ├── Dog              ├── __add__      └── create_animal()
  └── Cat              ├── __sub__
                        └── __mul__
```

`Animal` 是抽象基底類別，定義了 `speak()` 抽象方法。`Dog` 和 `Cat` 繼承自 `Animal` 並各自實作 `speak()`。`Vector` 展示了運算子重載，`AnimalFactory` 實作了工廠模式。

### 多型與鴨子型別

```python
class Duck:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return f"{self.name} says 呱呱!"

def make_it_speak(entity) -> str:
    return entity.speak()
```

`Duck` 類別沒有繼承 `Animal`，但因為它也有 `speak()` 方法，所以可以與 `Dog`、`Cat` 一起被 `make_it_speak()` 函式處理。這就是 Python 著名的鴨子型別。

### 工廠模式

```python
class AnimalFactory:
    @staticmethod
    def create_animal(animal_type: str, name: str, **kwargs) -> Animal:
        if animal_type == "dog":
            return Dog(name, kwargs.get("breed", "米克斯"))
        elif animal_type == "cat":
            return Cat(name, kwargs.get("color", "橘色"))
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")
```

工廠模式將物件的建立邏輯集中管理，客戶端只需提供類型參數即可獲得對應的物件實體。

## 執行結果

執行 `python3 _code/oop_basics.py` 可以看到：

```
[1] 類別與繼承
來福 says 汪汪!
小花 says 喵喵!

[2] 屬性封裝
狗的名稱: 來福, 品種: 黃金獵犬

[3] 多型與鴨子型別
阿福 says 汪汪!
小花 says 喵喵!
唐老鴨 says 呱呱!

[4] 運算子重載
v1 + v2 = Vector(6, 8)
v1 - v2 = Vector(-2, -2)

[5] 工廠模式
小白 says 汪汪!
咪咪 says 喵喵!

[6] 抽象基底類別
無法實例化抽象類別: Can't instantiate abstract class Animal...
```

## 結論

這個範例涵蓋了 OOP 的六大核心概念：類別與物件、繼承、封裝、多型、運算子重載以及工廠模式。透過實際執行程式碼，你可以更直觀地理解這些抽象概念的具體表現。

## 延伸閱讀

- [Python ABC 官方文件](https://www.google.com/search?q=Python+abc+module)
- [Python @property 裝飾器](https://www.google.com/search?q=Python+property+decorator)
- [Python 資料模型](https://www.google.com/search?q=Python+data+model+magic+methods)
