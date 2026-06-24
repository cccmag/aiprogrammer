# 文章 7：表單與輸入驗證

## Form Widget

Flutter 的 `Form` 元件提供表單驗證與資料收集的框架。

```dart
class _MyFormState extends State<MyForm> {
  final _formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        children: [
          TextFormField(
            decoration: InputDecoration(labelText: '姓名'),
            validator: (value) {
              if (value == null || value.isEmpty) {
                return '請輸入姓名';
              }
              return null;
            },
          ),
          ElevatedButton(
            onPressed: () {
              if (_formKey.currentState!.validate()) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('驗證通過！')),
                );
              }
            },
            child: Text('送出'),
          ),
        ],
      ),
    );
  }
}
```

## TextFormField 屬性

```dart
TextFormField(
  controller: _controller,          // 文字控制器
  decoration: InputDecoration(
    labelText: '密碼',
    hintText: '至少 8 個字元',
    prefixIcon: Icon(Icons.lock),
    border: OutlineInputBorder(),
    errorText: _errorText,          // 手動錯誤訊息
  ),
  obscureText: true,                // 密碼遮罩
  keyboardType: TextInputType.emailAddress,
  textInputAction: TextInputAction.next,
  onFieldSubmitted: (value) => print('送出: $value'),
  validator: (value) {
    if (value == null || value.length < 8) {
      return '密碼長度不足';
    }
    return null;
  },
)
```

## 驗證規則範例

```dart
// 電子郵件驗證
validator: (value) {
  if (value == null || value.isEmpty) return '請輸入 Email';
  if (!RegExp(r'^[^@]+@[^@]+\.[^@]+').hasMatch(value)) {
    return '請輸入有效的 Email';
  }
  return null;
},

// 手機號碼驗證
validator: (value) {
  if (value == null || value.isEmpty) return '請輸入手機號碼';
  if (value.length != 10) return '手機號碼應為 10 碼';
  return null;
},
```

## 表單送出與重設

```dart
// 驗證並送出
if (_formKey.currentState!.validate()) {
  _formKey.currentState!.save();  // 觸發 onSaved
  submitData();
}

// 重設表單
_formKey.currentState!.reset();
```

## 實務建議

- 使用 GlobalKey 管理 Form 狀態
- 驗證邏輯應獨立成方法或 extension
- 即時驗證使用 `autovalidateMode`
- 複雜表單考慮使用 reactive_forms 或 flutter_form_builder 套件

- https://www.google.com/search?q=Flutter+Form+TextFormField+validation
- https://www.google.com/search?q=Flutter+form+validation+best+practices
