# jQuery 程式實作

## DOM 操作範例

```html
<!DOCTYPE html>
<html>
<head>
    <script src="jquery-1.2.6.min.js"></script>
</head>
<body>
    <div id="container">
        <h1>標題</h1>
        <p class="intro">介紹文字</p>
        <ul id="list">
            <li>項目 1</li>
            <li>項目 2</li>
        </ul>
    </div>
    <script>
        $(document).ready(function() {
            // 選擇和操作
            $('#container').addClass('active');
            $('.intro').text('新文字');
            $('ul').find('li').first().css('color', 'red');

            // 事件處理
            $('#list li').click(function() {
                $(this).toggleClass('selected');
            });
        });
    </script>
</body>
</html>
```

## Ajax 請求範例

```javascript
$(document).ready(function() {
    // 載入 HTML
    $('#content').load('/api/html');

    // GET 請求
    $.get('/api/users', { limit: 10 }, function(users) {
        $.each(users, function(i, user) {
            $('#list').append('<li>' + user.name + '</li>');
        });
    });

    // POST 請求
    $.post('/api/submit', { name: 'John' }, function(response) {
        console.log(response);
    });

    // 完整 Ajax
    $.ajax({
        url: '/api/data',
        type: 'POST',
        dataType: 'json',
        data: { key: 'value' },
        success: function(data) {
            console.log(data);
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
});
```

## 動畫效果

```javascript
// 基礎動畫
$('#box').fadeIn();
$('#box').fadeOut();
$('#box').slideUp();
$('#box').slideDown();
$('#box').toggle();

// 自訂動畫
$('#box').animate({
    left: '100px',
    top: '50px',
    opacity: 0.5
}, 300, 'swing', function() {
    console.log('Animation complete');
});

// 鏈式動畫
$('#box')
    .fadeIn()
    .delay(1000)
    .fadeOut()
    .delay(500)
    .slideUp();
```

## 執行說明

```bash
# 包含 jQuery
# <script src="jquery-1.2.6.min.js"></script>

# 或使用 CDN
# <script src="http://code.jquery.com/jquery-1.2.6.min.js"></script>
```

## 參考資源

- [jQuery+documentation](https://www.google.com/search?q=jQuery+1.2+documentation)
- [jQuery+Ajax+tutorial](https://www.google.com/search?q=jQuery+Ajax+tutorial)