# Room 資料庫實作

## 本地持久化完整教學

Room 是 Android Jetpack 的持久化函式庫，提供 SQLite 的抽象層，讓資料庫操作更安全、更簡潔。

### 加入依賴

```kotlin
// app/build.gradle.kts
plugins {
  id("com.google.devtools.ksp") version "1.9.22-1.0.17"
}

android {
  // Room 需要 Java 8+
  compileOptions {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
  }
}

dependencies {
  implementation("androidx.room:room-runtime:2.6.1")
  implementation("androidx.room:room-ktx:2.6.1")
  ksp("androidx.room:room-compiler:2.6.1")
}
```

### Entity 定義

Entity 對應資料庫中的資料表：

```kotlin
// NoteEntity.kt
@Entity(
  tableName = "notes",
  indices = [Index(value = ["created_at"], order = Index.Order.DESC)]
)
data class NoteEntity(
  @PrimaryKey(autoGenerate = true)
  val id: Long = 0,

  @ColumnInfo(name = "title")
  val title: String,

  @ColumnInfo(name = "content")
  val content: String,

  @ColumnInfo(name = "created_at")
  val createdAt: Long = System.currentTimeMillis(),

  @ColumnInfo(name = "updated_at")
  val updatedAt: Long = System.currentTimeMillis(),

  @ColumnInfo(name = "is_archived")
  val isArchived: Boolean = false,

  @ColumnInfo(name = "category")
  val category: String = "general"
)

// CategoryEntity.kt (關聯資料表)
@Entity(tableName = "categories")
data class CategoryEntity(
  @PrimaryKey
  val name: String,

  @ColumnInfo(name = "color")
  val color: Int = 0xFF6200EE.toInt()
)
```

### DAO（資料存取物件）

```kotlin
// NoteDao.kt
@Dao
interface NoteDao {
  // 查詢
  @Query("SELECT * FROM notes WHERE is_archived = 0 ORDER BY updated_at DESC")
  suspend fun getAllActiveNotes(): List<NoteEntity>

  @Query("SELECT * FROM notes WHERE id = :id")
  suspend fun getNoteById(id: Long): NoteEntity?

  @Query("SELECT * FROM notes WHERE title LIKE '%' || :query || '%' OR content LIKE '%' || :query || '%'")
  suspend fun searchNotes(query: String): List<NoteEntity>

  @Query("SELECT * FROM notes WHERE category = :category")
  suspend fun getNotesByCategory(category: String): List<NoteEntity>

  // Flow 查詢（即時更新）
  @Query("SELECT * FROM notes ORDER BY updated_at DESC")
  fun observeAllNotes(): Flow<List<NoteEntity>>

  @Query("SELECT * FROM notes WHERE id = :id")
  fun observeNoteById(id: Long): Flow<NoteEntity?>

  // 寫入
  @Insert(onConflict = OnConflictStrategy.REPLACE)
  suspend fun insertNote(note: NoteEntity): Long

  @Update
  suspend fun updateNote(note: NoteEntity)

  @Delete
  suspend fun deleteNote(note: NoteEntity)

  @Query("DELETE FROM notes WHERE id = :id")
  suspend fun deleteNoteById(id: Long)

  // 批量操作
  @Insert
  suspend fun insertAll(notes: List<NoteEntity>)

  @Query("DELETE FROM notes")
  suspend fun deleteAll()
}
```

### Database 類別

```kotlin
// AppDatabase.kt
@Database(
  entities = [NoteEntity::class, CategoryEntity::class],
  version = 2,
  exportSchema = true
)
abstract class AppDatabase : RoomDatabase() {
  abstract fun noteDao(): NoteDao

  companion object {
    @Volatile
    private var INSTANCE: AppDatabase? = null

    fun getInstance(context: Context): AppDatabase {
      return INSTANCE ?: synchronized(this) {
        INSTANCE ?: buildDatabase(context).also { INSTANCE = it }
      }
    }

    private fun buildDatabase(context: Context): AppDatabase {
      return Room.databaseBuilder(
        context.applicationContext,
        AppDatabase::class.java,
        "note_app.db"
      )
        .addMigrations(MIGRATION_1_2)
        .build()
    }

    // 資料庫遷移
    private val MIGRATION_1_2 = object : Migration(1, 2) {
      override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE notes ADD COLUMN category TEXT NOT NULL DEFAULT 'general'")
      }
    }
  }
}
```

