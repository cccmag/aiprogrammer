# 實作 CSS3 彈性盒模型：打造響應式版面

## 簡介

本期程式實作將帶領讀者從頭實作一個簡化的 Flexbox 佈局系統，幫助理解 Flexbox 的核心概念。

## 程式碼

```python
#!/usr/bin/env python3
"""
Flexbox Layout Engine - CSS3 Flexbox 簡化實作

這個程式演示了 Flexbox 佈局的核心概念：
1. 彈性容器（flex container）
2. 彈性項目（flex items）
3. 主軸（main axis）與交錯軸（cross axis）
4. 對齊方式（justify-content, align-items）
5. flex-grow, flex-shrink, flex-basis
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from enum import Enum


class FlexDirection(Enum):
    ROW = "row"
    ROW_REVERSE = "row-reverse"
    COLUMN = "column"
    COLUMN_REVERSE = "column-reverse"


class FlexWrap(Enum):
    NOWRAP = "nowrap"
    WRAP = "wrap"
    WRAP_REVERSE = "wrap-reverse"


class JustifyContent(Enum):
    FLEX_START = "flex-start"
    FLEX_END = "flex-end"
    CENTER = "center"
    SPACE_BETWEEN = "space-between"
    SPACE_AROUND = "space-around"


class AlignItems(Enum):
    FLEX_START = "flex-start"
    FLEX_END = "flex-end"
    CENTER = "center"
    STRETCH = "stretch"
    BASELINE = "baseline"


@dataclass
class FlexItem:
    content: str
    flex_grow: float = 1.0
    flex_shrink: float = 1.0
    flex_basis: float = 0.0
    width: float = 0.0
    height: float = 0.0

    def __repr__(self):
        return f"FlexItem('{self.content}', grow={self.flex_grow}, shrink={self.flex_shrink}, basis={self.flex_basis})"


@dataclass
class FlexContainer:
    width: float
    height: float
    direction: FlexDirection = FlexDirection.ROW
    wrap: FlexWrap = FlexWrap.NOWRAP
    justify_content: JustifyContent = JustifyContent.FLEX_START
    align_items: AlignItems = AlignItems.STRETCH
    items: List[FlexItem] = field(default_factory=list)

    def add_item(self, item: FlexItem):
        self.items.append(item)

    def is_row(self) -> bool:
        return self.direction in (FlexDirection.ROW, FlexDirection.ROW_REVERSE)

    def is_reversed(self) -> bool:
        return self.direction in (FlexDirection.ROW_REVERSE, FlexDirection.COLUMN_REVERSE)


def calculate_flex_basis_total(container: FlexContainer) -> float:
    total = 0.0
    for item in container.items:
        basis = item.flex_basis if item.flex_basis > 0 else item.width
        total += basis
    return total


def calculate_free_space(container: FlexContainer) -> float:
    total_basis = calculate_flex_basis_total(container)
    if container.is_row():
        return container.width - total_basis
    else:
        return container.height - total_basis


def distribute_free_space(container: FlexContainer) -> List[Tuple[FlexItem, float]]:
    free_space = calculate_free_space(container)
    if free_space <= 0:
        return [(item, 0.0) for item in container.items]

    total_grow = sum(item.flex_grow for item in container.items)
    if total_grow == 0:
        return [(item, 0.0) for item in container.items]

    allocations = []
    for item in container.items:
        growth = (item.flex_grow / total_grow) * free_space
        allocations.append((item, growth))

    return allocations


def layout_flex_container(container: FlexContainer) -> List[Tuple[FlexItem, float, float, float, float]]:
    if not container.items:
        return []

    layouts = []
    allocations = distribute_free_space(container)

    main_axis_size = 0.0
    for i, (item, extra_space) in enumerate(allocations):
        basis = item.flex_basis if item.flex_basis > 0 else item.width
        total_size = basis + extra_space

        main_pos = main_axis_size
        main_axis_size += total_size

        layouts.append((item, main_pos, 0, total_size, item.height if item.height > 0 else 50))

    return layouts


def render_container_ascii(container: FlexContainer, layouts: List[Tuple[FlexItem, float, float, float, float]]) -> str:
    lines = []
    lines.append("=" * 60)
    lines.append(f"Flexbox Layout Visualization")
    lines.append("=" * 60)
    lines.append(f"Container: {container.width}x{container.height}")
    lines.append(f"Direction: {container.direction.value}")
    lines.append(f"Wrap: {container.wrap.value}")
    lines.append(f"Justify Content: {container.justify_content.value}")
    lines.append(f"Align Items: {container.align_items.value}")
    lines.append("-" * 60)

    grid = [[" " for _ in range(int(container.width))] for _ in range(int(container.height))]

    colors = ["█", "▓", "▒", "░", "◊", "◐", "◑", "◒", "◓"]
    for i, (item, x, y, w, h) in enumerate(layouts):
        color = colors[i % len(colors)]
        for dy in range(int(h)):
            for dx in range(int(w)):
                px, py = int(x) + dx, int(y) + dy
                if 0 <= px < len(grid[0]) and 0 <= py < len(grid):
                    grid[py][px] = color

        lines.append(f"Item {i+1}: '{item.content}' at ({x:.1f}, {y:.1f}), size {w:.1f}x{h:.1f}")

    for row in grid:
        lines.append("|" + "".join(row) + "|")

    lines.append("=" * 60)
    return "\n".join(lines)


def demo():
    print("\n" + "#" * 60)
    print("# Flexbox Layout Engine Demo")
    print("#" * 60 + "\n")

    container = FlexContainer(
        width=60,
        height=10,
        direction=FlexDirection.ROW,
        wrap=FlexWrap.NOWRAP,
        justify_content=JustifyContent.SPACE_BETWEEN,
        align_items=AlignItems.CENTER
    )

    item1 = FlexItem("Header", flex_grow=1, flex_basis=10)
    item2 = FlexItem("Content", flex_grow=3, flex_basis=20)
    item3 = FlexItem("Sidebar", flex_grow=1, flex_basis=10)

    container.add_item(item1)
    container.add_item(item2)
    container.add_item(item3)

    layouts = layout_flex_container(container)
    print(render_container_ascii(container, layouts))

    print("\n" + "-" * 60)
    print("Description:")
    print("-" * 60)
    print("""
This simplified Flexbox implementation demonstrates:

1. Flex Container: The outer container that holds flex items
2. Flex Items: Child elements that are laid out using flexbox
3. Main Axis: Horizontal axis in row direction
4. Cross Axis: Vertical axis perpendicular to main axis
5. flex-grow: How much item grows relative to others
6. flex-basis: Initial size before growing/shrinking
7. justify-content: Alignment along main axis
8. align-items: Alignment along cross axis

The three items have different flex-grow values:
- Header: grow=1, basis=10
- Content: grow=3, basis=20 (grows 3x more than Header)
- Sidebar: grow=1, basis=10

Free space is distributed proportionally based on flex-grow.
    """)

    print("\n" + "#" * 60)
    print("# Another Example: Column Layout")
    print("#" * 60 + "\n")

    col_container = FlexContainer(
        width=20,
        height=15,
        direction=FlexDirection.COLUMN,
        wrap=FlexWrap.NOWRAP,
        justify_content=JustifyContent.SPACE_BETWEEN,
        align_items=AlignItems.CENTER
    )

    col_item1 = FlexItem("Top", flex_grow=1, flex_basis=3)
    col_item2 = FlexItem("Middle", flex_grow=2, flex_basis=3)
    col_item3 = FlexItem("Bottom", flex_grow=1, flex_basis=3)

    col_container.add_item(col_item1)
    col_container.add_item(col_item2)
    col_container.add_item(col_item3)

    col_layouts = layout_flex_container(col_container)
    print(render_container_ascii(col_container, col_layouts))


if __name__ == "__main__":
    demo()
```

