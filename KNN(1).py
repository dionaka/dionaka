#用sklearn 实现KNN
#echo   pip install scikit-learn
#       pip install pandas
from sklearn import datasets
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np

iris = datasets.load_iris()
#花的特征数据
X = iris.data
#花的种类
y = iris.target
#花的特征名字
z = iris.feature_names

#特征名与数据绘制表格
df = pd.DataFrame(X, columns = z, index = y)
print(df)
#保存为csv文件
df.to_csv('iris.csv')
#把数据分为训练集和测试集
X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=250)

"""
##KNN算法部分
#k值选择
dir=[]
for k in range(1,101):
    clf=KNeighborsClassifier(n_neighbors=k)
    clf.fit(X_train,y_train)
    #预测及计算准确率
    correct=np.count_nonzero(clf.predict(X_test)==y_test)
    accuracy=correct/len(y_test)
    print("Accuracy:",accuracy)
    # 或者 print(clf.score(X_test,y_test))
    dir.append(accuracy)
#绘制准确率（accuracy）随k变化的图
k_values=range(1,101)
# 设置字体为 SimHei 显示中文
rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
plt.figure()
plt.title("K-NN Classifier")
plt.xlabel("k值")
plt.ylabel("准确率")
plt.scatter(k_values,dir)
plt.grid(True)
#或plt.plot(k_values,dir)
plt.show()
"""

"""
##LogisticRegression算法
#创建实例
lr=LogisticRegression(max_iter=200)
lr.fit(X_train,y_train)
#进行预测
y_pred=lr.predict(X_test)
print(accuracy_score(y_test,y_pred))
#或print(lr.score(X_test,y_test))
"""

