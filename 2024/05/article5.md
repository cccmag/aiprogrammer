# FlatList 長列表渲染

## 為什麼需要 FlatList？

手機 App 中，列表是最常見的 UI 模式之一。從社群媒體的動態牆到電子商務的商品列表，資料數量可能從幾十筆到幾萬筆。

使用傳統的 `ScrollView` 渲染大量資料時，所有項目會一次性渲染，導致記憶體爆炸和 UI 卡頓：

```jsx
// ❌ ScrollView：一次渲染所有項目
<ScrollView>
    {data.map((item) => (
        <ListItem key={item.id} item={item} />
    ))}
</ScrollView>
// 10,000 筆 → 10,000 個元件 → 記憶體爆表
```

`FlatList` 使用虛擬化技術——只渲染螢幕可見區域的元件，不可見的項目會被回收重用。

## FlatList 基本用法

```jsx
import { FlatList, Text, View, StyleSheet } from "react-native";

const DATA = Array.from({ length: 10000 }, (_, i) => ({
    id: String(i),
    title: `項目 ${i + 1}`,
    description: `這是第 ${i + 1} 個項目的描述文字`,
}));

const Item = ({ title, description }) => (
    <View style={styles.item}>
        <Text style={styles.title}>{title}</Text>
        <Text style={styles.description}>{description}</Text>
    </View>
);

const MyList = () => (
    <FlatList
        data={DATA}
        renderItem={({ item }) => (
            <Item title={item.title} description={item.description} />
        )}
        keyExtractor={(item) => item.id}
    />
);
```

## 核心 Props

```jsx
<FlatList
    // 必要 Props
    data={data}
    renderItem={({ item, index, separators }) => <Item />}
    keyExtractor={(item, index) => item.id}

    // 效能優化
    removeClippedSubviews={true}  // 回收不可見的元件
    maxToRenderPerBatch={10}      // 每批最大渲染數
    windowSize={21}               // 渲染視窗（上下各 10 個螢幕高度）
    initialNumToRender={10}       // 初始渲染數量
    updateCellsBatchingPeriod={50} // 批次更新間隔（ms）

    // 列表行為
    refreshing={refreshing}       // 下拉更新狀態
    onRefresh={handleRefresh}     // 下拉更新回呼
    onEndReached={handleLoadMore} // 觸底載入更多
    onEndReachedThreshold={0.5}   // 觸底閾值（螢幕高度比例）

    // 分隔線與空白
    ItemSeparatorComponent={Divider}
    ListHeaderComponent={Header}
    ListFooterComponent={Footer}
    ListEmptyComponent={<Text>暫無資料</Text>}

    // 水平模式
    horizontal={false}
    showsHorizontalScrollIndicator={false}
/>
```

## 無限滾動與分頁載入

```jsx
import { useState, useEffect, useCallback } from "react";
import { FlatList, ActivityIndicator, Text, View } from "react-native";

const PAGE_SIZE = 20;

const InfiniteList = () => {
    const [data, setData] = useState([]);
    const [page, setPage] = useState(1);
    const [loading, setLoading] = useState(false);
    const [hasMore, setHasMore] = useState(true);

    const fetchData = useCallback(async () => {
        if (loading || !hasMore) return;
        setLoading(true);

        try {
            const response = await fetch(
                `https://api.example.com/items?page=${page}&limit=${PAGE_SIZE}`
            );
            const newData = await response.json();

            setData((prev) => [...prev, ...newData.items]);
            setHasMore(newData.hasMore);
            setPage((p) => p + 1);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    }, [page, loading, hasMore]);

    const handleRefresh = async () => {
        setPage(1);
        setData([]);
        setHasMore(true);
        // 重新載入第一頁
    };

    return (
        <FlatList
            data={data}
            renderItem={({ item }) => <Item item={item} />}
            keyExtractor={(item) => item.id}
            onEndReached={fetchData}
            onEndReachedThreshold={0.5}
            refreshing={loading && page === 1}
            onRefresh={handleRefresh}
            ListFooterComponent={
                loading && <ActivityIndicator size="small" />
            }
        />
    );
};
```

## 複雜項目效能優化

### 使用 React.memo

```jsx
import React from "react";
import { View, Text, StyleSheet } from "react-native";

const ListItem = React.memo(({ item, onPress }) => {
    return (
        <TouchableOpacity style={styles.item} onPress={() => onPress(item.id)}>
            <Image source={{ uri: item.image }} style={styles.image} />
            <View style={styles.content}>
                <Text style={styles.title}>{item.title}</Text>
                <Text style={styles.price}>NT${item.price}</Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color="#ccc" />
        </TouchableOpacity>
    );
});

const styles = StyleSheet.create({
    item: {
        flexDirection: "row",
        padding: 12,
        alignItems: "center",
    },
    image: { width: 60, height: 60, borderRadius: 8, marginRight: 12 },
    content: { flex: 1 },
    title: { fontSize: 16, fontWeight: "500" },
    price: { fontSize: 14, color: "#007AFF", marginTop: 4 },
});
```

### getItemLayout

如果每個項目高度相同，可以指定 `getItemLayout` 來跳過佈局計算：

```jsx
const ITEM_HEIGHT = 80;

<FlatList
    data={data}
    renderItem={renderItem}
    keyExtractor={(item) => item.id}
    getItemLayout={(data, index) => ({
        length: ITEM_HEIGHT,
        offset: ITEM_HEIGHT * index,
        index,
    })}
/>
```

## SectionList

當列表需要分組時，使用 `SectionList`：

```jsx
import { SectionList, Text, View, StyleSheet } from "react-native";

const SECTIONS = [
    { title: "熱門商品", data: ["iPhone 15", "Galaxy S24", "Pixel 8"] },
    { title: "促銷商品", data: ["耳機特價", "充電器 6 折"] },
];

const SectionedList = () => (
    <SectionList
        sections={SECTIONS}
        keyExtractor={(item, index) => item + index}
        renderItem={({ item }) => <Text style={styles.item}>{item}</Text>}
        renderSectionHeader={({ section: { title } }) => (
            <Text style={styles.header}>{title}</Text>
        )}
    />
);
```

---

## 延伸閱讀

- [FlatList API 文件](https://www.google.com/search?q=React+Native+FlatList)
- [長列表效能優化](https://www.google.com/search?q=React+Native+long+list+performance)
- [SectionList 使用指南](https://www.google.com/search?q=React+Native+SectionList)
