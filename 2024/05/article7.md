# 網路請求與資料快取

## 離線優先的 App 設計

現代手機 App 需要在不穩定的網路環境下提供良好體驗。「離線優先」的設計哲學——先顯示快取資料，再在背景更新——已經成為行動開發的最佳實踐。

## fetch API 基礎

React Native 內建 `fetch` API，相容 Web 標準：

```jsx
const fetchProducts = async () => {
    try {
        const response = await fetch("https://api.example.com/products", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer YOUR_TOKEN",
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("API 請求失敗:", error);
        throw error;
    }
};
```

### Axios（進階選擇）

axios 是更受歡迎的 HTTP 客戶端，提供攔截器和請求取消：

```bash
npm install axios
```

```jsx
import axios from "axios";

const api = axios.create({
    baseURL: "https://api.example.com",
    timeout: 10000,
    headers: { "Content-Type": "application/json" },
});

// 請求攔截器
api.interceptors.request.use((config) => {
    const token = AsyncStorage.getItem("token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// 回應攔截器
api.interceptors.response.use(
    (response) => response.data,
    (error) => {
        if (error.response?.status === 401) {
            // Token 過期，重新導向登入
        }
        return Promise.reject(error);
    }
);

// API 服務
export const productApi = {
    getAll: () => api.get("/products"),
    getById: (id) => api.get(`/products/${id}`),
    create: (data) => api.post("/products", data),
    update: (id, data) => api.put(`/products/${id}`, data),
    delete: (id) => api.delete(`/products/${id}`),
};
```

## React Query（TanStack Query）

React Query（現名 TanStack Query）是資料擷取和快取的標準解決方案：

```bash
npm install @tanstack/react-query
```

### 基本用法

```jsx
import { QueryClient, QueryClientProvider, useQuery, useMutation } from "@tanstack/react-query";

const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            staleTime: 5 * 60 * 1000,     // 5 分鐘內視為新鮮
            cacheTime: 10 * 60 * 1000,    // 快取保留 10 分鐘
            retry: 3,                     // 失敗重試次數
            refetchOnWindowFocus: false,  // 不自動重新請求
        },
    },
});

const App = () => (
    <QueryClientProvider client={queryClient}>
        <MainNavigator />
    </QueryClientProvider>
);
```

### Query 範例

```jsx
const useProducts = (categoryId) => {
    return useQuery({
        queryKey: ["products", categoryId],
        queryFn: () => productApi.getAll({ category: categoryId }),
        enabled: !!categoryId, // 只在有 categoryId 時執行
    });
};

const ProductList = ({ categoryId }) => {
    const { data, isLoading, error, refetch } = useProducts(categoryId);

    if (isLoading) return <ActivityIndicator />;
    if (error) return <ErrorView message={error.message} onRetry={refetch} />;

    return (
        <FlatList
            data={data}
            renderItem={({ item }) => <ProductCard product={item} />}
        />
    );
};
```

### Mutation 範例

```jsx
const useCreateProduct = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (newProduct) => productApi.create(newProduct),
        onSuccess: (data) => {
            // 成功後重新獲取產品列表
            queryClient.invalidateQueries({ queryKey: ["products"] });
            // 顯示成功訊息
            Alert.alert("成功", "商品已建立");
        },
        onError: (error) => {
            Alert.alert("錯誤", error.message);
        },
    });
};

const CreateProductScreen = () => {
    const mutation = useCreateProduct();

    const handleSubmit = (formData) => {
        mutation.mutate(formData);
    };

    return (
        <View>
            {mutation.isLoading && <LoadingOverlay />}
            {/* 表單內容 */}
            <Button title="建立" onPress={handleSubmit} />
        </View>
    );
};
```

## 離線快取策略

### AsyncStorage + React Query 持久化

```jsx
import { persistQueryClient } from "@tanstack/react-query-persist-client";
import { createAsyncStoragePersister } from "@tanstack/query-async-storage-persister";
import AsyncStorage from "@react-native-async-storage/async-storage";

const asyncStoragePersister = createAsyncStoragePersister({
    storage: AsyncStorage,
    key: "REACT_QUERY_OFFLINE_CACHE",
});

// 配置持久化
<QueryClientProvider client={queryClient}>
    <PersistQueryClientProvider
        client={queryClient}
        persistOptions={{
            persister: asyncStoragePersister,
            maxAge: 24 * 60 * 60 * 1000, // 24 小時
        }}
        onSuccess={() => {
            // 快取回復完成，恢復監聽
            queryClient.resumePausedMutations();
        }}
    >
        <MainNavigator />
    </PersistQueryClientProvider>
</QueryClientProvider>
```

## 網路狀態監控

```bash
npm install @react-native-community/netinfo
```

```jsx
import NetInfo from "@react-native-community/netinfo";
import { useState, useEffect } from "react";

const useNetworkStatus = () => {
    const [isConnected, setIsConnected] = useState(true);

    useEffect(() => {
        const unsubscribe = NetInfo.addEventListener((state) => {
            setIsConnected(state.isConnected);
        });
        return () => unsubscribe();
    }, []);

    return isConnected;
};

const OfflineBanner = () => {
    const isConnected = useNetworkStatus();

    if (isConnected) return null;

    return (
        <View style={styles.banner}>
            <Text style={styles.text}>
                您目前處於離線狀態
            </Text>
        </View>
    );
};
```

---

## 延伸閱讀

- [TanStack Query 文件](https://www.google.com/search?q=TanStack+Query+React)
- [Axios HTTP 客戶端](https://www.google.com/search?q=Axios+HTTP+client)
- [React Native NetInfo](https://www.google.com/search?q=React+Native+NetInfo)
