//已知f为单链表的表头指针, 链表中存储的都是整型数据，
//试写出实现下列运算的递归算法：① 求链表中的最大整数；
//② 求链表的结点个数；③ 求所有整数的平均值
//3月21日,思路:while(list->next)
#include<stdio.h>
typedef struct List{
    struct List *next;
    int data;
}List;

List *CreatElem(int r){
    List *l = (List*)malloc(sizeof(List));
    //可加内存分配是否成功判断,省略
    l->next = NULL;
    l->data = r;
    return l;
}

int main()
{
    int max=0,sort=-1,sum=0;
    //f头
    List *list = CreatElem(0);
    list->next = CreatElem(40);
    list->next->next = CreatElem(20);
    list->next->next->next = CreatElem(30);
    list->next->next->next->next = CreatElem(80);
    list->next->next->next->next->next = CreatElem(77);
    while(list){
        sort++;
        max = max>list->data?max:list->data;
        sum += list->data;
        list = list->next;
    }
    printf("%d\n%d\n%.2lf\n",max,sort,(double)sum/sort);
    return 0;
}
/*
#include <stdio.h>
#include <stdlib.h>

typedef struct List {
    int data;
    struct List *next;
} List;

int main() {
    int max = 0, sort = 0, sum = 0;
    char *arr = "123564825";
    List *f = (List *)malloc(sizeof(List));
    f->next = NULL;
    List *current = f;
    for (int i = 0; i < 9; i++) {
        List *newNode = (List *)malloc(sizeof(List));
        newNode->data = arr[i] - '0'; 
        newNode->next = NULL; 
        current->next = newNode; 
        current = newNode; 
    }
    List *list = f->next; 
    while (list != NULL) {
        sort++; 
        max = (max > list->data) ? max : list->data; 
        sum += list->data; 
        list = list->next; 
    }
    printf("最大整数: %d\n", max);
    printf("结点个数: %d\n", sort);
    printf("平均值: %.2f\n", (float)sum / sort); 
    
    //释放内存
    List *temp;
    while (f != NULL) {
        temp = f;
        f = f->next;
        free(temp);
    }
    return 0;
}
 */   