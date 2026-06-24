# JSX 在手機開發的應用

## 從 Web 到 App 的語法橋樑

JSX（JavaScript XML）是 React 生態系的標誌性語法擴展。它讓開發者可以在 JavaScript 中編寫類似 HTML 的標記語言，而 React Native 將這個概念延伸到手機開發。

### JSX 的本質

JSX 不是模板語言，而是語法糖。每段 JSX 都會被編譯為 `React.createElement` 呼叫：

```jsx
// JSX 寫法
<View style={styles.container}>
    <Text>Hello, World!</Text>
</View>

// 編譯後的 JavaScript
React.createElement(View, { style: styles.container },
    React.createElement(Text, null, "Hello, World!")
);
```

## React Native 中的 JSX 差異

與 Web 的 React DOM 相比，React Native 的 JSX 有以下關鍵差異：

### 1. 沒有 HTML 元素

在 React Native 中不能使用 HTML 元素：

```jsx
// ❌ 錯誤：React Native 沒有 div、span、p
<div>Hello</div>
<span>World</span>
<p>Paragraph</p>

// ✅ 正確：使用 React Native 核心元件
<View>
    <Text>Hello World</Text>
</View>
```

### 2. 所有樣式都是物件

```jsx
// Web React：字串 class 名稱
<div className="container">...</div>

// React Native：StyleSheet 物件
<View style={styles.container}>...</View>
```

### 3. 事件處理差異

```jsx
// Web：onClick
<button onClick={handleClick}>點我</button>

// React Native：onPress
<Button onPress={handleClick} title="點我" />
<TouchableOpacity onPress={handleClick}>
    <Text>點我</Text>
</TouchableOpacity>
```

### 4. 條件渲染

```jsx
const Greeting = ({ isLoggedIn }) => (
    <View>
        {/* 邏輯與運算子 */}
        {isLoggedIn && <Text>歡迎回來！</Text>}

        {/* 三元運算子 */}
        <Text>{isLoggedIn ? "已登入" : "請登入"}</Text>

        {/* IIFE 模式（複雜邏輯） */}
        {(() => {
            if (isLoggedIn) return <ProfileCard />;
            return <LoginButton />;
        })()}
    </View>
);
```

### 5. 列表渲染

```jsx
const ProductList = ({ products }) => (
    <FlatList
        data={products}
        renderItem={({ item, index }) => (
            <View style={styles.item}>
                <Text style={styles.name}>{item.name}</Text>
                <Text style={styles.price}>${item.price}</Text>
            </View>
        )}
        keyExtractor={(item) => item.id}
        ListEmptyComponent={<Text>暫無商品</Text>}
        ItemSeparatorComponent={() => <View style={styles.separator} />}
    />
);
```

## JSX 與 TypeScript

JSX 與 TypeScript 的整合讓 React Native 開發更加安全：

```tsx
// 定義 props 型別
type ProductCardProps = {
    product: {
        id: string;
        name: string;
        price: number;
        image?: string;
    };
    onPress: (id: string) => void;
    variant?: "compact" | "full";
};

const ProductCard = ({
    product,
    onPress,
    variant = "full",
}: ProductCardProps) => (
    <TouchableOpacity
        style={styles[variant]}
        onPress={() => onPress(product.id)}
    >
        <Text>{product.name}</Text>
        <Text>NT${product.price}</Text>
    </TouchableOpacity>
);
```

## 常用的 JSX 模式

### 複合元件模式

```jsx
const Card = ({ children }) => <View style={styles.card}>{children}</View>;

Card.Header = ({ children }) => (
    <View style={styles.header}>{children}</View>
);

Card.Body = ({ children }) => <View style={styles.body}>{children}</View>;

Card.Footer = ({ children }) => (
    <View style={styles.footer}>{children}</View>
);

// 使用方式
<Card>
    <Card.Header>
        <Text>標題</Text>
    </Card.Header>
    <Card.Body>
        <Text>內容</Text>
    </Card.Body>
    <Card.Footer>
        <Button title="確定" onPress={() => {}} />
    </Card.Footer>
</Card>;
```

### Render Props 模式

```jsx
const DataLoader = ({ url, render }) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(url)
            .then((res) => res.json())
            .then(setData)
            .finally(() => setLoading(false));
    }, [url]);

    return render({ data, loading });
};

// 使用方式
<DataLoader
    url="https://api.example.com/products"
    render={({ data, loading }) =>
        loading ? <Loading /> : <ProductList data={data} />
    }
/>;
```

## 結語

JSX 從 Web 延伸到手機開發，證明了「Learn once, write anywhere」的哲學。熟悉 JSX 的開發者可以將 React 的思維模式直接帶到行動開發，大幅降低學習成本。理解 JSX 的編譯原理和 React Native 的特殊規則，能幫助開發者寫出更高效的程式碼。

---

## 延伸閱讀

- [JSX 深入介紹](https://www.google.com/search?q=JSX+React+in-depth)
- [React Native 中的 JSX](https://www.google.com/search?q=React+Native+JSX+guide)
- [TypeScript + React Native](https://www.google.com/search?q=TypeScript+React+Native)
