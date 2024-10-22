#周文博 20233231070
#1
a,b,c=eval(input("输入 x,y,z:"))
print("最大的数是：",max(a,b,c),"\n最小的数是：",min(a,b,c))

#2
i=1
arr=""
while i<=100:
    arr+=str(i)+" "
    i+=2  
print(arr)

#3
long=int(input("请输入距离:"))
begin=13
if long<=3:
    add=0
elif long>15:
    add=3.45
else:
    add=2.3
print(begin+add*(long-3))

#4
arr=input("输入十个数字，并用逗号隔开:").split(",")
for i in arr:
    print(i,end=" ")
print("\n最大的数是:",max(arr))
print("最小的数是:",min(arr))

#5
#遍历
char="abc123"
newchar=""
for i in range(len(char)):
    newchar+=char[-1-i]
print(newchar)

#or
char="abc123"
print(''.join(reversed(char)))

#or
char="abc123"
print(char[::-1])

#or
char="abc123"
def vex(s):
    if s=="":
        return s
    else:
        return vex(s[1:])+s[0]
print(vex(char))
  
#6


