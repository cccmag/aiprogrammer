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