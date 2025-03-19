//设计一个算法，删除递增有序链表中值大于mink且小于maxk的所有元素
//（mink和maxk是给定的两个参数，其值可以和表中的元素相同，也可以不同 ）。
#include<stdio.h>

typedef struct node{
    int data;
    struct node* next;
}Node,*LinkList;
void InitList(LinkList *l){
    *l = (LinkList)malloc(sizeof(Node));
    (*l)->next = NULL;
}
void CreList_H(LinkList *l,int len,int num[]){
    InitList(l);
    for(int i=0;i<len;i++){
        LinkList p = (LinkList)malloc(sizeof(Node));
        p->data = num[i];
        p->next = (*l)->next;
        (*l)->next = p;
    }
}
void CreList_R(){}
void DelList(LinkList *l,int max,int min){
    if(*l == NULL || (*l)->next == NULL) return;
    LinkList pre = *l,cur = (*l)->next;
    while(cur != NULL){
        if(cur->data > min && cur->data < max){
            pre->next = cur->next;
            free(cur);
            cur = pre->next;
        }
        else{
            pre = cur;
            cur = cur->next;
        }
    }
}
void PrinList(LinkList l){
    LinkList p = l->next;
    while(p != NULL){
        printf("%d ",p->data);
        p = p->next;
    }
    printf("\n");
}
int main(){   
    int num[50],i,n=0,max,min;
    printf("输入链表元素，值用空格隔开\n");
    while(scanf("%d",&i)){
        num[n++] = i;
        if(getchar() == '\n') break;
    }
    printf("输入maxk:\n");scanf("%d",&max);
    printf("输入mink:\n");scanf("%d",&min);
    LinkList linklist;
    CreList_H(&linklist,n,num);
    DelList(&linklist,max,min);
    PrinList(linklist);
    return 0;
}