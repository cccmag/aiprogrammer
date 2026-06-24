# 本地儲存 AsyncStorage

## 為什麼需要本地儲存？

手機 App 需要在本地儲存資料，以便在離線時使用、記住使用者偏好、快取 API 回應等場景。與 Web 的 localStorage 相對應，React Native 提供了 AsyncStorage。

## AsyncStorage 基本用法

AsyncStorage 是一個基於鍵值對的非同步持久化儲存系統。它將資料以字串形式儲存在裝置上。

```bash
npm install @react-native-async-storage/async-storage
```

```jsx
import AsyncStorage from "@react-native-async-storage/async-storage";

// 儲存資料
const storeData = async (key, value) => {
    try {
        await AsyncStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
        console.error("儲存失敗", e);
    }
};

// 讀取資料
const getData = async (key) => {
    try {
        const value = await AsyncStorage.getItem(key);
        return value ? JSON.parse(value) : null;
    } catch (e) {
        console.error("讀取失敗", e);
        return null;
    }
};

// 刪除資料
const removeData = async (key) => {
    try {
        await AsyncStorage.removeItem(key);
    } catch (e) {
        console.error("刪除失敗", e);
    }
};

// 清除所有資料
const clearAll = async () => {
    try {
        await AsyncStorage.clear();
    } catch (e) {
        console.error("清除失敗", e);
    }
};
```

## 實戰：記住登入狀態

```jsx
import AsyncStorage from "@react-native-async-storage/async-storage";
import { createContext, useContext, useState, useEffect } from "react";

const AUTH_KEY = "@auth_user";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // 啟動時檢查是否有已儲存的登入資訊
        restoreAuth();
    }, []);

    const restoreAuth = async () => {
        try {
            const savedUser = await AsyncStorage.getItem(AUTH_KEY);
            if (savedUser) {
                setUser(JSON.parse(savedUser));
            }
        } catch (e) {
            console.error("無法恢復登入狀態", e);
        } finally {
            setIsLoading(false);
        }
    };

    const login = async (credentials) => {
        const response = await api.login(credentials);
        const userData = response.user;
        await AsyncStorage.setItem(AUTH_KEY, JSON.stringify(userData));
        setUser(userData);
    };

    const logout = async () => {
        await AsyncStorage.removeItem(AUTH_KEY);
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, isLoading }}>
            {children}
        </AuthContext.Provider>
    );
};
```

## 管理使用者偏好設定

```jsx
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useState, useEffect } from "react";

const SETTINGS_KEY = "@app_settings";

type AppSettings = {
    theme: "light" | "dark" | "system";
    fontSize: "small" | "medium" | "large";
    notifications: boolean;
    language: string;
};

const defaultSettings: AppSettings = {
    theme: "system",
    fontSize: "medium",
    notifications: true,
    language: "zh-TW",
};

const useSettings = () => {
    const [settings, setSettings] = useState(defaultSettings);
    const [loaded, setLoaded] = useState(false);

    useEffect(() => {
        loadSettings();
    }, []);

    const loadSettings = async () => {
        const saved = await AsyncStorage.getItem(SETTINGS_KEY);
        if (saved) {
            setSettings({ ...defaultSettings, ...JSON.parse(saved) });
        }
        setLoaded(true);
    };

    const updateSettings = async (newSettings: Partial<AppSettings>) => {
        const merged = { ...settings, ...newSettings };
        setSettings(merged);
        await AsyncStorage.setItem(SETTINGS_KEY, JSON.stringify(merged));
    };

    return { settings, updateSettings, loaded };
};
```

## 資料快取實作

```jsx
import AsyncStorage from "@react-native-async-storage/async-storage";

const CACHE_PREFIX = "@cache_";
const DEFAULT_TTL = 5 * 60 * 1000; // 5 分鐘

const cache = {
    set: async (key, data, ttl = DEFAULT_TTL) => {
        const item = {
            data,
            expiresAt: Date.now() + ttl,
        };
        await AsyncStorage.setItem(
            `${CACHE_PREFIX}${key}`,
            JSON.stringify(item)
        );
    },

    get: async (key) => {
        const raw = await AsyncStorage.getItem(`${CACHE_PREFIX}${key}`);
        if (!raw) return null;

        const item = JSON.parse(raw);
        if (Date.now() > item.expiresAt) {
            await AsyncStorage.removeItem(`${CACHE_PREFIX}${key}`);
            return null;
        }

        return item.data;
    },

    remove: async (key) => {
        await AsyncStorage.removeItem(`${CACHE_PREFIX}${key}`);
    },

    clearExpired: async () => {
        const keys = await AsyncStorage.getAllKeys();
        const cacheKeys = keys.filter((k) => k.startsWith(CACHE_PREFIX));

        for (const key of cacheKeys) {
            const raw = await AsyncStorage.getItem(key);
            if (raw) {
                const item = JSON.parse(raw);
                if (Date.now() > item.expiresAt) {
                    await AsyncStorage.removeItem(key);
                }
            }
        }
    },
};

// 使用範例：快取 API 回應
const fetchWithCache = async (url, options = {}) => {
    const cacheKey = url;
    const cached = await cache.get(cacheKey);
    if (cached) return cached;

    const response = await fetch(url, options);
    const data = await response.json();
    await cache.set(cacheKey, data);
    return data;
};
```

## 安全儲存

對於敏感資料（如 Token），應使用安全儲存方案：

```bash
npm install react-native-keychain
# 或
npm install expo-secure-store
```

```jsx
import * as Keychain from "react-native-keychain";

export const secureStorage = {
    setToken: async (token) => {
        await Keychain.setGenericPassword("auth_token", token, {
            service: "com.myapp.auth",
            accessible: Keychain.ACCESSIBLE.WHEN_UNLOCKED_THIS_DEVICE_ONLY,
        });
    },

    getToken: async () => {
        const credentials = await Keychain.getGenericPassword({
            service: "com.myapp.auth",
        });
        return credentials ? credentials.password : null;
    },

    removeToken: async () => {
        await Keychain.resetGenericPassword({
            service: "com.myapp.auth",
        });
    },
};
```

---

## 延伸閱讀

- [AsyncStorage 文件](https://www.google.com/search?q=React+Native+AsyncStorage)
- [React Native 安全儲存](https://www.google.com/search?q=React+Native+secure+storage)
- [react-native-keychain](https://www.google.com/search?q=react-native-keychain)
