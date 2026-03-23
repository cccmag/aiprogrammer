# 主流語言的函式化（2000s-2010s）

## 函式概念的普及

經過半個世紀的發展，函式程式設計的概念終於開始滲透到主流語言中。這一趨勢在 2000 年代加速，2010 年代達到高峰。

---

## C# 與 LINQ（2007）

2007 年，微軟在 .NET 3.5 中引入了 LINQ（Language Integrated Query）。這是函式程式設計進入主流企業語言的里程碑。

### LINQ 的查詢語法

```csharp
// 查詢語法（SQL 風格）
var result = from o in orders
             where o.Total > 1000
             orderby o.Date descending
             select new { o.Id, o.Total };

// 對應的方法語法（函式風格）
var result = orders
    .Where(o => o.Total > 1000)
    .OrderByDescending(o => o.Date)
    .Select(o => new { o.Id, o.Total });
```

### 延遲執行

LINQ 使用延遲執行（Lazy Evaluation）：

```csharp
// 延遲執行
var query = orders.Where(o => o.Total > 1000);
orders.Add(new Order { Total = 2000 });
foreach (var o in query)  // 這裡才真正執行查詢
    Console.WriteLine(o);

// 立即執行
var list = orders
    .Where(o => o.Total > 1000)
    .ToList();  // 立即執行並存入清單
```

### 與資料來源整合

LINQ 可以查詢任何實現 `IEnumerable<T>` 的集合：

```csharp
// LINQ to Objects
var expensiveProducts = products
    .Where(p => p.Price > 1000)
    .OrderBy(p => p.Name);

// LINQ to SQL
var query = from c in dbContext.Customers
            where c.Orders.Count() > 5
            select c;

// LINQ to XML
var xmlQuery = from e in XDocument.Load("data.xml").Descendants("person")
               where (int)e.Attribute("age") > 18
               select e.Attribute("name").Value;
```

---

## Java 8 與 Stream API（2014）

2014 年，Java 8 發布。這是 Java 自 1995 年诞生以来最大的一次更新。

### Stream API 基礎

```java
// 基本操作：filter, map, collect
List<String> result = orders.stream()
    .filter(o -> o.getTotal() > 1000)           // 過濾
    .map(Order::getId)                           // 轉換
    .map(Object::toString)                       // 轉換為字串
    .collect(Collectors.toList());                // 收集結果

// 聚合操作
int sum = numbers.stream()
    .filter(n -> n > 0)
    .mapToInt(Integer::intValue)
    .sum();

// 查找
Optional<Order> first = orders.stream()
    .filter(o -> o.getTotal() > 1000)
    .findFirst();
```

### 平行流

Java 8 的 Stream API 支援自動並行化：

```java
// 順序執行
double average = orders.stream()
    .mapToDouble(Order::getTotal)
    .average()
    .orElse(0.0);

// 平行執行（自動使用多核心）
double parallelAverage = orders.parallelStream()
    .mapToDouble(Order::getTotal)
    .average()
    .orElse(0.0);

// 效能對比
// 對於大型集合，parallelStream() 可以獲得線性加速比
```

### Optional：處理空值

```java
// 巢狀空值檢查（傳統方式）
String city = null;
if (user != null) {
    if (user.getAddress() != null) {
        if (user.getAddress().getCity() != null) {
            city = user.getAddress().getCity();
        }
    }
}

// Optional 方式
String city = user
    .map(User::getAddress)
    .map(Address::getCity)
    .orElse("Unknown");

// Optional 鏈
Optional<String> result = user
    .map(User::getAddress)
    .flatMap(Address::getOptionalCity)
    .filter(c -> c.length() > 2)
    .map(String::toUpperCase);
```

### 方法參照

```java
// 四種方法參照
// 1. 靜態方法
List<Integer> lengths = names.stream()
    .map(String::length)
    .collect(Collectors.toList());

// 2. 實例方法（特定物件）
String concat = names.stream()
    .reduce("", String::concat);

// 3. 實例方法（任意物件）
List<String> sorted = names.stream()
    .sorted(String::compareToIgnoreCase)
    .collect(Collectors.toList());

// 4. 建構函式
List<String> names = Arrays.asList("Alice", "Bob");
List<Person> people = names.stream()
    .map(Person::new)
    .collect(Collectors.toList());
```

