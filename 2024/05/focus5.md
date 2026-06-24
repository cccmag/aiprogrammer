# 狀態管理與資料流

## React 狀態管理的演進

React Native 繼承了 React 的狀態管理哲學——單向資料流。從最早的 `setState` 到現代的 Context API 和 Redux Toolkit，狀態管理的演進反映了前端開發對可預測性和可維護性的追求。

### 元件本地狀態

最簡單的狀態管理是元件的本地狀態：

```jsx
import { useState } from "react";
import { View, Text, Button, StyleSheet } from "react-native";

const Counter = () => {
    const [count, setCount] = useState(0);

    return (
        <View style={styles.container}>
            <Text style={styles.count}>{count}</Text>
            <View style={styles.buttons}>
                <Button
                    title="增加"
                    onPress={() => setCount((c) => c + 1)}
                />
                <Button
                    title="重置"
                    onPress={() => setCount(0)}
                    color="red"
                />
            </View>
        </View>
    );
};
```

## Context API 與 useReducer

當狀態需要在多個元件間共享時，Context API 是內建的解決方案：

```jsx
import React, { createContext, useContext, useReducer } from "react";

// 1. 定義狀態類型與動作
type AuthState = {
    user: User | null;
    isLoading: boolean;
};

type AuthAction =
    | { type: "LOGIN"; payload: User }
    | { type: "LOGOUT" }
    | { type: "SET_LOADING"; payload: boolean };

// 2. 定義 Reducer
const authReducer = (state: AuthState, action: AuthAction): AuthState => {
    switch (action.type) {
        case "LOGIN":
            return { ...state, user: action.payload, isLoading: false };
        case "LOGOUT":
            return { ...state, user: null, isLoading: false };
        case "SET_LOADING":
            return { ...state, isLoading: action.payload };
        default:
            return state;
    }
};

// 3. 建立 Context
const AuthContext = createContext<{
    state: AuthState;
    dispatch: React.Dispatch<AuthAction>;
} | null>(null);

// 4. Provider 元件
export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [state, dispatch] = useReducer(authReducer, {
        user: null,
        isLoading: false,
    });

    return (
        <AuthContext.Provider value={{ state, dispatch }}>
            {children}
        </AuthContext.Provider>
    );
};

// 5. 自訂 Hook
export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error("useAuth must be used within AuthProvider");
    }
    return context;
};
```

## Redux Toolkit

對於大型應用，Redux Toolkit 提供了更結構化的狀態管理：

```jsx
import { configureStore, createSlice } from "@reduxjs/toolkit";

// Slice：包含 Reducer 和 Actions
const cartSlice = createSlice({
    name: "cart",
    initialState: {
        items: [],
        total: 0,
    },
    reducers: {
        addItem: (state, action) => {
            state.items.push(action.payload);
            state.total += action.payload.price;
        },
        removeItem: (state, action) => {
            state.items = state.items.filter(
                (item) => item.id !== action.payload
            );
            state.total = state.items.reduce(
                (sum, item) => sum + item.price, 0
            );
        },
        clearCart: (state) => {
            state.items = [];
            state.total = 0;
        },
    },
});

export const { addItem, removeItem, clearCart } = cartSlice.actions;

// Store 配置
export const store = configureStore({
    reducer: {
        cart: cartSlice.reducer,
        auth: authSlice.reducer,
        products: productsSlice.reducer,
    },
});

// App 入口
import { Provider } from "react-redux";

const App = () => (
    <Provider store={store}>
        <MainNavigator />
    </Provider>
);
```

## 元件中使用狀態

```jsx
import { useSelector, useDispatch } from "react-redux";
import { addItem, removeItem } from "../store/cartSlice";

const ProductCard = ({ product }) => {
    const dispatch = useDispatch();
    const cartItems = useSelector((state) => state.cart.items);
    const inCart = cartItems.some((item) => item.id === product.id);

    return (
        <View style={styles.card}>
            <Text style={styles.name}>{product.name}</Text>
            <Text style={styles.price}>NT${product.price}</Text>
            <Button
                title={inCart ? "移除" : "加入購物車"}
                onPress={() =>
                    dispatch(inCart ? removeItem(product.id) : addItem(product))
                }
            />
        </View>
    );
};
```

## Zustand：輕量化替代方案

如果 Redux 對你的專案來說太重，Zustand 是受歡迎的替代：

```jsx
import { create } from "zustand";

const useStore = create((set) => ({
    user: null,
    token: null,
    login: async (credentials) => {
        const response = await api.login(credentials);
        set({ user: response.user, token: response.token });
    },
    logout: () => set({ user: null, token: null }),
}));

// 在元件中直接使用
const ProfileScreen = () => {
    const user = useStore((state) => state.user);
    const logout = useStore((state) => state.logout);
    // ...
};
```

### 狀態管理選擇指南

```
專案大小    推薦方案
────────    ────────
小型專案     useState + useContext
中型專案     Zustand 或 Jotai
大型專案     Redux Toolkit + RTK Query
```

---

## 延伸閱讀

- [Redux Toolkit 文件](https://www.google.com/search?q=Redux+Toolkit+documentation)
- [React Context API 指南](https://www.google.com/search?q=React+Context+API+guide)
- [Zustand 狀態管理](https://www.google.com/search?q=Zustand+React+state+management)

---

*本篇文章為「AI 程式人雜誌 2024 年 5 月號」焦點系列之五。*
