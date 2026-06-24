# JavaScript 測試框架：QUnit 與 YUI Test

## 前言

2009 年，JavaScript 測試框架開始成熟。jQuery 的 QUnit 和 Yahoo! 的 YUI Test 為 JavaScript 單元測試提供了可靠的工具。

## QUnit

### 起源

QUnit 由 jQuery 團隊開發，最初用於 jQuery 本身的測試，後來成為獨立的測試框架。

```javascript
// QUnit 基本用法

module("String Tests");

test("String reverse", function() {
    var result = reverseString("hello");
    equal(result, "olleh", "Reverse should work");
});

test("String capitalize", function() {
    var result = capitalize("hello");
    equal(result, "Hello", "Capitalize should work");
});
```

### 斷言

```javascript
// QUnit 斷言

ok(value, "truthy value");
equal(actual, expected, "equal");
notEqual(actual, expected, "not equal");
deepEqual(actual, expected, "deep equal");
strictEqual(actual, expected, "strict equal");
throws(block, expected, "throws");

// 範例
test("Array operations", function() {
    var arr = [1, 2, 3];

    ok(arr.length === 3, "Array has 3 elements");
    equal(arr.push(4), 4, "push returns new length");
    deepEqual(arr, [1, 2, 3, 4], "Array contains expected values");
});
```

## YUI Test

### Yahoo! 的測試框架

```javascript
// YUI Test 用法

YUI().use('test', function(Y) {
    var testCase = new Y.Test.Case({
        name: "Calculator Tests",

        setUp: function() {
            this.calc = new Calculator();
        },

        tearDown: function() {
            this.calc = null;
        },

        testAddition: function() {
            Y.Assert.areEqual(5, this.calc.add(2, 3));
        },

        testDivision: function() {
            Y.Assert.areEqual(2, this.calc.divide(6, 3));
        }
    });

    Y.Test.Runner.add(testCase);
});
```

## JavaScript TDD 的價值

```javascript
// TDD 的 JavaScript 範例

// 1. 紅：寫測試
test("add should return sum", function() {
    equal(add(2, 3), 5);
});

// 2. 綠：快速實現
function add(a, b) {
    return 5; // 臨時值
}

// 3. 重構：正確實現
function add(a, b) {
    return a + b;
}
```

## 結語

JavaScript 測試框架的成熟，推動了前端測試的普及。TDD 不再只屬於後端開發者。

## 延伸閱讀

- [QUnit 官方網站](https://www.google.com/search?q=QUnit+official+website)
- [YUI Test 文件](https://www.google.com/search?q=YUI+Test+documentation)
- [JavaScript TDD](https://www.google.com/search?q=JavaScript+TDD+testing)

---

*本篇文章為「AI 程式人雜誌 2009 年 8 月號」文章系列之一。*