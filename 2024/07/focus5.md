# ViewModel 與資料流

## MVVM 架構核心

ViewModel 是 Android Jetpack 架構元件的核心，負責管理 UI 相關的資料，並在配置變更（如螢幕旋轉）時保持資料存活。

---

## MVVM 架構模式

```
┌──────────┐    觀察/事件    ┌──────────┐    資料請求    ┌──────────┐
│   View    │◄──────────────►│ ViewModel│◄──────────────►│  Model   │
│ (Compose) │   StateFlow    │          │   Repository   │ (Room/   │
│           │                │          │                │  Retrofit)│
└──────────┘                └──────────┘                └──────────┘
```

- **View**：負責 UI 渲染，觀察 ViewModel 的狀態
- **ViewModel**：持有 UI 狀態，處理業務邏輯
- **Model**：資料層，包含資料庫和網路來源

---

## ViewModel 原理

### 基本使用

```kotlin
class CounterViewModel : ViewModel() {
  private val _count = MutableStateFlow(0)
  val count: StateFlow<Int> = _count.asStateFlow()

  fun increment() { _count.value++ }
  fun decrement() { _count.value-- }
}
```

### 在 Composable 中使用

```kotlin
@Composable
fun CounterScreen(viewModel: CounterViewModel = viewModel()) {
  val count by viewModel.count.collectAsState()

  Column(horizontalAlignment = Alignment.CenterHorizontally) {
    Text("Count: $count", style = MaterialTheme.typography.headlineLarge)
    Row {
      Button(onClick = { viewModel.decrement() }) { Text("-") }
      Spacer(modifier = Modifier.width(16.dp))
      Button(onClick = { viewModel.increment() }) { Text("+") }
    }
  }
}
```

### ViewModel 的生命週期

ViewModel 存活於 `ViewModelStoreOwner` 的範圍內（如 Activity 或 Navigation 目的地）：

```
Activity 建立 ──┐
                ├──► ViewModel 建立
Activity 旋轉 ──┤
                ├──► ViewModel 存活（不重建）
Activity 銷毀 ──┘
                └──► ViewModel.onCleared()
```

---

## StateFlow 與 LiveData

### StateFlow（推薦）

StateFlow 是 Kotlin 協程的狀態持有者：

```kotlin
class UserViewModel : ViewModel() {
  private val _user = MutableStateFlow<User?>(null)
  val user: StateFlow<User?> = _user.asStateFlow()

  private val _isLoading = MutableStateFlow(false)
  val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

  fun loadUser(id: String) {
    viewModelScope.launch {
      _isLoading.value = true
      try {
        _user.value = userRepository.fetchUser(id)
      } catch (e: Exception) {
        _user.value = null
      } finally {
        _isLoading.value = false
      }
    }
  }
}
```

### LiveData（傳統方案）

```kotlin
class LiveDataViewModel : ViewModel() {
  private val _user = MutableLiveData<User?>()
  val user: LiveData<User?> = _user

  fun loadUser(id: String) {
    viewModelScope.launch {
      _user.value = userRepository.fetchUser(id)
    }
  }
}
```

StateFlow 優於 LiveData：支援協程、不與 Lifecycle 耦合（需手動 collect）、提供初始值。

---

## 狀態提升（State Hoisting）

Compose 的狀態提升模式將狀態移到 ViewModel 或 Composable 上游：

```kotlin
// 低層元件 - 無狀態
@Composable
fun TextField(
  value: String,
  onValueChange: (String) -> Unit,
  modifier: Modifier = Modifier
) {
  OutlinedTextField(
    value = value,
    onValueChange = onValueChange,
    modifier = modifier
  )
}

// 高層元件 - 持有狀態
@Composable
fun LoginScreen(viewModel: LoginViewModel = viewModel()) {
  val email by viewModel.email.collectAsState()
  val password by viewModel.password.collectAsState()

  Column {
    TextField(value = email, onValueChange = viewModel::onEmailChange)
    TextField(value = password, onValueChange = viewModel::onPasswordChange)
    Button(onClick = { viewModel.login() }) { Text("Login") }
  }
}
```

---

## SharedViewModel

多個 Fragment 共享同一個 ViewModel：

```kotlin
// 在 Navigation Compose 中
@Composable
fun SharedViewModelExample() {
  val viewModel: SharedViewModel = viewModel()

  NavHost(navController, startDestination = "screenA") {
    composable("screenA") { ScreenA(viewModel) }
    composable("screenB") { ScreenB(viewModel) }
  }
}
```

---

## 總結

ViewModel 結合 StateFlow 和 Compose 的狀態提升模式，形成了一個清晰、可測試的 MVVM 架構。ViewModel 負責管理 UI 狀態的完整生命週期，開發者只需要關注商業邏輯。

---

## 延伸閱讀

- [ViewModel 官方指南](https://www.google.com/search?q=Android+ViewModel+guide)
- [StateFlow 與 LiveData 對比](https://www.google.com/search?q=StateFlow+vs+LiveData+Android)
- [Compose 狀態管理](https://www.google.com/search?q=Compose+state+management)
