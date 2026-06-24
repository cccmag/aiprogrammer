# Navigation Compose

## 宣告式頁面導航實作

Navigation Compose 是 Jetpack Navigation 的 Compose 版本，提供類型安全的宣告式導航。

### 加入依賴

```kotlin
// app/build.gradle.kts
dependencies {
  implementation("androidx.navigation:navigation-compose:2.7.7")
}
```

### 基本設定

```kotlin
@Composable
fun AppNavigation() {
  val navController = rememberNavController()

  NavHost(navController = navController, startDestination = "home") {
    composable("home") {
      HomeScreen(
        onNavigateToProfile = { navController.navigate("profile") },
        onNavigateToSettings = { navController.navigate("settings") }
      )
    }
    composable("profile") {
      ProfileScreen(onNavigateBack = { navController.popBackStack() })
    }
    composable("settings") {
      SettingsScreen(onNavigateBack = { navController.popBackStack() })
    }
  }
}
```

### 帶參數導航

```kotlin
NavHost(navController, startDestination = "home") {
  composable(
    route = "detail/{itemId}",
    arguments = listOf(navArgument("itemId") { type = NavType.IntType })
  ) { backStackEntry ->
    val itemId = backStackEntry.arguments?.getInt("itemId") ?: 0
    DetailScreen(itemId, onNavigateBack = { navController.popBackStack() })
  }
}

// 導航到 Detail
navController.navigate("detail/${item.id}")

// 可選參數
composable(
  route = "search?query={query}",
  arguments = listOf(
    navArgument("query") {
      type = NavType.StringType
      defaultValue = ""
    }
  )
) { /* ... */ }

// 導航時傳遞參數
navController.navigate("search?query=android")
```

### 安全導航（Serializable 參數）

```kotlin
// 定義導航參數
@Parcelize
data class UserProfile(
  val userId: Int,
  val displayName: String
) : Parcelable

// 路線定義
const val PROFILE_ROUTE = "profile/{userId}/{displayName}"

// 使用 NavType
composable(
  route = "profile/{user}",
  arguments = listOf(
    navArgument("user") { type = NavType.ParcelableType(UserProfile::class.java) }
  )
) {
  val user = it.arguments?.getParcelable<UserProfile>("user")
  UserProfileScreen(user)
}

// 新版 Kotlin Serialization（Navigation 2.8+）
// @Serializable
// data class ProfileRoute(val userId: Int)
//
// composable<ProfileRoute> {
//   val args = it.toRoute<ProfileRoute>()
//   ProfileScreen(args.userId)
// }
```

### 底部導航整合

```kotlin
data class BottomNavItem(
  val route: String,
  val label: String,
  val icon: ImageVector
)

@Composable
fun MainScreen() {
  val navController = rememberNavController()
  val items = listOf(
    BottomNavItem("home", "Home", Icons.Default.Home),
    BottomNavItem("search", "Search", Icons.Default.Search),
    BottomNavItem("profile", "Profile", Icons.Default.Person)
  )

  Scaffold(
    bottomBar = {
      NavigationBar {
        val navBackStackEntry by navController.currentBackStackEntryAsState()
        val currentRoute = navBackStackEntry?.destination?.route

        items.forEach { item ->
          NavigationBarItem(
            icon = { Icon(item.icon, contentDescription = item.label) },
            label = { Text(item.label) },
            selected = currentRoute == item.route,
            onClick = {
              navController.navigate(item.route) {
                popUpTo(navController.graph.startDestinationId) {
                  saveState = true
                }
                launchSingleTop = true
                restoreState = true
              }
            }
          )
        }
      }
    }
  ) { padding ->
    NavHost(
      navController = navController,
      startDestination = "home",
      modifier = Modifier.padding(padding)
    ) {
      composable("home") { HomeScreen() }
      composable("search") { SearchScreen() }
      composable("profile") { ProfileScreen() }
    }
  }
}
```

### 動畫轉場

```kotlin
composable(
  route = "detail/{itemId}",
  arguments = listOf(navArgument("itemId") { type = NavType.IntType }),
  enterTransition = { slideInHorizontally(initialOffsetX = { it }) },
  exitTransition = { slideOutHorizontally(targetOffsetX = { -it }) },
  popEnterTransition = { slideInHorizontally(initialOffsetX = { -it }) },
  popExitTransition = { slideOutHorizontally(targetOffsetX = { it }) }
) { backStackEntry ->
  DetailScreen(
    itemId = backStackEntry.arguments?.getInt("itemId") ?: 0,
    onNavigateBack = { navController.popBackStack() }
  )
}
```

### 深連結（Deep Link）

```kotlin
// 在 NavHost 中定義深連結
composable(
  route = "profile/{userId}",
  arguments = listOf(navArgument("userId") { type = NavType.IntType }),
  deepLinks = listOf(
    navDeepLink {
      uriPattern = "myapp://profile/{userId}"
    }
  )
) { /* ... */ }

// AndroidManifest.xml
<intent-filter>
  <action android:name="android.intent.action.VIEW" />
  <category android:name="android.intent.category.DEFAULT" />
  <category android:name="android.intent.category.BROWSABLE" />
  <data android:scheme="myapp" android:host="profile" />
</intent-filter>
```

### 嵌套 NavHost

```kotlin
// 主圖形
NavHost(navController, startDestination = "main") {
  composable("main") {
    MainScreen(
      onNavigateToAuth = { navController.navigate("auth") }
    )
  }
  composable("auth") {
    // 子導航圖形
    val authNavController = rememberNavController()
    NavHost(authNavController, startDestination = "login") {
      composable("login") { LoginScreen(authNavController) }
      composable("register") { RegisterScreen(authNavController) }
      composable("forgot_password") { ForgotPasswordScreen(authNavController) }
    }
  }
}
```

### 測試導航

```kotlin
@Composable
fun NavigationTest() {
  val navController = rememberNavController()
  NavHost(navController, startDestination = "home") {
    composable("home") {
      HomeScreen(
        onNavigateToDetail = { id ->
          navController.navigate("detail/$id")
        }
      )
    }
    composable("detail/{id}", arguments = listOf(
      navArgument("id") { type = NavType.IntType }
    )) {
      DetailScreen()
    }
  }
}

// 單元測試
@Test
fun navigation_to_detail_works() {
  composeTestRule.setContent { NavigationTest() }
  composeTestRule.onNodeWithText("Item 5").performClick()
  composeTestRule.onNodeWithText("Detail: 5").assertIsDisplayed()
}
```

---

## 總結

Navigation Compose 為宣告式 UI 提供了完善的路由解決方案。從基本導航到參數傳遞、底部導航、動畫和深連結，Navigation Compose 滿足了現代應用程式的所有導航需求。

---

## 延伸閱讀

- [Navigation Compose 官方文檔](https://www.google.com/search?q=Navigation+Compose+official+documentation)
- [Compose 導航最佳實踐](https://www.google.com/search?q=Compose+navigation+best+practices)
- [Android 導航架構指南](https://www.google.com/search?q=Android+Navigation+architecture)
