# Mocha 與 Chai 測試組合

## 前言

Mocha 是靈活的 JavaScript 測試框架，Chai 是優雅的斷言庫。兩者結合提供了極大的彈性與可讀性。

## 安裝設定

```bash
npm install --save-dev mocha chai
```

```javascript
// test/setup.js
const chai = require('chai');
global.expect = chai.expect;
```

## Mocha 基礎結構

```javascript
// calculate.test.js
describe('Calculator', function() {
  
  describe('add', function() {
    it('should add two positive numbers', function() {
      expect(2 + 3).to.equal(5);
    });
    
    it('should handle zero', function() {
      expect(0 + 5).to.equal(5);
    });
  });
  
  describe('divide', function() {
    it('should divide two numbers', function() {
      expect(10 / 2).to.equal(5);
    });
    
    it('should throw on division by zero', function() {
      expect(function() {
        10 / 0;
      }).to.throw();
    });
  });
});
```

## Chai 斷言語法

### Expect 語法

```javascript
const expect = require('chai').expect;

// 相等
expect(2 + 2).to.equal(4);
expect({a: 1}).to.deep.equal({a: 1});
expect([1, 2, 3]).to.have.members([2, 3, 1]);

// 包含
expect('Hello World').to.include('World');
expect([1, 2]).to.include(2);

// 類型
expect('test').to.be.a('string');
expect({}).to.be.an('object');

// 真假
expect(true).to.be.true;
expect(null).to.be.null;

// 長度
expect([1, 2, 3]).to.have.length(3);
expect('test').to.have.length(4);

// 屬性
expect({a: 1}).to.have.property('a').to.equal(1);

// 錯誤
expect(function() {
  throw new Error('test error');
}).to.throw('test error');
```

### Should 語法

```javascript
const should = require('chai').should();

'test'.should.be.a('string');
({a: 1}).should.have.property('a').to.equal(1);
```

### Assert 語法

```javascript
const assert = require('chai').assert;

assert.equal(2 + 2, 4);
assert.deepEqual({a: 1}, {a: 1});
assert.isArray([1, 2, 3]);
assert.isObject({});
assert.throw(function() {
  throw new Error();
});
```

## 非同步測試

```javascript
describe('Async operations', function() {
  
  it('should handle callbacks', function(done) {
    asyncOperation(function(result) {
      expect(result).to.equal('success');
      done();
    });
  });
  
  it('should handle promises', function() {
    return asyncPromise()
      .then(function(result) {
        expect(result).to.equal('success');
      });
  });
  
  it('should handle async/await', async function() {
    const result = await asyncPromise();
    expect(result).to.equal('success');
  });
});
```

## Mocha 鉤子

```javascript
describe('Hooks demo', function() {
  before(function() {
    // 整個 describe 區塊前執行一次
  });
  
  after(function() {
    // 整個 describe 區塊後執行一次
  });
  
  beforeEach(function() {
    // 每個 it 前執行
  });
  
  afterEach(function() {
    // 每個 it 後執行
  });
});
```

## 執行方式

```bash
# 在 package.json 中設定
{
  "scripts": {
    "test": "mocha --recursive --require test/setup.js 'test/**/*.test.js'"
  }
}

# 或直接執行
./node_modules/.bin/mocha --recursive test/
```

## 延伸閱讀

- [Mocha 官方文檔](https://www.google.com/search?q=mocha+javascript+testing+2016)
- [Chai 斷言庫](https://www.google.com/search?q=chai+assertion+library+2016)
- [Mocha + Chai 教學](https://www.google.com/search?q=mocha+chai+tutorial+2016)

---

*本篇文章為「AI 程式人雜誌 2016 年 10 月號」軟體測試系列之一。*