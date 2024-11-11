import sklearn
from sklearn.datasets import load_breast_cancer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import pandas as pd

lw=load_breast_cancer()
#print(dir(lw))
x=lw.data
x=x[:,:10]
y=lw.feature_names
y=y[:10]
z=lw.target
lw_df=pd.DataFrame(x,columns=y,index=z)
#print(lw_df)
lw_df.to_csv("load_breast_cancer.csv")

x_train,x_test,y_train,y_test=train_test_split(x,z,random_state=100)
knn=KNeighborsClassifier(n_neighbors=5)
knn.fit(x_train,y_train)
print(knn.score(x_test,y_test))

