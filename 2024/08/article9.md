# 文章 9：本地資料庫 sqflite

## sqflite 簡介

sqflite 是 Flutter 生態中最常用的 SQLite 資料庫套件，提供輕量級的本地持久化儲存。

```yaml
# pubspec.yaml
dependencies:
  sqflite: ^2.3.0
  path: ^1.9.0
```

## 資料庫初始化

```dart
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

class DatabaseHelper {
  static final DatabaseHelper instance = DatabaseHelper._init();
  static Database? _database;

  DatabaseHelper._init();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB('app.db');
    return _database!;
  }

  Future<Database> _initDB(String filePath) async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, filePath);

    return await openDatabase(
      path,
      version: 1,
      onCreate: _createDB,
    );
  }

  Future<void> _createDB(Database db, int version) async {
    await db.execute('''
      CREATE TABLE todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        isDone INTEGER DEFAULT 0,
        createdAt TEXT NOT NULL
      )
    ''');
  }
}
```

## CRUD 操作

```dart
// 建立 (Create)
Future<int> insertTodo(Todo todo) async {
  final db = await instance.database;
  return await db.insert('todos', todo.toMap());
}

// 讀取 (Read)
Future<List<Todo>> getAllTodos() async {
  final db = await instance.database;
  final maps = await db.query('todos', orderBy: 'createdAt DESC');
  return maps.map((map) => Todo.fromMap(map)).toList();
}

// 更新 (Update)
Future<int> updateTodo(Todo todo) async {
  final db = await instance.database;
  return await db.update(
    'todos',
    todo.toMap(),
    where: 'id = ?',
    whereArgs: [todo.id],
  );
}

// 刪除 (Delete)
Future<int> deleteTodo(int id) async {
  final db = await instance.database;
  return await db.delete('todos', where: 'id = ?', whereArgs: [id]);
}
```

## 資料模型

```dart
class Todo {
  final int? id;
  final String title;
  final String? description;
  final bool isDone;
  final DateTime createdAt;

  Todo({this.id, required this.title, this.description, this.isDone = false, DateTime? createdAt})
    : createdAt = createdAt ?? DateTime.now();

  Map<String, dynamic> toMap() => {
    'id': id,
    'title': title,
    'description': description,
    'isDone': isDone ? 1 : 0,
    'createdAt': createdAt.toIso8601String(),
  };

  factory Todo.fromMap(Map<String, dynamic> map) => Todo(
    id: map['id'],
    title: map['title'],
    description: map['description'],
    isDone: map['isDone'] == 1,
    createdAt: DateTime.parse(map['createdAt']),
  );
}
```

## 替代方案

- **drift**（前身 moor）：型別安全的 SQLite 封裝，使用程式碼產生器
- **Hive**：NoSQL 本地儲存，適合輕量資料
- **Isar**：高效能的跨平台資料庫

- https://www.google.com/search?q=Flutter+sqflite+tutorial+CRUD
- https://www.google.com/search?q=Flutter+local+database+sqflite+vs+hive
