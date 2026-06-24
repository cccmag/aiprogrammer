# ViewModel 實戰

## MVVM 架構完整範例

### 專案場景：使用者管理 App

我們將建立一個簡單的使用者管理 App，展示 ViewModel 在實際專案中的應用：

- 顯示使用者列表
- 新增使用者
- 編輯使用者資訊
- 刪除使用者

### 資料層

```kotlin
// User.kt — 資料模型
data class User(
  val id: Long = 0,
  val name: String,
  val email: String,
  val age: Int
)

// UserRepository.kt — 資料倉儲
class UserRepository {
  private val users = mutableListOf<User>(
    User(1, "Alice", "alice@example.com", 28),
    User(2, "Bob", "bob@example.com", 35),
    User(3, "Charlie", "charlie@example.com", 22)
  )
  private var nextId = 4L

  fun getUsers(): List<User> = users.toList()

  fun getUser(id: Long): User? = users.find { it.id == id }

  fun addUser(user: User): User {
    val newUser = user.copy(id = nextId++)
    users.add(newUser)
    return newUser
  }

  fun updateUser(user: User): Boolean {
    val idx = users.indexOfFirst { it.id == user.id }
    return if (idx != -1) {
      users[idx] = user
      true
    } else false
  }

  fun deleteUser(id: Long): Boolean {
    return users.removeAll { it.id == id }
  }
}
```

### ViewModel 實作

```kotlin
// UserViewModel.kt
sealed class UserUiState {
  object Loading : UserUiState()
  data class Success(val users: List<User>) : UserUiState()
  data class Error(val message: String) : UserUiState()
}

class UserViewModel : ViewModel() {
  private val repository = UserRepository()

  private val _uiState = MutableStateFlow<UserUiState>(UserUiState.Loading)
  val uiState: StateFlow<UserUiState> = _uiState.asStateFlow()

  private val _selectedUser = MutableStateFlow<User?>(null)
  val selectedUser: StateFlow<User?> = _selectedUser.asStateFlow()

  init { loadUsers() }

  fun loadUsers() {
    _uiState.value = try {
      UserUiState.Success(repository.getUsers())
    } catch (e: Exception) {
      UserUiState.Error(e.message ?: "Failed to load users")
    }
  }

  fun selectUser(id: Long) {
    _selectedUser.value = repository.getUser(id)
  }

  fun clearSelection() {
    _selectedUser.value = null
  }

  fun addUser(name: String, email: String, age: Int) {
    val newUser = repository.addUser(User(name = name, email = email, age = age))
    loadUsers()
  }

  fun updateUser(id: Long, name: String, email: String, age: Int) {
    repository.updateUser(User(id = id, name = name, email = email, age = age))
    loadUsers()
  }

  fun deleteUser(id: Long) {
    repository.deleteUser(id)
    loadUsers()
  }
}
```

### UI 層（Compose）

