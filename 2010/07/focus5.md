# 前端工具鏈：Less、Sass 與建構系統

## 前言

隨著 Web 應用的複雜性增加，傳統的手寫 CSS 已經無法滿足大型專案的需求。CSS 預處理器（Preprocessor）的出現徹底改變了樣式表的開發方式，而任務執行器（Task Runner）則讓重複性的建構工作得以自動化。

本章節將探討前端工具鏈的演化歷程，從手寫 CSS 到現代的自動化建構系統。

## CSS 預處理器

### 為什麼需要預處理器？

手寫 CSS 的幾個痛點：

1. **沒有變數**：重複的顏色、字體大小需要手動複製
2. **無法複用**：沒有繼承和 mixin 機制
3. **運算能力弱**：無法進行基本的數學運算
4. **巢狀困難**：多層選擇器的縮進難以維護

### Less 動態樣式表

Less 由 Alexis Sellier 於 2010 年發布，是第一個流行的 CSS 預處理器。

#### 變數

```less
// 定義變數
@primary-color: #0460A3;
@base-font-size: 13px;
@border-radius: 3px;

// 使用變數
.btn-primary {
  background: @primary-color;
  font-size: @base-font-size;
  border-radius: @border-radius;
}
```

編譯後：

```css
.btn-primary {
  background: #0460A3;
  font-size: 13px;
  border-radius: 3px;
}
```

#### Mixin

```less
// 無參數 mixin
.center-block() {
  display: block;
  margin-left: auto;
  margin-right: auto;
}

.container {
  .center-block();
  max-width: 960px;
}

// 帶參數 mixin
.border-radius(@radius) {
  -webkit-border-radius: @radius;
  -moz-border-radius: @radius;
  border-radius: @radius;
}

.btn {
  .border-radius(3px);
}
```

#### 巢狀規則

```less
// Less 巢狀
.nav {
  background: #333;

  ul {
    margin: 0;
    padding: 0;
    list-style: none;
  }

  li {
    display: inline-block;

    a {
      color: #fff;
      text-decoration: none;

      &:hover {
        text-decoration: underline;
      }
    }
  }
}
```

編譯後：

```css
.nav { background: #333; }
.nav ul { margin: 0; padding: 0; list-style: none; }
.nav li { display: inline-block; }
.nav li a { color: #fff; text-decoration: none; }
.nav li a:hover { text-decoration: underline; }
```

#### 運算

```less
// 運算支援
@base-width: 960px;
@column-count: 12;
@column-width: @base-width / @column-count;

.sidebar { width: @column-width * 3; }  /* 240px */
.content { width: @column-width * 9; }  /* 720px */
```

#### 內建函數

```less
// 顏色函數
@base: #0460A3;

.lighten-color { color: lighten(@base, 20%); }   /* 更亮 */
.darken-color { color: darken(@base, 20%); }     /* 更暗 */
.saturate-color { color: saturate(@base, 20%); } /* 更飽和 */
.desaturate-color { color: desaturate(@base, 20%); }

/* 混合顏色 */
.mixed { background: mix(#ff0000, #0000ff, 50%); }
```

### Sass（Syntactically Awesome Stylesheets）

Sass 由 Hampton Catlin 開發，2007 年發布首個版本，比 Less 更早。

#### 語法差異

Sass 有兩種語法：

```scss
// SCSS（類似 CSS 的語法）
$primary-color: #0460A3;
$border-radius: 3px;

.btn-primary {
  background: $primary-color;
  border-radius: $border-radius;
}
```

```sass
// 縮排語法（無需分號和大括號）
$primary-color: #0460A3

.btn-primary
  background: $primary-color
  border-radius: $border-radius
```

#### Sass 的獨特功能

```scss
// 條件語句
@if $theme == dark {
  $bg-color: #1a1a1a;
} @else {
  $bg-color: #ffffff;
}

// 迴圈
@for $i from 1 through 12 {
  .col-#{$i} {
    width: (100% / 12) * $i;
  }
}

// 迭代
@each $name, $color in (primary: blue, danger: red, success: green) {
  .btn-#{$name} {
    background: $color;
  }
}

// 內建函數
$dark-color: darken($primary-color, 20%);
$light-color: lighten($primary-color, 10%);
$complementary: complement($primary-color);
```

### Less vs Sass 比較

| 特性 | Less | Sass |
|------|------|------|
| 發布年份 | 2010 | 2007 |
| 語法 | CSS 超集 | CSS 超集 + 縮排語法 |
| 變數前綴 | @ | $ |
| 社區 | 較小 | 較大 |
| Bootstrap 使用 | 是 | 是（後來採用） |

## 編譯工具

### 命令行編譯

