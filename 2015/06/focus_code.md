# 附加：C 語言實作範例

## 程式實作總覽

本期我們提供三個 C 語言的實作範例，展示指標、資料結構和系統程式設計的實際應用。

## 指標範例

```c
/*
 * 指標基礎範例
 * 展示指標的基本操作和記憶體概念
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void demo(void) {
    printf("=== C 語言指標展示 ===\n\n");

    // 基本指標操作
    int x = 42;
    int *p = &x;

    printf("基本指標：\n");
    printf("  x 的值：%d\n", x);
    printf("  x 的位址：%p\n", (void*)&x);
    printf("  p 儲存的位址：%p\n", (void*)p);
    printf("  *p 的值：%d\n\n", *p);

    // 指標算術
    int arr[] = {10, 20, 30, 40, 50};
    int *ap = arr;

    printf("指標算術：\n");
    printf("  arr[0] = %d, *(ap+0) = %d\n", arr[0], *(ap + 0));
    printf("  arr[2] = %d, *(ap+2) = %d\n\n", arr[2], *(ap + 2));

    // 字串指標
    const char *str = "Hello, World!";
    printf("字串指標：\n");
    printf("  字串：%s\n", str);
    printf("  第一個字元：%c\n", str[0]);
    printf("  長度：%zu\n\n", strlen(str));

    // 動態記憶體配置
    int *dyn_arr = (int*)malloc(5 * sizeof(int));
    if (dyn_arr == NULL) {
        printf("記憶體配置失敗\n");
        return;
    }

    printf("動態配置：\n");
    for (int i = 0; i < 5; i++) {
        dyn_arr[i] = (i + 1) * 10;
    }
    printf("  配置的陣列：");
    for (int i = 0; i < 5; i++) {
        printf("%d ", dyn_arr[i]);
    }
    printf("\n");

    free(dyn_arr);
    printf("  記憶體已釋放\n\n");

    printf("=== C 語言指標展示完成 ===\n");
}

int main(void) {
    demo();
    return 0;
}
```

## 連結串列範例

```c
/*
 * 連結串列範例
 * 展示連結串列的建立、新增、刪除操作
 */

#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node *next;
};

struct Node* create_node(int data) {
    struct Node *node = (struct Node*)malloc(sizeof(struct Node));
    if (node == NULL) {
        return NULL;
    }
    node->data = data;
    node->next = NULL;
    return node;
}

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

void print_list(struct Node *head) {
    struct Node *current = head;
    while (current != NULL) {
        printf("%d", current->data);
        if (current->next != NULL) {
            printf(" -> ");
        }
        current = current->next;
    }
    printf("\n");
}

void free_list(struct Node *head) {
    struct Node *current = head;
    while (current != NULL) {
        struct Node *next = current->next;
        free(current);
        current = next;
    }
}

void demo(void) {
    printf("=== 連結串列展示 ===\n\n");

    struct Node *list = NULL;

    printf("新增元素：1, 2, 3, 4, 5\n");
    append(&list, 1);
    append(&list, 2);
    append(&list, 3);
    append(&list, 4);
    append(&list, 5);

    printf("串列內容：");
    print_list(list);

    free_list(list);
    printf("\n=== 連結串列展示完成 ===\n");
}

int main(void) {
    demo();
    return 0;
}
```

## 檔案操作範例

```c
/*
 * Unix 檔案操作範例
 * 展示基本的 Unix 系統呼叫
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>

void demo(void) {
    printf("=== Unix 檔案操作展示 ===\n\n");

    const char *filename = "demo_output.txt";
    const char *content = "Hello from C!\nThis is a test file.\n";

    // 使用標準 I/O
    printf("使用標準 I/O：\n");
    FILE *f = fopen(filename, "w");
    if (f == NULL) {
        perror("fopen");
        return;
    }
    fprintf(f, "%s", content);
    fclose(f);
    printf("  已寫入檔案：%s\n", filename);

    // 讀回並顯示
    f = fopen(filename, "r");
    if (f == NULL) {
        perror("fopen");
        return;
    }
    printf("  檔案內容：\n    ");
    char buffer[256];
    while (fgets(buffer, sizeof(buffer), f) != NULL) {
        printf("%s", buffer);
    }
    fclose(f);

    // 使用 Unix 系統呼叫
    printf("\n使用 Unix 系統呼叫：\n");
    int fd = open(filename, O_RDONLY);
    if (fd < 0) {
        perror("open");
        return;
    }

    struct stat st;
    if (fstat(fd, &st) == 0) {
        printf("  檔案大小：%ld 位元組\n", (long)st.st_size);
        printf("  檔案權限：%o\n", st.st_mode & 0777);
    }
    close(fd);

    // 清理測試檔案
    unlink(filename);
    printf("\n  已刪除測試檔案\n");

    printf("\n=== Unix 檔案操作展示完成 ===\n");
}

int main(void) {
    demo();
    return 0;
}
```

## 編譯和執行

```bash
# 編譯所有範例
gcc -Wall -Wextra -o pointer_demo pointer_demo.c
gcc -Wall -Wextra -o list_demo list_demo.c
gcc -Wall -Wextra -o file_demo file_demo.c

# 執行
./pointer_demo
./list_demo
./file_demo
```

或使用 test.sh 自動編譯和執行所有範例。