```kotlin
// UserListScreen.kt
@Composable
fun UserListScreen(
  viewModel: UserViewModel = viewModel(),
  onNavigateToDetail: (Long) -> Unit
) {
  val uiState by viewModel.uiState.collectAsState()

  Scaffold(
    topBar = {
      TopAppBar(title = { Text("User Manager") })
    },
    floatingActionButton = {
      FloatingActionButton(onClick = { onNavigateToDetail(-1) }) {
        Icon(Icons.Default.Add, contentDescription = "Add User")
      }
    }
  ) { padding ->
    Box(modifier = Modifier.fillMaxSize().padding(padding)) {
      when (val state = uiState) {
        is UserUiState.Loading -> {
          CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
        }
        is UserUiState.Error -> {
          Text(
            text = state.message,
            color = MaterialTheme.colorScheme.error,
            modifier = Modifier.align(Alignment.Center)
          )
        }
        is UserUiState.Success -> {
          LazyColumn {
            items(state.users, key = { it.id }) { user ->
              UserListItem(
                user = user,
                onClick = { onNavigateToDetail(user.id) }
              )
            }
          }
        }
      }
    }
  }
}

// UserListItem.kt
@Composable
fun UserListItem(
  user: User,
  onClick: () -> Unit
) {
  Card(
    modifier = Modifier
      .fillMaxWidth()
      .padding(horizontal = 16.dp, vertical = 4.dp)
      .clickable(onClick = onClick)
  ) {
    Row(
      modifier = Modifier.padding(16.dp),
      verticalAlignment = Alignment.CenterVertically
    ) {
      Icon(Icons.Default.Person, contentDescription = null)
      Spacer(modifier = Modifier.width(12.dp))
      Column(modifier = Modifier.weight(1f)) {
        Text(user.name, style = MaterialTheme.typography.titleMedium)
        Text(user.email, style = MaterialTheme.typography.bodySmall)
      }
      Text("${user.age}", style = MaterialTheme.typography.bodyMedium)
    }
  }
}

// UserDetailScreen.kt
@Composable
fun UserDetailScreen(
  userId: Long,
  viewModel: UserViewModel = viewModel(),
  onNavigateBack: () -> Unit
) {
  val selectedUser by viewModel.selectedUser.collectAsState()

  LaunchedEffect(userId) {
    if (userId == -1L) {
      // 新增模式
    } else {
      viewModel.selectUser(userId)
    }
  }

  // 表單欄位
  var name by remember { mutableStateOf("") }
  var email by remember { mutableStateOf("") }
  var age by remember { mutableStateOf("") }

  LaunchedEffect(selectedUser) {
    selectedUser?.let {
      name = it.name
      email = it.email
      age = it.age.toString()
    }
  }

  Scaffold(
    topBar = {
      TopAppBar(
        title = { Text(if (userId == -1L) "Add User" else "Edit User") },
        navigationIcon = {
          IconButton(onClick = onNavigateBack) {
            Icon(Icons.Default.ArrowBack, contentDescription = "Back")
          }
        }
      )
    }
  ) { padding ->
    Column(
      modifier = Modifier
        .fillMaxSize()
        .padding(padding)
        .padding(16.dp)
    ) {
      OutlinedTextField(
        value = name, onValueChange = { name = it },
        label = { Text("Name") },
        modifier = Modifier.fillMaxWidth()
      )
      Spacer(modifier = Modifier.height(8.dp))
      OutlinedTextField(
        value = email, onValueChange = { email = it },
        label = { Text("Email") },
        modifier = Modifier.fillMaxWidth()
      )
      Spacer(modifier = Modifier.height(8.dp))
      OutlinedTextField(
        value = age, onValueChange = { age = it },
        label = { Text("Age") },
        modifier = Modifier.fillMaxWidth()
      )
      Spacer(modifier = Modifier.height(16.dp))
      Button(
        onClick = {
          if (userId == -1L) {
            viewModel.addUser(name, email, age.toIntOrNull() ?: 0)
          } else {
            viewModel.updateUser(userId, name, email, age.toIntOrNull() ?: 0)
          }
          onNavigateBack()
        },
        modifier = Modifier.fillMaxWidth()
      ) {
        Text("Save")
      }
      if (userId != -1L) {
        Spacer(modifier = Modifier.height(8.dp))
        OutlinedButton(
          onClick = {
            viewModel.deleteUser(userId)
            onNavigateBack()
          },
          modifier = Modifier.fillMaxWidth(),
          colors = ButtonDefaults.outlinedButtonColors(
            contentColor = MaterialTheme.colorScheme.error
          )
        ) {
          Text("Delete")
        }
      }
    }
  }
}
```

### 測試 ViewModel

```kotlin
class UserViewModelTest {
  private lateinit var viewModel: UserViewModel

  @Before
  fun setup() {
    viewModel = UserViewModel()
  }

  @Test
  fun `load users returns success state`() = runTest {
    val state = viewModel.uiState.first()
    assert(state is UserUiState.Success)
    assertEquals(3, (state as UserUiState.Success).users.size)
  }

  @Test
  fun `add user increases user count`() = runTest {
    viewModel.addUser("Test", "test@test.com", 25)
    val state = viewModel.uiState.first()
    assertEquals(4, (state as UserUiState.Success).users.size)
  }

  @Test
  fun `delete user removes from list`() = runTest {
    viewModel.deleteUser(1L)
    val state = viewModel.uiState.first()
    val users = (state as UserUiState.Success).users
    assert(users.none { it.id == 1L })
  }
}
```

---

## 總結

這個使用者管理範例展示了 ViewModel 在實戰中的完整應用流程：從資料層的 Repository 到 ViewModel 的狀態管理，再到 Compose UI 的狀態收集與顯示。ViewModel 作為中介層，讓 UI 與資料邏輯保持清晰的職責分離。

---

## 延伸閱讀

- [ViewModel 概覽](https://www.google.com/search?q=Android+ViewModel+overview)
- [MVVM 架構模式](https://www.google.com/search?q=MVVM+architecture+Android)
- [Compose + ViewModel 整合](https://www.google.com/search?q=Compose+ViewModel+integration)