```bash
# 編譯 Less
$ lessc styles.less styles.css

# 監視檔案變化自動編譯
$ lessc --watch styles.less styles.css

# 壓縮輸出
$ lessc --compress styles.less styles.min.css

# 編譯 Sass
$ sass style.scss style.css

# 監視檔案變化
$ sass --watch style.scss:style.css
```

### GUI 工具

- **Koala**：跨平台 Less/Sass 編譯器
- **CodeKit**：Mac 上的專業前端工具
- **Prepros**：支援多種預處理器

### 線上編譯

- **Less.js.org/lesscss**：Less 官方線上編譯器
- **SassMeister**：線上 Sass 編譯器

## 任務執行器

### Grunt

Grunt 由 Ben Alman 開發，2012 年發布，是第一個流行的 JavaScript 任務執行器。

#### 安裝

```bash
npm install -g grunt-cli
npm install grunt --save-dev
```

#### 基本配置

```javascript
// Gruntfile.js
module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    // Less 編譯
    less: {
      development: {
        files: {
          'dist/css/style.css': 'src/less/style.less'
        }
      },
      production: {
        options: {
          compress: true
        },
        files: {
          'dist/css/style.min.css': 'src/less/style.less'
        }
      }
    },

    // 監視檔案變化
    watch: {
      less: {
        files: ['src/less/**/*.less'],
        tasks: ['less:development']
      }
    },

    // 清除目錄
    clean: {
      dist: ['dist/css/*.css']
    }
  });

  // 載入插件
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-clean');

  // 註冊任務
  grunt.registerTask('default', ['less:production']);
  grunt.registerTask('dev', ['less:development', 'watch']);
};
```

#### 使用

```bash
# 執行預設任務
$ grunt

# 執行特定任務
$ grunt less:development

# 監視變化
$ grunt watch
```

### Gulp

Gulp 由 Fractal Innovations 開發，2013 年發布，採用流處理方式，效能更佳。

```javascript
// Gulpfile.js
var gulp = require('gulp');
var less = require('gulp-less');
var csso = require('gulp-csso');
var watch = require('gulp-watch');

gulp.task('less', function() {
  return gulp.src('src/less/**/*.less')
    .pipe(less())
    .pipe(gulp.dest('dist/css'));
});

gulp.task('css', function() {
  return gulp.src('src/less/**/*.less')
    .pipe(less())
    .pipe(csso())
    .pipe(gulp.dest('dist/css'));
});

gulp.task('watch', function() {
  gulp.watch('src/less/**/*.less', ['less']);
});

gulp.task('default', ['less']);
```

### Grunt vs Gulp

| 特性 | Grunt | Gulp |
|------|-------|------|
| 配置方式 | 宣告式 | 程式化 |
| 執行模型 | 基於配置 | 基於流 |
| 記憶體 | 較高 | 較低 |
| 學習曲線 | 平緩 | 較陡 |

## 自動化工作流

### 典型的前端建構流程

```bash
# 開發階段
1. 監視 Less/Sass 檔案 → 自動編譯
2. 瀏覽器自動重新載入（LiveReload）
3. 原始碼錯誤提示

# 發布階段
1. 清除舊的構建檔案
2. 編譯 Less/Sass
3. 压缩 CSS/JS
4. 合併檔案
5. 複製靜態資源
6. 生成 Source Map
```

### Yeoman

Yeoman 是 Google 開發的專案腳手架工具，整合了 Grunt/Gulp：

```bash
# 安裝 Yeoman
npm install -g yo

# 安裝 Bootstrap 生成器
npm install -g generator-bootstrap

# 創建新專案
$ yo bootstrap
```

### Bower

Bower 是 Twitter 開發的前端套件管理器：

```bash
# 安裝
npm install -g bower

# 安裝套件
$ bower install jquery
$ bower install bootstrap

# 更新
$ bower update
```

## 結語

2010 年代初期的前端工具鏈革命，改變了 Web 開發的工作方式：

1. **CSS 預處理器**讓樣式表更具可維護性
2. **任務執行器**讓重複工作自動化
3. **包管理器**讓依賴管理更簡單

這些工具為後來的現代前端構建系統（如 Webpack、Vite）奠定了基礎。

下一篇文章我們將比較主流的前端框架，幫助讀者選擇適合自己專案的工具。

---

## 延伸閱讀

- [Less CSS 官方文檔](https://www.google.com/search?q=Less+CSS+documentation)
- [Sass 官方文檔](https://www.google.com/search?q=Sass+documentation)
- [Grunt 官方網站](https://www.google.com/search?q=Grunt+task+runner)
- [Gulp 官方網站](https://www.google.com/search?q=Gulp+task+runner)

---

*本篇文章為「AI 程式人雜誌 2010 年 7 月號」歷史回顧系列之一。*