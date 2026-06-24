# jQuery UI 元件庫

## jQuery UI 簡介

jQuery UI 是基於 jQuery 的 UI 元件庫，提供互動、元件和效果。

## 互動（Interactions）

### Draggable

```javascript
$('#draggable').draggable({
    axis: 'y',              // 只允許垂直拖曳
    handle: '.handle',      // 把手元素
    containment: 'parent',  // 限制在父元素內
    cursor: 'move',
    opacity: 0.5,
    revert: true,           // 放開時回到原位
    start: function(event, ui) {
        console.log('Drag started');
    },
    stop: function(event, ui) {
        console.log('Drag stopped');
    }
});
```

### Droppable

```javascript
$('#droppable').droppable({
    accept: '.item',         // 接受的元素
    hoverClass: 'highlight', // 放置時的類別
    drop: function(event, ui) {
        $(this).addClass('dropped');
        console.log('Item dropped!');
    }
});
```

### Resizable

```javascript
$('#resizable').resizable({
    handles: 'e, s, se',    // 調整把手
    minWidth: 100,
    minHeight: 100,
    maxWidth: 500,
    maxHeight: 500,
    alsoResize: '.mirror',  // 同步調整其他元素
    resize: function(event, ui) {
        console.log('Size:', ui.size);
    }
});
```

### Selectable

```javascript
$('#selectable').selectable({
    filter: 'li',           // 可選擇的元素
    selected: function(event, ui) {
        console.log('Selected');
    }
});
```

### Sortable

```javascript
$('#sortable').sortable({
    placeholder: 'placeholder',
    update: function(event, ui) {
        console.log('Order changed');
    }
});
```

## 元件（Widgets）

### Dialog

```javascript
$('#dialog').dialog({
    autoOpen: false,
    modal: true,
    buttons: {
        '確定': function() {
            $(this).dialog('close');
        },
        '取消': function() {
            $(this).dialog('close');
        }
    },
    title: '標題',
    width: 400,
    open: function(event, ui) {
        console.log('Dialog opened');
    },
    close: function(event, ui) {
        console.log('Dialog closed');
    }
});

// 開啟對話框
$('#dialog').dialog('open');

// 關閉對話框
$('#dialog').dialog('close');
```

### Datepicker

```javascript
$('#date').datepicker({
    dateFormat: 'yy-mm-dd',
    showButtonPanel: true,
    changeMonth: true,
    changeYear: true,
    minDate: new Date(2008, 0, 1),
    maxDate: new Date(2008, 11, 31),
    defaultDate: new Date(2008, 5, 15),
    onSelect: function(dateText, inst) {
        console.log('Selected:', dateText);
    }
});
```

### Autocomplete

```javascript
var availableTags = ['ActionScript', 'AppleScript', 'Asp', 'BASIC'];
$('#tags').autocomplete({
    source: availableTags,
    minLength: 2,
    select: function(event, ui) {
        console.log('Selected:', ui.item.value);
    }
});

// 動態資料
$('#search').autocomplete({
    source: function(request, response) {
        $.ajax({
            url: '/api/search',
            data: { q: request.term },
            success: function(data) {
                response(data);
            }
        });
    }
});
```

### Tabs

```javascript
$('#tabs').tabs({
    collapsible: true,
    selected: 0,
    show: function(event, ui) {
        console.log('Tab shown:', ui.index);
    },
    select: function(event, ui) {
        console.log('Tab selected:', ui.index);
    }
});

// 程式控制
$('#tabs').tabs('select', 2);  // 切換到第三個標籤
```

### Accordion

```javascript
$('#accordion').accordion({
    collapsible: true,
    autoHeight: false,
    navigation: true,
    change: function(event, ui) {
        console.log('Section changed');
    }
});
```

## 結論

jQuery UI 提供了豐富的互動和元件，大幅加速前端開發。其主題系統也方便自訂外觀。

---

**延伸閱讀**

- [jQuery 的設計哲學](focus1.md)
- [jQuery+UI+documentation](https://www.google.com/search?q=jQuery+UI+documentation)