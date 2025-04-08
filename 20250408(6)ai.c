#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

typedef struct Node {
    int data;
    struct Node* next;
} Node;

// 1. 求链表中的最大整数
int maxInList(Node* f) {
    if (f == NULL) {
        return INT_MIN;
    }
    int current = f->data;
    int restMax = maxInList(f->next);
    return (current > restMax) ? current : restMax;
}

// 2. 求链表的结点个数
int countNodes(Node* f) {
    if (f == NULL) {
        return 0;
    }
    return 1 + countNodes(f->next);
}

// 3. 辅助函数：计算链表的总和和节点数
void sumAndCount(Node* f, int* sum, int* count) {
    if (f == NULL) {
        *sum = 0;
        *count = 0;
        return;
    }
    sumAndCount(f->next, sum, count);
    *sum += f->data;
    *count += 1;
}

// 3. 求所有整数的平均值
float average(Node* f) {
    int sum, count;
    sumAndCount(f, &sum, &count);
    if (count == 0) {
        return 0.0f;
    }
    return (float)sum / count;
}

// 测试代码
int main() {
    // 创建链表 3 -> 1 -> 4 -> 2
    Node* head = (Node*)malloc(sizeof(Node));
    head->data = 3;
    head->next = (Node*)malloc(sizeof(Node));
    head->next->data = 1;
    head->next->next = (Node*)malloc(sizeof(Node));
    head->next->next->data = 4;
    head->next->next->next = (Node*)malloc(sizeof(Node));
    head->next->next->next->data = 2;
    head->next->next->next->next = NULL;

    printf("Max: %d\n", maxInList(head)); // 输出 4
    printf("Count: %d\n", countNodes(head)); // 输出 4
    printf("Average: %.2f\n", average(head)); // 输出 2.50

    // 释放链表
    Node* temp;
    while (head != NULL) {
        temp = head;
        head = head->next;
        free(temp);
    }

    return 0;
}