---

## Python 的函式特性

Python 雖然不是純函式語言，但早早引入了多種函式概念。

### Lambda 表達式

```python
# Lambda 表達式
square = lambda x: x ** 2
add = lambda x, y: x + y
sort_key = lambda x: x['name']

# 在高階函式中使用
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x ** 2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
total = reduce(lambda x, y: x + y, numbers)
```

### 列表推導

Python 的列表推導直接受 Haskell 啟發：

```python
# 基本列表推導
squares = [x ** 2 for x in range(10)]
evens = [x for x in range(100) if x % 2 == 0]

# 巢狀列表推導
pairs = [(x, y) for x in range(3) for y in range(3) if x != y]

# 字典推導
word_lengths = {word: len(word) for word in ['hello', 'world']}

# 生成器表達式（惰性）
gen = (x ** 2 for x in range(1000000))
# 不會立即創建大型清單
```

### 生成器與惰性求值

```python
# 生成器函式
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# 使用生成器
fibs = fibonacci()
first_10 = [next(fibs) for _ in range(10)]

# 無限序列的惰性處理
def primes():
    n = 2
    while True:
        if all(n % p != 0 for p in range(2, int(n**0.5) + 1)):
            yield n
        n += 1

def sieve():
    n = 2
    while True:
        if all(n % p != 0 for p in primes()):
            yield n
        n += 1

# itertools 的惰性工具
from itertools import islice, count, takewhile

first_20_primes = list(islice(sieve(), 20))
evens = takewhile(lambda x: x < 20, count(0, 2))
```

### 裝飾器

裝飾器是高階函式的一種應用：

```python
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start}s")
        return result
    return wrapper

def memoize(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@timer
@memoize
def slow_function(n):
    time.sleep(1)
    return n * 2

# 使用
slow_function(5)  # 第一次：打印耗時
slow_function(5)  # 第二次：使用快取，幾乎瞬間返回
```

---

## JavaScript 的函式復興（2015）

JavaScript 從一開始就內建函式特性，但 ES6（2015）帶來了革命性的改變。

### 箭頭函式

```javascript
// 箭頭函式
const square = x => x ** 2;
const add = (x, y) => x + y;
const greet = name => `Hello, ${name}!`;

// 與普通函式的區別：沒有自己的 this
const obj = {
    name: 'Alice',
    // 普通函式：this 指向 obj
    getName: function() { return this.name; },
    // 箭頭函式：this 繼承封閉作用域
    getNameArrow: () => this.name  // undefined
};
```

### 解構與展開

```javascript
// 物件解構
const { name, age, city = 'Unknown' } = person;

// 陣列解構
const [first, second, ...rest] = array;

// 巢狀解構
const { address: { city, zip } } = person;

// 展開運算子
const combined = [...arr1, ...arr2];
const merged = { ...obj1, ...obj2 };
const copied = [...array];
```

### async/await

async/await 是 Promise 的語法糖，讓非同步程式像同步一樣易讀：

```javascript
// Promise 方式
function fetchData(url) {
    return fetch(url)
        .then(response => response.json())
        .then(data => process(data))
        .catch(error => handleError(error));
}

// async/await 方式
async function fetchData(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return process(data);
    } catch (error) {
        handleError(error);
    }
}

// 並行執行
async function fetchAll(urls) {
    const promises = urls.map(url => fetch(url));
    const responses = await Promise.all(promises);
    return Promise.all(responses.map(r => r.json()));
}
```

### 函式組合

```javascript
// 函式組合
const compose = (...fns) => x => fns.reduceRight((v, f) => f(v), x);
const pipe = (...fns) => x => fns.reduce((v, f) => f(v), x);

// 使用
const processData = pipe(
    filter(x => x > 0),
    map(x => x * 2),
    reduce((a, b) => a + b, 0)
);

const result = processData([1, -2, 3, -4, 5]);
```

---

## React 與函式元件（2013）

2013 年，Facebook 開源了 React。這個庫將函式程式設計的概念帶入了前端開發。

### 從類別元件到函式元件

