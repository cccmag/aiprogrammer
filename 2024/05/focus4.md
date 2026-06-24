# 導航與頁面切換

## 行動應用的導航挑戰

手機 App 的導航與 Web 有本質差異。Web 使用 URL 和瀏覽器的前進/後退按鈕；App 則需要自行管理頁面棧、標籤頁和抽屜選單。

React Navigation 是 React Native 社群最受歡迎的導航解決方案，它提供了完整的導航模式。

## 安裝與設定

```bash
npm install @react-navigation/native @react-navigation/native-stack
npm install @react-navigation/bottom-tabs @react-navigation/drawer
npm install react-native-screens react-native-safe-area-context
```

## Stack Navigator：頁面堆疊

Stack Navigator 是最基本的導航模式，管理一個頁面堆疊（LIFO）：

```jsx
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import HomeScreen from "../screens/HomeScreen";
import ProfileScreen from "../screens/ProfileScreen";
import SettingsScreen from "../screens/SettingsScreen";

const Stack = createNativeStackNavigator();

const HomeStack = () => (
    <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
            headerStyle: { backgroundColor: "#007AFF" },
            headerTintColor: "#fff",
            headerTitleStyle: { fontWeight: "700" },
        }}
    >
        <Stack.Screen
            name="Home"
            component={HomeScreen}
            options={{ title: "首頁" }}
        />
        <Stack.Screen
            name="Profile"
            component={ProfileScreen}
            options={({ route }) => ({
                title: route.params?.username ?? "個人檔案",
            })}
        />
        <Stack.Screen
            name="Settings"
            component={SettingsScreen}
            options={{ title: "設定" }}
        />
    </Stack.Navigator>
);
```

### 導航操作

```jsx
import { useNavigation } from "@react-navigation/native";

const HomeScreen = () => {
    const navigation = useNavigation();

    return (
        <View>
            <Button
                title="查看個人檔案"
                onPress={() => navigation.navigate("Profile", {
                    userId: "123",
                    username: "Alice",
                })}
            />
            <Button
                title="返回"
                onPress={() => navigation.goBack()}
            />
        </View>
    );
};
```

## Tab Navigator：標籤頁導航

底部標籤導航是手機 App 最常見的模式：

```jsx
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { Ionicons } from "@expo/vector-icons";

const Tab = createBottomTabNavigator();

const MainTabs = () => (
    <Tab.Navigator
        screenOptions={({ route }) => ({
            tabBarIcon: ({ focused, color, size }) => {
                const icons = {
                    Home: focused ? "home" : "home-outline",
                    Search: focused ? "search" : "search-outline",
                    Cart: focused ? "cart" : "cart-outline",
                    Profile: focused ? "person" : "person-outline",
                };
                return (
                    <Ionicons
                        name={icons[route.name]}
                        size={size}
                        color={color}
                    />
                );
            },
            tabBarActiveTintColor: "#007AFF",
            tabBarInactiveTintColor: "gray",
        })}
    >
        <Tab.Screen name="Home" component={HomeStack} options={{ title: "首頁" }} />
        <Tab.Screen name="Search" component={SearchScreen} options={{ title: "搜尋" }} />
        <Tab.Screen name="Cart" component={CartScreen} options={{ title: "購物車" }} />
        <Tab.Screen name="Profile" component={ProfileStack} options={{ title: "我的" }} />
    </Tab.Navigator>
);
```

## Drawer Navigator：抽屜導航

抽屜導航從螢幕左側滑出選單：

```jsx
import { createDrawerNavigator } from "@react-navigation/drawer";

const Drawer = createDrawerNavigator();

const AppDrawer = () => (
    <Drawer.Navigator
        screenOptions={{
            drawerStyle: { width: 280 },
            drawerActiveTintColor: "#007AFF",
        }}
    >
        <Drawer.Screen name="Home" component={HomeTabs} />
        <Drawer.Screen name="About" component={AboutScreen} />
        <Drawer.Screen name="Contact" component={ContactScreen} />
    </Drawer.Navigator>
);
```

## 巢狀導航結構

真實應用通常組合多種導航模式：

```
NavigationContainer
└── Drawer Navigator
    ├── Tab Navigator
    │   ├── Stack Navigator（首頁）
    │   │   ├── HomeScreen
    │   │   ├── ProductDetailScreen
    │   │   └── CheckoutScreen
    │   ├── SearchScreen
    │   ├── CartScreen
    │   └── ProfileScreen
    ├── AboutScreen
    └── ContactScreen
```

```jsx
const App = () => (
    <NavigationContainer>
        <AppDrawer />
    </NavigationContainer>
);
```

## 參數傳遞

導航參數的接收與型別安全：

```typescript
type RootStackParamList = {
    Home: undefined;
    Profile: { userId: string; username: string };
    Settings: { section?: string };
};

const Stack = createNativeStackNavigator<RootStackParamList>();

// 接收參數
const ProfileScreen = ({ route }: Props) => {
    const { userId, username } = route.params;
    return <Text>歡迎 {username}！</Text>;
};
```

---

## 延伸閱讀

- [React Navigation 官方文件](https://www.google.com/search?q=React+Navigation+documentation)
- [導航模式設計指南](https://www.google.com/search?q=mobile+app+navigation+patterns)
- [React Navigation TypeScript](https://www.google.com/search?q=React+Navigation+TypeScript)

---

*本篇文章為「AI 程式人雜誌 2024 年 5 月號」焦點系列之四。*
