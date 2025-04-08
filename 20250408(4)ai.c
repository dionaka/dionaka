#include <stdio.h>
#include <stdlib.h>

#define MAX_SIZE 100

typedef struct {
    int Q[MAX_SIZE];
    int front;
    int rear;
    int tag;
} TagQueue;

// 初始化队列
void initQueue(TagQueue* q) {
    q->front = 0;
    q->rear = 0;
    q->tag = 0; // 初始为空
}

// 入队
void enqueue(TagQueue* q, int val) {
    if (q->front == q->rear && q->tag == 1) {
        printf("Queue is full!\n");
        return;
    }
    q->Q[q->rear] = val;
    q->rear = (q->rear + 1) % MAX_SIZE;
    if (q->front == q->rear) {
        q->tag = 1;
    }
}

// 出队
int dequeue(TagQueue* q) {
    if (q->front == q->rear && q->tag == 0) {
        printf("Queue is empty!\n");
        return -1;
    }
    int val = q->Q[q->front];
    q->front = (q->front + 1) % MAX_SIZE;
    if (q->front == q->rear) {
        q->tag = 0;
    }
    return val;
}

// 测试代码
int main() {
    TagQueue q;
    initQueue(&q);

    enqueue(&q, 1);
    enqueue(&q, 2);
    enqueue(&q, 3);

    printf("Dequeue: %d\n", dequeue(&q)); // 输出1
    printf("Dequeue: %d\n", dequeue(&q)); // 输出2

    enqueue(&q, 4);
    enqueue(&q, 5);

    printf("Dequeue: %d\n", dequeue(&q)); // 输出3
    printf("Dequeue: %d\n", dequeue(&q)); // 输出4

    return 0;
}
