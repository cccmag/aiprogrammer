# Retrofit 網路請求

## RESTful API 呼叫與錯誤處理

Retrofit 是 Square 公司開發的類型安全 HTTP 用戶端，廣泛應用於 Android 網路通訊。

### 加入依賴

```kotlin
// app/build.gradle.kts
dependencies {
  implementation("com.squareup.retrofit2:retrofit:2.9.0")
  implementation("com.squareup.retrofit2:converter-gson:2.9.0")
  implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")
  implementation("com.google.code.gson:gson:2.10.1")

  // 如果需要 Kotlin Serialization
  // implementation("com.jakewharton.retrofit:retrofit2-kotlinx-serialization-converter:1.0.0")
}
```

### 定義 API 介面

```kotlin
// 回應包裝
data class ApiResponse<T>(
  val success: Boolean,
  val message: String?,
  val data: T?
)

// 資料模型
data class Post(
  val id: Long,
  val title: String,
  val body: String,
  val userId: Long
)

data class CreatePostRequest(
  val title: String,
  val body: String,
  val userId: Long
)

// API 介面
interface JsonPlaceholderApi {
  @GET("posts")
  suspend fun getPosts(): List<Post>

  @GET("posts/{id}")
  suspend fun getPost(@Path("id") id: Long): Post

  @GET("posts")
  suspend fun getPostsByUser(@Query("userId") userId: Long): List<Post>

  @POST("posts")
  suspend fun createPost(@Body post: CreatePostRequest): Post

  @PUT("posts/{id}")
  suspend fun updatePost(@Path("id") id: Long, @Body post: Post): Post

  @PATCH("posts/{id}")
  suspend fun patchPost(@Path("id") id: Long, @Body body: Map<String, Any>): Post

  @DELETE("posts/{id}")
  suspend fun deletePost(@Path("id") id: Long)
}
```

### 建立 Retrofit 實例

```kotlin
object RetrofitClient {
  private const val BASE_URL = "https://jsonplaceholder.typicode.com/"

  private val loggingInterceptor = HttpLoggingInterceptor().apply {
    level = HttpLoggingInterceptor.Level.BODY
  }

  private val okHttpClient = OkHttpClient.Builder()
    .addInterceptor(loggingInterceptor)
    .addInterceptor { chain ->
      // 添加認證標頭
      val request = chain.request().newBuilder()
        .addHeader("Authorization", "Bearer ${getToken()}")
        .addHeader("Content-Type", "application/json")
        .build()
      chain.proceed(request)
    }
    .connectTimeout(30, TimeUnit.SECONDS)
    .readTimeout(30, TimeUnit.SECONDS)
    .writeTimeout(30, TimeUnit.SECONDS)
    .build()

  val api: JsonPlaceholderApi by lazy {
    Retrofit.Builder()
      .baseUrl(BASE_URL)
      .client(okHttpClient)
      .addConverterFactory(GsonConverterFactory.create())
      .build()
      .create(JsonPlaceholderApi::class.java)
  }

  private fun getToken(): String {
    // 從安全儲存獲取 token
    return "your-auth-token"
  }
}
```

### ViewModel 中的使用

```kotlin
// 定義 UI 狀態
sealed class PostUiState {
  object Idle : PostUiState()
  object Loading : PostUiState()
  data class PostsLoaded(val posts: List<Post>) : PostUiState()
  data class PostLoaded(val post: Post) : PostUiState()
  data class Error(val message: String) : PostUiState()
}

class PostViewModel : ViewModel() {
  private val api = RetrofitClient.api

  private val _state = MutableStateFlow<PostUiState>(PostUiState.Idle)
  val state: StateFlow<PostUiState> = _state.asStateFlow()

  fun loadPosts() {
    viewModelScope.launch {
      _state.value = PostUiState.Loading
      try {
        val posts = api.getPosts()
        _state.value = PostUiState.PostsLoaded(posts)
      } catch (e: Exception) {
        _state.value = PostUiState.Error(parseError(e))
      }
    }
  }

  fun loadPost(id: Long) {
    viewModelScope.launch {
      _state.value = PostUiState.Loading
      try {
        val post = api.getPost(id)
        _state.value = PostUiState.PostLoaded(post)
      } catch (e: Exception) {
        _state.value = PostUiState.Error(parseError(e))
      }
    }
  }

  fun createPost(title: String, body: String) {
    viewModelScope.launch {
      _state.value = PostUiState.Loading
      try {
        val request = CreatePostRequest(title = title, body = body, userId = 1)
        val post = api.createPost(request)
        _state.value = PostUiState.PostLoaded(post)
      } catch (e: Exception) {
        _state.value = PostUiState.Error(parseError(e))
      }
    }
  }

  private fun parseError(e: Exception): String {
    return when (e) {
      is java.net.UnknownHostException -> "No internet connection"
      is java.net.SocketTimeoutException -> "Request timed out"
      is retrofit2.HttpException -> {
        when (e.code()) {
          401 -> "Unauthorized"
          403 -> "Forbidden"
          404 -> "Not found"
          500 -> "Server error"
          else -> "HTTP error: ${e.code()}"
        }
      }
      else -> e.message ?: "Unknown error"
    }
  }
}
```

