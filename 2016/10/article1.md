# Jest 框架實戰

## 前言

Jest 是 Facebook 開發的 JavaScript 測試框架，以零配置與內建 Mock 聞名。2016 年的 Jest 16.x 版本大幅改善了效能與 DX（開發者體驗）。

## 基礎設定

```bash
npm install --save-dev jest
```

```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'node',
  verbose: true,
  collectCoverage: true,
  coverageDirectory: 'coverage',
  testMatch: ['**/*.test.js']
};
```

## 基本測試結構

```javascript
// math.test.js
describe('Math utilities', () => {
  
  test('adds two numbers', () => {
    expect(2 + 3).toBe(5);
  });
  
  test('subtracts two numbers', () => {
    expect(5 - 2).toBe(3);
  });
  
  describe('multiply', () => {
    test('positive numbers', () => {
      expect(3 * 4).toBe(12);
    });
    
    test('with zero', () => {
      expect(5 * 0).toBe(0);
    });
    
    test('negative numbers', () => {
      expect(-2 * 3).toBe(-6);
    });
  });
});
```

## Matchers 常用語法

```javascript
test('matcher examples', () => {
  // 相等
  expect(2 + 2).toBe(4);
  expect({name: 'test'}).toEqual({name: 'test'});
  
  // 真假值
  expect(null).toBeNull();
  expect(undefined).toBeUndefined();
  expect(true).toBeTruthy();
  expect(0).toBeFalsy();
  
  // 陣列
  expect([1, 2, 3]).toContain(2);
  expect(['a', 'b']).toHaveLength(2);
  
  // 例外
  expect(() => { throw new Error(); }).toThrow();
  
  // 正規表達式
  expect('hello').toMatch(/^hello/);
});
```

## Mock 函數

```javascript
// mock.test.js
const fetchData = require('./fetchData');

test('mocks a function', () => {
  const mockCallback = jest.fn(x => x * 2);
  
  mockCallback(1);
  mockCallback(2);
  
  expect(mockCallback.mock.calls).toHaveLength(2);
  expect(mockCallback.mock.results[0].value).toBe(2);
});

// Mock 模組
jest.mock('./api');
const api = require('./api');

test('mocks API call', async () => {
  api.getUser.mockResolvedValue({ id: 1, name: 'Test' });
  
  const user = await fetchData(1);
  expect(user.name).toBe('Test');
});
```

## 測試非同步程式碼

```javascript
test('async/await', async () => {
  const data = await fetchData();
  expect(data).toEqual({ success: true });
});

test('promises', () => {
  return expect(fetchData()).resolves.toEqual({ success: true });
});
```

## 測試生命週期

```javascript
beforeEach(() => {
  // 每個測試前執行
  setup();
});

afterEach(() => {
  // 每個測試後執行
  cleanup();
});

beforeAll(() => {
  // 所有測試前執行一次
  connectDB();
});

afterAll(() => {
  // 所有測試後執行一次
  disconnectDB();
});
```

## 執行方式

```bash
# 執行所有測試
jest

# 執行特定檔案
jest math.test.js

# 執行包含特定名稱的測試
jest -t "adds"

# 監視模式
jest --watch

# 覆蓋率報告
jest --coverage
```

## 延伸閱讀

- [Jest 官方文檔](https://www.google.com/search?q=jest+javascript+testing+framework+2016)
- [Jest Mock 教學](https://www.google.com/search?q=jest+mocks+tutorial+2016)
- [JavaScript 測試最佳實踐](https://www.google.com/search?q=javascript+testing+best+practices+2016)

---

*本篇文章為「AI 程式人雜誌 2016 年 10 月號」軟體測試系列之一。*