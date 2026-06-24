# useState 與表單

## 前言

表單是 Web 應用中最常見的元件之一。在 React 中，表單處理的核心是「可控元件」模式——表單元素的值由 React 狀態控制，而非由 DOM 自己管理。

## 可控元件基礎

可控元件的關鍵：表單元素的值綁定到 state，變更事件觸發 state 更新：

```jsx
function SimpleForm() {
  const [name, setName] = useState('')
  
  function handleChange(e) {
    setName(e.target.value)
  }
  
  return (
    <div>
      <input value={name} onChange={handleChange} />
      <p>Hello, {name}!</p>
    </div>
  )
}
```

每個 `onChange` 事件都會更新 state，而 state 的變化又驅動 React 重新渲染 input，形成一個閉鎖循環。

## 多欄位表單

當表單有多個欄位時，可以將所有欄位值放在一個物件中：

```jsx
function RegistrationForm() {
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  })
  
  function handleChange(e) {
    const { name, value } = e.target
    setForm(prev => ({ ...prev, [name]: value }))
  }
  
  function handleSubmit(e) {
    e.preventDefault()
    if (form.password !== form.confirmPassword) {
      alert('Passwords do not match!')
      return
    }
    submitForm(form)
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <input name="username" value={form.username} onChange={handleChange} placeholder="Username" />
      <input name="email" type="email" value={form.email} onChange={handleChange} placeholder="Email" />
      <input name="password" type="password" value={form.password} onChange={handleChange} placeholder="Password" />
      <input name="confirmPassword" type="password" value={form.confirmPassword} onChange={handleChange} placeholder="Confirm" />
      <button type="submit">Register</button>
    </form>
  )
}
```

利用 `e.target.name` 來區分不同的表單欄位，所有 input 共用同一個 `handleChange` 函式。

## 不同表單元素的處理

### Checkbox

```jsx
function Settings() {
  const [notifications, setNotifications] = useState({
    email: true,
    sms: false,
    push: true,
  })
  
  function handleCheckbox(e) {
    const { name, checked } = e.target
    setNotifications(prev => ({ ...prev, [name]: checked }))
  }

  return (
    <div>
      <label>
        <input type="checkbox" name="email" checked={notifications.email} onChange={handleCheckbox} />
        Email
      </label>
      <label>
        <input type="checkbox" name="sms" checked={notifications.sms} onChange={handleCheckbox} />
        SMS
      </label>
      <label>
        <input type="checkbox" name="push" checked={notifications.push} onChange={handleCheckbox} />
        Push
      </label>
    </div>
  )
}
```

### Select 下拉選單

```jsx
function CitySelector() {
  const [city, setCity] = useState('')
  
  return (
    <select value={city} onChange={e => setCity(e.target.value)}>
      <option value="">Select a city</option>
      <option value="taipei">Taipei</option>
      <option value="kaohsiung">Kaohsiung</option>
      <option value="taichung">Taichung</option>
    </select>
  )
}
```

### Radio 按鈕

```jsx
function GenderSelector() {
  const [gender, setGender] = useState('')
  
  return (
    <div>
      <label>
        <input type="radio" name="gender" value="male" checked={gender === 'male'} onChange={e => setGender(e.target.value)} />
        Male
      </label>
      <label>
        <input type="radio" name="gender" value="female" checked={gender === 'female'} onChange={e => setGender(e.target.value)} />
        Female
      </label>
    </div>
  )
}
```

## 表單驗證

可以在 submit 時或即時進行驗證：

```jsx
function ValidatedForm() {
  const [email, setEmail] = useState('')
  const [error, setError] = useState('')
  
  function validateEmail(value) {
    if (!value.includes('@')) return 'Invalid email'
    if (!value.includes('.')) return 'Invalid email'
    return ''
  }
  
  function handleChange(e) {
    const value = e.target.value
    setEmail(value)
    setError(validateEmail(value))
  }
  
  function handleSubmit(e) {
    e.preventDefault()
    const err = validateEmail(email)
    if (err) {
      setError(err)
      return
    }
    submitEmail(email)
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <input value={email} onChange={handleChange} />
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button disabled={!!error}>Submit</button>
    </form>
  )
}
```

## 自訂 useForm Hook

可以將表單邏輯封裝為自訂 Hook，提升複用性：

```javascript
function useForm(initialValues) {
  const [values, setValues] = useState(initialValues)
  const [errors, setErrors] = useState({})
  
  function handleChange(e) {
    const { name, value, type, checked } = e.target
    setValues(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }))
  }
  
  function reset() {
    setValues(initialValues)
    setErrors({})
  }
  
  return { values, errors, handleChange, reset, setErrors }
}

// 使用
function MyForm() {
  const { values, errors, handleChange, handleSubmit } = useForm({
    name: '',
    email: '',
  })
  
  function handleSubmit(e) {
    e.preventDefault()
    console.log(values)
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <input name="name" value={values.name} onChange={handleChange} />
      <input name="email" value={values.email} onChange={handleChange} />
      <button type="submit">Submit</button>
    </form>
  )
}
```

## 結語

React 表單處理的核心是可控元件模式。透過 `useState` 管理表單狀態、統一的事件處理器、即時驗證，以及自訂 Hook 封裝邏輯，可以建構出健壯且可維護的表單元件。

---

## 延伸閱讀

- [React 表單文件](https://www.google.com/search?q=React+forms+controlled+components)
- [React Hook Form](https://www.google.com/search?q=React+Hook+Form+library)
- [Formik 表單管理](https://www.google.com/search?q=Formik+React+forms)

---

*本篇文章為「AI 程式人雜誌 2024 年 4 月號」精選文章之四。*