```jsx
// 類別元件（過去）
class Counter extends React.Component {
    constructor(props) {
        super(props);
        this.state = { count: 0 };
        this.handleClick = this.handleClick.bind(this);
    }
    
    handleClick() {
        this.setState({ count: this.state.count + 1 });
    }
    
    render() {
        return (
            <button onClick={this.handleClick}>
                Count: {this.state.count}
            </button>
        );
    }
}

// 函式元件（現在）
function Counter() {
    const [count, setCount] = useState(0);
    return (
        <button onClick={() => setCount(c => c + 1)}>
            Count: {count}
        </button>
    );
}
```

### Hooks：狀態的函式管理

```jsx
// useState：狀態管理
function UserProfile({ userId }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        fetchUser(userId)
            .then(setUser)
            .finally(() => setLoading(false));
    }, [userId]);
    
    if (loading) return <Loading />;
    return <Profile user={user} />;
}

// useCallback：記憶化回調
const handleSubmit = useCallback((data) => {
    saveData(data);
    updateUI(data);
}, [saveData, updateUI]);

// useMemo：記憶化計算
const sortedList = useMemo(
    () => items.slice().sort(compareFn),
    [items]
);

// 自訂 Hook：邏輯重用
function useDebounce(value, delay) {
    const [debouncedValue, setDebouncedValue] = useState(value);
    
    useEffect(() => {
        const timer = setTimeout(() => {
            setDebouncedValue(value);
        }, delay);
        
        return () => clearTimeout(timer);
    }, [value, delay]);
    
    return debouncedValue;
}
```

### 函式式的思想

```jsx
// 不可變更新
const reducer = (state, action) => {
    switch (action.type) {
        case 'ADD_ITEM':
            return {
                ...state,
                items: [...state.items, action.item]
            };
        case 'REMOVE_ITEM':
            return {
                ...state,
                items: state.items.filter(i => i.id !== action.id)
            };
        default:
            return state;
    }
};

// Context：依賴注入
const ThemeContext = createContext('light');

function App() {
    return (
        <ThemeContext.Provider value="dark">
            <Toolbar />
        </ThemeContext.Provider>
    );
}

function Toolbar() {
    const theme = useContext(ThemeContext);
    return <div className={theme}>...</div>;
}
```

---

## 函式程式設計的原則

這些語言的共同趨勢體現了 FP 的核心原則：

### 1. 偏好不可變資料

```csharp
// ❌ 可變
var list = new List<int> { 1, 2, 3 };
list.Add(4);

// ✅ 不可變
var list = ImmutableList<int>.Empty.Add(1).Add(2).Add(3);
var newList = list.Add(4);
```

### 2. 使用純函式

```java
// ❌ 副作用
public int total = 0;
public void sum(List<Integer> nums) {
    total = 0;
    for (int n : nums) total += n;
}

// ✅ 純函式
public int sum(List<Integer> nums) {
    return nums.stream().mapToInt(Integer::intValue).sum();
}
```

### 3. 高階函式

```python
# 將行為作為參數傳遞
def apply_twice(f, x):
    return f(f(x))

result = apply_twice(lambda x: x * 2, 5)  # 20
```

### 4. 避免空值

```kotlin
// 使用 Option 模式
val name: String? = user?.address?.city?.name
val safeName = name ?: "Unknown"

// 或鏈式操作
val displayName = user
    ?.address
    ?.let { "${it.city} ${it.street}" }
    ?: "No address"
```

---

## 結語：FP 的普及化

經過半個世紀的發展，函式程式設計終於成為主流。這帶來了：

1. **更好的並行性**：不可變資料讓並行更安全
2. **更易推理的程式**：純函式沒有副作用
3. **更簡潔的代碼**：高階函式減少樣板
4. **更好的抽象**：組合子模式

未來，我們可以期待：
- 更多語言採用類型推論
- 並行和分散式程式設計更加普及
- AI 輔助的函式程式設計

---

## 延伸閱讀

- [LINQ 設計哲學](https://www.google.com/search?q=C%23+LINQ+design+patterns)
- [Java Stream API](https://www.google.com/search?q=Java+8+Stream+API+functional+programming)
- [React Hooks 深入](https://www.google.com/search?q=React+Hooks+functional+programming)

---

*本篇文章為「AI 程式人雜誌 2026 年 3 月號」歷史回顧系列之五。*
