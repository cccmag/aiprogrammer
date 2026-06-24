# 文章 8：Firebase Firestore

## 即時文件資料庫實戰

Firebase Firestore 是 Google 提供的全託管文件資料庫，支援即時同步、離線存取與自動擴展。本文介紹 Firestore 的核心功能與實作技巧。

### 環境設定

```bash
npm install firebase
```

### 初始化

```javascript
import { initializeApp } from 'firebase/app'
import {
  getFirestore,
  collection,
  doc,
  setDoc,
  addDoc,
  getDoc,
  getDocs,
  query,
  where,
  orderBy,
  limit,
  onSnapshot,
  updateDoc,
  deleteDoc,
  Timestamp,
  increment,
  arrayUnion,
  arrayRemove
} from 'firebase/firestore'

const firebaseConfig = {
  apiKey: process.env.FIREBASE_API_KEY,
  authDomain: process.env.FIREBASE_AUTH_DOMAIN,
  projectId: process.env.FIREBASE_PROJECT_ID
}

const app = initializeApp(firebaseConfig)
const db = getFirestore(app)
```

### 資料操作

```javascript
// 新增文件 (自動 ID)
async function addPost(title, content, authorId) {
  const docRef = await addDoc(collection(db, 'posts'), {
    title,
    content,
    authorId,
    likes: 0,
    tags: ['firebase', 'database'],
    createdAt: Timestamp.now(),
    updatedAt: Timestamp.now()
  })
  return docRef.id
}

// 新增文件 (指定 ID)
async function setUserProfile(userId, profile) {
  await setDoc(doc(db, 'users', userId), {
    ...profile,
    createdAt: Timestamp.now()
  })
}

// 讀取文件
async function getPost(postId) {
  const docSnap = await getDoc(doc(db, 'posts', postId))
  if (!docSnap.exists()) return null
  return { id: docSnap.id, ...docSnap.data() }
}

// 查詢文件
async function getPostsByAuthor(authorId) {
  const q = query(
    collection(db, 'posts'),
    where('authorId', '==', authorId),
    orderBy('createdAt', 'desc'),
    limit(20)
  )
  const snapshot = await getDocs(q)
  return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }))
}

// 更新文件
async function likePost(postId) {
  await updateDoc(doc(db, 'posts', postId), {
    likes: increment(1)
  })
}

// 陣列操作
async function addTag(postId, tag) {
  await updateDoc(doc(db, 'posts', postId), {
    tags: arrayUnion(tag)
  })
}

async function removeTag(postId, tag) {
  await updateDoc(doc(db, 'posts', postId), {
    tags: arrayRemove(tag)
  })
}

// 刪除文件
async function deletePost(postId) {
  await deleteDoc(doc(db, 'posts', postId))
}
```

### 即時資料監聽

Firestore 最強大的功能之一就是即時監聽：

```javascript
// 即時監聽單一文件
function listenToPost(postId, onData, onError) {
  const unsubscribe = onSnapshot(
    doc(db, 'posts', postId),
    (doc) => {
      if (doc.exists()) {
        onData({ id: doc.id, ...doc.data() })
      } else {
        onData(null)
      }
    },
    onError
  )
  return unsubscribe // 呼叫 unsubscribe() 停止監聽
}

// 即時監聽查詢
function listenToRecentPosts(callback) {
  const q = query(
    collection(db, 'posts'),
    orderBy('createdAt', 'desc'),
    limit(10)
  )

  return onSnapshot(q, (snapshot) => {
    snapshot.docChanges().forEach((change) => {
      const data = { id: change.doc.id, ...change.doc.data() }
      switch (change.type) {
        case 'added':
          console.log('新增文章:', data.title)
          break
        case 'modified':
          console.log('文章更新:', data.title)
          break
        case 'removed':
          console.log('文章刪除:', data.title)
          break
      }
    })
    const posts = snapshot.docs.map(d => ({ id: d.id, ...d.data() }))
    callback(posts)
  })
}

// 使用範例
const unsubscribe = listenToRecentPosts((posts) => {
  console.log('最新文章:', posts.length)
})

// 清理監聽
// unsubscribe()
```

### 批次操作與事務

```javascript
import { writeBatch, runTransaction } from 'firebase/firestore'

// 批次寫入
async function batchWrite() {
  const batch = writeBatch(db)

  batch.set(doc(db, 'users', 'user1'), { name: 'Alice', active: true })
  batch.update(doc(db, 'users', 'user1'), { lastLogin: Timestamp.now() })
  batch.delete(doc(db, 'temporary', 'data'))

  await batch.commit()
}

// 事務操作
async function transferLikes(fromPostId, toPostId, amount) {
  try {
    await runTransaction(db, async (transaction) => {
      const fromDoc = await transaction.get(doc(db, 'posts', fromPostId))
      const toDoc = await transaction.get(doc(db, 'posts', toPostId))

      if (!fromDoc.exists() || !toDoc.exists()) {
        throw new Error('文章不存在')
      }

      const fromLikes = fromDoc.data().likes
      if (fromLikes < amount) {
        throw new Error('點讚數不足')
      }

      transaction.update(doc(db, 'posts', fromPostId), {
        likes: fromLikes - amount
      })
      transaction.update(doc(db, 'posts', toPostId), {
        likes: toDoc.data().likes + amount
      })
    })
    console.log('轉移成功')
  } catch (err) {
    console.error('轉移失敗:', err)
  }
}
```

### 安全規則範例

```javascript
// Firestore 安全規則
rules_version = '2'
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId
    }
    match /posts/{postId} {
      allow read: if true
      allow create: if request.auth != null
      allow update, delete: if request.auth != null
        && request.auth.uid == resource.data.authorId
    }
  }
}
```

延伸閱讀：https://www.google.com/search?q=Firebase+Firestore+tutorial+2024
https://www.google.com/search?q=Firestore+real-time+listener+best+practices
