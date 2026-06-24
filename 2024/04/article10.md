# 測試 React 元件

## 前言

測試是確保軟體品質的重要手段。在前端開發中，元件測試是最常見的測試形式。本文將介紹如何使用 Vitest 和 Testing Library 對 React 元件進行測試。

## 測試環境設定

首先安裝必要的套件：

```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom
```

在 `vite.config.js` 中設定：

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.js'],
  },
})
```

建立 `setup.js`：

```javascript
import '@testing-library/jest-dom'
```

在 `package.json` 中加入測試指令：

```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}
```

## 元件測試基礎

Testing Library 的核心原則是：測試應該模擬使用者如何使用元件，而非測試實作細節。

```javascript
import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import Counter from './Counter'

describe('Counter', () => {
  it('renders with initial count', () => {
    render(<Counter />)
    expect(screen.getByText('Count: 0')).toBeDefined()
  })
  
  it('increments count on button click', () => {
    render(<Counter />)
    const button = screen.getByText('+1')
    
    fireEvent.click(button)
    expect(screen.getByText('Count: 1')).toBeDefined()
  })
  
  it('decrements count on minus button', () => {
    render(<Counter />)
    const button = screen.getByText('-1')
    
    fireEvent.click(button)
    fireEvent.click(button)
    expect(screen.getByText('Count: -2')).toBeDefined()
  })
})
```

## 表單測試

測試表單需要模擬使用者輸入和提交：

```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import LoginForm from './LoginForm'

describe('LoginForm', () => {
  it('shows validation errors for empty fields', async () => {
    render(<LoginForm />)
    
    const submitButton = screen.getByRole('button', { name: /login/i })
    fireEvent.click(submitButton)
    
    await waitFor(() => {
      expect(screen.getByText(/email is required/i)).toBeDefined()
      expect(screen.getByText(/password is required/i)).toBeDefined()
    })
  })
  
  it('submits form with valid data', async () => {
    const onSubmit = vi.fn()
    render(<LoginForm onSubmit={onSubmit} />)
    
    await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com')
    await userEvent.type(screen.getByLabelText(/password/i), 'password123')
    
    fireEvent.click(screen.getByRole('button', { name: /login/i }))
    
    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      })
    })
  })
})
```

## 非同步測試

測試含有非同步操作的元件：

```javascript
import { render, screen, waitFor } from '@testing-library/react'
import { rest } from 'msw'
import { setupServer } from 'msw/node'
import UserList from './UserList'

const server = setupServer(
  rest.get('/api/users', (req, res, ctx) => {
    return res(ctx.json([
      { id: 1, name: 'Alice' },
      { id: 2, name: 'Bob' },
    ]))
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe('UserList', () => {
  it('displays users after loading', async () => {
    render(<UserList />)
    
    expect(screen.getByText(/loading/i)).toBeDefined()
    
    await waitFor(() => {
      expect(screen.getByText('Alice')).toBeDefined()
      expect(screen.getByText('Bob')).toBeDefined()
    })
  })
  
  it('shows error message on API failure', async () => {
    server.use(
      rest.get('/api/users', (req, res, ctx) => {
        return res(ctx.status(500))
      })
    )
    
    render(<UserList />)
    
    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeDefined()
    })
  })
})
```

## Hook 測試

使用 `renderHook` 測試自訂 Hook：

```javascript
import { renderHook, act } from '@testing-library/react'
import useCounter from './useCounter'

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter())
    expect(result.current.count).toBe(0)
  })
  
  it('initializes with custom value', () => {
    const { result } = renderHook(() => useCounter(10))
    expect(result.current.count).toBe(10)
  })
  
  it('increments count', () => {
    const { result } = renderHook(() => useCounter(0))
    
    act(() => result.current.increment())
    expect(result.current.count).toBe(1)
    
    act(() => result.current.increment())
    expect(result.current.count).toBe(2)
  })
  
  it('decrements count', () => {
    const { result } = renderHook(() => useCounter(5))
    
    act(() => result.current.decrement())
    expect(result.current.count).toBe(4)
  })
  
  it('resets to initial value', () => {
    const { result } = renderHook(() => useCounter(5))
    
    act(() => result.current.increment())
    act(() => result.current.increment())
    expect(result.current.count).toBe(7)
    
    act(() => result.current.reset())
    expect(result.current.count).toBe(5)
  })
})
```

## Router 測試

測試使用 React Router 的元件時，需要用 MemoryRouter 包裹：

```javascript
import { render, screen } from '@testing-library/react'
import { MemoryRouter, Routes, Route } from 'react-router-dom'
import UserPage from './UserPage'

describe('UserPage', () => {
  it('renders user detail with route params', () => {
    render(
      <MemoryRouter initialEntries={['/users/42']}>
        <Routes>
          <Route path="/users/:id" element={<UserPage />} />
        </Routes>
      </MemoryRouter>
    )
    
    expect(screen.getByText(/user 42/i)).toBeDefined()
  })
})
```

## Context 測試

測試使用 Context 的元件時，需要提供對應的 Provider：

```javascript
import { render, screen } from '@testing-library/react'
import { ThemeContext } from './ThemeContext'
import ThemedButton from './ThemedButton'

describe('ThemedButton', () => {
  it('uses dark theme', () => {
    render(
      <ThemeContext.Provider value={{ theme: 'dark' }}>
        <ThemedButton />
      </ThemeContext.Provider>
    )
    
    expect(screen.getByRole('button')).toHaveClass('dark')
  })
})
```

## 測試覆蓋率

Vitest 支援內建的覆蓋率報告：

```bash
npx vitest --coverage
```

## 測試最佳實踐

1. **優先測試使用者行為**：Testing Library 的理念是「測試應該像使用者一樣使用應用」
2. **避免測試實作細節**：不要測試 state、props 或內部方法
3. **使用 data-testid 作為最後手段**：優先使用 role、label、text
4. **保持測試簡單**：一個測試案例測試一個行為
5. **使用 Mock 服務**：使用 MSW 模擬 API，避免實際網路請求

## 結語

測試 React 元件不再困難。搭配 Vitest 的快速執行和 Testing Library 的使用者中心測試哲學，開發者可以建立可靠且可維護的測試套件。

---

## 延伸閱讀

- [Testing Library 文件](https://www.google.com/search?q=Testing+Library+React+documentation)
- [Vitest 文件](https://www.google.com/search?q=Vitest+React+testing)
- [MSW 模擬服務](https://www.google.com/search?q=MSW+Mock+Service+Worker+React)

---

*本篇文章為「AI 程式人雜誌 2024 年 4 月號」精選文章之十。*
