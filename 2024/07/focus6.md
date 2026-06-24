# Room 資料庫與網路

## 本地與遠端資料

現代 Android 應用通常需要處理兩類資料來源：本地資料庫（Room）和遠端 API（Retrofit）。Repository 模式將兩者整合在一起。

---

## Room 資料庫

Room 是 SQLite 的抽象層，提供編譯時期 SQL 檢查。

### Entity（資料表）

```kotlin
@Entity(tableName = "users")
data class UserEntity(
  @PrimaryKey val id: Long,
  @ColumnInfo(name = "full_name") val name: String,
  val email: String,
  val age: Int
)
```

### DAO（資料存取物件）

```kotlin
@Dao
interface UserDao {
  @Query("SELECT * FROM users ORDER BY name ASC")
  suspend fun getAllUsers(): List<UserEntity>

  @Query("SELECT * FROM users WHERE id = :id")
  suspend fun getUserById(id: Long): UserEntity?

  @Insert(onConflict = OnConflictStrategy.REPLACE)
  suspend fun insertUser(user: UserEntity)

  @Update
  suspend fun updateUser(user: UserEntity)

  @Delete
  suspend fun deleteUser(user: UserEntity)
}
```

### Database 類別

```kotlin
@Database(entities = [UserEntity::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
  abstract fun userDao(): UserDao

  companion object {
    @Volatile
    private var INSTANCE: AppDatabase? = null

    fun getInstance(context: Context): AppDatabase {
      return INSTANCE ?: synchronized(this) {
        Room.databaseBuilder(context, AppDatabase::class.java, "app_db")
          .fallbackToDestructiveMigration()
          .build()
          .also { INSTANCE = it }
      }
    }
  }
}
```

### Flow 查詢（即時更新）

Room 支援 Kotlin Flow，資料變更時自動發出新值：

```kotlin
@Dao
interface FlowUserDao {
  @Query("SELECT * FROM users")
  fun observeAllUsers(): Flow<List<UserEntity>>
}

// 在 ViewModel 中
class UserViewModel(private val dao: UserDao) : ViewModel() {
  val users: StateFlow<List<UserEntity>> =
    dao.observeAllUsers().stateIn(
      viewModelScope,
      SharingStarted.WhileSubscribed(5000),
      emptyList()
    )
}
```

---

## Retrofit 網路請求

Retrofit 是類型安全的 HTTP 用戶端。

### 加入依賴

```kotlin
// build.gradle.kts
implementation("com.squareup.retrofit2:retrofit:2.9.0")
implementation("com.squareup.retrofit2:converter-gson:2.9.0")
implementation("com.squareup.okhttp3:logging-interceptor:4.11.0")
```

### API 介面

```kotlin
data class ApiResponse<T>(
  val code: Int,
  val message: String,
  val data: T
)

data class UserResponse(
  val id: Long,
  val name: String,
  val email: String
)

interface UserApi {
  @GET("users")
  suspend fun getUsers(): ApiResponse<List<UserResponse>>

  @GET("users/{id}")
  suspend fun getUser(@Path("id") id: Long): ApiResponse<UserResponse>

  @POST("users")
  suspend fun createUser(@Body user: UserResponse): ApiResponse<UserResponse>

  @PUT("users/{id}")
  suspend fun updateUser(@Path("id") id: Long, @Body user: UserResponse): ApiResponse<UserResponse>

  @DELETE("users/{id}")
  suspend fun deleteUser(@Path("id") id: Long): ApiResponse<Unit>
}
```

### Retrofit 實例

```kotlin
object RetrofitClient {
  private const val BASE_URL = "https://api.example.com/"

  private val okHttpClient = OkHttpClient.Builder()
    .addInterceptor(HttpLoggingInterceptor().apply {
      level = HttpLoggingInterceptor.Level.BODY
    })
    .connectTimeout(30, TimeUnit.SECONDS)
    .readTimeout(30, TimeUnit.SECONDS)
    .build()

  val instance: UserApi by lazy {
    Retrofit.Builder()
      .baseUrl(BASE_URL)
      .client(okHttpClient)
      .addConverterFactory(GsonConverterFactory.create())
      .build()
      .create(UserApi::class.java)
  }
}
```

---

## Repository 模式

Repository 協調本地與遠端資料來源：

```kotlin
class UserRepository(
  private val api: UserApi,
  private val dao: UserDao
) {
  fun observeUsers(): Flow<List<UserEntity>> = dao.observeAllUsers()

  suspend fun refreshUsers() {
    try {
      val response = api.getUsers()
      if (response.code == 200) {
        val entities = response.data.map { it.toEntity() }
        entities.forEach { dao.insertUser(it) }
      }
    } catch (e: Exception) {
      // 網路失敗——保留本地資料
      Log.e("UserRepository", "Failed to refresh", e)
    }
  }

  private fun UserResponse.toEntity() = UserEntity(id, name, email)
}
```

---

## 網路狀態管理

```kotlin
sealed class UiState<out T> {
  object Idle : UiState<Nothing>()
  object Loading : UiState<Nothing>()
  data class Success<T>(val data: T) : UiState<T>()
  data class Error(val message: String) : UiState<Nothing>()
}

class UserViewModel(private val repo: UserRepository) : ViewModel() {
  private val _state = MutableStateFlow<UiState<List<UserEntity>>>(UiState.Idle)
  val state: StateFlow<UiState<List<UserEntity>>> = _state.asStateFlow()

  init { loadUsers() }

  fun loadUsers() {
    viewModelScope.launch {
      _state.value = UiState.Loading
      try {
        repo.refreshUsers()
        repo.observeUsers().collect { users ->
          _state.value = UiState.Success(users)
        }
      } catch (e: Exception) {
        _state.value = UiState.Error(e.message ?: "Unknown error")
      }
    }
  }
}
```

---

## 總結

Room 提供類型安全的本地儲存，Retrofit 簡化網路通訊。透過 Repository 模式，開發者可以統一管理資料來源，實現離線優先的應用設計。

---

## 延伸閱讀

- [Room 資料庫官方指南](https://www.google.com/search?q=Room+database+Android)
- [Retrofit 官方文檔](https://www.google.com/search?q=Retrofit+Android+tutorial)
- [Repository 模式介紹](https://www.google.com/search?q=Repository+pattern+Android)
