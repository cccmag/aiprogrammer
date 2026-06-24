# 串流與管線

## 什麼是 Stream？

Stream（串流）是 Node.js 中處理資料流的抽象介面。與一次將所有資料載入記憶體不同，Stream 允許分段處理資料，特別適合大檔案、網路通訊和即時資料處理。

```javascript
// 不使用 Stream：一次載入整個檔案
const fs = require('fs');
const data = fs.readFileSync('huge-file.txt', 'utf8'); // 記憶體爆炸！

// 使用 Stream：分段讀取
const stream = fs.createReadStream('huge-file.txt', 'utf8');
stream.on('data', chunk => process(chunk));
```

## Stream 的類型

Node.js 有四種基本的 Stream 類型：

```javascript
const { Readable, Writable, Transform, Duplex } = require('stream');

// 1. Readable：可讀取資料
const readable = fs.createReadStream('input.txt');

// 2. Writable：可寫入資料
const writable = fs.createWriteStream('output.txt');

// 3. Transform：可讀寫並轉換資料
const { Transform } = require('stream');

// 4. Duplex：雙向通訊（如 TCP socket）
```

## pipe 管線

`pipe` 是 Stream 最強大的功能之一，它自動處理背壓（Backpressure）：

```javascript
const fs = require('fs');

// 檔案複製（使用 pipe）
const source = fs.createReadStream('source.txt');
const dest = fs.createWriteStream('dest.txt');
source.pipe(dest);

// 壓縮管線
const zlib = require('zlib');
fs.createReadStream('data.txt')
  .pipe(zlib.createGzip())
  .pipe(fs.createWriteStream('data.txt.gz'));

// HTTP 回應管線
const http = require('http');
http.createServer((req, res) => {
  fs.createReadStream('index.html').pipe(res);
}).listen(3000);
```

## 自訂 Stream

### 自訂 Readable

```javascript
const { Readable } = require('stream');

class CounterStream extends Readable {
  constructor(max = 10) {
    super({ objectMode: true });
    this.max = max;
    this.index = 0;
  }

  _read() {
    if (this.index < this.max) {
      this.push({ count: this.index++ });
    } else {
      this.push(null); // 結束訊號
    }
  }
}

const counter = new CounterStream(3);
counter.on('data', chunk => console.log(chunk));
// { count: 0 }
// { count: 1 }
// { count: 2 }
```

### 自訂 Transform

```javascript
const { Transform } = require('stream');

class UpperCaseTransform extends Transform {
  _transform(chunk, encoding, callback) {
    this.push(chunk.toString().toUpperCase());
    callback();
  }
}

// 使用
process.stdin
  .pipe(new UpperCaseTransform())
  .pipe(process.stdout);
```

## 背壓機制

背壓是 Stream 最重要的概念。當資料生產速度大於消費速度時，Stream 會自動暫停生產：

```javascript
const fs = require('fs');

const readable = fs.createReadStream('large-file.txt');
const writable = fs.createWriteStream('output.txt');

readable.on('data', (chunk) => {
  // 如果寫入緩衝區已滿
  const canContinue = writable.write(chunk);
  if (!canContinue) {
    console.log('Backpressure: pausing read');
    readable.pause();
    writable.once('drain', () => {
      console.log('Drain: resuming read');
      readable.resume();
    });
  }
});

// pipe 會自動處理上述邏輯
```

## 實戰範例：CSV 處理

```javascript
const fs = require('fs');
const { Transform } = require('stream');

// CSV 解析 Transform
class CSVParser extends Transform {
  constructor() {
    super({ objectMode: true });
    this.buffer = '';
  }

  _transform(chunk, encoding, callback) {
    this.buffer += chunk.toString();
    const lines = this.buffer.split('\n');
    this.buffer = lines.pop(); // 保留不完整的行

    for (const line of lines) {
      if (line.trim()) {
        this.push(line.split(',').map(s => s.trim()));
      }
    }
    callback();
  }

  _flush(callback) {
    if (this.buffer.trim()) {
      this.push(this.buffer.split(',').map(s => s.trim()));
    }
    callback();
  }
}

fs.createReadStream('data.csv')
  .pipe(new CSVParser())
  .on('data', row => console.log('Row:', row));
```

## pipeline API

Node.js 14+ 提供了更安全的 `pipeline` API：

```javascript
const { pipeline } = require('stream/promises');
const fs = require('fs');
const zlib = require('zlib');

async function compress() {
  try {
    await pipeline(
      fs.createReadStream('input.txt'),
      zlib.createGzip(),
      fs.createWriteStream('input.txt.gz')
    );
    console.log('Compression successful');
  } catch (err) {
    console.error('Pipeline failed:', err);
  }
}
```

## Stream 事件

```javascript
const stream = fs.createReadStream('file.txt');

stream.on('open', (fd) => console.log('File opened'));
stream.on('data', (chunk) => console.log('Data:', chunk.length));
stream.on('end', () => console.log('Reading complete'));
stream.on('close', () => console.log('File closed'));
stream.on('error', (err) => console.error('Error:', err));
```

## 總結

Stream 是 Node.js 高效處理資料的關鍵機制。掌握 pipe、背壓處理和自訂 Stream 的能力，能夠讓程式以極低的記憶體開銷處理大量資料。

## 延伸閱讀

- [Node.js Stream 官方文件](https://www.google.com/search?q=Node.js+stream+documentation)
- [stream/promises pipeline](https://www.google.com/search?q=Node.js+pipeline+stream+promises)
- [背壓機制詳解](https://www.google.com/search?q=Node.js+stream+backpressure)
