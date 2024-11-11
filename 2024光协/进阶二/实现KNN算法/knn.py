import pandas as pd
import csv
import operator
import math
import time
#把广州做训练集，上海测试集
class MyClassifier:
    def __init__(self):
        self.trainSet=[]#训练集
        self.testSet=[]#测试集

    def readDataset(self,fileName1,fileName2,trainSet,testSet):
        with open(fileName1,"r") as f:
            lines=csv.reader(f)#csv.reader读txt文档,返回迭代器
            data1=list(lines)#[[],["","","",""],[...]]
            for i in range(1,len(data1)):
                for j in range(8):         
                    '''print(data1[i])
                    time.sleep(500)'''
                    data1[i][j]=float(data1[i][j])
                trainSet.append(data1[i])
        with open(fileName2,"r") as f:
            lines=csv.reader(f)
            data2=list(lines)
            for i in range(1,len(data2)):
                for j in range(8):
                    data2[i][j]=float(data2[i][j])
                testSet.append(data2[i])

    def calculateDistance(self,trainData,testData,length):#计算距离
        distance=0
        for i in range(length):
            """print(testData[5])
            time.sleep(500)"""
            """print(len(trainData))
            print(len(testData))
            time.sleep(500)"""
            distance+=(float(trainData[i])-float(testData[i]))**2
        return round(math.sqrt(distance))
        
    def getNeighbors(self,trainSet,testSet,k):#k个临近,引用calculateDistance()
        distance=[]
        length=len(testSet)
        for i in range(len(trainSet)):
            dis=self.calculateDistance(trainSet[i],testSet,length)
            print("训练集：{}\t 距离：{}".format(trainSet[i],dis))
            distance.append((trainSet[i],dis))
        distance.sort(key=operator.itemgetter(1))#距离（1）从小到大排
        #print(distance)
        neighbors=[]
        for i in range(k):
            neighbors.append(distance[i][0])#取距离最小的前k个的训练集
        return(neighbors)
    
    def getResponse(self,neighbors):#决定归到哪一类
        classVote={}
        for  i in range(len(neighbors)):
            j=neighbors[i][-1]#.txt最后一位为空气质量代号
            if j in classVote:
                classVote[j]+=1
            else:
                classVote[j]=1
        print(classVote.items())
        sortedVote=sorted(classVote.items(),key=operator.itemgetter(1),reverse=True)#.items()使用sorted方法后返回包含键值对的列表，/倒序
        return sortedVote[0][0]

    def getAccuracy(self,testSet,predict):#预测准确率
        correct=0
        for i in range(len(testSet)):
            if testSet[i][-1]==predict[i]:
                correct+=1
            else:
                continue
        print("有{}个值预测正确，{}个值预测错误".format(correct,(len(testSet)-correct)))
        return float(correct/len(testSet))

    def run(self):
        trainSet=self.trainSet
        testSet=self.testSet
        predict=[]
        k=5
        fileName1="../生成测试集和训练集/广州预处理.txt"
        fileName2="../生成测试集和训练集/上海预处理.txt"
        self.readDataset(fileName1,fileName2,trainSet,testSet)
        for i in range(len(testSet)):#[["","","",...],[...]]
            neighbor=self.getNeighbors(trainSet,testSet[i],k)
            result=self.getResponse(neighbors=neighbor)
            predict.append(result)
        accuracy=self.getAccuracy(testSet,predict)
        print(f"预测精度为：{accuracy}")

        
myClassifier=MyClassifier()
myClassifier.run()
#调取路径
#../生成测试集和训练集/广州预处理.txt
#../获取数据/2019年上海空气质量数据.csv

    
