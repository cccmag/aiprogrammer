# 核心元件：View、Text、ScrollView

## React Native 的核心元件

React Native 提供一組跨平台的核心 UI 元件，它們會對應到平台原生的 UI 元件。

```
React Native 元件   iOS 原生          Android 原生
─────────────────   ────────          ────────────
<View>             UIView             android.view.View
<Text>             UILabel            android.widget.TextView
<ScrollView>       UIScrollView       android.widget.ScrollView
<Image>            UIImageView        android.widget.ImageView
<TextInput>        UITextField        android.widget.EditText
<TouchableOpacity> 手勢處理           可繪製狀態
```

## View：基本容器

`View` 是 React Native 中最基礎的 UI 元件，相當於 Web 的 `div` 或原生的 `UIView`。它是一個支援 Flexbox 排版、觸控事件和樣式的容器。

```jsx
import { View, StyleSheet } from "react-native";

const Card = ({ children }) => (
    <View style={styles.card}>
        <View style={styles.cardHeader}>
            {/* 卡片頭部 */}
        </View>
        <View style={styles.cardBody}>
            {children}
        </View>
    </View>
);

const styles = StyleSheet.create({
    card: {
        backgroundColor: "#ffffff",
        borderRadius: 12,
        padding: 16,
        marginVertical: 8,
        marginHorizontal: 16,
        shadowColor: "#000",
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
        elevation: 3, // Android 陰影
    },
    cardHeader: {
        borderBottomWidth: 1,
        borderBottomColor: "#e0e0e0",
        paddingBottom: 8,
        marginBottom: 8,
    },
    cardBody: {
        paddingTop: 4,
    },
});
```

## Text：文字顯示

`Text` 用於顯示文字內容。與 Web 不同，React Native 中的所有文字都必須放在 `Text` 元件中：

```jsx
import { Text, View, StyleSheet } from "react-native";

const TypographyExample = () => (
    <View style={styles.container}>
        <Text style={styles.h1}>大標題</Text>
        <Text style={styles.h2}>副標題</Text>
        <Text style={styles.body}>
            這是內文。React Native 的 Text 元件支援巢狀結構，
            <Text style={styles.bold}>其中可以嵌入粗體文字</Text>，
            以及{" "}
            <Text style={styles.highlight}>不同樣式的文字片段</Text>。
        </Text>
        <Text style={styles.caption} numberOfLines={2}>
            這是一段較長的說明文字，我們使用 numberOfLines
            來限制最多顯示兩行，超出部分會自動以省略號結尾。
        </Text>
    </View>
);

const styles = StyleSheet.create({
    container: { padding: 16 },
    h1: { fontSize: 28, fontWeight: "700", marginBottom: 8 },
    h2: { fontSize: 22, fontWeight: "600", marginBottom: 6 },
    body: { fontSize: 16, lineHeight: 24, marginBottom: 12 },
    bold: { fontWeight: "700" },
    highlight: { color: "#007AFF", fontWeight: "600" },
    caption: { fontSize: 12, color: "#666" },
});
```

### Text 的巢狀結構

`Text` 元件可以巢狀，繼承父層的樣式並可覆蓋：

```jsx
<Text style={{ fontSize: 16, color: "black" }}>
    這是{" "}
    <Text style={{ color: "blue", fontWeight: "bold" }}>藍色粗體</Text>
    的文字
</Text>
```

## ScrollView：滾動容器

`ScrollView` 是一個可滾動的容器，適合內容長度不確定的場景：

```jsx
import { ScrollView, View, Text, StyleSheet } from "react-native";

const ProfileScreen = () => (
    <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={true}
        bounces={true}
        refreshControl={
            // iOS 下拉更新
            <RefreshControl refreshing={false} onRefresh={() => {}} />
        }
    >
        <View style={styles.section}>
            <Text style={styles.title}>個人資訊</Text>
        </View>
        <View style={styles.section}>
            <Text style={styles.title}>近期活動</Text>
        </View>
        <View style={styles.section}>
            <Text style={styles.title}>設定</Text>
        </View>
    </ScrollView>
);

const styles = StyleSheet.create({
    scrollView: { flex: 1, backgroundColor: "#f5f5f5" },
    content: { padding: 16 },
    section: {
        backgroundColor: "#fff",
        borderRadius: 12,
        padding: 16,
        marginBottom: 12,
    },
    title: { fontSize: 18, fontWeight: "600", marginBottom: 8 },
});
```

### ScrollView vs FlatList

- **ScrollView**：一次性渲染所有子元件。適合頁面內容較少（通常為螢幕高度數倍內）
- **FlatList**：虛擬化列表，只渲染可見區域。適合包含大量資料的列表

```jsx
// 何時使用 ScrollView？
<ScrollView>
    <ProfileHeader />
    <StatsSection />
    <RecentActivity />
    <SettingsPanel />
</ScrollView>

// 何時使用 FlatList？
<FlatList
    data={thousandsOfItems}
    renderItem={({ item }) => <ListItem item={item} />}
    keyExtractor={(item) => item.id}
/>
```

---

## 延伸閱讀

- [React Native 核心元件](https://www.google.com/search?q=React+Native+core+components)
- [ScrollView API 文件](https://www.google.com/search?q=React+Native+ScrollView)
- [Flexbox 排版指南](https://www.google.com/search?q=React+Native+Flexbox+guide)

---

*本篇文章為「AI 程式人雜誌 2024 年 5 月號」焦點系列之三。*
