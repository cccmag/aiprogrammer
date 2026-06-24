# 電腦視覺與影像處理

## Canvas 基礎

```javascript
var canvas = document.getElementById('myCanvas');
var ctx = canvas.getContext('2d');
ctx.fillStyle = 'red';
ctx.fillRect(0, 0, 100, 100);
```

## 影像處理

```javascript
var img = new Image();
img.onload = function() {
    ctx.drawImage(img, 0, 0);
    var imageData = ctx.getImageData(0, 0, width, height);
    // 處理像素
};
img.src = 'photo.jpg';
```

## 結論

Canvas 開啟了客戶端影像處理的大門。

---

**延伸閱讀**

- [Canvas+image+processing](https://www.google.com/search?q=Canvas+image+processing)