### Repository 模式

```kotlin
// NoteRepository.kt
class NoteRepository(private val dao: NoteDao) {

  fun observeNotes(): Flow<List<NoteEntity>> = dao.observeAllNotes()

  suspend fun getNote(id: Long): NoteEntity? = dao.getNoteById(id)

  suspend fun createNote(title: String, content: String, category: String = "general"): Long {
    val note = NoteEntity(
      title = title,
      content = content,
      category = category
    )
    return dao.insertNote(note)
  }

  suspend fun updateNote(id: Long, title: String, content: String, category: String) {
    val existing = dao.getNoteById(id) ?: return
    dao.updateNote(existing.copy(
      title = title,
      content = content,
      category = category,
      updatedAt = System.currentTimeMillis()
    ))
  }

  suspend fun archiveNote(id: Long) {
    val note = dao.getNoteById(id) ?: return
    dao.updateNote(note.copy(isArchived = true, updatedAt = System.currentTimeMillis()))
  }

  suspend fun deleteNote(id: Long) = dao.deleteNoteById(id)

  suspend fun searchNotes(query: String) = dao.searchNotes(query)
}
```

### ViewModel 整合

```kotlin
// NoteViewModel.kt
class NoteViewModel(application: Application) : AndroidViewModel(application) {
  private val repository: NoteRepository

  val allNotes: StateFlow<List<NoteEntity>>

  init {
    val dao = AppDatabase.getInstance(application).noteDao()
    repository = NoteRepository(dao)
    allNotes = repository.observeNotes().stateIn(
      viewModelScope,
      SharingStarted.WhileSubscribed(5000),
      emptyList()
    )
  }

  fun addNote(title: String, content: String, category: String = "general") {
    viewModelScope.launch(Dispatchers.IO) {
      repository.createNote(title, content, category)
    }
  }

  fun updateNote(id: Long, title: String, content: String, category: String) {
    viewModelScope.launch(Dispatchers.IO) {
      repository.updateNote(id, title, content, category)
    }
  }

  fun archiveNote(id: Long) {
    viewModelScope.launch(Dispatchers.IO) {
      repository.archiveNote(id)
    }
  }

  fun deleteNote(id: Long) {
    viewModelScope.launch(Dispatchers.IO) {
      repository.deleteNote(id)
    }
  }
}
```

### Compose UI

```kotlin
@Composable
fun NoteApp() {
  val viewModel: NoteViewModel = viewModel()
  val notes by viewModel.allNotes.collectAsState()

  LazyColumn {
    items(notes, key = { it.id }) { note ->
      NoteCard(
        note = note,
        onDelete = { viewModel.deleteNote(note.id) },
        onArchive = { viewModel.archiveNote(note.id) }
      )
    }
  }
}

@Composable
fun NoteCard(
  note: NoteEntity,
  onDelete: () -> Unit,
  onArchive: () -> Unit
) {
  Card(
    modifier = Modifier
      .fillMaxWidth()
      .padding(horizontal = 16.dp, vertical = 4.dp)
  ) {
    Column(modifier = Modifier.padding(16.dp)) {
      Text(note.title, style = MaterialTheme.typography.titleMedium)
      Spacer(modifier = Modifier.height(4.dp))
      Text(
        note.content,
        style = MaterialTheme.typography.bodyMedium,
        maxLines = 3,
        color = MaterialTheme.colorScheme.onSurfaceVariant
      )
      Spacer(modifier = Modifier.height(8.dp))
      Row(horizontalArrangement = Arrangement.End) {
        IconButton(onClick = onArchive) {
          Icon(Icons.Default.Archive, contentDescription = "Archive")
        }
        IconButton(onClick = onDelete) {
          Icon(Icons.Default.Delete, contentDescription = "Delete")
        }
      }
    }
  }
}
```

---

## 總結

Room 資料庫為 Android 提供了型別安全、編譯時期檢查的持久化解決方案。搭配 Kotlin Flow 的反應式查詢，資料庫內容變更會自動通知 UI 更新，實現真正的資料驅動應用。

---

## 延伸閱讀

- [Room 官方指南](https://www.google.com/search?q=Room+database+official+guide)
- [Room 遷移策略](https://www.google.com/search?q=Room+migration+strategy)
- [Kotlin Flow 與 Room](https://www.google.com/search?q=Kotlin+Flow+Room+database)
