# 前端工具鏈：npm、Browserify、Webpack、Gulp

## 前言

隨著 JavaScript 應用複雜度提升，前端工具鏈成為開發必需品。2015 年，npm、Browserify、Webpack、Gulp 構成了前端開發的標準工具生態系。

## npm 套件管理

### 基本命令

```bash
# 初始化專案
npm init

# 安裝套件
npm install lodash                # 安裝到 node_modules
npm install --save express        # 加入 dependencies
npm install --save-dev mocha      # 加入 devDependencies
npm install -g nodemon            # 全域安裝

# 更新
npm update                        # 更新所有套件
npm update lodash                 # 更新特定套件

# 移除
npm uninstall lodash

# 查看
npm list                          # 顯示已安裝套件
npm list --depth=0                # 只顯示第一層
npm outdated                      # 顯示有更新的套件
```

### package.json

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "description": "我的 Web 應用",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "build": "webpack --mode production",
    "dev": "webpack-dev-server --mode development",
    "test": "mocha test/**/*.js",
    "lint": "eslint src/**/*.js"
  },
  "keywords": ["web", "app"],
  "author": "Your Name",
  "license": "MIT",
  "dependencies": {
    "express": "^4.13.0"
  },
  "devDependencies": {
    "webpack": "^1.12.0",
    "mocha": "^2.3.0"
  }
}
```

### npm scripts

```bash
# 自訂腳本
"scripts": {
  "build": "webpack --config webpack.config.js",
  "watch": "webpack --watch --mode development",
  "serve": "http-server dist -p 8080"
}

# 執行
npm run build
npm run serve
```

## Browserify 模組打包

### 為什麼需要 Browserify？

瀏覽器不支援 Node.js 的 `require()` 語法。Browserify 讓我們能在瀏覽器中使用 Node.js 風格的模組：

```javascript
// math.js
module.exports = {
  add: (a, b) => a + b,
  multiply: (a, b) => a * b
};

// app.js
const math = require('./math');
console.log(math.add(2, 3));  // 5
console.log(math.multiply(4, 5));  // 20
```

### 安裝與使用

```bash
# 安裝
npm install --save-dev browserify

# 打包
browserify app.js -o bundle.js

# 轉譯 + 打包（需要 watchify）
watchify app.js -o bundle.js -v
```

### 第三方模組

```bash
# 安裝 lodash
npm install lodash

# 使用
const _ = require('lodash');
const arr = [1, 2, 3, 4, 5];
console.log(_.sum(arr));  // 15
```

### 插件

```bash
# 自動重構
watchify app.js -o bundle.js -v

# Gulp 整合
npm install gulp-browserify
```

## Webpack 模組打包

### 基本設定

```javascript
// webpack.config.js
module.exports = {
  entry: './src/app.js',
  output: {
    filename: 'bundle.js',
    path: './dist'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      },
      {
        test: /\.(png|svg|jpg|gif)$/,
        use: ['file-loader']
      }
    ]
  }
};
```

### 核心概念

```
Webpack 核心概念：
──────────────────

1. Entry（入口）
   - 告訴 Webpack 從哪裡開始
   - 建立依賴圖

2. Output（輸出）
   - 告訴 Webpack 把檔案輸出到哪裡

3. Loaders（載入器）
   - 轉換非 JS 檔案為有效模組
   - babel-loader: ES6+ → ES5
   - css-loader: CSS → JS 模組
   - file-loader: 圖片/字體

4. Plugins（插件）
   - UglifyJsPlugin: 壓縮程式碼
   - HtmlWebpackPlugin: 生成 HTML
   - DefinePlugin: 定義環境變數

5. Mode（模式）
   - development: 開發模式
   - production: 生產模式
```

### 常見設定

```javascript
// webpack.config.js
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  mode: 'production',

  entry: './src/index.js',

  output: {
    filename: 'bundle.[contenthash].js',
    path: path.resolve(__dirname, 'dist'),
    clean: true
  },

  devServer: {
    static: './dist',
    hot: true,
    port: 3000
  },

  module: {
    rules: [
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      },
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: 'babel-loader'
      }
    ]
  },

  plugins: [
    new HtmlWebpackPlugin({
      template: './src/index.html',
      minify: true
    })
  ]
};
```

## Gulp 任務自動化

### 安裝

```bash
npm install --save-dev gulp
npm install --save-dev gulp-uglify gulp-concat gulp-sass
```

### 基本使用

```javascript
// gulpfile.js
const gulp = require('gulp');
const uglify = require('gulp-uglify');
const concat = require('gulp-concat');

// 任務定義
gulp.task('scripts', () => {
  return gulp.src('src/**/*.js')
    .pipe(concat('all.js'))
    .pipe(uglify())
    .pipe(gulp.dest('dist/'));
});

gulp.task('styles', () => {
  return gulp.src('src/**/*.css')
    .pipe(concat('all.css'))
    .pipe(gulp.dest('dist/'));
});

// 預設任務
gulp.task('default', gulp.parallel('scripts', 'styles'));

// 監控變更
gulp.task('watch', () => {
  gulp.watch('src/**/*.js', gulp.parallel('scripts'));
  gulp.watch('src/**/*.css', gulp.parallel('styles'));
});
```

### 常用插件

```javascript
const gulp = require('gulp');
const sass = require('gulp-sass');
const browserSync = require('browser-sync').create();
const autoprefixer = require('gulp-autoprefixer');

gulp.task('sass', () => {
  return gulp.src('src/**/*.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(autoprefixer())
    .pipe(gulp.dest('dist/css'))
    .pipe(browserSync.stream());
});

gulp.task('serve', () => {
  browserSync.init({
    server: './dist',
    files: ['dist/**/*']
  });
});

gulp.task('default', gulp.parallel('sass', 'serve'));
```

## Grunt vs Gulp

```
Grunt vs Gulp：
──────────────
Grunt:
  - 基於設定檔（JSON）
  - 外掛各自獨立
  - 設定較繁瑣

Gulp:
  - 基於程式碼（Node.js streams）
  - 管道式處理
  - 記憶體操作，效能更好

2015 年趨勢：Gulp 逐漸取代 Grunt
```

## 現代工具鏈整合

```javascript
// 完整的 webpack.config.js（2015 年风格）
var path = require('path');
var webpack = require('webpack');

module.exports = {
  entry: './src/app.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js'
  },
  module: {
    loaders: [
      { test: /\.js$/, exclude: /node_modules/, loader: 'babel-loader' },
      { test: /\.css$/, loader: 'style-loader!css-loader' },
      { test: /\.json$/, loader: 'json-loader' }
    ]
  },
  plugins: [
    new webpack.optimize.UglifyJsPlugin(),
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify('production')
    })
  ],
  devtool: 'source-map'
};
```

## 結語

前端工具鏈在 2015 年已經相當成熟。npm 解決了依賴管理問題、Browserify/Webpack 解決了模組打包問題、Gulp/Grunt 解決了任務自動化問題。這套工具鏈成為現代前端開發的標準配置。

---

## 延伸閱讀

- [npm 官方文檔](https://www.google.com/search?q=npm+tutorial+package.json)
- [Webpack 官方文檔](https://www.google.com/search?q=Webpack+tutorial+beginners)
- [Gulp 快速上手](https://www.google.com/search?q=Gulp+tutorial+tasks+automation)

---

*本篇文章為「AI 程式人雜誌 2015 年 1 月號」歷史回顧系列之一。*