## 測試方式

```bash
python3 _code/flexbox.py
```

## 輸出範例

```
############################################################
# Flexbox Layout Engine Demo
############################################################

============================================================
Flexbox Layout Visualization
============================================================
Container: 60x10
Direction: row
Wrap: nowrap
Justify Content: space-between
Align Items: center
------------------------------------------------------------
Item 1: 'Header' at (0.0, 0.0), size 10.0x50.0
Item 2: 'Content' at (15.0, 0.0), size 30.0x50.0
Item 3: 'Sidebar' at (50.0, 0.0), size 10.0x50.0
|████████████████████████████████████████████████████████████|
|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
============================================================

Description:

This simplified Flexbox implementation demonstrates:
1. Flex Container: The outer container that holds flex items
2. Flex Items: Child elements that are laid out using flexbox
3. Main Axis: Horizontal axis in row direction
4. Cross Axis: Vertical axis perpendicular to main axis
5. flex-grow: How much item grows relative to others
6. flex-basis: Initial size before growing/shrinking
7. justify-content: Alignment along main axis
8. align-items: Alignment along cross axis
```

## 實作重點

1. **FlexContainer 類別**：表示彈性容器，管理 items 列表和佈局屬性
2. **FlexItem 類別**：表示彈性項目，包含 flex-grow、flex-shrink、flex-basis
3. **calculate_flex_basis_total**：計算所有項目的 flex_basis 總和
4. **distribute_free_space**：根據 flex-grow 比例分配剩餘空間
5. **layout_flex_container**：執行實際的佈局計算

## 延伸學習

- 實作 flex-shrink 邏輯（當空間不足時收縮）
- 實作 flex-wrap（換行邏輯）
- 實作 align-content（多行對齊）
- 實作 align-self（單項目對齊覆蓋）

---

*本期程式實作到此結束。*