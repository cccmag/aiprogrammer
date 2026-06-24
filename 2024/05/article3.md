# StyleSheet 與 Flexbox 排版

## 手機螢幕的排版挑戰

手機螢幕尺寸多樣——從 iPhone SE 的 4.7 吋到 iPhone Pro Max 的 6.9 吋，再到 Android 裝置的各種比例。開發者需要一個靈活的排版系統來適應所有螢幕。React Native 使用 Flexbox 作為其排版引擎。

## StyleSheet.create

React Native 提供 `StyleSheet.create` 來定義樣式，它與一般物件相比有以下優勢：

```jsx
import { StyleSheet, View, Text } from "react-native";

// StyleSheet.create 會驗證樣式屬性
// 而且只會在建置時建立一次，避免不必要的重新計算
const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#fff",
        paddingHorizontal: 16,
    },
    title: {
        fontSize: 24,
        fontWeight: "700",
        color: "#1a1a1a",
        marginBottom: 12,
    },
    card: {
        backgroundColor: "#f8f8f8",
        borderRadius: 12,
        padding: 16,
        marginBottom: 8,
    },
});
```

### 行內樣式 vs StyleSheet

```jsx
// 行內樣式（適合動態值）
<View style={{ backgroundColor: dynamicColor, width: width }} />

// StyleSheet（適合靜態樣式）
<View style={styles.staticCard} />

// 組合樣式
<View style={[styles.base, isActive && styles.active]} />
```

## Flexbox 核心概念

React Native 的 Flexbox 與 CSS Flexbox 大致相同，但預設值不同：預設 `flexDirection` 為 `column`（而非 CSS 的 `row`）。

### 容器屬性

```jsx
const styles = StyleSheet.create({
    container: {
        flex: 1,
        flexDirection: "column",     // column（預設）| row
        justifyContent: "flex-start", // flex-start | center | flex-end | space-between | space-around
        alignItems: "stretch",       // stretch（預設）| flex-start | center | flex-end
        flexWrap: "nowrap",          // nowrap | wrap
        gap: 8,                      // 子元件間距
    },
});
```

### 子元件屬性

```jsx
const styles = StyleSheet.create({
    item: {
        flex: 1,           // 佔據可用空間的比例
        alignSelf: "auto", // auto | flex-start | center | flex-end | stretch
    },
    logo: {
        width: 50,
        height: 50,
    },
    content: {
        flex: 2,           // 比 item 多佔一倍空間
        marginLeft: 12,
    },
});
```

## 常見排版模式

### 水平居中

```jsx
const CenteredView = () => (
    <View style={styles.center}>
        <Text>水平垂直居中</Text>
    </View>
);

const styles = StyleSheet.create({
    center: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
    },
});
```

### 列表行

```jsx
const ListRow = ({ title, subtitle, icon }) => (
    <View style={styles.row}>
        <View style={styles.iconContainer}>{icon}</View>
        <View style={styles.textContainer}>
            <Text style={styles.title}>{title}</Text>
            {subtitle && (
                <Text style={styles.subtitle}>{subtitle}</Text>
            )}
        </View>
        <Ionicons name="chevron-forward" size={20} color="#ccc" />
    </View>
);

const styles = StyleSheet.create({
    row: {
        flexDirection: "row",
        alignItems: "center",
        padding: 16,
        backgroundColor: "#fff",
        borderBottomWidth: StyleSheet.hairlineWidth,
        borderBottomColor: "#e0e0e0",
    },
    iconContainer: {
        width: 40,
        height: 40,
        borderRadius: 20,
        backgroundColor: "#f0f0f0",
        justifyContent: "center",
        alignItems: "center",
        marginRight: 12,
    },
    textContainer: {
        flex: 1,
    },
    title: { fontSize: 16, color: "#1a1a1a" },
    subtitle: { fontSize: 13, color: "#999", marginTop: 2 },
});
```

### 網格布局

```jsx
const GridLayout = ({ data }) => (
    <View style={styles.grid}>
        {data.map((item) => (
            <View key={item.id} style={styles.gridItem}>
                <Text>{item.name}</Text>
            </View>
        ))}
    </View>
);

const styles = StyleSheet.create({
    grid: {
        flexDirection: "row",
        flexWrap: "wrap",
        padding: 8,
    },
    gridItem: {
        width: "50%",    // 兩列
        padding: 8,
    },
});
```

### 絕對定位

```jsx
const Badge = ({ count, children }) => (
    <View style={styles.badgeContainer}>
        {children}
        {count > 0 && (
            <View style={styles.badge}>
                <Text style={styles.badgeText}>{count}</Text>
            </View>
        )}
    </View>
);

const styles = StyleSheet.create({
    badgeContainer: {
        position: "relative",
    },
    badge: {
        position: "absolute",
        top: -4,
        right: -4,
        backgroundColor: "red",
        borderRadius: 10,
        minWidth: 20,
        height: 20,
        justifyContent: "center",
        alignItems: "center",
        paddingHorizontal: 4,
    },
    badgeText: {
        color: "#fff",
        fontSize: 11,
        fontWeight: "700",
    },
});
```

## 響應式設計

```jsx
import { useWindowDimensions } from "react-native";

const ResponsiveCard = () => {
    const { width, height } = useWindowDimensions();
    const isLandscape = width > height;

    return (
        <View style={[
            styles.card,
            isLandscape && styles.cardLandscape,
        ]}>
            <Text>螢幕寬度：{Math.round(width)}px</Text>
        </View>
    );
};
```

---

## 延伸閱讀

- [React Native Flexbox 指南](https://www.google.com/search?q=React+Native+Flexbox+guide)
- [StyleSheet API 文件](https://www.google.com/search?q=React+Native+StyleSheet)
- [CSS Flexbox 完整教學](https://www.google.com/search?q=CSS+Flexbox+complete+guide)
