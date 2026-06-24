# 常用 HTML 標籤

## 文字與標題

### 標題標籤

HTML 提供 h1 到 h6 六個層級的標題：

```html
<h1>一級標題（頁面主標題）</h1>
<h2>二級標題（區塊標題）</h2>
<h3>三級標題</h3>
<h4>四級標題</h4>
<h5>五級標題</h5>
<h6>六級標題</h6>
```

每個頁面應該只有一個 h1，用於描述頁面主題。標題層級不應跳級（不要從 h1 直接跳到 h3）。

### 段落與文字格式化

```html
<p>這是一個段落。段落之間會自動產生垂直間距。</p>

<strong>重要文字（粗體）</strong>
<em>強調文字（斜體）</em>
<mark>標記文字</mark>
<small>次要文字</small>
<del>刪除文字</del>
<ins>插入文字</ins>
<sup>上標</sup><sub>下標</sub>
<br>換行
```

### 引用

```html
<blockquote>
  <p>這是一段長引用。</p>
</blockquote>

<q>短引用</q> — <cite>來源名稱</cite>
```

---

## 連結與圖片

### 超連結

```html
<!-- 外部連結 -->
<a href="https://example.com">造訪 Example</a>

<!-- 內部頁面 -->
<a href="/about.html">關於我們</a>

<!-- 頁面錨點 -->
<a href="#section2">跳到第二節</a>

<!-- 開啟新分頁 -->
<a href="https://example.com" target="_blank" rel="noopener">
  新分頁開啟
</a>
```

### 圖片

```html
<img src="photo.jpg" alt="描述文字" width="800" height="600" loading="lazy">
```

alt 屬性對無障礙和 SEO 非常重要。loading="lazy" 啟用延遲載入。

### 圖片與連結組合

```html
<a href="detail.html">
  <img src="thumbnail.jpg" alt="縮圖描述">
</a>
```

---

## 列表

### 無序列表

```html
<ul>
  <li>項目一</li>
  <li>項目二</li>
  <li>項目三</li>
</ul>
```

### 有序列表

```html
<ol>
  <li>第一步</li>
  <li>第二步</li>
  <li>第三步</li>
</ol>
```

### 定義列表

```html
<dl>
  <dt>HTML</dt>
  <dd>超文本標記語言，用於建立網頁結構</dd>
  <dt>CSS</dt>
  <dd>層疊樣式表，用於控制網頁外觀</dd>
</dl>
```

---

## 表格

```html
<table>
  <caption>每月銷售報表</caption>
  <thead>
    <tr>
      <th>月份</th>
      <th>銷售額</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>一月</td>
      <td>$10,000</td>
    </tr>
    <tr>
      <td>二月</td>
      <td>$12,000</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td>總計</td>
      <td>$22,000</td>
    </tr>
  </tfoot>
</table>
```

---

## 表單元素

### 文字輸入

```html
<input type="text" name="username" placeholder="輸入帳號" required>
<input type="email" name="email" placeholder="Email">
<input type="password" name="password" autocomplete="current-password">
<input type="search" name="q" placeholder="搜尋...">
<textarea name="bio" rows="4" cols="50">個人簡介</textarea>
```

### 選項輸入

```html
<select name="country">
  <option value="">請選擇國家</option>
  <option value="tw">台灣</option>
  <option value="jp">日本</option>
</select>

<input type="radio" name="gender" value="male"> 男性
<input type="radio" name="gender" value="female"> 女性

<input type="checkbox" name="agree"> 同意條款
```

### 按鈕

```html
<button type="submit">送出</button>
<button type="reset">重設</button>
<button type="button">自訂功能</button>
<input type="submit" value="送出">
```

---

## 多媒體標籤

### 影片

```html
<video controls width="640">
  <source src="video.mp4" type="video/mp4">
  <source src="video.webm" type="video/webm">
  您的瀏覽器不支援影片播放。
</video>
```

### 音訊

```html
<audio controls>
  <source src="audio.mp3" type="audio/mpeg">
  <source src="audio.ogg" type="audio/ogg">
</audio>
```

---

## 分組與容器

```html
<div>通用區塊容器</div>
<span>通用行內容器</span>
<pre>
  保留空白    和換行
</pre>
<hr>  <!-- 主題分隔線 -->
```

---

## 延伸閱讀

- [MDN: HTML 元素參考](https://www.google.com/search?q=MDN+HTML+elements+reference)
- [HTML 標籤列表](https://www.google.com/search?q=HTML+tags+list+cheat+sheet)
- [W3Schools HTML 教學](https://www.google.com/search?q=W3Schools+HTML+tutorial)

---

*本篇文章為「AI 程式人雜誌 2024 年 3 月號」精選文章之一。*
