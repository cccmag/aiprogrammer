# JSON Schema 驗證

## 為何需要 JSON Schema

API 接收的請求資料需要驗證。傳統的方法是每個端點手動驗證，但這種作法導致程式碼重複且容易遺漏邊界情況。JSON Schema 提供了一種宣告式的方式來描述資料結構，並自動驗證。

## 基本語法

```javascript
// 最簡單的 Schema
const userSchema = {
  type: 'object',
  properties: {
    name: { type: 'string' },
    email: { type: 'string', format: 'email' },
    age: { type: 'integer', minimum: 0, maximum: 150 }
  },
  required: ['name', 'email']
};
```

### 型別與格式

```javascript
{
  type: 'object',
  properties: {
    // 基本型別
    name: { type: 'string' },
    count: { type: 'integer' },
    price: { type: 'number' },
    isActive: { type: 'boolean' },
    tags: { type: 'array', items: { type: 'string' } },

    // 字串格式
    email: { type: 'string', format: 'email' },
    url: { type: 'string', format: 'uri' },
    date: { type: 'string', format: 'date-time' },
    uuid: { type: 'string', pattern: '^[0-9a-f-]+$' }
  }
}
```

## 陣列與巢狀物件

```javascript
const orderSchema = {
  type: 'object',
  properties: {
    items: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          productId: { type: 'integer' },
          quantity: { type: 'integer', minimum: 1, maximum: 100 },
          price: { type: 'number', exclusiveMinimum: 0 }
        },
        required: ['productId', 'quantity']
      },
      minItems: 1,
      maxItems: 50
    },
    shippingAddress: {
      type: 'object',
      properties: {
        street: { type: 'string' },
        city: { type: 'string' },
        zipCode: { type: 'string', pattern: '^[0-9]{3,10}$' }
      },
      required: ['street', 'city']
    }
  },
  required: ['items']
};
```

## 條件式驗證

JSON Schema 2020-12 支援複雜的條件約束：

```javascript
const paymentSchema = {
  type: 'object',
  properties: {
    method: { type: 'string', enum: ['credit_card', 'bank_transfer', 'paypal'] },
    cardNumber: { type: 'string' },
    bankCode: { type: 'string' },
    paypalEmail: { type: 'string', format: 'email' }
  },
  required: ['method'],
  allOf: [
    {
      if: { properties: { method: { const: 'credit_card' } } },
      then: { required: ['cardNumber'] }
    },
    {
      if: { properties: { method: { const: 'bank_transfer' } } },
      then: { required: ['bankCode'] }
    },
    {
      if: { properties: { method: { const: 'paypal' } } },
      then: { required: ['paypalEmail'] }
    }
  ]
};
```

## 在 Express 中整合

```javascript
const Ajv = require('ajv');
const addFormats = require('ajv-formats');
const ajv = new Ajv({ allErrors: true, coerceTypes: true });
addFormats(ajv);

function validateSchema(schema) {
  const validate = ajv.compile(schema);
  return (req, res, next) => {
    const valid = validate(req.body);
    if (!valid) {
      const details = validate.errors.map(err => ({
        field: err.instancePath.slice(1) || err.params.missingProperty,
        message: err.message,
        code: err.keyword
      }));
      return res.status(422).json({
        error: 'VALIDATION_ERROR',
        message: '資料驗證失敗',
        details
      });
    }
    next();
  };
}

// 使用方式
const createUserSchema = {
  type: 'object',
  properties: {
    name: { type: 'string', minLength: 1, maxLength: 100 },
    email: { type: 'string', format: 'email' },
    role: { type: 'string', enum: ['admin', 'editor', 'viewer'] }
  },
  required: ['name', 'email']
};

router.post('/users', validateSchema(createUserSchema), async (req, res) => {
  const user = await db.users.create(req.body);
  res.status(201).json({ data: user });
});
```

## JSON Schema 2020-12 新特性

```javascript
{
  // prefixItems：陣列前綴的結構化驗證
  type: 'array',
  prefixItems: [
    { type: 'string' },   // 第一個元素必須是字串
    { type: 'integer' },  // 第二個元素必須是整數
    { type: 'boolean' }   // 第三個元素必須是布林值
  ],
  items: false,  // 禁止額外元素
  minItems: 3,
  maxItems: 3

  // unevaluatedProperties：允許未在 properties 中列出的屬性
  // 但不允許在 patternProperties 或 additionalProperties 之外的屬性
}
```

## 效能考量

編譯 Schema 是昂貴的操作，應該在應用啟動時一次性編譯：

```javascript
const validator = ajv.compile(schema);
// ✅ 正確：啟動時編譯一次
// ❌ 錯誤：每次請求重新編譯
```

## 小結

JSON Schema 提供了標準化、可組合、自描述的驗證方式。與手動驗證相比，它減少了程式碼量、提高了正確性，更重要的是它可以從 Schema 自動產生文件。

---

## 延伸閱讀

- [JSON Schema 官方文件](https://www.google.com/search?q=JSON+Schema+official+documentation)
- [Ajv: JSON Schema Validator](https://www.google.com/search?q=Ajv+JSON+Schema+validator)
- [JSON Schema 2020-12 新特性](https://www.google.com/search?q=JSON+Schema+2020-12+new+features)
