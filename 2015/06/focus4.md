# 主題四：指標運算與資料結構

## 指標運算的更多細節

### 多重指標

```c
int x = 42;
int *p = &x;
int **pp = &p;  // 指向指標的指標

printf("%d\n", **pp);  // 42
```

### const 與指標

```c
int x = 10, y = 20;

// 指標指向 const int（指標可以改變，但指向的值不行）
const int *p1 = &x;
// *p1 = 30;  // 錯誤！
p1 = &y;     // OK

// const 指標指向 int（指標不能改變）
int *const p2 = &x;
*p2 = 30;     // OK
// p2 = &y;   // 錯誤！

// 兩者都不能變
const int *const p3 = &x;
// *p3 = 30;  // 錯誤！
// p3 = &y;   // 錯誤！
```

### void 指標

```c
void *memcpy(void *dest, const void *src, size_t n);

int a = 42;
double b;
void *vp = &a;

int *ip = (int*)vp;
printf("%d\n", *ip);
```

## 結構

### 定義和使用

```c
struct Point {
    int x;
    int y;
};

struct Point p1 = {10, 20};
struct Point p2 = {.x = 5, .y = 15};  // 指定初始化

p1.x = 30;
p1.y = 40;
```

### 指標與結構

```c
struct Point {
    int x;
    int y;
};

struct Point p = {10, 20};
struct Point *pp = &p;

(*pp).x = 30;    // 透過指標存取成員
pp->y = 40;      // 相同效果，更簡潔的語法
```

### 結構指標與動態配置

```c
struct Person {
    char name[50];
    int age;
};

struct Person *person = (struct Person*)malloc(sizeof(struct Person));
if (person == NULL) {
    return;
}

strcpy(person->name, "張小明");
person->age = 28;

free(person);
```

## 連結串列

### 結構定義

```c
struct Node {
    int data;
    struct Node *next;
};
```

### 基本操作

```c
#include <stdlib.h>
#include <stdio.h>

struct Node {
    int data;
    struct Node *next;
};

// 建立新節點
struct Node* create_node(int data) {
    struct Node *node = (struct Node*)malloc(sizeof(struct Node));
    if (node == NULL) {
        return NULL;
    }
    node->data = data;
    node->next = NULL;
    return node;
}

// 在串列末尾新增
void append(struct Node **head, int data) {
    struct Node *new_node = create_node(data);
    if (*head == NULL) {
        *head = new_node;
        return;
    }

    struct Node *current = *head;
    while (current->next != NULL) {
        current = current->next;
    }
    current->next = new_node;
}

// 印出串列
void print_list(struct Node *head) {
    struct Node *current = head;
    while (current != NULL) {
        printf("%d ", current->data);
        current = current->next;
    }
    printf("\n");
}

// 釋放記憶體
void free_list(struct Node *head) {
    struct Node *current = head;
    while (current != NULL) {
        struct Node *next = current->next;
        free(current);
        current = next;
    }
}
```

### 完整範例

```c
int main(void) {
    struct Node *list = NULL;

    append(&list, 1);
    append(&list, 2);
    append(&list, 3);
    append(&list, 4);

    print_list(list);  // 輸出：1 2 3 4

    free_list(list);
    return 0;
}
```

## 雙向連結串列

```c
struct DNode {
    int data;
    struct DNode *prev;
    struct DNode *next;
};
```

## 二元樹

### 節點結構

```c
struct TreeNode {
    int data;
    struct TreeNode *left;
    struct TreeNode *right;
};
```

### 基本操作

```c
struct TreeNode* create_tree_node(int data) {
    struct TreeNode *node = (struct TreeNode*)malloc(sizeof(struct TreeNode));
    if (node == NULL) {
        return NULL;
    }
    node->data = data;
    node->left = NULL;
    node->right = NULL;
    return node;
}

// 中序遍歷
void inorder(struct TreeNode *root) {
    if (root == NULL) {
        return;
    }
    inorder(root->left);
    printf("%d ", root->data);
    inorder(root->right);
}

// 前序遍歷
void preorder(struct TreeNode *root) {
    if (root == NULL) {
        return;
    }
    printf("%d ", root->data);
    preorder(root->left);
    preorder(root->right);
}

// 後序遍歷
void postorder(struct TreeNode *root) {
    if (root == NULL) {
        return;
    }
    postorder(root->left);
    postorder(root->right);
    printf("%d ", root->data);
}
```

## 指標與二維陣列

```c
int matrix[3][4] = {
    {1, 2, 3, 4},
    {5, 6, 7, 8},
    {9, 10, 11, 12}
};

int (*p)[4] = matrix;  // 指向 4 個 int 的指標

printf("%d\n", *(*(p + 1) + 2));  // 7
printf("%d\n", p[1][2]);          // 7
```

## 函式指標與回呼

```c
typedef int (*compare_func)(int, int);

int compare_asc(int a, int b) {
    return a > b ? 1 : (a < b ? -1 : 0);
}

int compare_desc(int a, int b) {
    return -compare_asc(a, b);
}

void bubble_sort(int *arr, int n, compare_func cmp) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (cmp(arr[j], arr[j + 1]) > 0) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}
```

## 結論

指標是 C 語言實現各種資料結構的基礎。熟練掌握指標運算，可以實現連結串列、樹、圖等複雜資料結構，這是系統程式設計的重要技能。