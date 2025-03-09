//已知某整数序列A[1....n],假设其中只有A[1]、A[2]、A[n]三个元素是非零,
//设计一个算法，将A中所有元素循环左移k位。
#include<stdio.h>
int LeftMove(int* arr,int k,int n){
    k = k%n;
    int* brr = (int*)calloc(n,sizeof(int));
    brr[n-k-1] = arr[n-1];
    if(!(k&~1)){
        brr[n-1] = arr[0];
        brr[0] = arr[1];
        }
    else if(k>1){
        brr[n-k] = arr[0];
        brr[n-k+1] = arr[1];
    }
    else{
    printf("error");
    return 0;
    }
    for(int i=0;i<n;i++) arr[i]=brr[i];
    free(brr);
    return 1;
}
int main()
{
    int n,k,i;
    printf("输入n,k\n");
    scanf("%d%d",&n,&k);
    int* arr = (int*)calloc(n,sizeof(int));
    printf("输入A[1]、A[2]、A[n]\n");
    scanf("%d%d%d",&arr[0],&arr[1],&arr[n-1]);
    if(LeftMove(arr,k,n))
    for(i=0;i<n;i++) printf("%d ",arr[i]);
    free(arr);
    return 0;
}