//1.将两个递增的有序链表合并为一个递增的有序链表。
//要求结果链表使用原来两个链表的存储空间，不另外申请其他的存储空间。
//表中不允许有重复的数据。
#include<stdio.h>
#include<stdlib.h>
#define DataType int
typedef struct y{
    char data;
    struct y* next;
}Node,*LinkList;

//初始化(这里选用直接操作链表指针.亦可以传入指针地址,双重指针(linklist*)解决)
LinkList CreatElem(DataType r){
    LinkList l = (LinkList)malloc(sizeof(Node));
    //可加内存分配是否成功判断,省略
    l->next = NULL;
    l->data = r;
    return l;
}

//合并
LinkList AddSort(LinkList a,LinkList b){
    //创建临时头节点.亦可用malloc，但需free手动释放内存
    Node head;
    head.next = NULL;
    LinkList c = &head;
    while(a && b){
        if(a->data <= b->data){
            c->next = a;
            a = a->next;
        }
        else{
            c->next = b;
            b = b->next;
        }
        c = c->next;
    }
    //剩余节点加入
    if(a) c->next = a;
    if(b) c->next = b;
    return head.next;
}

//打印
void PrintList(LinkList l){
    while(l){
    printf("%d ",l->data);
    l = l->next;
    }
    printf("\n");
}

int main()
{
    LinkList l1,l2;
    l1 = CreatElem(0);
    l1->next = CreatElem(1);
    l1->next->next = CreatElem(2);
    l1->next->next->next = CreatElem(6);
    l1->next->next->next->next = CreatElem(9);
    l2 = CreatElem(1);
    l2->next = CreatElem(3);
    l2->next->next = CreatElem(5);
    l2->next->next->next = CreatElem(7);
    PrintList(l1);
    PrintList(l2);
    LinkList l3 = AddSort(l1,l2);
    PrintList(l3);
    //释放内存略
}