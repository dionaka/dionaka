//回文是指正读反读均相同的字符序列，如“abba”和“abdba”均是回文，
//但“good”不是回文。试写一个算法判定给定的字符向量是否为回文。(提示：将一半字符入栈)
#include<stdio.h>
#include<string.h>
#include<time.h>
int sample1(char* a,int size){
    //为奇
    if(size%2){
        //printf("中间数为 %c\n",a[size/2]);
        for(int i=1;i<=size/2;i++){
            if(a[size/2+i] != a[size/2-i]){
                //printf("非回文串\n");
                return 0;
            }
        }
        //printf("为回文串\n");
    }
    //为偶
    else{
        //printf("中间数为 %c %c\n",a[size/2-1],a[size/2]);
        for(int i=0;i<size/2;i++){
            if(a[size/2-1-i] != a[size/2+i]){
                //printf("非回文串\n");
                return 0;
            }
        }
        //printf("为回文串\n");
    }
    return 1;
}

int sample2(char* a,int size){
    int left=0,right=size-1;
    while(left<right){
        if(a[left] != a[right])
            return 0;
        left++;
        right--;    
    }
    return 1;
}

int sample3(char* a, int size) {
    if (size == 0) return 1;
    int mid = size / 2;
    char stack[mid];
    for (int i = 0; i < mid; i++) {
        stack[i] = a[i];
    }
    int start = (size % 2 == 1) ? mid + 1 : mid;
    for (int i = start; i < size; i++) {
        if (stack[--mid] != a[i]) {
            return 0;
        }
    }
    return 1;
}

void testtime(char* a,int size,char* samplename,int (*sample)(char*,int)){
    struct timespec start,end;
    clock_gettime(CLOCK_MONOTONIC,&start);
    sample(a,size);
    clock_gettime(CLOCK_MONOTONIC,&end);
    printf("%s 用时 %.9f\n",samplename, (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9);
}

int main()
{    
    //当然,这里只是为回文数时与一定长度时时间比较,不代表平均时间复杂度,
    //比如当在中间位置字符不一样,sample1无疑快于另外两种方法
    //理论上sample2(双指针法)快于sample1快于sample3(栈)
    char a[] = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzzyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcba";
    int size = strlen(a);
    if(sample3(a,size) == 1) printf("为回文数\n");
    else printf("非回文数\n");
    testtime(a,size,"sample1",sample1);
    testtime(a,size,"sample2",sample2);
    testtime(a,size,"sample3",sample3);
    return 0;
}
    