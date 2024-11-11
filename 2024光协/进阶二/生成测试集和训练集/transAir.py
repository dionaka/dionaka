import pandas as pd

def transAir(city_zh):
    sample=pd.read_csv(f'../获取数据/2019年{city_zh}空气质量数据.csv')
    sample1=sample[["AQI指数","当天AQI排名","PM2.5","PM10","So2","No2","Co","O3"]].copy()		
    dixc=[]
    for i in sample["质量等级"]:
        if i=="优":
            dixc.append(1)
        elif i=="良":
            dixc.append(2)
        elif i=="轻度污染":
            dixc.append(3)
        elif i=="中度污染":
            dixc.append(4)
        elif i=="重度污染":
            dixc.append(5)
        elif i=="严重污染":
            dixc.append(6)
        else:
            dixc.append("未知")
            print("出现未知数据")
    sample1["质量等级"]=dixc
    #转为txt
    with open ("{}预处理.txt".format(city_zh),"w") as f:
        for i in sample1.values:
            s=",".join(str(j) for j in i)
            f.write("\n"+s)
        f.close()  
transAir("上海")
transAir("广州")