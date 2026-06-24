# SaaS 程式實作

## RESTful API 設計

### 基本結構

```python
# 假設的 REST API
class CloudAppAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {'Authorization': f'Bearer {token}'}

    def get(self, endpoint):
        """GET 請求"""
        response = requests.get(
            f'{self.base_url}/{endpoint}',
            headers=self.headers
        )
        return response.json()

    def post(self, endpoint, data):
        """POST 請求"""
        response = requests.post(
            f'{self.base_url}/{endpoint}',
            json=data,
            headers=self.headers
        )
        return response.json()

# 使用範例
api = CloudAppAPI('https://api.example.com', 'token123')
users = api.get('users')
new_user = api.post('users', {'name': 'John', 'email': 'john@example.com'})
```

## Salesforce API 範例

```python
# 使用 requests 呼叫 Salesforce REST API
import requests

def salesforce_query():
    """Salesforce SOQL 查詢"""
    instance = 'na1.salesforce.com'
    token = 'your_access_token'

    query = "SELECT Id, Name FROM Account LIMIT 10"
    url = f'https://{instance}/services/data/v20.0/query'

    response = requests.get(
        url,
        headers={'Authorization': f'Bearer {token}'},
        params={'q': query}
    )

    return response.json()
```

## Google Apps API

```python
# Google Calendar API
def create_calendar_event():
    """建立 Google Calendar 事件"""
    service_account_email = 'service@project.iam.gserviceaccount.com'
    credentials = get_credentials()

    calendar_service = build('calendar', 'v3', credentials=credentials)

    event = {
        'summary': '會議',
        'start': {
            'dateTime': '2008-07-15T10:00:00',
            'timeZone': 'Asia/Taipei',
        },
        'end': {
            'dateTime': '2008-07-15T11:00:00',
            'timeZone': 'Asia/Taipei',
        },
    }

    event = calendar_service.events().insert(
        calendarId='primary',
        body=event
    ).execute()

    return event['id']
```

## 雲端儲存

```python
# S3 風格的儲存服務
class CloudStorage:
    def __init__(self, access_key, secret_key, endpoint):
        self.client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint
        )

    def upload(self, bucket, key, data):
        """上傳檔案"""
        self.client.put_object(
            Bucket=bucket,
            Key=key,
            Body=data
        )

    def download(self, bucket, key):
        """下載檔案"""
        response = self.client.get_object(
            Bucket=bucket,
            Key=key
        )
        return response['Body'].read()
```

## 參考資源

- [Salesforce+API+documentation](https://www.google.com/search?q=Salesforce+REST+API+documentation)
- [Google+Apps+API](https://www.google.com/search?q=Google+Apps+API)
- [AWS+S3+Python](https://www.google.com/search?q=boto3+S3+tutorial)