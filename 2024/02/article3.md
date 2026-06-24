# 檔案系統操作實戰

## 前言

Node.js 的 `fs`（File System）模組是後端開發中最常用的內建模組之一。本文將從基礎到進階，全面介紹檔案系統操作的各種技巧。

## 基礎操作

### 讀取與寫入

```javascript
const fs = require('fs');

// 字串讀寫
fs.writeFileSync('data.txt', 'Hello World');
const data = fs.readFileSync('data.txt', 'utf8');

// 二進制讀寫
const buffer = Buffer.from([0x48, 0x65, 0x6c, 0x6c, 0x6f]);
fs.writeFileSync('binary.dat', buffer);
const read = fs.readFileSync('binary.dat');
```

### 串流讀寫（適合大檔案）

```javascript
const fs = require('fs');

// 使用串流讀取大檔案
const readStream = fs.createReadStream('large-file.txt', {
  highWaterMark: 64 * 1024, // 64KB 區塊
  encoding: 'utf8'
});

readStream.on('data', (chunk) => {
  console.log('Received chunk:', chunk.length);
});

readStream.on('end', () => {
  console.log('File reading completed');
});

// 串流寫入
const writeStream = fs.createWriteStream('output.txt');
writeStream.write('Line 1\n');
writeStream.write('Line 2\n');
writeStream.end('Final line\n');
```

## 目錄操作進階

### 遞迴目錄操作

```javascript
const fs = require('fs');
const path = require('path');

// 遞迴建立目錄
fs.mkdirSync('a/b/c', { recursive: true });

// 遞迴刪除目錄
function removeDir(dirPath) {
  if (fs.existsSync(dirPath)) {
    fs.readdirSync(dirPath).forEach(file => {
      const curPath = path.join(dirPath, file);
      if (fs.lstatSync(curPath).isDirectory()) {
        removeDir(curPath); // 遞迴
      } else {
        fs.unlinkSync(curPath); // 刪除檔案
      }
    });
    fs.rmdirSync(dirPath);
  }
}

removeDir('a');
```

### 監控檔案變更

```javascript
const fs = require('fs');

// 監控單一檔案
fs.watchFile('config.json', (curr, prev) => {
  console.log(`config.json changed at ${curr.mtime}`);
});

// 監控目錄
fs.watch('uploads/', (eventType, filename) => {
  console.log(`${filename}: ${eventType}`);
});
```

## 檔案資訊與權限

```javascript
const fs = require('fs');
const path = require('path');

const stats = fs.statSync('data.txt');

console.log({
  size: stats.size,            // 檔案大小（bytes）
  isFile: stats.isFile(),
  isDirectory: stats.isDirectory(),
  birthtime: stats.birthtime,  // 建立時間
  mtime: stats.mtime,          // 修改時間
  atime: stats.atime,          // 存取時間
  mode: stats.mode.toString(8) // 權限
});

// 權限檢查
fs.accessSync('data.txt', fs.constants.R_OK | fs.constants.W_OK);
console.log('File is readable and writable');
```

## fs/promises API

Node.js 提供了 Promise 版本的 fs API：

```javascript
const fsp = require('fs/promises');

async function handleFiles() {
  try {
    // 檢查目錄是否存在
    await fsp.mkdir('backup', { recursive: true });

    // 複製檔案
    await fsp.copyFile('source.txt', 'backup/source.txt');

    // 讀取並修改
    let data = await fsp.readFile('config.json', 'utf8');
    const config = JSON.parse(data);
    config.version = 2;
    await fsp.writeFile('config.json', JSON.stringify(config, null, 2));

    // 讀取目錄
    const files = await fsp.readdir('.');
    console.log('Files:', files);

    // 取得檔案資訊
    const stats = await fsp.stat('config.json');
    console.log('Size:', stats.size);
  } catch (err) {
    console.error('Error:', err.message);
  }
}
```

## 實戰範例：檔案備份工具

```javascript
const fs = require('fs');
const path = require('path');
const fsp = require('fs/promises');

async function backupDirectory(src, dest) {
  await fsp.mkdir(dest, { recursive: true });
  const items = await fsp.readdir(src);

  for (const item of items) {
    const srcPath = path.join(src, item);
    const destPath = path.join(dest, item);
    const stat = await fsp.stat(srcPath);

    if (stat.isDirectory()) {
      await backupDirectory(srcPath, destPath);
    } else {
      await fsp.copyFile(srcPath, destPath);
      console.log(`Copied: ${item}`);
    }
  }
}

backupDirectory('./data', './backup')
  .then(() => console.log('Backup complete'))
  .catch(err => console.error('Backup failed:', err));
```

## 安全性注意事項

```javascript
const fs = require('fs');
const path = require('path');

// 防止路徑遍歷攻擊
function safeRead(filePath, baseDir) {
  const fullPath = path.resolve(baseDir, filePath);
  if (!fullPath.startsWith(path.resolve(baseDir))) {
    throw new Error('Invalid path');
  }
  return fs.readFileSync(fullPath, 'utf8');
}

// 避免 Race Condition
const tmpFile = `/tmp/${Date.now()}.tmp`;
const fd = fs.openSync(tmpFile, 'wx'); // 'x' 表示獨佔建立
fs.writeSync(fd, 'data');
fs.closeSync(fd);
```

## 總結

Node.js 的 fs 模組功能強大且完整。從基本的讀寫到大檔案的串流處理，從同步到 Promise API，掌握這些操作對於後端開發至關重要。在使用時，務必注意路徑安全和非同步錯誤處理。

## 延伸閱讀

- [Node.js fs 官方文件](https://www.google.com/search?q=Node.js+fs+module+documentation)
- [Node.js Stream 指南](https://www.google.com/search?q=Node.js+stream+guide)
- [fs/promises API](https://www.google.com/search?q=Node.js+fs+promises+API)
