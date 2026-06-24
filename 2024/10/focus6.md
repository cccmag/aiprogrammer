# 專題 6：Firebase 後端即服務

## Google 的全端開發平台

Firebase 是 Google 的行動與 Web 應用開發平台，提供後端即服務 (BaaS) 解決方案。開發者可以直接在用戶端整合後端功能，無需自行管理伺服器基礎設施。

### 核心產品

#### Firestore 資料庫
Firestore 是 Firebase 的文件資料庫，支援即時同步、離線支援與自動擴展。

```javascript
// Firebase Firestore 操作
import { initializeApp } from 'firebase/app'
import { getFirestore, collection, addDoc, getDocs, query, where, onSnapshot } from 'firebase/firestore'

const app = initializeApp({
  apiKey: 'YOUR_API_KEY',
  projectId: 'YOUR_PROJECT_ID'
})

const db = getFirestore(app)

// 新增文件
async function addPost(title, content) {
  const docRef = await addDoc(collection(db, 'posts'), {
    title,
    content,
    createdAt: new Date(),
    likes: 0
  })
  return docRef.id
}

// 即時查詢
function subscribePosts(userId) {
  const q = query(collection(db, 'posts'), where('authorId', '==', userId))
  return onSnapshot(q, (snapshot) => {
    snapshot.docChanges().forEach(change => {
      console.log('文件變更:', change.type, change.doc.data())
    })
  })
}
```

#### Authentication
Firebase Authentication 提供多種身分驗證方式，包括電子郵件/密碼、Google 登入、Facebook 登入、匿名驗證等。

```javascript
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword } from 'firebase/auth'

const auth = getAuth(app)

async function register(email, password) {
  const userCredential = await createUserWithEmailAndPassword(auth, email, password)
  return userCredential.user
}

async function login(email, password) {
  const userCredential = await signInWithEmailAndPassword(auth, email, password)
  return userCredential.user
}
```

#### Cloud Functions
在 Google Cloud 上執行的無伺服器函數，用於處理後端邏輯。

```javascript
import { onDocumentCreated } from 'firebase-functions/v2/firestore'

export const onNewPost = onDocumentCreated('posts/{postId}', (event) => {
  const snapshot = event.data
  const post = snapshot.data()
  console.log('新文章發布:', post.title)
  return null
})
```

#### Cloud Storage
用於儲存使用者上傳檔案的物件儲存服務，如圖片、影片等。

```javascript
import { getStorage, ref, uploadBytes, getDownloadURL } from 'firebase/storage'

const storage = getStorage(app)

async function uploadFile(file, path) {
  const storageRef = ref(storage, path)
  await uploadBytes(storageRef, file)
  return await getDownloadURL(storageRef)
}
```

### Firebase 的優勢

1. **快速開發**：內建後端功能，減少開發時間
2. **即時同步**：Firestore 與 Realtime Database 支援即時資料同步
3. **自動擴展**：Google Cloud 基礎設施自動處理擴展
4. **離線支援**：用戶端 SDK 支援離線讀寫
5. **整合生態**：與 Google Analytics、AdMob、Cloud Functions 深度整合

### 適用場景

- **MVP 開發**：快速驗證產品概念
- **即時應用**：聊天、協作編輯、即時遊戲
- **行動應用**：Android 與 iOS 開發
- **小型到中型專案**：減少後端維護負擔

### 注意事項

- **廠商鎖定**：遷移到其他平台可能需要較大改動
- **成本管理**：隨著規模增長，Firebase 成本可能較高
- **查詢限制**：Firestore 查詢有特定限制（如複合查詢需要索引）

延伸閱讀：https://www.google.com/search?q=Firebase+BaaS+tutorial+2024
https://www.google.com/search?q=Firebase+Firestore+vs+Realtime+Database
