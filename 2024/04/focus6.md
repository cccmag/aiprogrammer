# React Router 與 SPA

## SPA 的概念

單頁應用程式（Single Page Application, SPA）是一種 Web 應用架構，在初始載入後，後續的頁面切換不需要重新載入整個頁面，而是透過 JavaScript 動態更新內容。

SPA 的優點是使用者體驗流暢，頁面切換迅速；缺點是初始載入較慢、SEO 相對困難，以及對瀏覽器歷史管理有較高要求。

React 常見的 SPA 實現方式有兩種：

- **客戶端路由**：React Router、TanStack Router
- **框架內建路由**：Next.js、Remix 的檔案系統路由

## React Router 基礎

React Router 是 React 生態系統中最受歡迎的路由解決方案。在 v6 中，API 變得更加簡潔和直覺：

```jsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/users">Users</Link>
      </nav>
      
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/users" element={<Users />} />
      </Routes>
    </BrowserRouter>
  )
}
```

`Routes` 元件會根據當前 URL 匹配對應的 `Route`，並渲染其 `element` 屬性。`Link` 元件取代了 HTML 的 `<a>`，可以無刷新切換頁面。

## 動態路由與參數

React Router v6 支援動態路由參數：

```jsx
function App() {
  return (
    <Routes>
      <Route path="/users/:userId" element={<UserDetail />} />
    </Routes>
  )
}

function UserDetail() {
  const { userId } = useParams()
  const [user, setUser] = useState(null)
  
  useEffect(() => {
    fetch(`/api/users/${userId}`).then(r => r.json()).then(setUser)
  }, [userId])
  
  if (!user) return <p>Loading...</p>
  return <div><h1>{user.name}</h1></div>
}
```

`useParams` Hook 回傳 URL 參動物件，`userId` 的值來自路由模式中的 `:userId`。

## 巢狀路由

React Router v6 支援巢狀路由，讓頁面佈局更加靈活：

```jsx
function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="products" element={<Products />} />
        <Route path="products/:id" element={<ProductDetail />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  )
}

function Layout() {
  return (
    <div>
      <Header />
      <main>
        <Outlet /> {/* 子路由在這裡渲染 */}
      </main>
      <Footer />
    </div>
  )
}
```

`Outlet` 元件是巢狀路由的關鍵——它表示子路由內容的渲染位置。`index` 屬性表示預設子路由。

## 路由導航

除了使用 `Link` 元件，React Router 還提供了程式化導航的方式：

```jsx
import { useNavigate } from 'react-router-dom'

function LoginPage() {
  const navigate = useNavigate()
  
  async function handleLogin(data) {
    await login(data)
    navigate('/dashboard', { replace: true })
  }
  
  return <LoginForm onSubmit={handleLogin} />
}
```

`useNavigate` 回傳一個導航函式，可以接受路徑字串或數字（用於前進後退）。`replace: true` 表示取代當前歷史記錄而非新增。

## 路由守衛

在實務中，某些頁面需要登入才能存取：

```jsx
function ProtectedRoute({ children }) {
  const { user } = useAuth()
  
  if (!user) {
    return <Navigate to="/login" replace />
  }
  
  return children
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={
        <ProtectedRoute>
          <Dashboard />
        </ProtectedRoute>
      } />
    </Routes>
  )
}
```

使用 `Navigate` 元件進行宣告式重定向，在路由層級檢查使用者的驗證狀態。

## SEO 考量

對於需要 SEO 的 SPA，可以考慮：

- **SSR（Server-Side Rendering）**：使用 Next.js 或 Remix
- **SSG（Static Site Generation）**：預先生成靜態 HTML
- **Prerender**：使用 prerender.io 等服務

## 結語

React Router 為 SPA 提供了完整的路由解決方案，從基本的頁面切換到複雜的巢狀佈局、路由守衛，都能優雅地實現。理解 React Router 的工作原理，是建構大型 React 應用的必備技能。

---

## 延伸閱讀

- [React Router v6 文件](https://www.google.com/search?q=React+Router+v6+documentation)
- [SPA 架構深入](https://www.google.com/search?q=SPA+architecture+explained)
- [React Router vs Next.js Router](https://www.google.com/search?q=React+Router+vs+Next.js+routing)

---

*本篇文章為「AI 程式人雜誌 2024 年 4 月號」焦點系列之六。*
