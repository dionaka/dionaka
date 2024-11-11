import random
dic={}
error=0
testnum=10000
partnum=100
boxnum=50
arr=list(range(1,partnum+1))
def mode(error):
    brr=list(range(1,partnum+1))
    random.shuffle(brr)
    for i in range(partnum):
        dic[arr[i]]=brr[i]
    for i in range(1,partnum+1):
        #1--partnum试验人员
        found=False
        num=i
        #num设为要抓的盒子
        for j in range(boxnum):
        #boxnum次抽取
            if dic[num]==i:
            #找到号码
                found=True
                break
            else:
                num=dic[num]
        if not found:
            error+=1
            return error
    return error       
for i in range(testnum):
    #模拟testnum次
    error=mode(error)
accuracy=(testnum-error)/testnum
print(accuracy)
