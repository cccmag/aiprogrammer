# React Navigation 實戰

## 從基礎到進階的導航配置

React Navigation 是 React Native 生態系中最受歡迎的導航函式庫。本文將從實戰角度，深入探討常見的導航場景與配置技巧。

## 深度連結（Deep Linking）

深度連結允許使用者從外部 URL 直接打開 App 的特定頁面：

```jsx
import { NavigationContainer, LinkingOptions } from "@react-navigation/native";

const linking = {
    prefixes: ["myapp://", "https://myapp.com"],
    config: {
        screens: {
            Home: {
                screens: {
                    ProductDetail: "product/:id",
                    Profile: "user/:username",
                },
            },
            Settings: "settings",
        },
    },
};

const App = () => (
    <NavigationContainer linking={linking}>
        <RootNavigator />
    </NavigationContainer>
);
```

這樣當使用者點擊 `myapp://product/123` 時，App 會直接導航到商品詳情頁。

## 認證流程導航

許多 App 需要根據登入狀態切換導航結構：

```jsx
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { useAuth } from "../hooks/useAuth";

const Stack = createNativeStackNavigator();

const RootNavigator = () => {
    const { user, isLoading } = useAuth();

    if (isLoading) return <SplashScreen />;

    return (
        <Stack.Navigator screenOptions={{ headerShown: false }}>
            {user ? (
                // 已登入：主畫面
                <Stack.Screen name="Main" component={MainTabs} />
            ) : (
                // 未登入：認證流程
                <Stack.Group screenOptions={{ animationTypeForReplace: "pop" }}>
                    <Stack.Screen name="Login" component={LoginScreen} />
                    <Stack.Screen name="Register" component={RegisterScreen} />
                    <Stack.Screen name="ForgotPassword" component={ForgotScreen} />
                </Stack.Group>
            )}
        </Stack.Navigator>
    );
};
```

## 自訂導航動畫

React Navigation 支援自訂頁面切換動畫：

```jsx
import { TransitionPresets } from "@react-navigation/stack";

const Stack = createStackNavigator();

const RootStack = () => (
    <Stack.Navigator
        screenOptions={{
            ...TransitionPresets.SlideFromRightIOS,
        }}
    >
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen
            name="Modal"
            component={ModalScreen}
            options={{
                ...TransitionPresets.ModalPresentationIOS,
                headerShown: false,
            }}
        />
    </Stack.Navigator>
);
```

## Tab 導航的進階用法

### 自訂 Tab Bar

```jsx
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { View, TouchableOpacity, StyleSheet } from "react-native";

const CustomTabBar = ({ state, descriptors, navigation }) => (
    <View style={styles.tabBar}>
        {state.routes.map((route, index) => {
            const { options } = descriptors[route.key];
            const isFocused = state.index === index;

            const onPress = () => {
                const event = navigation.emit({
                    type: "tabPress",
                    target: route.key,
                });
                if (!isFocused && !event.defaultPrevented) {
                    navigation.navigate(route.name);
                }
            };

            return (
                <TouchableOpacity
                    key={route.key}
                    onPress={onPress}
                    style={[styles.tab, isFocused && styles.tabFocused]}
                >
                    {options.tabBarIcon({
                        focused: isFocused,
                        color: isFocused ? "#007AFF" : "#999",
                        size: 24,
                    })}
                </TouchableOpacity>
            );
        })}
    </View>
);

const Tab = createBottomTabNavigator();

const MainTabs = () => (
    <Tab.Navigator tabBar={(props) => <CustomTabBar {...props} />}>
        <Tab.Screen name="Home" component={HomeScreen} />
        <Tab.Screen name="Search" component={SearchScreen} />
        <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
);
```

## 導航事件監聽

```jsx
import { useFocusEffect } from "@react-navigation/native";
import { useCallback } from "react";

const ProfileScreen = ({ navigation }) => {
    // 每次頁面獲得焦點時執行
    useFocusEffect(
        useCallback(() => {
            refreshProfile();
            return () => {
                // 頁面離開焦點時清理
                cleanup();
            };
        }, [])
    );

    // 監聽特定事件
    useEffect(() => {
        const unsubscribe = navigation.addListener("blur", () => {
            console.log("頁面離開");
        });
        return unsubscribe;
    }, [navigation]);
};
```

## 模態視窗（Modal）

```jsx
const RootStack = () => (
    <Stack.Navigator>
        <Stack.Screen name="Main" component={MainTabs} />
        <Stack.Group screenOptions={{ presentation: "modal" }}>
            <Stack.Screen name="CreatePost" component={CreatePostScreen} />
            <Stack.Screen name="ImagePicker" component={ImagePickerScreen} />
        </Stack.Group>
    </Stack.Navigator>
);
```

## Drawer 選單客製化

```jsx
import { DrawerContentScrollView, DrawerItemList } from "@react-navigation/drawer";

const CustomDrawerContent = (props) => (
    <DrawerContentScrollView {...props}>
        <View style={styles.drawerHeader}>
            <Image source={{ uri: user.avatar }} style={styles.avatar} />
            <Text style={styles.userName}>{user.name}</Text>
        </View>
        <DrawerItemList {...props} />
        <TouchableOpacity style={styles.logout} onPress={handleLogout}>
            <Text>登出</Text>
        </TouchableOpacity>
    </DrawerContentScrollView>
);

const AppDrawer = () => (
    <Drawer.Navigator
        drawerContent={(props) => <CustomDrawerContent {...props} />}
    >
        <Drawer.Screen name="Home" component={HomeTabs} />
        <Drawer.Screen name="Settings" component={SettingsScreen} />
    </Drawer.Navigator>
);
```

---

## 延伸閱讀

- [React Navigation 官方文件](https://www.google.com/search?q=React+Navigation+documentation)
- [React Navigation 深度連結](https://www.google.com/search?q=React+Navigation+deep+linking)
- [React Navigation 動畫指南](https://www.google.com/search?q=React+Navigation+animations)
