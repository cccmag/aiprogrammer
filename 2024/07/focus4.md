# Activity 與 Fragment 導航

## 頁面生命週期管理

Activity 和 Fragment 是 Android 應用中負責管理畫面與使用者互動的核心元件。了解它們的生命週期是寫出穩定應用的關鍵。

---

## Activity 生命週期

Activity 經歷七個主要生命週期回呼：

```
         ┌─────────────┐
         │ onCreate()  │ ← 初始化、設定佈局
         └──────┬──────┘
                ▼
         ┌─────────────┐
         │ onStart()   │ ← Activity 變得可見
         └──────┬──────┘
                ▼
         ┌─────────────┐
         │ onResume()  │ ← 使用者可互動
         └──────┬──────┘
                ▼
  ┌─────────────┴─────────────┐
  ▼                           ▼
┌─────────────┐        ┌─────────────┐
│ 執行中       │        │ onPause()   │ ← 部分遮擋
└─────────────┘        └──────┬──────┘
                              ▼
                       ┌─────────────┐
                       │ onStop()    │ ← 完全不可見
                       └──────┬──────┘
                              ▼
                       ┌─────────────┐
                       │ onDestroy() │ ← 銷毀
                       └─────────────┘
```

```kotlin
class MainActivity : AppCompatActivity() {
  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    setContentView(R.layout.activity_main)
    // 初始化 ViewModel、設定 RecyclerView
  }

  override fun onResume() {
    super.onResume()
    // 開始動畫、註冊感應器監聽
  }

  override fun onPause() {
    super.onPause()
    // 暫停動畫、取消感應器監聽
  }

  override fun onSaveInstanceState(outState: Bundle) {
    super.onSaveInstanceState(outState)
    outState.putString("key", "value")
  }
}
```

### 配置變更（Configuration Change）

螢幕旋轉、語言切換等配置變更會導致 Activity 重新建立：

```kotlin
// 在 AndroidManifest.xml 中宣告
<activity
  android:name=".MainActivity"
  android:configChanges="orientation|screenSize" />
```

但建議使用 ViewModel 保留資料，而非手動處理。

---

## Fragment 生命週期

Fragment 有比 Activity 更豐富的生命週期：

```kotlin
class ProfileFragment : Fragment() {
  override fun onAttach(context: Context) { super.onAttach(context) }
  override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?,
    savedInstanceState: Bundle?): View? {
    return inflater.inflate(R.layout.fragment_profile, container, false)
  }
  override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
    super.onViewCreated(view, savedInstanceState)
    // 設定 UI、觀察 ViewModel
  }
  override fun onDestroyView() { super.onDestroyView() }
  override fun onDetach() { super.onDetach() }
}
```

Fragment 的生命週期與宿主的 Activity 相關聯，但擁有獨立的回呼順序。

---

## Navigation Component

Navigation Component 是 Jetpack 提供的統一導航解決方案：

### NavGraph 設定

```xml
<!-- res/navigation/nav_graph.xml -->
<navigation xmlns:android="http://schemas.android.com/apk/res/android"
  app:startDestination="@id/homeFragment">

  <fragment
    android:id="@+id/homeFragment"
    android:name=".HomeFragment"
    android:label="Home">
    <action
      android:id="@+id/action_home_to_detail"
      app:destination="@id/detailFragment" />
  </fragment>

  <fragment
    android:id="@+id/detailFragment"
    android:name=".DetailFragment"
    android:label="Detail" />
</navigation>
```

### 程式碼導航

```kotlin
class HomeFragment : Fragment() {
  override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
    super.onViewCreated(view, savedInstanceState)
    view.findViewById<Button>(R.id.btn_detail).setOnClickListener {
      val action = HomeFragmentDirections.actionHomeToDetail(itemId = 42)
      findNavController().navigate(action)
    }
  }
}
```

### Navigation Compose

在 Compose 中使用 Navigation：

```kotlin
@Composable
fun AppNavHost() {
  val navController = rememberNavController()

  NavHost(navController = navController, startDestination = "home") {
    composable("home") {
      HomeScreen(onNavigateToDetail = { id ->
        navController.navigate("detail/$id")
      })
    }
    composable("detail/{id}", arguments = listOf(
      navArgument("id") { type = NavType.IntType }
    )) { backStackEntry ->
      val id = backStackEntry.arguments?.getInt("id") ?: 0
      DetailScreen(id)
    }
  }
}
```

---

## 深連結（Deep Link）

Navigation 支援深連結：

```xml
<fragment android:id="@+id/profileFragment">
  <deepLink app:uri="myapp://profile/{userId}" />
</fragment>
```

```kotlin
// 在 AndroidManifest.xml 中啟用深連結
<intent-filter>
  <action android:name="android.intent.action.VIEW" />
  <data android:scheme="myapp" android:host="profile" />
</intent-filter>
```

---

## 總結

掌握 Activity 和 Fragment 的生命週期，並使用 Navigation Component 統一管理頁面轉換，是建構穩定 Android 應用的基礎。推薦使用單 Activity 架構配合 Navigation Compose。

---

## 延伸閱讀

- [Activity 生命週期官方指南](https://www.google.com/search?q=Android+Activity+lifecycle)
- [Fragment 使用指南](https://www.google.com/search?q=Android+Fragment+guide)
- [Navigation Component 官方文檔](https://www.google.com/search?q=Navigation+Component+Android)
