#include <stdio.h>
#include <stdlib.h>
//循环队列
#define MAXSIZE 6  // 队列的最大容量（实际可存储 MAXSIZE-1 个元素）
typedef struct {
    int *data;     // 存储队列元素的数组
    int front;     // 队头指针
    int rear;      // 队尾指针
    int size;      // 队列的最大容量
} CircularQueue;

// 初始化队列
int InitQueue(CircularQueue *q) {
    q->data = (int *)malloc(MAXSIZE * sizeof(int));  // 分配存储队列元素的数组
    if (!q->data) return 0;  // 分配失败返回 0
    q->front = q->rear = 0;  // 初始化队头和队尾指针
    q->size = MAXSIZE;       // 设置队列的最大容量
    return 1;                // 初始化成功返回 1
}

// 判断队列是否为空
int IsEmpty(CircularQueue *q) {
    return q->front == q->rear;  // 队头指针等于队尾指针时，队列为空
}

// 判断队列是否已满
int IsFull(CircularQueue *q) {
    return (q->rear + 1) % q->size == q->front;  // 队尾指针的下一个位置等于队头指针时，队列已满
}

// 入队操作
int EnQueue(CircularQueue *q, int value) {
    if (IsFull(q)) {
        return 0;  // 队列已满，返回 0
    }
    q->data[q->rear] = value;          // 将元素插入队尾
    q->rear = (q->rear + 1) % q->size; // 队尾指针循环递增
    return 1;                          // 入队成功返回 1
}

// 出队操作
int DeQueue(CircularQueue *q, int *value) {
    if (IsEmpty(q)) {
        return 0;  // 队列为空，返回 0
    }
    *value = q->data[q->front];         // 获取队头元素
    q->front = (q->front + 1) % q->size; // 队头指针循环递增
    return 1;                           // 出队成功返回 1
}

// 获取队列长度
int QueueLength(CircularQueue *q) {
    return (q->rear - q->front + q->size) % q->size;  // 计算队列中元素的个数
}

// 销毁队列
void DestroyQueue(CircularQueue *q) {
    free(q->data);  // 释放存储队列元素的数组
    q->data = NULL; // 将指针置为 NULL
    q->front = q->rear = 0;  // 重置队头和队尾指针
}

// 主函数
int main() {
    CircularQueue queue;
    if (!InitQueue(&queue)) {
        printf("队列初始化失败！\n");
        return 1;
    }

    // 测试入队操作
    for (int i = 1; i <= 5; i++) {
        if (EnQueue(&queue, i)) {
            printf("入队元素：%d\n", i);
        } else {
            printf("队列已满，无法入队元素：%d\n", i);
        }
    }

    // 测试出队操作
    int value;
    while (DeQueue(&queue, &value)) {
        printf("出队元素：%d\n", value);
    }

    // 销毁队列
    DestroyQueue(&queue);

    return 0;
}