### Compose UI

```kotlin
@Composable
fun PostListScreen(viewModel: PostViewModel = viewModel()) {
  val state by viewModel.state.collectAsState()

  LaunchedEffect(Unit) {
    viewModel.loadPosts()
  }

  Scaffold(
    topBar = {
      TopAppBar(title = { Text("Posts") })
    }
  ) { padding ->
    when (val s = state) {
      is PostUiState.Idle -> {}
      is PostUiState.Loading -> {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
          CircularProgressIndicator()
        }
      }
      is PostUiState.PostsLoaded -> {
        LazyColumn(modifier = Modifier.padding(padding)) {
          items(s.posts) { post ->
            PostItem(post = post)
          }
        }
      }
      is PostUiState.PostLoaded -> {
        PostDetailView(post = s.post)
      }
      is PostUiState.Error -> {
        Column(
          modifier = Modifier.fillMaxSize().padding(padding),
          horizontalAlignment = Alignment.CenterHorizontally,
          verticalArrangement = Arrangement.Center
        ) {
          Text(
            text = s.message,
            color = MaterialTheme.colorScheme.error
          )
          Spacer(modifier = Modifier.height(16.dp))
          Button(onClick = { viewModel.loadPosts() }) {
            Text("Retry")
          }
        }
      }
    }
  }
}

@Composable
fun PostItem(post: Post) {
  Card(
    modifier = Modifier
      .fillMaxWidth()
      .padding(horizontal = 16.dp, vertical = 4.dp)
  ) {
    Column(modifier = Modifier.padding(16.dp)) {
      Text(
        text = post.title,
        style = MaterialTheme.typography.titleMedium,
        maxLines = 2
      )
      Spacer(modifier = Modifier.height(4.dp))
      Text(
        text = post.body,
        style = MaterialTheme.typography.bodyMedium,
        maxLines = 3,
        color = MaterialTheme.colorScheme.onSurfaceVariant
      )
    }
  }
}

@Composable
fun PostDetailView(post: Post) {
  Column(modifier = Modifier.padding(16.dp)) {
    Text(
      text = post.title,
      style = MaterialTheme.typography.headlineSmall
    )
    Spacer(modifier = Modifier.height(16.dp))
    Text(
      text = post.body,
      style = MaterialTheme.typography.bodyLarge
    )
  }
}
```

### 檔案上傳

```kotlin
interface FileUploadApi {
  @Multipart
  @POST("upload")
  suspend fun uploadFile(
    @Part file: MultipartBody.Part,
    @Part("description") description: RequestBody
  ): ApiResponse<String>

  @Multipart
  @POST("upload/multiple")
  suspend fun uploadMultipleFiles(
    @Part files: List<MultipartBody.Part>
  ): ApiResponse<List<String>>
}

// 使用
fun uploadImage(uri: Uri, context: Context) {
  val file = uri.toFile(context)
  val requestFile = file.asRequestBody("image/*".toMediaTypeOrNull())
  val part = MultipartBody.Part.createFormData("file", file.name, requestFile)
  val desc = "Upload description".toRequestBody("text/plain".toMediaTypeOrNull())
  // api.uploadFile(part, desc)
}
```

---

## 總結

Retrofit 簡化了 Android 的網路通訊。搭配 Kotlin 協程的 suspend 函數、Gson 轉換器和 OkHttp 攔截器，開發者可以輕鬆實現類型安全的 API 呼叫、錯誤處理和檔案上傳。

---

## 延伸閱讀

- [Retrofit 官方文檔](https://www.google.com/search?q=Retrofit+Android+official)
- [OkHttp 使用指南](https://www.google.com/search?q=OkHttp+Android+guide)
- [Android 網路請求最佳實踐](https://www.google.com/search?q=Android+networking+best+practices)
