# 文章 8：HTTP 與 JSON 解析

## http 套件

Flutter 使用 `http` 套件發送網路請求。

```yaml
# pubspec.yaml
dependencies:
  http: ^1.2.0
```

### GET 請求

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<List<Post>> fetchPosts() async {
  final response = await http.get(
    Uri.parse('https://jsonplaceholder.typicode.com/posts'),
  );

  if (response.statusCode == 200) {
    final List<dynamic> jsonList = json.decode(response.body);
    return jsonList.map((json) => Post.fromJson(json)).toList();
  } else {
    throw Exception('請求失敗: ${response.statusCode}');
  }
}
```

### POST 請求

```dart
Future<Post> createPost(Post post) async {
  final response = await http.post(
    Uri.parse('https://jsonplaceholder.typicode.com/posts'),
    headers: {'Content-Type': 'application/json'},
    body: json.encode(post.toJson()),
  );

  if (response.statusCode == 201) {
    return Post.fromJson(json.decode(response.body));
  } else {
    throw Exception('建立失敗');
  }
}
```

## JSON 序列化

### 手動序列化

```dart
class Post {
  final int id;
  final String title;
  final String body;

  Post({required this.id, required this.title, required this.body});

  factory Post.fromJson(Map<String, dynamic> json) {
    return Post(
      id: json['id'],
      title: json['title'],
      body: json['body'],
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'title': title,
    'body': body,
  };
}
```

### 使用 json_serializable

自動產生序列化程式碼，減少重複工作。

```dart
import 'package:json_annotation/json_annotation.dart';

part 'post.g.dart';

@JsonSerializable()
class Post {
  final int id;
  final String title;
  final String body;

  Post({required this.id, required this.title, required this.body});

  factory Post.fromJson(Map<String, dynamic> json) => _$PostFromJson(json);
  Map<String, dynamic> toJson() => _$PostToJson(this);
}
```

## dio 套件

對於需要攔截器、逾時、檔案上傳的場景，`dio` 是更強大的選擇。

```dart
final dio = Dio();
dio.options.baseUrl = 'https://api.example.com';
dio.interceptors.add(LogInterceptor());

final response = await dio.get('/posts');
```

## 錯誤處理

```dart
try {
  final posts = await fetchPosts();
} on SocketException {
  print('網路連線異常');
} on HttpException {
  print('HTTP 錯誤');
} on FormatException {
  print('資料格式錯誤');
} catch (e) {
  print('未知錯誤: $e');
}
```

- https://www.google.com/search?q=Flutter+http+package+tutorial+2024
- https://www.google.com/search?q=Flutter+json_serializable+json+annotation
