#include <stdio.h>
#include <stdlib.h>

#define MAX_SIZE 100

typedef struct {
    int data[MAX_SIZE];
    int front;
    int rear;
    int size;
    int count;
} Deque;

// 初始化队列
void initDeque(Deque* dq, int size) {
    dq->front = 0;
    dq->rear = 0;
    dq->size = size;
    dq->count = 0;
}

// 从队尾删除
int deleteRear(Deque* dq) {
    if (dq->count == 0) {
        printf("Queue is empty!\n");
        return -1;
    }
    dq->rear = (dq->rear - 1 + dq->size) % dq->size;
    int val = dq->data[dq->rear];
    dq->count--;
    return val;
}

// 从队头插入
void insertFront(Deque* dq, int val) {
    if (dq->count == dq->size) {
        printf("Queue is full!\n");
        return;
    }
    dq->front = (dq->front - 1 + dq->size) % dq->size;
    dq->data[dq->front] = val;
    dq->count++;
}

// 测试代码
int main() {
    Deque dq;
    initDeque(&dq, 5); // 容量为5

    insertFront(&dq, 1);
    insertFront(&dq, 2);
    insertFront(&dq, 3);

    printf("Delete rear: %d\n", deleteRear(&dq)); // 输出1
    printf("Delete rear: %d\n", deleteRear(&dq)); // 输出2

    insertFront(&dq, 4);
    insertFront(&dq, 5);

    printf("Delete rear: %d\n", deleteRear(&dq)); // 输出3
    printf("Delete rear: %d\n", deleteRear(&dq)); // 输出4

    return 0;
}
