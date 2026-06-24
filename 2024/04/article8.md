# React Router 路由設定

## 前言

路由是現代 Web 應用的基礎設施。React Router 是 React 生態中最受歡迎的路由解決方案，v6 版本提供了完整而簡潔的 API。本文將深入探討 React Router 的各種設定方式。

## 安裝與基本設定

```bash
npm install react-router-dom
```

最簡單的路由設定：

```jsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
      </nav>
      
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  )
}
```

## 路由模式

React Router 支援三種路由模式：

```jsx
// BrowserRouter：使用 HTML5 History API（推薦）
<BrowserRouter>
  <App />
</BrowserRouter>

// HashRouter：使用 URL hash（#）
<HashRouter>
  <App />
</HashRouter>

// MemoryRouter：記憶體路由（測試用）
<MemoryRouter>
  <App />
</MemoryRouter>
```

BrowserRouter 需要伺服器端支援（所有路徑返回 index.html），HashRouter 則不需要。

## 動態路由與 useParams

```jsx
function App() {
  return (
    <Routes>
      <Route path="/users/:userId" element={<UserDetail />} />
      <Route path="/posts/:postId/comments/:commentId" element={<CommentDetail />} />
    </Routes>
  )
}

function UserDetail() {
  const { userId } = useParams()
  const navigate = useNavigate()
  
  useEffect(() => {
    fetchUser(userId).catch(() => navigate('/not-found'))
  }, [userId])
  
  return <UserProfile id={userId} />
}
```

## 巢狀路由與 Outlet

React Router v6 的巢狀路由讓頁面佈局更加靈活：

```jsx
function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="products" element={<Products />}>
          <Route index element={<ProductList />} />
          <Route path=":id" element={<ProductDetail />} />
          <Route path=":id/edit" element={<ProductEdit />} />
        </Route>
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  )
}

function Layout() {
  return (
    <div>
      <Header />
      <Sidebar />
      <main>
        <Outlet />
      </main>
      <Footer />
    </div>
  )
}

function Products() {
  return (
    <div>
      <ProductSidebar />
      <div className="content">
        <Outlet />
      </div>
    </div>
  )
}
```

## 查詢參數

使用 `useSearchParams` 處理 URL 查詢參數：

```jsx
function ProductList() {
  const [searchParams, setSearchParams] = useSearchParams()
  
  const category = searchParams.get('category') || 'all'
  const sort = searchParams.get('sort') || 'newest'
  const page = parseInt(searchParams.get('page') || '1')
  
  function updateFilter(key, value) {
    setSearchParams(prev => {
      if (value) prev.set(key, value)
      else prev.delete(key)
      return prev
    })
  }
  
  return (
    <div>
      <select value={category} onChange={e => updateFilter('category', e.target.value)}>
        <option value="all">All</option>
        <option value="electronics">Electronics</option>
      </select>
      <ProductGrid category={category} sort={sort} page={page} />
    </div>
  )
}
```

## 路由守衛與認證

```jsx
function ProtectedRoute({ children, requiredRole }) {
  const { user } = useAuth()
  const location = useLocation()
  
  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }
  
  if (requiredRole && user.role !== requiredRole) {
    return <Navigate to="/unauthorized" replace />
  }
  
  return children
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<PublicLayout />}>
        <Route index element={<Home />} />
        <Route path="login" element={<Login />} />
      </Route>
      
      <Route path="/dashboard" element={
        <ProtectedRoute requiredRole="admin">
          <DashboardLayout />
        </ProtectedRoute>
      }>
        <Route index element={<Dashboard />} />
        <Route path="users" element={<UserManagement />} />
      </Route>
    </Routes>
  )
}
```

## Lazy Loading

使用 `React.lazy` 實現路由層級的程式碼分割：

```jsx
import { lazy, Suspense } from 'react'

const Dashboard = lazy(() => import('./pages/Dashboard'))
const Settings = lazy(() => import('./pages/Settings'))
const UserProfile = lazy(() => import('./pages/UserProfile'))

function App() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/users/:id" element={<UserProfile />} />
      </Routes>
    </Suspense>
  )
}
```

## 客製化 Link

可以建立自訂的連結元件，統一處理樣式和行為：

```jsx
import { NavLink } from 'react-router-dom'

function CustomLink({ to, children, ...props }) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}
      {...props}
    >
      {children}
    </NavLink>
  )
}
```

## 結語

React Router v6 提供了一套完整的路由解決方案。從基本的頁面切換到複雜的巢狀佈局、路由守衛、Lazy Loading，都能以直覺的方式實現。搭配 TypeScript，路由設定可以做到型別安全。

---

## 延伸閱讀

- [React Router v6 文件](https://www.google.com/search?q=React+Router+v6+documentation)
- [React 程式碼分割](https://www.google.com/search?q=React+code+splitting+lazy+loading)
- [React Router 認證模式](https://www.google.com/search?q=React+Router+authentication+pattern)

---

*本篇文章為「AI 程式人雜誌 2024 年 4 月號」精選文章之八。*
