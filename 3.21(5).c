//假设以数组Q[m]存放循环队列中的元素, 同时设置一个标志tag，
//以tag == 0和tag == 1来区别在队头指针(front)和队尾指针(rear)相等时，
//队列状态为“空”还是“满”。试编写与此结构相应的插入(enqueue)和删除(dlqueue)算法。
#include<stdio.h>
#define TYPE int

typedef struct circle{
    TYPE *Q;  //队列数组
    int front;      //队头指针
    int rear;       //队尾指针
    int tag;        //标志位
    int m;     //队列的最大容量
}Circle;

void enqueue(Circle *cir,TYPE x){
    if(cir->front == cir->rear && cir->tag == 1){
        printf("队列已满，无法插入\n");
    }
    else{
        cir->Q[cir->rear] = x;
        cir->rear = (cir->rear + 1) % (cir->m);
        if(cir->rear == cir->front){
            cir->tag = 1;
            printf("队列已满\n");
        }
    }
    return;
}

void dequeue(Circle *cir){
    if(cir->front == cir->rear && cir->tag == 0){
        printf("队列为空，无法删除\n");
    }
    else{
        TYPE x = cir->Q[cir->front];
        cir->front = (cir->front + 1) % (cir->m);
        printf("%d\n",x);
        if(cir->front == cir->rear){
            cir->tag = 0;
            printf("队列为空\n");
        }
    }
    return;
}

int main(){
    Circle *cir;
    cir->m = 5;
    cir->front = 0;
    cir->rear = 0;
    cir->tag = 0;
    enqueue(cir,10);
    enqueue(cir,20);
    enqueue(cir,30);
    enqueue(cir,40);
    enqueue(cir,50);
    enqueue(cir,60);
    dequeue(cir);
    dequeue(cir);
    dequeue(cir);
    dequeue(cir);
    dequeue(cir);
    dequeue(cir);
    return 0;
}